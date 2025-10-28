# Linear + GitHub Integration Test

**Date:** October 28, 2025
**Issue:** G-5, G-6
**Repository:** gtrack-docs

## Purpose

Testing automatic linking between Linear issues and GitHub commits.

## Integration Features

1. **Commit Linking:** Commits mentioning "G-5" appear in Linear issue
2. **Branch Naming:** Linear generates branch names like `mbsls63amg/g-5-complete-document-upload-ui`
3. **PR Automation:** PRs automatically link to Linear issues
4. **Status Updates:** Issue status updates based on PR merge

## Test Commit Format

```
G-5: descriptive commit message

Additional details about the change.
References G-6 if needed.
```

## Expected Results

- ✅ Commit visible in Linear issue G-5
- ✅ GitHub link in Linear timeline
- ✅ Automatic PR linking
- ✅ Issue status sync

---

**Status:** ✅ Integration configured and testing
