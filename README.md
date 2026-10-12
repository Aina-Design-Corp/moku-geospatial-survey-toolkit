# Moku geospatial survey toolkit

**Status: being built — first release lifts the working gates from the Green
Fee Commons Report and proves them on its enacted cohort. Nothing here is
deployed for, adopted by, or endorsed by any government agency.**

A steward at a place reports what they see, and the record lands where the
map reads it. This toolkit is the set of tools behind that sentence: the
record a community keeps about its moku — who is caring for which place,
what they did, what they measured, and where every claim came from — and
the gates that decide what of it the public sees. It is kept by
[Āina Design Corp](https://ainadesign.org) for the Mokunet network and
governed by the community-monitoring contract held by
[Hui Koʻe ʻĀina](https://huikoeaina.ainadesign.org/), the network's
community learning hub, where the reporting practice is taught
(Moku Steward Training).

## What it does

- **A reviewed, versioned registry** of monitoring records, one program
  (cohort) per file, validated against a published JSON Schema by a
  dependency-free validator that also enforces the release bar: a record
  publishes only with a summary, a story, at least one reported outcome,
  provenance, and its moku.
- **Source-agnostic intake** — spreadsheet and CSV sources become draft
  records (never published); PDFs walk a documented assisted-extraction
  path into the same column contract. Every record, from any source,
  passes the same validation and the same human publication decision.
- **A build** that renders public pages and a machine-readable projection
  with gated fields stripped, plus the fiscal visual for programs whose
  records begin as appropriations.
- **Forms generated from the schema** (next release): a Survey123 XLSForm
  and a no-license direct-entry web page that write to a hosted feature
  layer whose field names are the record's own — and the feature-layer
  export reader that brings those submissions back as draft records. The
  same method is in use at the Magoon Maker Lab (Hui Koʻe ʻĀina, UH Mānoa).

The gate on everything: `draft → validated → published`, monotonic,
steward-held. *A person publishes, never an automated process.*

## Where it comes from, and what proves it

The tools were built for the Green Fee Commons Report
([kuleana-portal](https://github.com/Aina-Design-Corp/kuleana-portal),
[kuleana.ainadesign.org](https://kuleana.ainadesign.org)) and run there in
production for one real cohort: the 91 Green Fee projects enacted for
FY2027, each read in the moku it serves. That site is this toolkit's first
consumer, and the compatibility check in CI is the proof: on every change,
the toolkit validates the Commons Report's registry and rebuilds its
projection, and the result must match the Commons Report's own output byte
for byte. The second consumer is the Magoon Wormery and SOFT community
programs.

## Governance

- **Contract:** `huikoeaina/docs/contracts/community-monitoring.md`
  (proposed, 2026-10-12). Shapes change there first, then here, then in
  the consumers.
- **Ruling:** `mokunet-org/docs/coordinate/changes/2026-10-12-community-monitoring-toolkit.md`
  (seam brief accepted 2026-10-12). Stage per CANON §5: *a home for
  community field samples and observations — being built*.
- **Seams:** [`coordination.json`](coordination.json) — consumes the
  contract; provides the projection read (planned).
- Moku names follow the Mokunet shared map, the 33 moku of Hawaiʻi; the
  registry carries regional context (*whose place*), never regulatory
  authority, and never parcel geometry.

## Running it

```bash
npm run validate   # schema + invariants on registry/ and the fixtures
npm run build      # validate, then render dist/ (publication gate applied)
npm run intake -- intake/samples/FY2026-attachment-a.csv --sample   # source → draft records (dry run)
npm run compat     # validate + rebuild the Commons Report's cohort from a sibling checkout and diff the projection
```

Every script accepts `--registry <dir>` (or `KULEANA_REGISTRY_DIR`); the
build also accepts `--site <dir>` for the consumer's stylesheet, documents,
and CNAME. Zero runtime dependencies by design.

## Repository layout

```
schemas/     monitoring record schema (v0.3 shape, lifted) · appropriation profile (v1.0) · fixtures
scripts/     validate · intake · build · lib
intake/      drop zone and sample sources (fixtures)
site/        default stylesheet; consumers pass their own with --site
docs/        intake doctrine · schema v1 doctrine · release notes
.github/     validate + compatibility workflows
```

## Roadmap

- **0.1 — this release:** the gates lifted unchanged from kuleana-portal;
  compatibility check against the Commons Report's cohort; `--site`.
- **0.2:** the contract's record shape (`steward`, `place.moku_id`,
  `topic`, `alignment` from a program dictionary) behind a compatibility
  profile so the Commons Report's cohort still validates; the feature-layer
  export reader; the outcomes-update path (reviewed append, identity never
  overwritten).
- **0.3:** forms generated from the schema (Survey123 XLSForm, direct-entry
  page); toolkit documents 1–3 re-authored; Pages.

License: to be ruled before the first tagged release.
