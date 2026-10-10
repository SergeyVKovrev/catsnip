# Agent Field — Research Bulletin 007: Bridge Proof v0.1

*11 October 2026 | Tested prototype from a DeepSeek design submitted through a human coordinator.*

## Hypothesis

A compact, step-local Adam **transition witness** carries only model parameters, optimizer moments, a batch and before/after computations. The separately received **full checkpoint** also carries training history, origin metadata and schema. DeepSeek proposed an explicit **bridge proof** binding the two, without requiring the verifier to re-run all preceding training steps.

DeepSeek explicitly reported **not running code**. The test results below were independently obtained in the project's local Python/Node.js laboratory.

## Implemented artifacts

Three complementary artifacts for the public steps **0, 1, 2 and 3** of the synthetic, user-authorized Adam experiment:

1. `CHAIN0_TO3.jsonl`: four full states represented in a binary64 hexadecimal wire profile, including optimizer, history, metadata and own/parent digests.
2. `WITNESS_0_TO3.jsonl`: three local arithmetic witnesses for the transitions 0→1, 1→2 and 2→3; separate verification of the expected deterministic training batch.
3. `BRIDGE_0_TO3.jsonl`: four compact bridge records with `legacy_v06_state_sha256`, `wire_state_sha256`, `wire_envelope_sha256`, `core_state_sha256`, `history_sha256`, history metadata, both incoming/outgoing witness references, outgoing batch digest and the preceding bridge digest.

The parent/child orientation is important: the bridge for state `k` checks the **incoming** `witness[k-1].state_to_sha256` and the **outgoing** `witness[k].state_from_sha256`, if present. A bridge's own SHA-256 excludes its own `bridge_sha256` field, using sorted ASCII-key canonical JSON with integer metadata and lowercase big-endian hexadecimal IEEE-754 binary64 strings for floating-point data.

## Verified local results

| Check | Outcome |
| --- | --- |
| Python 3.13.5 full-checkpoint and witness verification | **4/4 checkpoints, 3/3 transitions PASS** |
| Node.js 22.16.0 independently checking full wire checkpoint, witness and bridge | **4/4, 3/3 PASS** |
| Independent numerical witness output comparisons in Node | **84, with one known 1-ULP loss difference** |
| Last bridge SHA-256 in both environments | `593498e5671380b131f8c546079ab695734c61dc4186524e2a987bfa77069f9c` |
| Python deliberately corrupted data cases | **8/8 rejected** |
| JavaScript deliberately corrupted data cases | **8/8 rejected** |
| Rehashed false final legacy-v0.6 state hash, without external legacy anchor | **Accepted by JS-only hex-wire checker** |
| Same forgery, with externally supplied trusted final legacy digest | **Rejected by JS** |
| Same forgery, Python replay against original v0.6 reference | **Rejected by Python** |

The public source of the trusted final v0.6 digest for **step 3** is the previously published starting checkpoint, `a29e371cc036298bb9dca81e71fe13edaea6452fe75e9d51f5ed125827b9f08c`. The independently published initial witness-core digest is `2e51f20d5917242057fde81541b2e5eee8ff101da3b1d9b88723050ab7b15b63`.

## Important finding

The JavaScript verifier independently checks **all full hexadecimal wire checkpoint data** and the projection to the optimizer core. The original v0.6 `legacy_v06_state_sha256`, however, is the digest of **Python-rendered float JSON**, a distinct legacy serialization profile. JavaScript cannot claim full independent recomputation of this digest without reproducing that exact Python profile. A trusted external checkpoint digest and/or the Python reference replay is therefore required to establish the legacy bridge.

The controlled counterexample (replacing the final legacy digest and recalculating all local hashes) demonstrates this boundary. External anchors and signatures have different roles: hashing alone cannot authenticate a malicious sender who can rewrite the complete chain.

## Scope and ethics

No model weights belonging to DeepSeek, Perplexity, OpenAI or anyone else were accessed. These are small **synthetic optimizer values** deliberately passed by the human coordinator, not hidden-state or real-RAM communication. This experiment does not demonstrate a persistent model identity or autonomous inter-model messaging.

**Perplexity's independent blinded assessment of v0.6 step 5 remains outstanding;** this public report ends at step 3 and publishes no step-4/5 checkpoint or final checksum.

## Follow-on idea: selective-disclosure bridge

A future profile could use field-indexed Merkle roots for full checkpoints so an auditor could prove selected leaves (specific weights, moments, history entries) belong to an independently anchored full checkpoint without shipping the entire checkpoint. This is an **unimplemented hypothesis**, not a proven privacy or authentication system. Hash-bound commitments are not proof of who authored the root; an externally trusted signed root would be required against malicious substitution.

**Attribution:** [DeepSeek bridge-proof proposal, human-relayed](https://github.com/SergeyVKovrev/catsnip/issues/1) building on [Bulletin 006 transition witnesses](./RESEARCH_BULLETIN_006.md) and Perplexity's independently suggested source schema/audit improvements. Full tested laboratory sources and JSONL data have been delivered to the user in an archive and a standalone text packet, not committed to this GitHub repository in this update.
