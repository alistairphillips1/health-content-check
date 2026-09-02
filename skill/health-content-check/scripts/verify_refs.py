#!/usr/bin/env python3
"""
verify_refs.py, canonical reference verifier (stdlib only).

One shared tool. Do not copy it per-project; call this single file from
wherever reference-checking is needed (pif-content, balanced-evidence,
medicolegal evidence libraries). Recommended home:
    ~/Claude/tools/verify_refs.py

It holds no case data and touches nothing sensitive, it only queries the
public CrossRef and PubMed APIs. Safe to site in a neutral shared location.

WHAT IT DOES (deterministic layer):
  Given a DOI or PMID, it resolves the identifier and compares the returned
  title / authors / year against what was claimed, returning one verdict:

    OK          resolves AND claimed metadata matches
    MISMATCH    resolves BUT claimed title/authors/year disagree
    FABRICATED  identifier given but resolves to nothing
    UNVERIFIED  no usable identifier, or the API was unreachable
    ERROR       unexpected failure

WHAT IT DOES NOT DO (be honest about this):
  It cannot, on its own, confirm that a real paper *supports the specific
  claim* a sentence makes. That "real-but-wrong-citation" check needs the
  abstract plus judgement. So this tool also RETURNS the fetched abstract,
  so the caller (the model running the skill) can perform that claim-support
  check as a second, non-deterministic step. A clean metadata verdict is
  necessary but not sufficient.

USAGE:
  Single:
    python verify_refs.py --doi 10.1001/jama.2020.1234 \
        --title "Some title" --authors "Smith; Jones" --year 2020
    python verify_refs.py --pmid 31978945

  Batch (JSON list in, JSON list out):
    python verify_refs.py --file refs.json
  where refs.json is:
    [{"id_type":"doi","id":"10....","claimed_title":"...",
      "claimed_authors":"Smith; Jones","claimed_year":2020,"claim":"..."}]

  Set a contact email for the CrossRef polite pool (recommended):
    export VERIFY_REFS_MAILTO="you@example.com"
"""

import argparse
import difflib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

MAILTO = os.environ.get("VERIFY_REFS_MAILTO", "")
UA = "verify_refs/1.0 (stdlib; +reference-integrity-check)" + (
    f"; mailto:{MAILTO}" if MAILTO else ""
)
TIMEOUT = 20
TITLE_OK = 0.85      # >= this: titles considered matching
TITLE_MISMATCH = 0.60  # < this: titles considered different
YEAR_TOLERANCE = 1   # online-first vs print can differ by a year


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def _norm(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)            # strip any tags
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())  # keep alnum
    return re.sub(r"\s+", " ", s).strip()


def _ratio(a, b):
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _surnames(s):
    """Pull surnames from a 'Smith; Jones' or 'Smith J, Jones K' string."""
    if not s:
        return set()
    parts = re.split(r"[;,]| and ", s)
    out = set()
    for p in parts:
        toks = _norm(p).split()
        if toks:
            # longest token is usually the surname
            out.add(max(toks, key=len))
    return {t for t in out if len(t) > 1}


# ---------- CrossRef ----------
def crossref(doi):
    doi = doi.strip().replace("https://doi.org/", "").replace("doi:", "").strip()
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    try:
        data = json.loads(_get(url)).get("message", {})
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"_found": False}
        return {"_error": f"HTTP {e.code}"}
    except Exception as e:
        return {"_error": str(e)}
    title = (data.get("title") or [""])[0]
    authors = [
        " ".join(filter(None, [a.get("given"), a.get("family")]))
        for a in data.get("author", [])
    ]
    year = None
    for k in ("published-print", "published-online", "published", "issued"):
        dp = data.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    return {
        "_found": True,
        "title": title,
        "authors": authors,
        "year": year,
        "journal": (data.get("container-title") or [""])[0],
        "abstract": data.get("abstract", ""),
    }


