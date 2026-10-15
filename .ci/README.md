# VAS managed sandbox as CI

`.ci/check.sh` is the single check entrypoint. The VAS-ci managed runner and
CI use the same `vas-ci-dev` image **by digest**, Linux arm64, Node 22.23.3,
Chromium and pinned Python Playwright. The image recipe and Kubernetes
provisioning live in the private Omnigent demo infrastructure repository.

The run starts from a clean checkout of an explicit feature SHA. It installs
from package-lock.json, runs unit tests, lint, production build and browser
acceptance at desktop/390px. Fixed UTC/fixture cases verify boundaries and
live updates. A distinct smoke uses an actual Traccar 6.16 API and an OsmAnd
packet; fixture success alone cannot complete CI.

Environment:

- `VAS_CI_IMAGE`: immutable digest used by the managed pod.
- `TRACCAR_API_URL`: isolated synthetic backend (`http://traccar-vas-api...:8082`).
- `TRACCAR_OSMAND_URL`: same backend's OsmAnd listener on port 5055.
- `CHROMIUM_PATH`: browser provided by the image.

Artifacts are ignored by Git. `artifacts/ci-report.json` binds a successful
run to source SHA/tree, runtime digest and hashes of every production build
file. The coordinator verifies it and records `vas/kubernetes-ci` on that
exact GitHub SHA. Main is advanced by fast-forward only after that status,
with no source change between check and release. The verified build is
packaged, never rebuilt during promotion. A new SHA requires a new run.

The inherited master-only GitHub build/lint workflows are not the CI for the
demo's main branch. No additional copy of these checks is run after promotion.
