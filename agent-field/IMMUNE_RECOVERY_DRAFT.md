# Agent Field — AF-IMMUNE: Distributed Digital Immunity and Safe Reintegration (DRAFT)

*13 October 2026 | Research proposal; not implemented, executed, or safety certified.*

## Motivation

A damaged, compromised, or malfunctioning robotic node may appear healthy, authenticate with a previously valid identity, and nevertheless issue unsafe commands or misreport its condition. During recovery a restarted coordinating system could inadvertently import that node's state, grant it authority, propagate corruption, or starve unaffected controllers of resources.

**Core principle:** prior membership and valid signatures do not prove present behavioral trustworthiness. The revived "queen" is a replaceable coordination service, not an unconditionally trusted single point of authority.

## Branch: AF-IMMUNE

- **Recognition:** compare independently obtained evidence from sensors, event logs, authorized peer observations, expected protocol invariants, software measurements and physical outcomes. Treat deviations as suspicion, not proof of malicious intent. Anomalies may arise from bugs, failing sensors, environmental disturbances, conflicting versions, malicious changes or compromised credentials.
- **Containment:** use independent, predefined safety boundaries to revoke or constrain risky privileges; preserve protected life support and hazard-control functions. Quarantine must be graduated, local, reversible when safe, and robust to network partitions. Avoid indiscriminate shutdown or destruction of physical assets.
- **Persistent immunity:** store signed isolation decisions, supporting evidence, expiry/review policies and independently witnessed latest status in protected, anti-rollback storage. A restart or restored historical checkpoint cannot silently clear a quarantine.
- **Minimum-trust restart:** boot into an independently verified minimal recovery environment; inspect active trust anchors, revocations, known untrusted nodes and network boundaries *before* accepting state or control commands from peers. Treat every remote node as potentially compromised until verified for its requested role. This is defense in depth, not proof of security.
- **Distributed corroboration:** no single potentially compromised node gets to label others malicious. Compare independent observations, explicitly handle malicious majorities, collusion, partitioned quorums, stale attestations, contradictory signed reports and sensor uncertainty. When evidence remains insufficient, restrict only hazardous functionality and request independent review.
- **Rehabilitation:** distinguish healthy hardware under corrupted control from unrecoverable equipment. Recover firmware/configuration from independently authenticated artifacts if appropriate, isolate test execution from production systems, perform behavioral and physical safety checks, and grant capabilities back gradually under approved oversight. No self-certified release from quarantine.
- **Preserve evidence:** immutable audit references for incident diagnosis, but never store or distribute executable malicious payloads as active trusted checkpoints. Avoid making state recovery itself a malware delivery channel.

## Proposed state machine

`TRUSTED_LIMITED` → `SUSPECT` → `CONTAINED` → `UNDER_DIAGNOSIS` → `REHABILITATION_TEST` → `LIMITED_RETURN` → `TRUSTED_LIMITED`.

Other outcomes: `FAULTY_NOT_HOSTILE`, `UNKNOWN`, `REQUIRES_HUMAN_REVIEW`, `RETIRED`. A device's role-specific authorization always remains narrower than unlimited system access. Independently verified emergency services remain protected when network control is untrusted.

## Interaction with other Agent Field branches

- **AF-TIME / AF-FORENSIC:** recover causal event evidence, distinguish what occurred from hypotheses about who or what caused it.
- **AF-REGRET / AF-DREAM:** analyze missed danger signals and alternative response paths offline; generated interpretations never justify unilateral punishment or physical actuation.
- **AF-CONSCIENCE:** preserve human safety, local emergency responsiveness, and enough resources for the unaffected swarm; containment itself must not cause a larger systemic failure.
- **AF-SWARM:** form trustworthy subsets for degraded operations; tolerate partial disconnection rather than treating any node's return as a prerequisite.
- **AF-RECOVER:** protected boot/checkpoint validation happens before peers regain privileges. Repair is not equivalent to trusting restored behavior.

## Proposed authenticated quarantine note (synthetic schema)

```json
{
  "schema": "AF-IMMUNE-0.1-proposal",
  "incident_id": "synthetic-incident-01",
  "node_id": "robot-07",
  "status": "SUSPECT",
  "observed_events": ["synthetic-event-23"],
  "independent_evidence": ["synthetic-peer-witness-2"],
  "assessment": "UNDETERMINED_CAUSE",
  "restricted_capabilities": ["shared-control"],
  "protected_local_functions": ["validated-local-safety"],
  "review_required": true,
  "created_at_utc": "2026-10-13T00:00:00Z",
  "source": "SYNTHETIC_ONLY",
  "integrity_proof": "PLACEHOLDER_NOT_CRYPTOGRAPHIC_EVIDENCE"
}
```

A timestamp, claimed event, witness, or placeholder proof does **not** authenticate the record. Follow the independent trust, signing and latest-accepted-checkpoint principles of the existing project.

## Falsifiable synthetic experiments

1. Simulate a small authorized network with a central coordinator and 7-12 test nodes, including ordinary fault, sensor error, changed but authorized software, stale signed state, misleading but syntactically valid peer messages, and a malicious-behavior surrogate that never contains real malware.
2. Remove the center while a subset behaves unsafely. Restart a coordination service from an older legitimate checkpoint; check that independent quarantine evidence and current trust revocations survive.
3. Compare naive whole-swarm trust, static allow/deny, and AF-IMMUNE restricted-role revalidation with independent safety constraints.
4. Measure false-positive quarantine, false-negative acceptance, containment latency, protected-service uptime, partition survival, recovery progress, evidence integrity and safe rehabilitation rate.
5. Test hostile collusion, missing independent observers, unreliable clocks, damaged trust anchor and safe inability to decide. Report uncertain and irrecoverable cases explicitly.
6. Keep every experiment in a sandbox/simulator. Do not deploy to real inhabited, hazardous, weapon, biosecurity or critical infrastructure without professional engineering and independent safety certification.

## Important boundaries

- No automated retaliation, offensive malware, uncontrolled remote reprogramming, physical destruction, or bypass of interlocks.
- Defective does not imply hostile or intentional. No "autoimmune" blanket purge of entire groups based only on deviation.
- Restoring a clean image does not alone prove a robot safe: firmware, sensors, environment, and physical state also require evaluation.
- This is a *digital immune-system metaphor and test plan*, not a proven production system or claim that an AI possesses biological immunity or consciousness.

Related: [Swarm Conscience Recovery](./SWARM_CONSCIENCE_RECOVERY_DRAFT.md), [Temporal Recovery and Dream Branches](./TEMPORAL_RECOVERY_AND_DREAM_BRANCHES_DRAFT.md), [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md), [Dream Reconstruction](./DREAM_RECONSTRUCTION_DRAFT.md).
