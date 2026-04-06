#!/usr/bin/env bash
set -euo pipefail

branch_name="${BRANCH_NAME:-$(git rev-parse --abbrev-ref HEAD)}"

# Skip strict feature-doc enforcement on default branches.
if [[ "$branch_name" == "master" || "$branch_name" == "main" ]]; then
  echo "Feature-doc check skipped on default branch: $branch_name"
  exit 0
fi

ticket_raw="$(echo "$branch_name" | grep -oE '[A-Za-z]{2,}-[0-9]+' | head -n1 || true)"

if [[ -z "$ticket_raw" ]]; then
  echo "ERROR: could not extract ticket ID from branch '$branch_name'."
  echo "Expected branch name to include a token like STU-108."
  exit 1
fi

ticket_id="$(echo "$ticket_raw" | tr '[:lower:]' '[:upper:]')"
base_dir="docs/features/$ticket_id"

required=(
  "$base_dir/spec.md"
  "$base_dir/design.md"
  "$base_dir/validation.md"
)

missing=0
for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "ERROR: missing required feature artifact: $file"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Create the required docs before pushing or merging."
  exit 1
fi

echo "Feature docs present for $ticket_id."
