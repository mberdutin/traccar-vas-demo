#!/usr/bin/env bash
# The managed VAS-ci sandbox and a CI worker execute exactly this entrypoint.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p artifacts
export npm_config_cache="${npm_config_cache:-/tmp/vas-npm-cache}"
node --version | tee artifacts/node-version.txt
npm --version | tee artifacts/npm-version.txt
npm ci --no-audit --no-fund 2>&1 | tee artifacts/npm-ci.log
node --test test/*.test.js 2>&1 | tee artifacts/unit.log
npm run lint 2>&1 | tee artifacts/lint.log
npm run build 2>&1 | tee artifacts/build.log
python3 demo/vas/ci/browser_check.py 2>&1 | tee artifacts/browser.log
python3 - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
sha=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=normal']).strip(), 'Dirty source checkout: report refused'
files=sorted(Path('build').rglob('*'))
hashes={p.relative_to('build').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
report={'status':'PASS','source_sha':sha,'base_main_sha':subprocess.check_output(['git','rev-parse','origin/main']).decode().strip(),'source_tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}']).decode().strip(),'ci_image':os.environ.get('VAS_CI_IMAGE','local-unpinned'),'platform':os.uname().machine,'backend':os.environ.get('TRACCAR_API_URL','not-set'),'checks':['npm ci','node --test','npm run lint','npm run build','browser acceptance','real Traccar integration'],'build_files':hashes}
Path('artifacts/ci-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('CI PASS',sha)
PY
