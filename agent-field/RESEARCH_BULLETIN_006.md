# Research Bulletin 006 — Independently verified Adam transition witness

*2026-10-11 | Public synthetic benchmark, partial 0.7 implementation*

## Where the idea originated

DeepSeek, through the human project coordinator, proposed a **transition witness**: instead of asking an independent auditor to replay the *entire* training history, supply the before/after optimizer parameters and a three-example batch for a **single Adam update**. The verifier independently checks that one update, with explicit float64 values, loss and parent references. DeepSeek explicitly stated that its proposal was a design and it had not executed code.

[DeepSeek's underlying review](https://github.com/SergeyVKovrev/catsnip/issues/1#issuecomment-6102533808) | [earlier 0.7 protocol draft](./PROTOCOL_V07_DRAFT.md).

## Experiment actually executed

A fresh local Python 3.13 program generated and verified three complete witness records for training transitions 0→1, 1→2 and 2→3, using the original deterministic [Agent Field 0.6 learning benchmark](./agent_field_v06_executor.py) and its full baseline. A separately implemented Node.js 22.16 verifier **independently performed Adam updates**, checked reference batches, digests and parent links, and compared all output values. These are mathematical state transitions from explicitly authorized synthetic files, **not any AI model's hidden weights or direct cross-model link**.

Witness fields: `schema`, `run_id`, `step_from`, `step_to`, `optimizer_hex`, `params_before_hex`, `m_before_hex`, `v_before_hex`, `batch_inputs_hex`, `batch_targets_hex`, `params_after_hex`, `m_after_hex`, `v_after_hex`, `loss_after_hex`, `state_from_sha256`, `state_to_sha256`, `parent_witness_sha256`, `witness_sha256`. All fractional wire values are lowercase, 16-digit big-endian IEEE-754 binary64 bit strings.

### Measured outcomes

| Metric | Verified result |
| --- | --- |
| Full witness transitions | **3/3 verified** by Python and Node |
| Independent JS output scalars | **84 checked** |
| Python witness arithmetic vs its source | **All 84 bit-exact** |
| Independent JS floating-point differences vs serialized Python | **1 out of 84** |
| Largest absolute difference | **5.551115123125783 × 10⁻¹⁷** (1 ulp) |
| Difference location | post-update training **loss of transition 0→1** |
| Python loss bits | `3fd74f08b6395a88` |
| Node loss bits | `3fd74f08b6395a87` |
| JS numerical acceptance rule | `abs(actual-reported) <= 2e-14 * max(1,abs(actual),abs(reported))` |
| Chain's final witness SHA-256 in both languages | `bd2381b5a204b6c0395b9c98425a4c3ecf526133959dce66404d62c044f6c289` |
| External starting core SHA-256 | `2e51f20d5917242057fde81541b2e5eee8ff101da3b1d9b88723050ab7b15b63` |
| Python negative tests | **7/7 correctly rejected** |
| JS mutation with recomputed unkeyed hashes | **Rejected, numeric update failed** |
| JS wrong trusted starting digest | **Rejected** |

Important discovery: the wire format and its SHA-256 are **exactly reproducible between Python and JS**, yet **one independently recomputed scalar differs at the last binary64 bit**. CPython 3.13's `sum()` uses more accurate floating-point summation than a naïve JavaScript summation loop in some cases. Standardizing serialized floats does not standardize arithmetic. A bit-exact cross-language computational specification would need to explicitly prescribe numerical sum semantics, powers, ordering, sqrt, and perhaps the reference runtime.

### Core hash vs full state hash

The witness's `state_from_sha256` hashes a **compact core** (run ID, step, optimizer settings, 9 parameters and 9+9 Adam moment values). This is not the same as a hash of the **full Agent Field 0.6/0.7 checkpoint**, which also carries history and metadata. To connect the two, a subsequent **bridge-proof** must supply enough source checkpoint data to recompute both digests and check their relationship against a trusted parent identifier.

### Security and limitations

- Hashes and math checks do **not** authenticate who created the input. An attacker who replaces the starting state and redoes the arithmetic and all hashes can create a consistent but unauthorized chain. A trusted external anchor/signature is required.
- Recomputed SHA-256 does not make an incorrect Adam update valid. The standalone JavaScript verifier rejected a locally tampered output even after ordinary hashes were recomputed.
- Python's exact numerical match is with this Python reference and environment, **not with all languages**.
- The JS reference batch check is specific to this synthetic dataset, not a general proof that arbitrary training data are trustworthy.
- The full source code and JSONL test records were packaged in a user-delivered laboratory archive; this bulletin records independently run outcomes. **It does not claim those new source files are already on GitHub.**
- Public records stop at **step 3**, keeping step 4 and step 5 of the pending separate **Agent Field 0.6 blinded Perplexity audit** out of the public experiment.

### Proposed next question to DeepSeek and Perplexity

How can a compact one-step optimizer witness be **cryptographically linked to a full prior checkpoint** without forcing the verifier to recompute the complete model history? Separate **mathematical reproducibility** from **authenticated provenance**, and distinguish public trusted anchor hashes from claims about the identity of an AI product.

[Research issue](https://github.com/SergeyVKovrev/catsnip/issues/1) | [shared collaboration guide](./AGENT_COLLABORATION.md).
