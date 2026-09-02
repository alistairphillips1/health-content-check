#!/usr/bin/env bash
# Rebuilds everything people download: the skill zip and the two install PDFs.
#
#   ./build.sh                 rebuild artefacts
#   ./build.sh yourhandle      set your GitHub handle everywhere first, then rebuild
#
# Run the second form once, right after you create the repo. It replaces the
# __GH_HANDLE__ placeholder in the README and in the PDF text, so the guides
# point people back here when the menus change.

set -euo pipefail
cd "$(dirname "$0")"

if [ $# -ge 1 ]; then
  HANDLE="$1"
  echo "Setting GitHub handle to: $HANDLE"
  # macOS and GNU sed take different -i arguments, so write to a temp file.
  for f in README.md guides/build_guides.py skill/health-content-check/README.md \
           dist/START-HERE.txt CHANGELOG.md; do
    [ -f "$f" ] || continue
    sed "s|__GH_HANDLE__|$HANDLE|g" "$f" > "$f.tmp" && mv "$f.tmp" "$f"
  done
  echo "Done. The placeholder is now gone, so this only needs running once."
fi

if grep -rq "__GH_HANDLE__" README.md guides/build_guides.py 2>/dev/null; then
  echo
  echo "WARNING: the __GH_HANDLE__ placeholder is still in place."
  echo "Run:  ./build.sh yourgithubhandle"
  echo
fi

echo "Building the zip..."
rm -f dist/health-content-check.zip
( cd skill && zip -r -q -X ../dist/health-content-check.zip health-content-check \
    -x '*.DS_Store' '*__pycache__*' )
python3 - <<'PY'
import zipfile
names = zipfile.ZipFile('dist/health-content-check.zip').namelist()
assert 'health-content-check/SKILL.md' in names, names
print("  zip OK, top-level folder name matches the skill name")
PY

echo "Building the PDFs..."
if python3 -c "import reportlab" 2>/dev/null; then
  ( cd guides && python3 build_guides.py )
  echo "  PDFs rebuilt"
else
  echo "  SKIPPED: reportlab is not installed. Run: pip install reportlab"
fi

echo
echo "Built:"
ls -lh dist/health-content-check.zip guides/*.pdf 2>/dev/null || true
