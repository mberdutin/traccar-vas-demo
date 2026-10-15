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
Existing status/group/geofence filters and lastUpdate sorting are documented
in `kb/03-existing-filters.md`. This preparation does not implement that feature.

`kb/` contains Russian product/architecture notes and public issue/PR source
cards. Each fact points to a source; proposed demo requirements are labeled.
`source-manifest.json` records the source revision, fetched records and file
hashes. The deployed VAS-project intake agent uses a separate knowledge service
containing this corpus. Private agent configuration and credentials are not
part of this public repository.

Current intake output: intake_notes.md, requirements.md, acceptance.md,
decisions.md, issue_draft.md and handoff.json. GitHub issue publication with
manager approval, the CI environment and release automation are the next
stages. They must be checked end to end before a demo recording.

Only synthetic fleet/device data should be used for the demo.
