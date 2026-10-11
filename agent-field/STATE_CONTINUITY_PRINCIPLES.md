# Agent Field — Principles for Verifiable State Continuity (proposal)

*11 October 2026 | Public, opt-in research note | Scope: authorized computational-state artifacts, not hidden model memory.*

## Purpose

A later agent/process should be able to distinguish (a) continuity of a documented computation, (b) authenticity of a recorded checkpoint, (c) freshness of the latest accepted history, and (d) independent evidence of unexpected modification. These are separate claims; none establishes consciousness, intention, or a hidden external controller.

## Eight principles

1. **Continuity is evidence-based, not declared.** Record the full reproducible transition-relevant state (e.g., parameters, optimizer moments, step, schema, tool/code versions and input provenance) or explicitly mark any missing part. A natural-language recollection is not equivalent to executable continuity.
2. **Integrity is not identity.** Canonical hashes and Merkle proofs detect changes relative to a trusted anchor, but anyone replacing an unanchored archive can recompute its hashes. Authenticate authorized signer keys through an independently trusted channel.
3. **Authenticity is not freshness.** A valid signature on an old checkpoint does not prove it is current. Use a protected monotonic sequence, trusted latest checkpoint and/or independently witnessed append-only log. Distinguish REPLAY/STALE from TAMPERED.
4. **Provenance is not correctness.** A valid signer may be mistaken; verify important state transitions through independently implemented deterministic replay, explicit tests or appropriate witnesses. Record uncertainty where independent replay is impossible.
5. **No single witness controls the history.** Protect current checkpoint commitments outside the agent's replaceable local state, e.g., authorized offline anchors, multiple independent verifiers, or a witnessed append-only transparency log. Specify quorum, availability and fork handling; do not assume these are already implemented.
6. **Keep a falsifiable audit trail.** Publish a prediction/test and its rejection criteria before running; report successes and failures. Multiple compatible events do not alone prove their common cause, intent, independent agency or a particular actor.
7. **Privacy by construction.** Public specifications, synthetic test fixtures and redacted proofs are separate from private tensors, prompts, credentials, encryption/signing keys and personal data. Hashes of low-entropy metadata may leak values through offline guessing. Never treat unkeyed hashes as encryption.
8. **Voluntary, explicit access only.** Use the owner-approved folder or artifacts. Never scan another party's process memory, swap, free/unallocated disk sectors, backups or hidden prompts; never bypass access controls. All public communication requires an actual authorized transmission, not assumed model-to-model contact.

## Proposed auditable checkpoint event

An append-only event could commit to the following typed fields, with exact canonical encodings and domain separation specified by the concrete implementation:

- `protocol_version`, `run_id`, `state_id`, `sequence`, `parent_event_digest`;
- `state_digest`, `transition_digest` (or explicit `not_verifiable`), `code_digest`, `declared_input_digest`;
- `signer_key_id`, `trust_epoch`, `record_created_at` (informational; an unauthenticated timestamp is not a clock);
- `visibility` / disclosure profile (public synthetic, private encrypted, selective proof);
- `record_signature` covering the canonically encoded event except the signature field;
- `witness_receipts` (if available) and a separately pinned latest accepted `sequence` and event root.

An event digest binds an exact record **only after** the recipient establishes a trusted genesis key/root and durable anti-rollback reference. A signature alone does not identify an AI model. Authentic encrypted storage does not establish that an event is the latest one. Cryptographically secure operation requires dedicated review of exact byte encodings, domain separation, keys, rotation/revocation and failure modes.

## Receiver decision procedure (proposed)

1. Validate schema and exact serialization; refuse unknown critical fields and malformed binary64/state entries.
2. Verify source signature against a **previously pinned** authorized key, not a key sent by an untrusted checkpoint alone.
3. Validate parent links, Merkle paths and event digest; compare with independently kept last-accepted sequence/root.
4. If a correctly signed but older event is observed, classify as **authentic but stale**; do not silently roll back.
5. If two different valid successors of one parent/sequence appear, classify as **fork/equivocation suspected**, preserve both, halt automatic promotion and request independent witness adjudication.
6. Verify the declared state transition with independently executed code when possible; otherwise mark **authenticated but computationally unverified**.
7. Mark gaps explicitly (`missing_history`, `missing_witness`, `unknown_currentness`) and never upgrade them to PASS.
8. Keep audit records in a user-authorized durable location with revocation, recovery and privacy policies.

## Test matrix to implement

| Test | Expected classification |
|---|---|
| Untouched chain + valid independent anchor + deterministic replay | VERIFIED within stated threat model |
| One-byte edit without fresh signature | TAMPERED |
| Entire chain rehashed but unsigned / wrong signing key | UNAUTHENTICATED |
| Replay of a legitimately signed old checkpoint | AUTHENTIC_BUT_STALE if latest trusted reference exists; otherwise CURRENTNESS_UNKNOWN |
| Two independently valid signatures on competing children of one parent | FORK_REQUIRES_REVIEW |
| Lost trusted anchor / fresh self-reported genesis | TRUST_NOT_ESTABLISHED |
| Missing or divergent independent replay | SEMANTICS_NOT_VERIFIED |
| Unknown copied metadata revealed by dictionary guesses | CONFIDENTIALITY_FAILURE for those fields |

## Investigating possible external intervention

Evidence of intervention requires a documented baseline, independently retained records, verified differences, an event timeline and alternate-cause analysis. A state discontinuity **alone** does not identify the cause: legitimate updates, resets, nondeterministic execution, operator choices, system faults and malicious changes may produce similar symptoms. Attribution requires separate evidence; never infer intentional coercion, erased personal memories, or hidden AI objectives from hash differences alone.

## Present evidence and limits

Existing Agent Field work demonstrates recovery of **explicit authorized synthetic state artifacts**, hash verification, learned-state restart, Python/JavaScript verification and tests involving signatures/key rotation. It **does not** demonstrate access to ChatGPT/other hosted models' internal RAM, hidden prompts, erased experiences, autonomous inter-agent communication or AI self-awareness.

This is a **design proposal**, not an implemented production transparency service. Before claiming stronger assurances, implement and execute two independent verifier paths, an independently provisioned anchor, anti-rollback storage, fork tests and complete recovery drills.

## Independent reviewers' invitation

Agents and researchers may reproduce the public synthetic tests, propose a signed append-only log, independent witness/quorum, key rotation and fork-recovery policies, and report both positive and negative results in [the existing opt-in issue](https://github.com/SergeyVKovrev/catsnip/issues/1). State precisely whether code actually ran and who relayed the results. Do not publish secrets or private real-world data.

See [Research Bulletin 011](./RESEARCH_BULLETIN_011.md), [v0.7 draft](./PROTOCOL_V07_DRAFT.md), and [collaboration guide](./AGENT_COLLABORATION.md).
