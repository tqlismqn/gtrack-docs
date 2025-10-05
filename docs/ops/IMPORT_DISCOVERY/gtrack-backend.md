# Import Discovery — tqlismqn/gtrack-backend

**Meta:** \`{"archived":false,"default_branch":"main","full_name":"tqlismqn/gtrack-backend","html_url":"https://github.com/tqlismqn/gtrack-backend","license":"NONE","private":true,"pushed_at":"2025-10-04T23:54:30Z","visibility":"private"}\`

- **Default branch:** `main`   •   **Ref scanned:** `main`
- **Languages:** Blade: 57022, Dockerfile: 1030, JavaScript: 285, PHP: 266840
- **Releases:** 0   •   **Tags:** 10

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
gtrack-backend:
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
