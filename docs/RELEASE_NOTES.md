# Moku geospatial survey toolkit — Release Notes

## 0.1.0 — 2026-10-12 (the gates, lifted and proven)

First release. The validator, intake, build, schemas, fixtures, sample
sources, and doctrine are lifted **unchanged** from the Green Fee Commons
Report (`Aina-Design-Corp/kuleana-portal`, main at 2026-10-12), with one
addition to the build: consumer flags `--site <dir>`, `--cname <host>`, and
`--label "<text>"`, so one build reproduces any consumer exactly.

- **Compatibility check** (`npm run compat`, CI job `compat`): validates the
  Commons Report's registry with this validator, rebuilds its site with this
  build against its own assets, and diffs projection and pages byte for
  byte against the Commons Report's own build. The toolkit's first consumer
  is its proof.
- **Own registry:** the fictional FY2026 demonstration cohort (`sample:
  true`, marked on every page it builds). The toolkit publishes nothing.
- **Governance:** huikoeaina contract `community-monitoring.md` (proposed);
  mokunet-org ruling `2026-10-12-community-monitoring-toolkit`; manifest
  seeded (`coordination.json`).

### Known limits, by design

- The build's index copy is still the Commons Report's (Green Fee wording
  when a real cohort is present). Templating per program lands in 0.2 with
  the contract's record shape.
- No forms, no feature-layer reader, no outcomes-update path yet (0.2–0.3).
- Schema and doctrine files keep their kuleana-portal names and wording
  until the contract's shape lands.

### Claims and boundaries

- Nothing here is deployed for, adopted by, or endorsed by any government
  agency. The toolkit supports professional review and community reporting;
  it makes no funding, eligibility, policy, or enforcement decisions.
- Moku context is regional (*whose place*), never regulatory authority; no
  parcel geometry is ever stored.
