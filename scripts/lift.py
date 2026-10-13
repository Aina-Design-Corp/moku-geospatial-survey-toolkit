#!/usr/bin/env python3
"""Lift the gates from the first consumer (kuleana-portal) into this toolkit.

Copies the lifted file set verbatim and re-applies the one toolkit patch to
build.mjs: consumer flags (--site, --cname, --label) so one build reproduces
any consumer exactly. Run after the consumer changes, then `npm run compat`.

    python3 scripts/lift.py [path-to-kuleana-portal]
"""
import pathlib, re, shutil, sys

here = pathlib.Path(__file__).resolve().parent.parent
consumer = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else here.parent / 'kuleana-portal').resolve()
LIFT = ['scripts/validate.mjs', 'scripts/intake.mjs', 'scripts/lib/registry-dir.mjs',
        'schemas/registry.schema.json', 'schemas/registry.v1.schema.json',
        'docs/INTAKE.md', 'docs/SCHEMA-V1.md', 'site/styles.css']
for rel in LIFT:
    src, dst = consumer / rel, here / rel
    dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
for d in ['schemas/fixtures/v0', 'schemas/fixtures/v1', 'intake/samples']:
    shutil.rmtree(here / d, ignore_errors=True); shutil.copytree(consumer / d, here / d)

t = (consumer / 'scripts/build.mjs').read_text(encoding='utf8')
def sub(a, b, count=1):
    global t
    n = len(re.findall(a, t, flags=re.S)) if count == 're' else t.count(a)
    assert n == 1, f'build.mjs anchor not found exactly once: {a[:60]!r} ({n})'
    t = re.sub(a, b, t, flags=re.S) if count == 're' else t.replace(a, b)
sub("import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, copyFileSync } from 'node:fs';",
    "import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, copyFileSync, existsSync } from 'node:fs';")
sub("import { join, dirname } from 'node:path';", "import { join, dirname, resolve } from 'node:path';")
sub("import { resolveRegistryDir } from './lib/registry-dir.mjs';",
    "import { resolveRegistryDir, withoutRegistryArgs } from './lib/registry-dir.mjs';")
sub(r"const VERSION = '[^']*';",
    """// Consumer flags: --site <dir> (stylesheet, docs/, the consumer's own assets;
// default: this repo's site/), --cname <host> (written to dist/CNAME when
// given), --label "<text>" (the version line in footer and embed). A consumer
// passes its own so the toolkit reproduces it exactly — the compat check.
const argv = withoutRegistryArgs(process.argv.slice(2));
const flag = (name, fallback) => {
  const eq = argv.find((a) => a.startsWith(`${name}=`));
  if (eq) return eq.slice(name.length + 1);
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] != null ? argv[i + 1] : fallback;
};
const siteDir = resolve(root, flag('--site', 'site'));
const cname = flag('--cname', null);
const VERSION = flag('--label', 'toolkit 0.1.1 (gates lifted from the Green Fee Commons Report · rule set v0.3 · v1.0 profile)');""", 're')
sub("copyFileSync(join(root, 'site', 'styles.css'), join(dist, 'styles.css'));", "copyFileSync(join(siteDir, 'styles.css'), join(dist, 'styles.css'));")
sub(r"// Custom-domain claim carried in the artifact itself \(Pages CNAME file\)\.\nwriteFileSync\(join\(dist, 'CNAME'\), '[^']*\\n'\);",
    "// Custom-domain claim carried in the artifact itself (Pages CNAME file) — only when the consumer names one.\nif (cname) writeFileSync(join(dist, 'CNAME'), `${cname}\\n`);", 're')
sub("""for (const f of readdirSync(join(root, 'site', 'docs')).filter((f) => f.endsWith('.html'))) {
  copyFileSync(join(root, 'site', 'docs', f), join(dist, 'docs', f));
}""", """if (existsSync(join(siteDir, 'docs'))) {
  for (const f of readdirSync(join(siteDir, 'docs')).filter((f) => f.endsWith('.html'))) {
    copyFileSync(join(siteDir, 'docs', f), join(dist, 'docs', f));
  }
}""")
(here / 'scripts/build.mjs').write_text(t, encoding='utf8')
print(f'lifted from {consumer}')
