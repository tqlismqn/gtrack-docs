# Branch protection configuration

To enforce branch protection on the `main` branch of the docs repository, run the following command. It requires the GitHub CLI (`gh`) to be installed and authenticated with sufficient permissions (typically repository admin access).

```bash
OWNER=tqlismqn
REPO=gtrack-docs
BASE=main

gh api --method PUT -H "Accept: application/vnd.github+json" \
  "repos/$OWNER/$REPO/branches/$BASE/protection" \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "docs-preview / build (pull_request)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null
}
JSON
```

To verify the current configuration, run:

```bash
gh api "repos/$OWNER/$REPO/branches/$BASE/protection" -q '.required_status_checks.contexts, .required_pull_request_reviews.required_approving_review_count'
```

If the GitHub CLI is not available in your environment, install it following the official documentation: <https://cli.github.com/manual/installation>.
