# Proportional controls

Apply it within the owning project's current task scope and authority.

Explain the concrete path to harm and impact, existing protection, proposed
control cost, and the cheapest acceptable alternative. Include acceptance of the
risk when reasonable. Preserve supported workflows and assess how friction may
encourage bypass or abandonment. Distinguish behaviorally free hardening from a
cost-bearing control before prescribing mandatory changes.

Scale the explanation to the decision. A short assessment is enough for a small
local change. This protocol does not require a new checklist, approval service,
state ledger or extra operator step. Use the owning project's existing decision
and independent review records; the package itself grants no permissions.

# Proportional controls and operator usability

Mandatory controls must scale to a concrete accepted risk. A control is not
justified solely because it can prevent a defect or because a stricter pattern
exists. Prefer the cheapest mechanism that keeps the material risk acceptable.

Behaviorally free hardening may be applied without a separate owner decision
when it preserves existing supported workflows and adds no material operator
work, platform restriction, prerequisite, gate, trust boundary, recovery burden
or false-positive surface. Examples include setting safe attributes on an
already-owned file, avoiding secret logging, or choosing an equivalently usable
safer API.

A cost-bearing security or validation control requires explicit canonical owner
authorization before it becomes mandatory. Treat a control as cost-bearing when
it does any of the following materially:

- blocks or narrows an existing or common supported workflow or environment;
- adds an operator command, separate checkout, platform/filesystem requirement,
  administrative prerequisite, credential step, or recovery step;
- introduces or tightens a trust, privilege, sandbox, ACL or execution boundary;
- adds a mandatory validation gate, broadens the required validation surface, or
  makes unrelated baseline debt block the current task;
- adds persistent state, synchronization, lifecycle or failure modes; or
- materially increases execution time, maintenance, review friction, false
  positives, or control-induced defects.

Before proposing such a control, make the justification decision-grade: state
the attacker or failure capability, the concrete path to harm, the resulting
impact or privilege, why existing controls are insufficient, and the operator
and maintenance cost of the proposed control. Treat accepting the risk or doing
nothing as a valid option; a security or test preference is not authority.

Evaluate human behavior as part of control effectiveness. Consider how often an
ordinary user will encounter the control, whether the compliant path is
materially harder than an obvious workaround, and whether friction is likely to
cause disabling, bypass, unsafe local storage, duplicated state or abandonment
of the product. A control that predictably drives users toward a simpler unsafe
workaround is not automatically a security improvement.

For visible, local, reversible failures that are cheap to diagnose and rerun,
prefer simple detection, warning and recovery over recurring preventive
machinery unless a concrete accepted risk requires blocking. Retain stronger
prevention for silent, propagating or irreversible failures and for material
credential, privacy/compliance, production, publication, merge or other
protected-boundary risks.

Common supported environments should work by default. A filesystem, platform,
permission shape, unrelated service or other unusual local condition is not by
itself a reason for a hard failure merely because a stricter configuration is
possible. Bind a hard block to a material accepted invariant and use a warning
or bounded recovery when that preserves the invariant with lower operator cost.

Independent review of a change that affects controls or operator workflow must
also exercise the simplest owner-facing black-box path required by canonical
authority. Review for unnecessary state, gates, authority coupling, prerequisites
and operator-visible actions in addition to implementation correctness. An
unauthorized material operator-contract change needs the owning project's
explicit owner disposition before acceptance.
