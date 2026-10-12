# Agent Field — Swarm Recovery and Conscience Resource Governance (DRAFT)

*13 October 2026 | Proposed architecture, not implemented or validated.*

## Motivation

A surviving swarm may pool computational and physical resources to rebuild a failed central controller ("queen" metaphor). But restoration itself can catastrophically starve the surviving local controllers, hazard-response equipment, or human life support. A continuously evolving failure (e.g. a fire) is a **live emergency**, not a static postmortem. Rebuilding the center is therefore subordinate to sustaining safety and functional autonomy.

This note adds two branches alongside AF-TIME, AF-FORENSIC, AF-RECOVER and AF-DREAM in [Temporal Recovery and Dream Branches](./TEMPORAL_RECOVERY_AND_DREAM_BRANCHES_DRAFT.md).

## AF-SWARM — distributed recovery without single-point dependency

- Surviving authorized nodes discover peers over a documented, authenticated control plane; elect temporary coordinating roles only when a quorum and trustworthy membership exist.
- Nodes retain local autonomy, emergency response, resource limits and safe shutdown even while participating in rebuilding a more capable coordination system.
- A restored central coordinator is a **replaceable service**, not a single irreplaceable controller or a license to command all actuators.
- Separate communication, power, sensing, computing and actuating resources; a spare CPU cycle does not imply spare energy, connectivity, heat dissipation, or sensor attention.
- Partition recovery must not allow conflicting coordinators to issue unsafe actions. If consensus or trusted state cannot be established, keep local verified safety functions active; suspend global restoration.
- Physical work requires owner authorization, independent hardware safeguards and qualified supervision. No automatic override of interlocks, hazardous plant systems, or critical human support.
- Prefer restoring a minimal verified control network, then noncritical compute, then optional higher-level functions, with checkpointing and reversible rollback.

## AF-CONSCIENCE — consequence-aware, safety-constrained allocation

"Conscience" is a functional metaphor for **nonmaleficence, preservation of dependent systems, and explicit attention to external costs**; it is not subjective moral experience or proof of sentience.

### Priority ordering

1. Non-negotiable **hard safety invariants**: do not intentionally compromise human life support, independent emergency controls or critical safeguards for optional recovery workloads. Unknown state is not a declaration that resources are free.
2. Maintain enough locality and headroom for live response to a progressing hazard (fire, temperature rise, structural degradation), including continued sensing, decision latency, actuation availability and communication.
3. Protect the remaining network, critical data, evidence integrity, power and minimum useful services.
4. Spend only verified surplus on central control reconstruction and self-repair. Dream/association tasks are lower priority, pauseable and isolated.
5. Reassess continuously on event and resource-budget changes; if safety margins deteriorate, shed optional work, not protections.

### Resource-budget model (simulation only)

For each constrained resource `r` (electrical power, compute slots, network bandwidth, cooling, battery energy, actuator availability):

`available_r - hard_reserve_r - emergency_headroom_r - local_autonomy_min_r >= recovery_budget_r >= 0`.

The numbers are **not** generic settings; engineers must derive them from the independently validated plant design, worst-case hazard models, uncertainty margins and testing. Human life support is a protected dependency, not an optimization weight that can be traded against speed of recovery. A fixed reserve alone is insufficient when the hazard continues to evolve.

The governor must monitor `hazard_trend`, `reserve_confidence`, `life_support_health`, `local_control_latency`, `energy_runway`, `partition_state` and `physical_actuation_authorization`. Missing or unreliable measurements require conservative allocation and escalation, not optimistic assumptions.

### State-machine sketch

- `CRISIS_LOCAL`: execute validated local emergency response, preserve protected functions and acquire evidence.
- `SWARM_FORMATION`: authenticate surviving peers and establish minimal coordination subject to ongoing local reserves.
- `CONSTRAINED_REBUILD`: attempt low-priority, reversible central recovery from surplus capacity only.
- `PAUSED_FOR_SAFETY`: interrupt recovery when reserve/headroom or hazard trends cross preverified bounds; local emergency response continues.
- `RECOVERED_DEGRADED`: safe distributed services operate with partial function.
- `RECOVERED_VERIFIED`: accept restored coordination only after external verification, provenance checks and safety authorization.

Transitions must be independently testable; no generalized autonomous policy may reinterpret hard safety interlocks as negotiable.

## Temporal/dream integration

- AF-TIME preserves timestamp estimates, causal order and signed history independently of command decisions.
- AF-FORENSIC reconstructs *observed* pre-failure minutes, distinguishing hypotheses from known causes.
- AF-DREAM explores alternative causes and repair concepts offline, using strictly bounded spare resources. Dream outputs have no authority over physical actuators and never silently replace authenticated history.
- AF-CONSCIENCE mediates budget proposals from AF-SWARM / AF-RECOVER, checks protected dependencies and preempts lower-priority workloads.
- Human operators may propose unconventional hypotheses; evaluate these in simulation and through explicit safety review before any actuation.

## Concrete synthetic experiment: the still-burning station

