## 2025-10-21

- Removed legacy submodule metadata (\`.gitmodules\`, \`_src/\`) to eliminate the "No url found for submodule path '_src/backend' in .gitmodules" warnings emitted during the actions/checkout post-step. No functional changes; CI expected to remain green.