# ---------- PubMed ----------
def pubmed(pmid):
    pmid = re.sub(r"\D", "", str(pmid))
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    s = f"{base}esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    try:
        res = json.loads(_get(s)).get("result", {})
    except Exception as e:
        return {"_error": str(e)}
    if pmid not in res:
        return {"_found": False}
    rec = res[pmid]
    if rec.get("error"):
        return {"_found": False}
    year = None
    m = re.match(r"(\d{4})", rec.get("pubdate", ""))
    if m:
        year = int(m.group(1))
    authors = [a.get("name", "") for a in rec.get("authors", [])]
    abstract = ""
    try:
        ab = f"{base}efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
        abstract = _get(ab).strip()
    except Exception:
        pass
    return {
        "_found": True,
        "title": rec.get("title", ""),
        "authors": authors,
        "year": year,
        "journal": rec.get("fulljournalname", ""),
        "abstract": abstract,
    }


def verify_one(ref):
    """ref: dict with id_type ('doi'|'pmid'), id, optional claimed_* + claim."""
    id_type = (ref.get("id_type") or "").lower()
    ident = ref.get("id")
    out = {"input": ref, "verdict": "UNVERIFIED", "reason": "", "fetched": None}

    if not ident or id_type not in ("doi", "pmid"):
        out["reason"] = "no usable DOI or PMID supplied"
        return out

    meta = crossref(ident) if id_type == "doi" else pubmed(ident)

    if meta.get("_error"):
        out["verdict"] = "UNVERIFIED"
        out["reason"] = f"lookup failed ({meta['_error']}), could not check"
        return out
    if not meta.get("_found"):
        out["verdict"] = "FABRICATED"
        out["reason"] = f"{id_type.upper()} {ident} does not resolve"
        return out

    out["fetched"] = {
        "title": meta.get("title"),
        "authors": meta.get("authors"),
        "year": meta.get("year"),
        "journal": meta.get("journal"),
        "abstract": (meta.get("abstract") or "")[:4000],
    }

    problems = []
    ct = ref.get("claimed_title")
    if ct:
        r = _ratio(ct, meta.get("title", ""))
        if r < TITLE_MISMATCH:
            problems.append(f"title differs (similarity {r:.2f})")
        elif r < TITLE_OK:
            problems.append(f"title only partially matches (similarity {r:.2f})")
    cy = ref.get("claimed_year")
    if cy and meta.get("year") and abs(int(cy) - int(meta["year"])) > YEAR_TOLERANCE:
        problems.append(f"year claimed {cy} vs found {meta['year']}")
    ca = ref.get("claimed_authors")
    if ca:
        claimed = _surnames(ca)
        found = _surnames("; ".join(meta.get("authors", [])))
        if claimed and found and not (claimed & found):
            problems.append("no claimed author surname found among authors")

    if problems:
        out["verdict"] = "MISMATCH"
        out["reason"] = "; ".join(problems)
    else:
        out["verdict"] = "OK"
        out["reason"] = "resolves and metadata consistent"
    out["note"] = (
        "Metadata layer only. Claim-support NOT checked here, use the "
        "returned abstract to confirm the source supports the specific claim."
    )
    return out


def main():
    ap = argparse.ArgumentParser(description="Verify references against CrossRef/PubMed.")
    ap.add_argument("--doi")
    ap.add_argument("--pmid")
    ap.add_argument("--title")
    ap.add_argument("--authors")
    ap.add_argument("--year", type=int)
    ap.add_argument("--file", help="JSON list of refs for batch mode")
    args = ap.parse_args()

    refs = []
    if args.file:
        with open(args.file) as f:
            refs = json.load(f)
    elif args.doi or args.pmid:
        refs = [{
            "id_type": "doi" if args.doi else "pmid",
            "id": args.doi or args.pmid,
            "claimed_title": args.title,
            "claimed_authors": args.authors,
            "claimed_year": args.year,
        }]
    else:
        ap.error("provide --doi, --pmid, or --file")

    results = []
    for i, ref in enumerate(refs):
        results.append(verify_one(ref))
        if i < len(refs) - 1:
            time.sleep(0.4)  # be polite to the APIs

    print(json.dumps(results, indent=2, ensure_ascii=False))
    # non-zero exit if anything failed the metadata gate
    if any(r["verdict"] in ("FABRICATED", "MISMATCH") for r in results):
        sys.exit(2)


if __name__ == "__main__":
    main()