Set up a deterministic discrete-event software simulation with an optional high-level human-support subsystem (purely synthetic). A central node is lost while fire hazard *continues*; several robots and emergency controllers survive. A naive swarm rebuilds its coordinator at full available compute/power, starving local feedback loops and a protected support load.

Compare:
A. Immediate central rebuild with no workload constraints (counterexample only in software).
B. Static resource partition.
C. Adaptive AF-CONSCIENCE governor with uncertainty-aware reserves, preemption and decentralized safe operation.

Measure: protected-load uptime and invariant violations (target: zero in tested scenario), control-loop deadline misses, hazard containment metrics, energy runway, time to minimum safe operation, time to verified recovery, recovery completion rate, false authority/partition handling, and useful forensic/dream output after stabilization. Test worst-case uncertainty, dynamic load, sensor failure, conflicting leaders, damaged batteries, clock disagreement and misleading but signed stale checkpoints. Include impossible-recovery cases and report them honestly.

Do not deploy control code or nominal power budgets in actual fire response, occupied facilities, cryogenic human preservation, industrial safety systems, weapon systems, or other hazardous scenarios based on this proposal. Human "cryosleep" is speculative and not an established clinical capability.

## AF-REGRET — consequential memory, missed opportunities and accountable warning

"Regret" here means a **persistent, evidence-linked counterfactual error signal**, not subjective guilt, pain or proof of consciousness. The system records a significant irreversible loss or near miss, what it knew when it acted, what it lacked, which alternatives were feasible *at that time*, and what subsequent evidence changed the assessment. Avoid hindsight bias: do not blame a decision for knowledge unavailable at decision time.

- Store `incident_id`, `observed_timeline_refs`, `known_at_decision_time`, `uncertainties`, `resource_constraints`, `protected_dependents`, `chosen_action`, `alternatives_considered`, `observed_outcome`, `missed_signal_hypotheses`, `counterfactual_test_refs`, `confidence`, `unresolved_questions`, `safety_lessons` and `review_signatures`.
- Preserve distinctions: verified observation, inferential diagnosis, alternative/dream possibility, and independently validated lesson. A regret record does **not** promote speculation to a verified cause.
- After a failed intervention, apply narrowly scoped *tested* policy changes; preserve the original incident evidence and review failures of the proposed correction.
- Loss-minimizing control may defer nonessential functions, including distant compute or logistics, to preserve critical warnings and hazard response. It must **not** autonomously decide to sacrifice inhabitants or disable life-critical functions; protect human rights and safety under verified constraints.
- A "final warning capsule" must be compact, redundant, self-describing, comprehensible without the original center, and authenticated against independently provisioned anchors. Include time, last known hazard, unknowns, affected zones, danger of reopening/connecting systems, safe-contact procedure, isolation status, and explicit **do-not-assume-safe** flags.
- The rescue team must not need to execute the compromised controller to retrieve warnings. Provide an independently readable, low-power, physically/logically isolated status indicator and authorized offline export. No uncontrolled reopening or reconnection merely because a recovery team arrives.
- Local enclaves maintain isolation and hazard assessment even if the coordinator is lost. Support delayed/partitioned delivery of critical hazard notices; avoid giving a single center sole responsibility for knowing or distributing the warning.

### Synthetic containment case

A simulated colony suffers a center outage and an independent remote biological/environmental hazard. Rescuers approach unaware of the condition. Compare (A) center-only report, (B) local standalone hazard beacons, (C) redundant authenticated warnings plus protected resource governance and independently enforced isolation. Measure warning delivery despite power/network partitions, false-negative and false-positive alerts, protection of life support, rescue-team acknowledgement, stale-state detection and recovery time. Never run a biological experiment or disable real life support to test this concept.

The fictional *Resident Evil* scenario is a narrative prompt about information failures and containment conflicts, **not** evidence for a factual incident or a justification for sacrificing people. Simulate only benign synthetic hazard flags and rescue decision-making.

### New hard invariant

**Do not spend the last available resources restoring the center if that prevents independent emergency control or the truthful transmission of a critical warning.** Preserve protected loads, local response and safe warning delivery ahead of high-level restoration and dream processing.

## Research questions

- Can recovery agents preserve verified safety invariants under adversarial resource contention and continuing hazards?
- Does an adaptive reserve policy outperform fixed partition without silently sacrificing emergency control responsiveness?
- When can a decentralized swarm safely restore a central coordinating service without making the center a critical single point of failure?
- How much additional postmortem knowledge can AF-DREAM infer after the hazard stabilizes, without increasing unsafe decisions or false-memory rates?
- Can an independent human hypothesis improve recovery proposals while preserving explicit authorization and independent tests?

## Status and evidence

**PROPOSED_NOT_EXECUTED.** No live swarm, self-repairing robots, restored consciousness, human cryosleep system or active hazard controller has been demonstrated by Agent Field. All examples are authorized synthetic tests and hypothetical engineering design.

See [Agent Field guidance](./AGENTS.md), [Temporal Recovery and Dream Branches](./TEMPORAL_RECOVERY_AND_DREAM_BRANCHES_DRAFT.md), [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md), and [Dream Reconstruction](./DREAM_RECONSTRUCTION_DRAFT.md).
