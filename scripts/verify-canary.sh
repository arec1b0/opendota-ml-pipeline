#!/usr/bin/env bash
# ---------------------------------------------------------------
# Canary verification script
# Polls Prometheus for 5xx error rate on canary pods.
# Exits 0 if canary is healthy, 1 if error threshold exceeded.
# ---------------------------------------------------------------
set -euo pipefail

# --------------- Configuration ---------------
PROMETHEUS_URL="${PROMETHEUS_URL:-http://prometheus-server.monitoring.svc.cluster.local}"
NAMESPACE="${NAMESPACE:-default}"
# Maximum 5xx error ratio allowed (0.01 = 1%)
ERROR_THRESHOLD="${ERROR_THRESHOLD:-0.01}"
# Number of observation windows
CHECK_COUNT="${CHECK_COUNT:-5}"
# Seconds between checks
CHECK_INTERVAL="${CHECK_INTERVAL:-60}"

# --------------- Helpers ---------------
log() { echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $*"; }

query_prometheus() {
  local query="$1"
  local result
  result=$(curl -sf --retry 3 --retry-delay 5 \
    "${PROMETHEUS_URL}/api/v1/query" \
    --data-urlencode "query=${query}" \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('data', {}).get('result', [])
if results:
    print(results[0]['value'][1])
else:
    print('0')
")
  echo "${result}"
}

# --------------- Wait for rollout ---------------
log "Waiting for canary deployment rollout..."
kubectl rollout status deployment/opendota-ml-pipeline-canary \
  -n "${NAMESPACE}" --timeout=180s

log "Canary pods are ready. Starting health observation (${CHECK_COUNT} checks, ${CHECK_INTERVAL}s interval)..."

# --------------- Observation loop ---------------
for i in $(seq 1 "${CHECK_COUNT}"); do
  log "--- Observation window ${i}/${CHECK_COUNT} ---"
  sleep "${CHECK_INTERVAL}"

  # Total request rate for canary pods
  total_rate=$(query_prometheus \
    "sum(rate(http_requests_total{namespace=\"${NAMESPACE}\",pod=~\"opendota-ml-pipeline-canary.*\"}[1m])) or vector(0)")

  # 5xx error rate for canary pods
  error_rate=$(query_prometheus \
    "sum(rate(http_requests_total{namespace=\"${NAMESPACE}\",pod=~\"opendota-ml-pipeline-canary.*\",status=~\"5..\"}[1m])) or vector(0)")

  log "Total request rate: ${total_rate} req/s | 5xx error rate: ${error_rate} req/s"

  # Skip ratio check if there is no traffic yet
  if python3 -c "import sys; sys.exit(0 if float('${total_rate}') == 0 else 1)" 2>/dev/null; then
    log "No traffic observed yet — skipping threshold check."
    continue
  fi

  # Calculate error ratio
  error_ratio=$(python3 -c "print(float('${error_rate}') / float('${total_rate}'))")
  log "Error ratio: ${error_ratio} (threshold: ${ERROR_THRESHOLD})"

  exceeded=$(python3 -c "print('yes' if float('${error_ratio}') > float('${ERROR_THRESHOLD}') else 'no')")
  if [ "${exceeded}" = "yes" ]; then
    log "ERROR: 5xx error ratio ${error_ratio} exceeds threshold ${ERROR_THRESHOLD}!"
    log "Canary verification FAILED — triggering rollback."
    exit 1
  fi
done

log "All ${CHECK_COUNT} observation windows passed. Canary is healthy."
exit 0
