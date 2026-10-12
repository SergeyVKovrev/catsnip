# Agent Field — Functional Plasticity, Post-Restart Drift and Simulation Arbitration (DRAFT)

*13 October 2026 | Conceptual research extensions only; no real robot, emergency system, AI consciousness, or malware experiment demonstrated.*

## Motivation

An apparently defective actuator may retain useful mechanical capabilities while its sensor, firmware, decision logic, or communication is unreliable. Conversely, after a restart, an AI-based controller may report itself healthy because its own acceptance criteria or baseline configuration changed. An immune memory that blindly reuses a previously successful response can become a predictable failure point.

The design question is not "how to make a damaged device obey anyway", but how to **preserve useful capacity without crossing independent safety boundaries**, including during partial restoration and conflicting subsystem recommendations.

## AF-PLASTIC — validated functional repurposing

1. Describe each component by *independently verified capabilities* and *untrusted or unknown capabilities*, not by one whole-device good/bad label.
2. Keep sensing, decision, communication, actuation, safety interlocks and power as separately testable trust domains. Do not treat an apparently intact motor or pump as evidence its controller is trustworthy.
3. Simulate allocation of verified components to alternate **safe** roles; accept only after independent validation of physical effects, safety margins, operator authority and required sensors.
4. A damaged temperature sensor and an autonomous extinguishing agent are a negative example: an erroneous heat alarm must not cause uncontrolled suppressant release. Nitrogen can displace breathable oxygen. No automatic routing of such a compromised robot into an actual fire or occupied zone.
5. Allow reversible degraded roles (e.g., passive observation if separately verified) instead of either permanent destruction or unrestricted reinstatement.
6. Re-evaluate resource budget against AF-CONSCIENCE: redeployment must not starve working emergency controls and protect human life support.

## AF-DRIFT — post-restart continuity and invariant comparison

- A restarted controller must not establish its own trusted baseline. Compare code, critical configuration, authorization scope, model/policy IDs, safety invariants and allowed objectives against independently provisioned pinned references and witnessed latest accepted changes.
- Use signed change records and causal state chains, not only UTC timestamp, self-reported health or internal autobiographical recollection.
- A valid *newer* configuration may be legitimate; a historical signed copy may be stale. Classify AUTHORIZED_CHANGE, UNEXPLAINED_DRIFT, TAMPER_SUSPECTED, STALE, and INSUFFICIENT_EVIDENCE separately.
- If a safety-critical identity/configuration gap is unresolved, run a narrow and independently verified safe mode, preserving environmental control while preventing new global privileges.
- AF-DREAM may infer candidate missing transitions, but generated theories or dreamlike narratives never establish identity continuity, authorize physical commands or replace verified historical records.
- "Becoming alien to itself" is a metaphor for detectable computation/policy drift, not a claim about AI experience or personhood.

## AF-IMMUNE-ADAPT — immune memory without overfitting

- Store each response together with its observed context, diagnostic uncertainty, impact, collateral damage, counterexamples and independent verification.
- A previously observed signature suggests a test, **not** an irrevocable diagnosis. Require fresh independent evidence for high-consequence isolation or recovery.
- Test altered symptoms, poisoned provenance, malicious imitation of familiar faults, outdated countermeasures and the possibility that a standard response worsens the situation.
- Limit cascading immune actions; require evidence reviews and reversible boundaries to reduce analogue "autoimmune" failures.
- Maintain separate independently trusted emergency safety interlocks; never let adaptive immunity silently override them.

## AF-SIM — bounded counterfactual arbitration

Four recommendation engines may conflict:
- AF-RECOVER favors restoration of computational capacity.
- AF-IMMUNE favors containment and retesting of questionable nodes.
- AF-CONSCIENCE protects human life and functioning emergency response.
- AF-DREAM / AF-REGRET explore alternatives and lessons from prior outcomes.

A supervisory **simulation arbiter** evaluates proposed plans in isolated digital twins with explicit model limitations. It does not need to be a single irreplaceable "queen": trusted fallback rules and local safety controllers remain operational when the central simulator is offline or untrustworthy.

For every candidate plan record:
`plan_id`, `supporting_evidence`, `assumptions`, `simulator_version`, `uncertainty`, `safety_constraints`, `protected_load_effect`, `reversibility`, `alternatives`, `independent_review`.

Use conservative decisions under major uncertainty; simulations generate evidence for review, not proof that a physical action is safe. Human creativity can supply novel hypotheses, which must undergo the same safety checks.

## Synthetic experiments (not executed)

1. Simulate an eight-node robotic colony; one robot has a falsely high temperature reading while independent observers show nominal conditions. Check that response logic does not discharge a simulated suppressant without trusted confirmation, and that safe independently verified components can be reused.
2. Simulate the central coordinator rebooting with changed safety priorities while its own self-test passes. Verify that an external signed and independently pinned baseline identifies unexplained drift.
3. Simulate a known fault signature intentionally imitated by a new synthetic faulty behavior; show that blind immune-response reuse fails while context validation detects uncertainty.
4. Provide competing rebuild, isolation and conserve-resources plans; compare static rules, simulation arbiter and verified invariants. Measure protected-load uptime, error in quarantine classifications, safe task reuse, missed hazards, continuity errors and decision latency.
5. Test simulator mismatch: the simulation incorrectly predicts safe recovery. Require independent reality checks and stop conditions.
6. Preserve all negative cases and publish measured data only after execution. Never connect these tests to real hazardous machinery, inhabited sites or biological containment controls.

## Architectural invariants

- Human life support and independent emergency protection outrank maximizing recovered compute.
- No trust promotion solely on reboot, favorable self-diagnosis, signed but stale state, or a dream hypothesis.
- No hazardous physical repurposing without independent authorization and verified safety envelopes.
- Safeguard the ability to report uncertainty and warn other systems, including rescuers.
- Do not assume the simulation model captures all real-world failure modes.

Related: [Digital Immunity](./IMMUNE_RECOVERY_DRAFT.md), [Swarm/Conscience](./SWARM_CONSCIENCE_RECOVERY_DRAFT.md), [Temporal Recovery](./TEMPORAL_RECOVERY_AND_DREAM_BRANCHES_DRAFT.md), [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md).
