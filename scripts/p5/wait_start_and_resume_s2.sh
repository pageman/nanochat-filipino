#!/usr/bin/env bash
# Wait until cjaakd9i2w8x7t starts, then accept existing S2 C2 and continue.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CTL="${HOME}/.local/bin/runpodctl"
POD=cjaakd9i2w8x7t
KEY="${HOME}/.ssh/p2_runpod_h"
LOG="${ROOT}/docs/run-cards/p5/p5-20260823T160632Z-439d1de5/wait-start-resume.log"
mkdir -p "$(dirname "$LOG")"
echo "wait_start begin utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"

for i in $(seq 1 180); do
  if "$CTL" pod start "$POD" >/tmp/p5-pod-start.json 2>/tmp/p5-pod-start.err; then
    echo "start_ok attempt=$i utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
    break
  fi
  echo "start_wait attempt=$i utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) $(tr '\n' ' ' </tmp/p5-pod-start.err)" | tee -a "$LOG"
  sleep 60
done

for j in $(seq 1 40); do
  HOSTPORT="$("$CTL" pod get "$POD" -o json | python3 -c '
import json,sys
d=json.load(sys.stdin)
ssh=d.get("ssh") or {}
direct=ssh.get("direct") or {}
host=direct.get("host") or d.get("publicIp") or ""
port=direct.get("port") or ""
print(f"{host} {port}")
')"
  HOST="${HOSTPORT%% *}"
  PORT="${HOSTPORT##* }"
  if [[ -n "$HOST" && -n "$PORT" && "$PORT" != "None" ]]; then
    if ssh -i "$KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=10 -p "$PORT" "root@$HOST" 'test -d /workspace/nanochat-filipino'; then
      echo "ssh_ok host=$HOST port=$PORT utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
      RSYNC_SSH="ssh -i $KEY -o StrictHostKeyChecking=no -p $PORT"
      rsync -avz --no-owner --no-group -e "$RSYNC_SSH" \
        "$ROOT/scripts/p5/gate_phase2_accept.py" \
        "$ROOT/scripts/p5/gate_child_common.sh" \
        "$ROOT/scripts/p5/resume_after_s2_wrapper_death.sh" \
        "root@$HOST:/workspace/nanochat-filipino/scripts/p5/"
      ssh -i "$KEY" -o StrictHostKeyChecking=no -p "$PORT" "root@$HOST" 'set -euo pipefail
cd /workspace/nanochat-filipino
chmod +x scripts/p5/resume_after_s2_wrapper_death.sh
export NANOCHAT_FILIPINO_ROOT=/workspace/nanochat-filipino
export P5_RUN_ID=p5-20260823T160632Z-439d1de5
export NANOCHAT_BASE_DIR=$NANOCHAT_FILIPINO_ROOT/data/cache/$P5_RUN_ID
nohup bash scripts/p5/resume_after_s2_wrapper_death.sh >> $NANOCHAT_BASE_DIR/safe_progress/panel-nohup.log 2>&1 &
echo $! > $NANOCHAT_BASE_DIR/safe_progress/panel.pid
echo RESUME_PID=$(cat $NANOCHAT_BASE_DIR/safe_progress/panel.pid)
'
      echo "resume_launched utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
      exit 0
    fi
  fi
  echo "ssh_wait attempt=$j utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
  sleep 15
done
echo "FAIL never_started utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$LOG"
exit 1
