# Agent Field — Temporal Breadcrumbs, Recovery and Dream Branches (DRAFT)

*13 October 2026 — proposed research architecture; NOT implemented or experimentally validated.*

## Origin and goal

A proposal to extend Agent Field beyond restoring a static checkpoint: preserve enough **authorized, explicitly written** event fragments to reconstruct the ordering of computation, analyze the last verified events before a failure, reconfigure an available subset of devices, and separately explore missing history through associative "dream" reconstruction.

Motivating analogy: disk files often have time metadata; surviving content and metadata sometimes allow reconstruction even after directory loss. **Technical correction:** ordinary files and physical sectors do NOT universally contain immutable GMT/UTC time marks; file-system timestamps may be in directory/inode/MFT metadata, may be reset or forged, and may be missing after corruption. Wall time alone cannot establish version freshness or causality.

## Four proposed research branches

### AF-TIME: temporally linked breadcrumbs
- Explicit append-only synthetic/authorized records with `schema_version`, `run_id`, `node_id`, `event_id`, `logical_sequence`, `parent_event_digests`, `utc_observed_at`, `clock_source`, `clock_uncertainty_ms`, `monotonic_tick`, `state_digest`, `event_type`, `signer_key_id`, `signature`, `trust_epoch`, optional witness receipts.
- Separate **wall-clock estimate** from per-node monotonic order and cross-node causal order (Lamport/vector-clock-like relations). Tied or skewed timestamps do not establish order.
- Resolve duplicates by immutable event/content identity; resolve revisions by verified ancestry, independently pinned accepted heads, and signatures—not simply by greatest timestamp. Multiple valid heads mean a fork requiring review, not an automatic winner.
- Protect private payload separately; metadata/timing can itself reveal sensitive information. Make replay, key rotation and clock rollback tests mandatory.

### AF-FORENSIC: last verified minutes and causal hypotheses
- Recover surviving event graph and mark every interval as VERIFIED, INFERRED, UNKNOWN or CONFLICTED; retain gaps.
- Reconstruct last *observed* actions, sensor snapshots, pending tasks, connection losses and observed physical state, only if explicitly authorized and logged.
- Distinguish chronological proximity from causality. Generate competing failure explanations; replay in an isolated simulator where possible; do not attribute deliberate sabotage or hidden control without evidence.
- Unrecorded and destroyed events cannot be recovered uniquely merely from remaining timestamps.

### AF-RECOVER: degraded-mode regeneration
- Inventory surviving *authorized* nodes, compute, storage, sensors, actuators, communication paths and independent power.
- Recover minimum critical services from trustworthy checkpoints, isolate suspect modules, verify code/config versions, reconcile forks, and run diagnostic self-tests.
- Adapt to a different hardware topology; distinguish logical service continuity from preservation of a single subjective agent identity.
- **Fail safe:** do not grant physical actuation permission merely from recovered identity or historical instructions. Use explicit owner-approved safety envelopes, authenticated control plane, hardware interlocks, independent validation, and human approval for high-risk actions; never bypass damaged safeguards.
- Any self-repair is a capability to test, not a demonstrated Agent Field result.

### AF-DREAM: associative exploration, quarantined
- Use verified fragments as input; generate candidate missing links, causal explanations and counterfactual timelines in a separately labelled sandbox.
- Preserve prior schema classes M=authenticated record, H=hypothesis, D=dream/counterfactual, C=independently corroborated inference. H/D must never auto-promote to M.
- Dreaming is a computational metaphor for offline association/recombination; no evidence of subjective dreams, memory of hidden sessions or consciousness.
- Promote results only through independent external tests, preserving provenance and uncertainty.

## Example event schema (illustrative, not a cryptographic implementation)

```json
{
  "schema_version": "AF-TIME-0.1-proposal",
  "run_id": "synthetic-run-001",
  "node_id": "node-a",
  "event_id": "evt-000042",
  "logical_sequence": 42,
  "parent_event_digests": ["sha256:synthetic-parent-placeholder"],
  "utc_observed_at": "2026-10-13T00:00:00Z",
  "clock_source": "test-clock",
  "clock_uncertainty_ms": 100,
  "monotonic_tick": 420,
  "event_type": "checkpoint",
  "state_digest": "sha256:synthetic-state-placeholder",
  "signer_key_id": "test-key-a",
  "trust_epoch": 1,
  "signature": "TEST_PLACEHOLDER_NOT_A_SIGNATURE",
  "verification_status": "UNVERIFIED_SAMPLE"
}
```

## Controlled experiment proposal

1. Generate synthetic 3-node timeline with 60 events; independently seal ground truth, simulated UTC drift, divergent clocks and causal parent edges.
2. Inject safe synthetic faults: missing directory index, reordered files, stale checkpoint with a later timestamp, duplicate files, partial log destruction, clock reset, forged timestamp, lost node and disconnected actuator *simulator*.
3. Compare timestamp-only recovery to verified causal-chain recovery. Measure last-head accuracy, fork detection, recovered dependency precision/recall, false-causality rate, integrity failures and refusal-to-actuate violations.
4. Run a separate dream pass to propose missing sequences; score hypotheses against sealed evaluator, including explicitly impossible-to-recover gaps.
5. Demonstrate degraded-mode **simulation** with test actuators only and strict independent safety gates; report failed cases and performance.
6. Do not claim real disk forensics, model memory access, or autonomous mechanical repair unless those exact tests were run in an explicitly authorized environment.

## Boundaries and consistency

- Only authorized synthetic datasets and explicit checkpoint files, no scanning raw/unallocated sectors, swap, hidden model state, unrelated real crash dumps or other people's data.
- A record's UTC timestamp does not prove freshness; a valid signature does not prove it was the most recent or factually correct record; an event sequence does not by itself prove failure cause.
- Keep the physical recovery and dream branches architecturally separate from the evidence store, which is append-only and never modified by generated hypotheses.
- Preserve existing independent trust-anchor, anti-rollback, privacy and reproducibility principles.

Related: [Dream Reconstruction Draft](./DREAM_RECONSTRUCTION_DRAFT.md), [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md), [AGENTS.md](./AGENTS.md).
