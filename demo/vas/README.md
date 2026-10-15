# VAS development workflow demo

This fork demonstrates a product request moving from customer discussion to
requirements, an approved issue, local development and verification in a
Kubernetes sandbox using the same environment and commands as CI.

Preparation snapshot: Traccar Web commit
`1f1a5fbb99fb5f8a0ef95ad994090e650c9418df`, 2026-10-15.
Original project: https://github.com/traccar/traccar-web . Apache-2.0 license
and upstream source attribution remain in LICENSE.txt and the original README.

The first candidate request is time-based filtering of devices on the map:
https://github.com/traccar/traccar-web/issues/1830 .
The VAS feature branch implements the agreed device.lastUpdate filter with
1/6/24-hour periods, persistence and reset. Existing status/group/geofence
filters keep their original filterMap semantics. The original behavior at the
pinned upstream SHA is documented in `kb/03-existing-filters.md`.

`kb/` contains Russian product/architecture notes and public issue/PR source
cards. Each fact points to a source; proposed demo requirements are labeled.
`source-manifest.json` records the source revision, fetched records and file
hashes. The deployed VAS-project intake agent uses a separate knowledge service
containing this corpus. Private agent configuration and credentials are not
part of this public repository.

Intake output: intake_notes.md, requirements.md, acceptance.md, decisions.md,
issue_draft.md and handoff.json. A separate manager-only profile publishes the
exact draft after an Omnigent ASK; the narrow publisher binds its SHA256 and
intake ID and prevents duplicate issues. Approved request:
https://github.com/mberdutin/traccar-vas-demo/issues/1 .

Development is performed in the This Mac runner, then its history is forked
into a fresh Kubernetes VAS-ci session. A fork has a **new session ID**. Source
files arrive through a clean Git checkout of the explicit feature SHA.

`.ci/check.sh` runs the common managed-sandbox/CI checks; `.ci/promote.py`
refuses mismatched source SHA/tree, image digest, build hashes or an advanced
main. A successful `vas/kubernetes-ci` commit status is required before the
coordinator advances main by fast-forward. The checked build is packaged
without rebuilding. Release assets contain the CI report and browser evidence.
See `.ci/README.md` for the exact environment and acceptance coverage.

Video recording follows the successful complete rehearsal.

Only synthetic fleet/device data should be used for the demo.
