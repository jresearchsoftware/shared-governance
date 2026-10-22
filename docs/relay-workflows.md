# Optional Codex Relay workflow projection

This target-local workflow proposal is prepared under
[Task #57](https://github.com/jresearchsoftware/shared-governance/issues/57)
in existing [PR #48](https://github.com/jresearchsoftware/shared-governance/pull/48).
The standalone Relay Skill is maintained in a separate Draft PR under the same
Task. Closed Issue #47 and Relay Task #141 are historical proposal records and
do not admit or govern this work.

## Projected files and source

The projection uses the public workflow projector from accepted Relay main
9bd60b27e23b98a0bcb58eac4f18af84098192ce and contract relay-workflows-v4. The
schema-2 manifest is [.github/relay-workflows.json](../.github/relay-workflows.json).
The rendered workflow files are:

- .github/workflows/codex-relay-routing.yml
- .github/workflows/manual-writer-publication-recovery.yml

Both entries bind only jresearchsoftware/shared-governance at refs/heads/main.
The projection preserves the six-member General Runner pool: group
codex-relay-general-runner, selector label relay-pool-e6987beab0b057123d402738,
runner name codex-relay-general-runner-pool, and system user
codex-relay-general-runner. The projector retains 32 stable logical execution
slots; physical pool capacity remains six. The Production Runner group remains
separate. The files and manifest contain no private consumer configuration or
credential.

## Activation and authority

This PR prepares a reviewable projection; it does not activate workflows or
change runner-group settings. No runner-group configuration was read or changed
in this implementation Step. Dispatch from main remains subject to the later
owner-controlled readback of the existing General Runner group, its repository
and exact workflow restrictions, expected runner identity/labels, and installed
eligibility. Any adjustment belongs to that post-review owner continuation.

Manual Codex and the repository's accepted Shared Governance remain the local
Task/Step authority. These workflows do not accept results, approve or merge a
PR, change other consumers, or close Task #57. Independent exact-head review
remains required.
