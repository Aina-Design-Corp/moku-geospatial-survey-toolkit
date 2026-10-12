#!/usr/bin/env bash
# Compatibility check — the toolkit must reproduce the Green Fee Commons
# Report (its first consumer) exactly: validate its registry with this
# validator, rebuild it with this build against its own site assets, and
# diff the projection and the pages byte for byte against the consumer's
# own build. Run locally with a sibling checkout, or in CI (clones it).
#
#   scripts/compat.sh [path-to-kuleana-portal]
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
consumer="${1:-$here/../kuleana-portal}"
if [ ! -d "$consumer/registry" ]; then
  echo "compat: kuleana-portal checkout not found at $consumer" >&2
  exit 1
fi
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

echo "compat: validating the consumer's registry with this validator"
node "$here/scripts/validate.mjs" --registry "$consumer/registry"

echo "compat: the consumer's own build"
( cd "$consumer" && node scripts/build.mjs >/dev/null )
cp -r "$consumer/dist" "$work/theirs"

# The consumer's own identity: its version label and custom domain, read from
# its build so the check follows the consumer's bumps without edits here.
label="$(sed -nE "s/^const VERSION = '(.*)';$/\1/p" "$consumer/scripts/build.mjs" | head -1)"
cname="$(sed -nE "s/.*writeFileSync\(join\(dist, 'CNAME'\), '([^']+)\\\\n'\).*/\1/p" "$consumer/scripts/build.mjs" | head -1)"
echo "compat: this toolkit's build against the consumer's registry and site (label: $label; cname: ${cname:-none})"
( cd "$here" && node scripts/build.mjs --registry "$consumer/registry" --site "$consumer/site" --label "$label" ${cname:+--cname "$cname"} >/dev/null )
cp -r "$here/dist" "$work/ours"

echo "compat: diff"
if diff -r "$work/theirs" "$work/ours"; then
  echo "compat: identical — projection and pages match byte for byte"
else
  echo "compat: DIFFERENCES — the toolkit no longer reproduces its first consumer" >&2
  exit 1
fi
