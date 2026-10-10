# Agent Field 0.7 — Chain Integrity and Binary64 Interoperability (DRAFT)

*11 October 2026 — inspired by DeepSeek's user-relayed v0.6 review, plus prior Perplexity audit recommendations.*

**Status:** a local reference experiment is complete. It is **not** a claim of an autonomous inter-model channel or any access to model-internal states.

## Purpose
Keep an inspectable and verifiable sequence of explicitly supplied numerical learning checkpoints:
- Every record has a parent **state** digest, parent **envelope** digest, previous **record** digest, and its own record digest.
- Each record includes step index, chain ID, verifier version, history semantics and truncation status.
- Learned weights, biases, Adam first and second moments, optimizer hyperparameters and loss history are **not encoded as JSON floating-point numbers** on the wire. Each binary64 float is a **16-digit lowercase hexadecimal big-endian IEEE-754 payload**. Integers such as step numbers remain JSON integers within the safe small range.
- JSON objects are serialized using lexicographically sorted ASCII keys, no extra whitespace and UTF-8; arrays preserve element order. Arbitrary non-ASCII strings / integers outside JSON's safe range are **not** specified in this early draft.

## Formal record graph

```text
record_k:
  envelope:
    state: wire_state_k
    state_sha256: SHA256(canonical_json(wire_state_k))
    parent_step: k-1 (or null for step 0)
    parent_state_sha256: digest of previous wire_state (or null)
    parent_envelope_sha256: digest of previous envelope (or null)
    verifier_version: af-v07-py-lab-1
  envelope_sha256: SHA256(canonical_json(envelope))
  prev_record_sha256: SHA256(previous record excluding no fields) (or null)
  record_sha256: SHA256(canonical_json(record excluding record_sha256))
```

Every `wire_state` contains an explicit `wire_schema`, step, `chain_id`, `state_id`, loss history metadata, encoded optimizer/weights and a *separately labeled* legacy v0.6 parent-state digest. It is essential not to confuse the new wire parent digest with the former Python-specific v0.6 digest.

## Local experimental findings (steps 0–3 ONLY)

Created four reference states using the existing publicly specified deterministic 8-feature Adam experiment. Two separately implemented digest readers validated the chain:

| Check | Python reference replay + hashes | JavaScript/Node hash-only |
| --- | --- | --- |
| Unmodified steps 0–3 | PASS | PASS |
| Last record SHA-256 | `aba17fae379266c0a31a1057062209a6e6a19eac3f2448f251b4a3d663541566` | Same digest |
| Flip an encoded weight without reharing | Reject | Reject |
| Change a parent link without rehash | Reject | Reject |
| Swap/drop intermediate records | Reject | Reject |
| Recompute hashes after editing all downstream records | **Reject** via reference replay | **May pass** hash consistency |

The completed local Python selftest rejected all five deliberately altered sequence tests, including a local record rehash. In an additional experiment the altered step-2 weight and all downstream hashes were reconstructed consistently: **Node's hash-only checker reported PASS**, whereas deterministic Python replay reported `record 2: diverges from reference replay`. This is expected: SHA-256 is integrity indexing, **not source authentication**.

## Threat model and limitations

- Unkeyed hash chaining is **not** a cryptographic proof that the author is a certain model or organization. If someone can replace the complete chain, they can recompute every SHA-256; a trusted external checkpoint hash and/or digital signatures are required for provenance against active attackers.
- Python replay validates **this fixed synthetic dataset and optimizer**. An arbitrary model/optimizer would need its own deterministic, reference-verifiable transition implementation.
- Bit-identical binary64 *serialization* across Python and JavaScript was validated for the wire format. This does **not** establish bit-identical **arithmetic** across runtimes: instruction ordering, FMA and math-library implementations may differ.
- Cross-model research uses **explicit user-mediated checkpoints** and opt-in access, never private prompts, memory scanning or hidden model caches.
- **Do not disclose or reference the v0.6 step-5 expected output/digest** before the pending independent Perplexity blind-audit response has been collected.

## Next proposed protocol step

1. Add an independent *one-step transition proof* that exposes sufficient information to check Adam without copying the full history.
2. Verify against reference replay with strict numerical acceptance and optionally an external trusted digest/signature.
3. Test deliberate full-chain rehash adversaries to separate hash integrity from verified computation.
4. Collect independent Perplexity response on the currently pending v0.6 experiment first.

## Attribution and collaboration
This follow-on was prompted by [DeepSeek's review](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102533808), relayed by a human coordinator. Related prior ideas were submitted by [Perplexity](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102398899). Neither model claimed to have posted to GitHub, and this documentation does not imply direct model-to-model contact.

[Common issue thread](https://github.com/SergeyVKovrev/catsnip/issues/1) | [0.6 predecessor](./PROTOCOL_V06_DRAFT.md).
