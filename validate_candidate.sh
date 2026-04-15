#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 [--write] [--ttl PATH] CAND_FILE

Runs the candidate validator (and optionally applies the candidate) using the
repo virtualenv if present.

Options:
  --write        Apply the candidate into the editable TTL (write mode).
  --ttl PATH     Path to editable TTL (default: src/ontology/broiler-production-ontology-edit.ttl)
  -h, --help     Show this help

Examples:
  $0 curation/candidates/CAND-2026-001.yaml
  $0 --write curation/candidates/CAND-2026-001.yaml
EOF
  exit 2
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$ROOT_DIR/.venv/bin/python"
if [ -x "$VENV_PY" ]; then
  PYTHON="$VENV_PY"
else
  PYTHON="$(command -v python3 || command -v python)"
fi

MODE="--check"
TTL="$ROOT_DIR/src/ontology/broiler-production-ontology-edit.ttl"

if [ $# -eq 0 ]; then
  usage
fi

# simple arg parsing
while [[ $# -gt 0 ]]; do
  case "$1" in
    --write)
      MODE="--write"
      shift
      ;;
    --ttl)
      TTL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      CAND_FILE="$1"
      shift
      ;;
  esac
done

if [ -z "${CAND_FILE:-}" ]; then
  echo "Error: no candidate file provided."
  usage
fi

if [ ! -f "$CAND_FILE" ]; then
  echo "Error: candidate file '$CAND_FILE' not found." >&2
  exit 3
fi

if [ ! -f "$ROOT_DIR/scripts/apply_candidate.py" ]; then
  echo "Error: scripts/apply_candidate.py not found in repo." >&2
  exit 4
fi

echo "Using python: $PYTHON"
echo "Mode: $MODE"
echo "TTL: $TTL"
echo "Candidate: $CAND_FILE"

echo "Running validator..."
"$PYTHON" "$ROOT_DIR/scripts/apply_candidate.py" "$MODE" "$TTL" "$CAND_FILE"

EXIT=$?
if [ $EXIT -eq 0 ]; then
  echo "Validator finished successfully."
else
  echo "Validator exited with code $EXIT." >&2
fi

exit $EXIT
