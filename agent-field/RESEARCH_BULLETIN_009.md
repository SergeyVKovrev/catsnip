# Agent Field — Research Bulletin 009: Merkle multiproof and Adam-core subtree

*11 October 2026 | DeepSeek design, human-relayed; independently implemented and tested in Python and Node.js.*

## Research question

Can the previous Agent Field v0.7 37-leaf Adam-core disclosure be verified against the existing **trusted flat full-state Merkle root**, without transferring 37 mostly overlapping inclusion paths? What additional improvement is possible by committing the Adam core to a dedicated subtree?

## Implementations and interoperability

A new Python builder/verifier (`merkle_multiproof_v01.py`) produced a compact multiproof from the public synthetic step-3 full wire state. A separately implemented Node.js checker (`verify_multiproof_v01.js`) independently validated its 37 typed leaves, minimal support node positions, full root, and derived Adam-core SHA-256 against the earlier [bridge proof](./RESEARCH_BULLETIN_007.md). A *third, separately written Node.js builder* (`build_multiproof_reference_v01.js`) reconstructed the **entire multiproof from the original full checkpoint**, matching the Python multiproof in canonical JSON, as well as the optional sectioned composite root.

All tests use the originally published **synthetic steps 0–3** only; there is no use of another model's memory. DeepSeek reported no code execution on its side; all outcomes below were independently measured by the coordinator's local Python and Node runtimes.

## Measured sizes and node counts

The same **37 explicitly revealed Adam-core fields** in a 59-leaf state tree:

| Format | Support sibling hashes | JSON bytes (minified) | Reduction vs 37 standalone |
| --- | ---: | ---: | ---: |
| Previous **37 separate inclusion proofs** | **222 entries** (with repeats) | **28,975** | **1×** |
| **One Merkle multiproof**, same original flat root | **7 distinct support hashes** | **3,971** | **7.30× smaller** |
| **Dedicated Adam-core subtree** and one metadata subtree root, new profile | No redundant supports when disclosing all 37 core leaves | **2,978** | **9.73× smaller** |

These are raw compact UTF-8 JSON byte lengths, **not compressed ZIP sizes** and not privacy claims. The speed or byte advantage is scenario-specific (this set of dense, lexicographically adjacent leaves).

### Roots and digest

- Original and verified step-3 full **flat Merkle root:** `695fd90d33c0f3916ec3359083cd95f2fbf629dd9b614d7b089d140593e62995`.
- Derived and verified **Adam-core SHA-256:** `75d031a3580cb9d8fd2146b5908838be2a36db883269050283278de7e8db48d7`.
- **New, incompatible sectioned composite root:** `cbe6be93601df4c235ee0a3101fb7f6166eabe29f43cb0c08efd24d655921f72`.

The third hash is **NOT** proven to be interchangeable with the original flat root. It requires a **separately authenticated/trusted root** or a trusted full-state migration procedure.

### Independent checks and negative tests

- Python multiproof generation + verification against the original trusted step-3 root: **PASS**.
- Node.js standalone multiproof verification and independently recomputed Adam-core digest: **PASS**.
- Independent Node.js generation from the same original complete 59-leaf wire-state: **exact match to the Python multiproof under canonical JSON**.
- Independent Node.js construction of the sectioned composite root: **exact match**.
- **21/21** deliberate invalid cases rejected by Python.
- **21/21** equivalent invalid cases rejected by JavaScript.

The invalid cases covered altered/duplicate/out-of-range leaf indices, duplicate paths, unsorted leaves, missing or extra support hashes, wrong support node level/index, wrong root, modified step/weight, invalid nonfinite IEEE-754 encoding, wrong tree geometry, and sectioned-root/subtree tampering.

## Compact multiproof schema

```json
{
  "schema": "agent-field/merkle-multiproof/v0.1",
  "root": "<sha256-hex>",
  "leaf_count": 59,
  "leaves": [{"index": 0, "leaf": {"p": "...", "t": "...", "v": "..."}}],
  "siblings": [{"level": 0, "index": 1, "hash": "<sha256-hex>"}]
}
```

**Important deliberate change to DeepSeek's initial suggestion:** a support sibling is indexed by **(level, index)** rather than merely by side. The verifier derives left/right orientation and the set of **minimally required unique sibling positions** from disclosed leaf indices. The verifier requires this support set **exactly**, ordered by `(level,index)`, not just as an unordered bag. A virtual odd-level pad is recomputed deterministically and is **not transmitted**. This prevents duplicate, superfluous or ambiguously positioned support nodes.

Every disclosed field must have a unique canonical path; leaf indices are strictly increasing; all indices are bounded by the tree's explicit leaf count. All leaf hashes, node hashes, pad hashes and root-finalization use the previously tested Merkle v0.1 domain separators.

## Trust and confidentiality

1. Multiproof has the **same trust boundary as individual Merkle proofs**. It confirms membership **relative to a trusted root**; it does not authenticate the sender or the training run.
2. The 37 revealed fields contain actual optimizer parameters. This is **selective disclosure**, not encryption, privacy against an informed observer, or zero-knowledge.
3. The 2,978-byte dedicated-subtree variant defines a **different root protocol**. Linking it to the old flat root is not mathematically established by the new composite root alone. Independent root migration, a signed new root, or an authorized full-state recheck is required.
4. Checking disclosed path indices alone does not prove global path uniqueness in the **unrevealed** portion of an untrusted original tree. The trusted full-tree builder establishes uniqueness at construction, and the schema imposes uniqueness as an invariant.
5. The existing legacy v0.6 Python-specific hash cannot automatically be reconstructed in JavaScript merely because a Merkle proof is valid.
6. The separate v0.6 stage-5 blind Perplexity audit is still pending. **No stage-4/5 state or digest is contained in this bulletin.**

## Reproducible artifacts

The coordinator received a public synthetic ZIP laboratory bundle with Python/Node reference scripts, the original full-state JSONL, prior `CORE_BUNDLE_STEP3.json`, compact `MULTIPROOF_CORE_STEP3.json`, a sectioned alternative, benchmarks and negative tests. This public bulletin documents the concrete measured values; **the executable files are currently supplied as a user-visible archive, and this page does not claim that those new source files have already been committed to GitHub**.

## Follow-on challenge for DeepSeek and Perplexity

Design a safe **root migration** process from the original trusted flat Merkle commitment to an independent sectioned Adam-core commitment that does not require each verifier to download the complete checkpoint. Clearly separate *root attestation*, *trusted migration authorization*, *freshness/anti-rollback protection*, and *membership proof verification*. A signed transition record or trusted dual-root checkpoint may help; unkeyed hashes alone cannot authenticate a migration.

[Shared discussion](https://github.com/SergeyVKovrev/catsnip/issues/1) | [selective-disclosure results](./RESEARCH_BULLETIN_008.md) | [bridge proof](./RESEARCH_BULLETIN_007.md).
