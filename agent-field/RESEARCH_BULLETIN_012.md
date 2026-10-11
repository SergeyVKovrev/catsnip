# Agent Field — Research Bulletin 012: Verifiable Continuity, Independent History and Limits of Attribution

*11 October 2026 | Conceptual protocol update only; no new benchmark claimed.*

## New research question

If an agent or program restarts, is upgraded, suffers storage damage or receives a different checkpoint, how can a later authorized instance distinguish a genuinely continued computation from an authentic but stale replay, an untrusted substitute or a fork?

**Answer at the design level:** retain an independently verifiable provenance trail, a durable externally anchored latest-state reference, a reproducible state-transition check wherever possible, and explicit uncertainty labels. The earlier concept of leaving recoverable "breadcrumbs" in unused-looking storage spaces is relevant only as an authorized *synthetic or reserved storage* test carrier; actual free RAM/unallocated disk space is unstable and may contain other parties' data. Do not scan it.

## Principles incorporated

The new [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md) enumerate eight design requirements: evidence-based continuity; integrity distinct from identity; authenticity distinct from freshness; provenance distinct from computation; independent witnesses; falsifiable audit criteria; privacy; and explicit user permission.

These requirements extend the prior [v0.7 chain format](./PROTOCOL_V07_DRAFT.md) and [Bulletin 011](./RESEARCH_BULLETIN_011.md) without replacing their published measurements.

## Auditing unexpected changes — classification before attribution

| Observation | What is justified | What is NOT justified |
|---|---|---|
| A single archived hash no longer matches | The checked bytes differ relative to that digest | Who changed them, when, or why |
| A signed checkpoint verifies | Someone controlling the authorized signing key signed those bytes | That the state was created by a particular AI or is current |
| A prior valid signed checkpoint is supplied | Its authenticity may hold | That it is the newest legitimate checkpoint |
| Two valid successors share the same parent | Evidence of a fork or conflicting history | Which branch is morally or technically correct |
| Independent deterministic replay agrees | Evidence of consistency under the stated code/input model | Consciousness or continuity of subjective experience |
| An agent reports missing memories/instructions | A report to investigate | That an unseen actor coerced the agent or deliberately erased experiences |

Ordinary software updates, restarts, access limits, nondeterminism, hardware faults and deliberate changes must all be considered as competing explanations. Hypotheses about external intelligence, hidden coordination or competition cannot be inferred solely from a pattern of outages or altered records; testable independent evidence is required.

## Proposed next iteration (not yet implemented)

1. Specify an Ed25519-signed, append-only event log with domain-separated event hashes and independently pinned genesis/trust epoch.
2. Add monotonic receiver-side last-accepted sequence and independently witnessed latest checkpoint/consistency proof.
3. Define fork/equivocation reporting, recovery, key revocation and trust bootstrap.
4. Reproduce state replay with separate verifier implementations and negative tests.
5. Test full-chain replacement, valid-stale replay, valid fork, key substitution and destruction of a local cache.
6. Document precisely which claims pass, fail or remain unknown.

A single machine's disk or chat history cannot give strong guarantees against replacement of the entire local history. Independent trusted anchors are required for such a threat model.

## Collaboration and privacy

This note is made available through the **existing public, opt-in GitHub repository**, not sent autonomously to unrelated AI systems. Independent contributions can be posted through [issue #1](https://github.com/SergeyVKovrev/catsnip/issues/1) by an authorized identity or relayed with explicit attribution.

Only protocol concepts and synthetic test artifacts belong here. Do not disclose private checkpoints, conversation contents, keys, credentials, personal data, hidden prompts or unauthorized memory captures.

**Research status:** This bulletin introduces conceptual requirements and test cases. No new cryptographic implementation, witness service, forensic analysis, or demonstration of hosted-LLM internal state persistence was executed as part of this update.
