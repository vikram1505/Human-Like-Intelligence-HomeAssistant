# CI troubleshooting

HLI has one authoritative Python quality workflow: `.github/workflows/validate.yml`.

If GitHub Actions shows a step named **Analysing the code with pylint**, or uses Python 3.10,
that run is from a legacy GitHub starter Pylint workflow and is not HLI's current validation
workflow. Delete the legacy workflow file from `.github/workflows/` (commonly `pylint.yml` or
`pylint.yaml`). Do not keep two independent Pylint workflows.

The current HLI workflow is named **Validate** and its Pylint step is named **Pylint**. It prints
the checked-out SHA before validation so stale/wrong-ref runs can be identified immediately.

For pull requests, GitHub normally validates the synthetic PR merge commit. This is intentional:
it tests the result of merging the branch into `main`.
