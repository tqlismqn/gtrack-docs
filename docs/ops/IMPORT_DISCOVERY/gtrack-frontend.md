# Import Discovery — tqlismqn/gtrack-frontend

**Meta:** \`{"archived":false,"default_branch":"main","full_name":"tqlismqn/gtrack-frontend","html_url":"https://github.com/tqlismqn/gtrack-frontend","license":"NONE","private":true,"pushed_at":"2025-10-05T00:51:39Z","visibility":"private"}\`

- **Default branch:** `main`   •   **Ref scanned:** `main`
- **Languages:** HTML: 106425, SCSS: 17423, TypeScript: 259698
- **Releases:** 0   •   **Tags:** 8

## Candidate roots

```json
{
  "message": "Not Found",
  "documentation_url": "https://docs.github.com/rest",
  "status": "404"
}[]
```

## Heuristic candidates

_No obvious doc/spec roots at repository root._

## Milestones
_No milestones_

## Roadmap issues (label: roadmap)
{"message":"Resource not accessible by personal access token","documentation_url":"https://docs.github.com/rest/issues/issues#list-repository-issues","status":"403"}

## Suggested import plan (edit in sync.plan.yaml)
```yaml
gtrack-frontend:
  ref: main
  include:
    - docs/**
    - spec/**
    - **/openapi/*.{yaml,yml,json}
    - **/README.md
  exclude:
    - node_modules/**
    - **/*.bak
```

_Generated 2025-10-05 09:41 UTC._
