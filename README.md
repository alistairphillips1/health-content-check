# Health Content Check

**A free checklist for anyone writing health information for patients or the public.**

It does two things. It checks a page you have written and tells you what to fix, with the fixes written out for you. And it works the other way round, as the checklist to write against before you start.

It runs inside Claude or ChatGPT. You do not need to be technical to use it.

---

## Download and install, about 5 minutes

**Not a developer? Start here.** You need two files. Click, download, follow the guide.

| I use | Download this | Then follow |
|---|---|---|
| **Claude** | [health-content-check.zip](https://github.com/alistairphillips1/health-content-check/releases/latest/download/health-content-check.zip) | [Install in Claude (PDF)](guides/Install-in-Claude.pdf) |
| **ChatGPT** | [health-content-check.zip](https://github.com/alistairphillips1/health-content-check/releases/latest/download/health-content-check.zip) | [Install in ChatGPT (PDF)](guides/Install-in-ChatGPT.pdf) |
| **Gemini** | [health-content-check.zip](https://github.com/alistairphillips1/health-content-check/releases/latest/download/health-content-check.zip) | [Install in Gemini (PDF)](guides/Install-in-Gemini.pdf) |

The zip downloads straight away. The guides open in your browser, with a download button at the top right of each.

A note on ChatGPT: OpenAI's Skills feature is limited to some business plans and its availability keeps changing, so the ChatGPT guide uses a Project instead. Projects work on every plan and do the same job here. Gemini uses a Gem, which is free on every plan.

**One thing is genuinely weaker outside Claude.** ChatGPT's Python sandbox has no internet access and Gemini has no sandbox, so `verify_refs.py` cannot run in either. Claude can confirm a citation is real. Elsewhere the assistant has to search for it, which is less reliable. If your pages cite references, check them yourself.

---

## No AI, or nothing to install

Two versions that need no account, no setup and no software.

| | |
|---|---|
| **[The one-page checklist (PDF)](guides/Health-Content-Check-One-Page.pdf)** | Print it, pin it, work through it by hand. Nothing to install and nothing to go stale. Also readable [here](checklist/one-page-checklist.md). |
| **[The paste-anywhere prompt](checklist/prompt.md)** | About 400 words. Paste it into any chatbot, paste your page under it. Works in Claude, ChatGPT, Gemini, Copilot or anything else. |

The one-page checklist is the version most likely to still be correct in two years, because it describes no menus.

---

## What it is not

**It is not certification.** It gives you no badge, tick or logo, and it is not run, endorsed or reviewed by NHS England or by the Patient Information Forum.

Quality marks are awarded by schemes that assess how you produce content over time, not by anything that inspects a single page. If you want one, apply to the scheme. The [production process template](skill/health-content-check/references/production-process.md) in this repo is the thing such a scheme would actually look at, so filling it in is not wasted either way.

What you can honestly say about content that passes this check: *written to the NHS standard for creating health content*, or *self-assessed against the published PIF TICK criteria*. Both are true.

---

## What it is built on

Free, public, self-assessable standards:

- [NHS digital service manual, Standard for creating health content](https://service-manual.nhs.uk/content/standard-for-creating-health-content), plus the writing and health literacy guidance alongside it.
- [The 10 published PIF TICK criteria](https://piftick.org.uk/about-pif-tick/), used as the map of what a formal assessment covers. Linked, not reproduced.
- WCAG 2.2 AA, for anything on the web.

These get revised. The skill links the live pages and states the date it checked.

---

## The part people skip

Most of what makes health information trustworthy cannot be checked by software. Whether a real patient read it and understood it. Whether a qualified person confirmed it is safe. Whether anyone acts on feedback. Whether the review date is honoured.

The check deliberately leaves those unticked and hands them back to you every time. That list is the point, not an omission.

---

## What is in here

```
skill/health-content-check/     the skill itself
  SKILL.md                      the review and writing workflow
  references/
    criteria-gate.md            what can be checked, and what only you can attest
    improvement-playbook.md     how to fix the twelve common failures
    production-process.md       the one-page method to fill in once
  scripts/
    verify_refs.py              resolves DOIs and PMIDs, catches invented citations

checklist/
  one-page-checklist.md         the no-AI checklist, readable on the web
  prompt.md                     the paste-anywhere prompt

guides/                         four PDFs, and the script that builds all of them
dist/                           health-content-check.zip, ready to upload
build.sh                        rebuilds the zip and every PDF
```

`verify_refs.py` is Python standard library only. It sends an identifier to the public CrossRef and PubMed interfaces and nothing else. No page content, no patient data, no keys.

---

## For developers

```bash
git clone https://github.com/alistairphillips1/health-content-check.git
cd health-content-check
./build.sh          # rebuilds dist/*.zip and the two PDFs
```

Building the PDFs needs `reportlab` (`pip install reportlab`). Rebuilding the zip needs nothing.

The install guides go stale when Claude, ChatGPT or Gemini change their menus. The steps live in `guides/build_guides.py`, near the top. Edit, run `./build.sh`, commit.

---

## Found a problem?

Open an issue. Useful ones: a step in a guide that no longer matches what you see on screen, a standard that has been revised, a check that produced a wrong or unhelpful result or a page it graded well that it should not have.

Pull requests welcome, particularly for other specialties and for translations.

---

## Maintainer

Ali Phillips MBBS FRCS (Tr & Orth), Consultant Hand, Wrist and Elbow Surgeon.

Maintained as a free resource. Contributions are welcome and the licence is deliberately permissive: fork it, adapt it for your own specialty and put it to work.

## Licence

MIT. See [LICENSE](LICENSE). Free to use, copy, adapt and redistribute, including commercially, provided the copyright notice travels with it.

No warranty. You remain responsible for whatever you publish, including anything you publish after this has looked at it.
