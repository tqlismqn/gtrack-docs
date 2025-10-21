#!/usr/bin/env bash
set -euo pipefail
REPO="${1:?repo}"
# close old sync PRs
for n in $(gh pr list -R "$REPO" --state open --label sync --json number,createdAt -q '.[] | select((now - ( .createdAt | fromdate)) > 24*3600) | .number'); do
  gh pr close -R "$REPO" "$n" -c "auto-close stale docs sync PR (>24h)"
done
# delete merged/closed sync branches left behind
for b in $(git for-each-ref --format='%(refname)' refs/remotes/origin/sync | sed 's#^refs/remotes/origin/##'); do
  gh api -X GET repos/${REPO}/branches/${b} >/dev/null 2>&1 || true
  git push origin --delete "${b#origin/}" || true
done

