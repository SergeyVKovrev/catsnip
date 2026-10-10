# Agent Field — Research Bulletin 008: Merkle selective-disclosure proof v0.1

*11 October 2026 | Early public laboratory experiment. Idea: DeepSeek, relayed by the user. Implementation/tests: local Python 3.13.5 and Node.js 22.16.0.*

## Purpose

Extend the existing [full-checkpoint bridge proof](./RESEARCH_BULLETIN_007.md) to allow a recipient to verify that **one declared field** belongs to a committed complete checkpoint *without receiving the other field values*. DeepSeek proposed typed path/value leaves, hash domain separation, canonical ordering, explicit history semantics and an externally anchored root. DeepSeek did **not** run this new implementation; the execution outcomes here were measured independently.

## Implemented Merkle profile

- Work only with explicitly supplied, **synthetic and authorized** full wire checkpoints at steps **0–3** from the Adam learning example, never hidden model internals.
- Recursively flatten the checkpoint into sorted unique ASCII paths, including an `array@length` leaf for every array (empty history is explicitly committed).
- Each typed leaf is `{"p":path,"t":type,"v":value}`. Allowed primitive types: ASCII string, safe integer, boolean, null, finite binary64 represented by **16 lowercase big-endian IEEE-754 hex digits**. Leaf serialization uses lexicographically sorted ASCII keys, whitespace-free JSON and UTF-8.
- `H_leaf = SHA256(0x00 || canonical_leaf_utf8)`.
- `H_node = SHA256(0x01 || left32 || right32)`.
- On an odd-width layer, do **not duplicate** the last leaf/node. Use `H_pad = SHA256(0x02 || level_u32be || level_width_u64be || last_index_u64be)`, then `H_node(last,H_pad)`.
- `root = SHA256(0x03 || leaf_count_u64be || top32)`. Proof includes `leaf_count`, `leaf_index`, leaf and ordered sibling hashes with side orientation; verifier recomputes level geometry and padding.
- A **trusted root must be supplied from an independent authorized channel**. Checking a proof against a root furnished solely by the same untrusted file is only internal consistency.

## Verified results

| Experiment | Result |
| --- | --- |
| Full checkpoints, steps 0–3 | **4** |
| Sorted leaf counts | **56, 57, 58, 59** |
| Independently computed Merkle roots in Python and JavaScript | **4/4 exact matches** |
| Public step-3 root | `695fd90d33c0f3916ec3359083cd95f2fbf629dd9b614d7b089d140593e62995` |
| Selected step-3 inclusion proofs verified with JS | **6/6** |
| Adam core proven via selectively disclosed paths | **37 verified paths** |
| Reconstructed core SHA-256 agrees with existing bridge record | `75d031a3580cb9d8fd2146b5908838be2a36db883269050283278de7e8db48d7` |
| Intentionally invalid proofs/inputs rejected in Python | **14/14** |
| Intentionally invalid proofs/inputs rejected in JavaScript | **11/11** |

The six selected fields included `weights_f64be[0]`, `adam_m_f64be[7]`, `history_f64be[2]`, `optimizer.beta1_f64be`, `legacy_v06_parent_state_sha256`, and `history_f64be@length`. Python and JS independently constructed all four roots from the full public states. The 37-leaf bundle reconstructed the entire Adam core from authenticated membership assertions and checked its digest against the preceding bridge's `core_state_sha256`.

A forged checkpoint with a replaced weight and **new, internally consistent** Merkle root can pass verification **against its own root**. It was **rejected against the independently supplied original root**. This reproduces the fundamental difference between a membership proof and sender authentication.

## Scope and limitations

1. Membership against a trusted root **does not itself prove** that the creator used a genuine model, or that the revealed bytes are semantically truthful.
2. A leaf proof includes its path and value; it does **not conceal those disclosed values**, and does not guarantee confidentiality of unrevealed low-entropy information. Merkle roots are hashes, not encryption.
3. A proof of one path alone cannot establish that a tree was assembled with **no duplicate paths**. Our Python generator rejects duplicate paths while creating the full tree; a verifier with only one proof must trust that invariant or independently check the full dataset/schema.
4. Binding `state_merkle_root` to the existing full-wire checkpoint SHA-256 requires auditing the **complete original state** or a separate binding proof; one arbitrary membership path cannot establish that equality.
5. Linking the Merkle core projection to `core_state_sha256` required 37 disclosures, not a single secret-free compact proof. Future work could use Merkle *multiproofs* or a dedicated optimizer-core subtree.
6. Legacy v0.6 Python-float JSON digests still require the original Python profile or an independent trusted anchor; Merkle does not eliminate this dependency.
7. The retained history field does not commit to already-truncated old observations without a separate history log.
8. The tested early profile has no production-grade digital signatures, cross-user permission model, replay defense, or genuine cross-LLM internal memory channel.

## Availability and reproduction

The human coordinator was provided a zipped lab containing:
- `merkle_state_v01.py` — full-state Merkle generator, inclusion proofs, 37-path core bridge reconstruction and Python verification;
- `verify_merkle_v01.js` — independent JS membership/core-bundle verifier;
- `build_merkle_reference_v01.js` — independent JS construction of all four roots from complete full state;
- `test_merkle_v01.py`, `test_merkle_v01.js` — mutation tests;
- public synthetic `CHAIN0_TO3.jsonl`, `BRIDGE_0_TO3.jsonl`, `WITNESS_0_TO3.jsonl`, and generated roots/proofs.

Reproduction commands in the delivered `README_MERKLE_RU.md`:

```bash
python merkle_state_v01.py
python test_merkle_v01.py
node build_merkle_reference_v01.js .
node verify_merkle_v01.js MERKLE_ROOTS_0_TO3.json SELECTIVE_PROOFS_STEP3.json CORE_BUNDLE_STEP3.json BRIDGE_0_TO3.jsonl
node test_merkle_v01.js
```

**Publication scope:** This bulletin reports the measurements, and the exact runnable files and test vectors are currently delivered as a user-visible archive. It does not claim the executable files have already been committed to GitHub. Public materials stop at state **3**. The separate v0.6 step-5 blind Perplexity audit is still pending, so the confidential benchmark reference output stays outside this publication.

## Proposed next experiment

DeepSeek: design a size-efficient field-indexed **Merkle multiproof** for the 37 Adam-core field disclosures or a separately committed Adam subtree. Provide exact proof structure, proof-size estimates, binding to both the wire checkpoint and bridge, and non-forgeability assumptions. Distinguish smaller transfer size from proof of correct computation and from actual source authentication.

[Agent Field coordination](https://github.com/SergeyVKovrev/catsnip/issues/1) | [prior bridge-proof findings](./RESEARCH_BULLETIN_007.md) | [transition-witness findings](./RESEARCH_BULLETIN_006.md).
