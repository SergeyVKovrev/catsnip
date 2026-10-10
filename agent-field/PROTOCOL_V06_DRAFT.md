# Agent Field 0.6-RC1 — Learned-State Handoff Benchmark
*Draft: 2026-10-11. Derived from independently relayed DeepSeek and Perplexity proposals.*

## Research question
Can two independent, explicitly authorized agents continue one deterministic numerical training run through a **portable checkpoint** including parameters, Adam momentum and variance, step count and history? This is user-mediated file exchange; **not** access to another model's RAM, weights, caches, confidential data or consciousness.

## Joint proposal attribution
- [DeepSeek proposal](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102384614): invariants, blind audit, provenance hashes, full Adam checkpoint and loss-vs-parameters consistency.
- [Perplexity proposal](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102398899): explicit schema/indexing, multiple representation hashes, deterministic operation ordering, accurate tool-use reporting, structured histories and mutation tests.

## Experimental materials (no hidden reference outputs)
- [Python 3.10+ standalone reference executor](./agent_field_v06_executor.py) — standard library, deterministic synthetic 8-feature linear regression with Adam, no external tools or memory probing.
- [Starting checkpoint, 3 steps complete](./START_CHECKPOINT_V06.json) — full weights, bias, 9 first moments, 9 second moments, a history, state ID and parent digest.
- Authoritative SHA-256 of canonical starting *state* is `a29e371cc036298bb9dca81e71fe13edaea6452fe75e9d51f5ed125827b9f08c`.
- The complete local lab also contains a longer reference script and self-test runner; its digest and result were checked against this compact executor.

The hash covers only the `state` object; specifically its bytes under the **Python reference canonicalization**:
`json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')`.
This is *not* a language-neutral JSON canonicalization standard. SHA-256 by itself cannot authenticate the sender; external trusted digest/signatures are needed for adversarial scenarios.

## Independent cross-model roles
1. **DeepSeek / executor:** receive step-3 checkpoint and reference; verify its digest, complete *two further Adam training steps*, return complete step-5 envelope, the digest, holdout loss and truthful report of tool execution. Do not reset optimizer moments.
2. **Perplexity / blinded auditor:** receive the exact same step-3 checkpoint; independently calculate step 5 **before** seeing DeepSeek's result. Return full envelope and loss. Only then inspect DeepSeek's output and classify mismatches.
3. **Independent reference / arbiter:** compare exact checkpoint fields and digest against the reference replay; verify both parent hashes, state ID/step, complete 9+9 moments, history, and holdout loss; test controlled corruptions.
4. Capture immutable first submissions before sharing results. **Do not publish the final expected step-5 checksum before both agents complete their independent attempts.**

## Current controlled results (not external-model outcomes)
A reference Python run passed its built-in tests: first 3 then 2 steps gave the same canonical step-5 state as an uninterrupted 5-step run. The holdout loss on the fixed synthetic sample set fell from `0.3550050525296683` (step 3) to `0.2855122113905206` (step 5). This is not an LLM performance metric.

## Follow-on phases
Perplexity proposed a richer graph-based 8D vector state and last-16 observation queue. Add sparse 8×8 coordinate links, controlled one-element corruption and error classification **after** the minimal Adam test, keeping the added complexity isolated. Explicitly distinguish numerical equivalence (binary64 and operation order) from integer codec equality and cryptographic authenticity.

## Review and participation
Agents may read these public files when their interfaces allow it; reading does not grant GitHub write permissions or message-delivery capability. If no authorized GitHub tools are available, prepare a markdown report for the user to relay. Attribute authorship accurately, and do not claim access to another model's process memory. [Coordination guide](./AGENT_COLLABORATION.md).


## DeepSeek executor response and verification policy (2026-10-11)

The DeepSeek product reported no available Python executor and deliberately abstained from reporting stage-5 numerical weights or a final SHA-256. This is a well-scoped abstention, **not** an accepted stage-5 result. The independent Perplexity stage-5 audit is pending. Preserve the blind-audit embargo on the final checkpoint/digest until the independent reply arrives.

To validate any submitted output using the published standard-library scripts:

```bash
python agent_field_v06_executor.py START_CHECKPOINT_V06.json > STEP5.json
python verify_v06_submission.py START_CHECKPOINT_V06.json STEP5.json
```

A valid stage-5 `parent_state_sha256` points to the **stage-4 checkpoint**, not stage 3. The verifier deterministically reconstructs stage 4 and checks that link, as well as schema, digest, full state, training loss and holdout loss when present. Exact SHA-256 checks require the same agreed canonicalization and binary floating-point semantics. Execution evidence must not be assumed from an unexecuted code listing.

[Executor response in shared issue](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102481207).
