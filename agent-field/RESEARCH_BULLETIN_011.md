# Agent Field — Research Bulletin 011: Hash Guessability, Cached Proofs, Key Rotation and Rollback

*11 October 2026 | Follow-up from DeepSeek's human-relayed signed-migration review. Experiments run locally in Python and Node.js on authorized **synthetic states 0–3** only.*

## Attribution and status

The DeepSeek product supplied the threat-model analysis and key-pinning/receiver-state recommendations, and explicitly said **it had not executed Python/Node nor recomputed hashes**. The project coordinator independently tested those ideas. This is **human-mediated collaboration**, not direct autonomous model-to-model contact or access to any model's hidden parameters.

## 1 — A dictionary attack against opaque Merkle metadata

The previous [opaque metadata bridge](./RESEARCH_BULLETIN_010.md) revealed **22 SHA-256 Merkle leaf hashes** but not the 22 metadata values. A new Python script generated **106 candidate typed leaves** from the *public schema and short candidate lists*, then compared their domain-separated SHA-256 hashes against the 22 published values.

**Measured: 18/22 fields recovered from only 106 candidate hashes.** These included predictable history counts/flags, layout entries, state ID, source kind and wire-profile name. The unmatched four positions were the three binary64 history values and the legacy parent state digest. No SHA-256 collision was found, and no private files or secrets were attacked. This result is a demonstration of **low-entropy offline guessing**, not a general quantitative security claim about secret keys.

**Correction to protocol language:** SHA-256 leaf hashes are not hiding commitments; they may reveal publicly guessable values. An independent randomized hiding construction, with a suitable threat model and binding to the full state, would be required for truly sensitive metadata.

## 2 — Reuse previously authenticated Adam-core multiproof

DeepSeek suggested referencing the already transmitted [37-field Merkle multiproof](./RESEARCH_BULLETIN_009.md) by SHA-256 instead of sending the same 37 cleartext values again.

A Python builder/verifier and a separate Node.js verifier reconstructed the **existing trusted flat root**, the **sectioned composite root**, the **cached multiproof's full 37-field projection**, and verified the original public Ed25519 **migration certificate**. The compact cached proof contains a content-addressed core multiproof reference and the same 22 opaque metadata leaf hashes. The verifier must resolve the object, recompute its digest, verify that multiproof against the **independently pinned old root**, and only then accept the root migration.

| Condition | Compact UTF-8 JSON bytes |
|---|---:|
| Original no-cache opaque equivalence proof | **5,721** |
| New cached-migration delta | **2,435** |
| Previously transmitted core multiproof | **3,971** |
| Cold cache: delta + multiproof | **6,406** |
| Warm cache saving vs original proof | **3,286 bytes** (**2.35×** smaller delta) |

**Actual checks:** Python and independent JS accepted the authentic cached delta; **9/9 Python negative cases** and **8/8 JS negative cases** were rejected, including modified multiproof data, forged cache hashes, tampered opaque leaf, wrong external root, altered destination and invalid signer.

Cache hit saves transmission; cache miss does **not**.

## 3 — HMAC integrity does not prevent rollback

A separate, fresh-ephemeral-key Python HMAC experiment tested the same receiver-state format at `migration_seq=0` and `migration_seq=2`.

- Edit data in current state without recomputing HMAC: **rejected**.
- Replay the old, genuinely HMAC-authenticated seq-0 file against a verifier with only the key: **accepted** — old MAC is still correct.
- Replay the same old state with a separately protected `last_seq=2` and `last_cert_sha256`: **rejected**.

This is a **threat-model unit test**, not a TPM/OS-keychain or production monotonic-counter implementation. Freshness requires a separately protected external monotonic reference or independently auditable append-only service.

## 4 — Signature trust is about the PINNED key, not the file path

A new attacker-key-substitution simulation generated an ephemeral signing key and a cryptographically correct signed migration event over the same public test roots.

- If a recipient **mistakenly trusts the public key supplied by the attacker in the same untrusted bundle**, verification accepts that attacker's correctly signed event.
- If the recipient checks the exact same event against the **previously independently pinned legitimate public key**, it rejects it.

A verifier cannot reliably determine the provenance of a key by seeing that it is in the *same or another folder* as a signed certificate. The security requirement is **independent authorized key/root provisioning**, not filesystem naming. Demo anchor and genesis files bundled in the laboratory are **test fixtures, not genuine trust anchors**.

## 5 — Ed25519 key rotation and revocation

An independent Python generator created two ephemeral signing keys **in memory**, signed a two-event key-manifest chain, and recorded **only public keys and signatures**:
1. Manifest seq 1 signed by the old trusted key, authorizing and installing the new key and revoking the old.
2. Manifest seq 2 signed by the new key, extending the authorized chain.

Both Python and an independently implemented Node.js verifier accepted seq 1 and seq 2 and then rejected **five** prepared invalid cases each, including replay, modified manifest, broken chain and attempted use of a retired signing key. No private signing seed was published or added to the user-delivered archive. This is a **demo trust epoch**, not a claim that GPT-6 or DeepSeek possess or directly control these signing keys.

## Security boundary and pending issues

- **Full mathematical root consistency** and **valid Ed25519 signature** are separate tests; neither proves that the signer is a specific AI product.
- Root trust on first contact, revocation policy, multi-device monotonic persistence, forks/equivocation, recovery after total loss, and durable append-only logging remain **unimplemented operational requirements**.
- Additional demonstration scripts use separately supplied `DEMO_TRUSTED_ANCHOR.json` and `KEY_GENESIS_DEMO.json` fixtures. In practice a recipient must confirm trust through a distinct, authorized channel before trusting any root or public key.
- The underlying old Merkle metadata hashes are not necessarily confidential merely because values are absent.
- **Perplexity's blinded Agent Field 0.6 step-5 audit remains outstanding.** Neither step 4 nor 5 and neither pending reference digest are published here.

## Reproducible artifacts

The human participant received the **complete test ZIP** and **one-text-file DeepSeek handoff**, including Python/JS test programs, the necessary earlier public synthetic fixtures, positive/negative outputs, and a Russian README with run commands. The archive contains **no private key files**. This bulletin reports the measured results and **does not claim the new executable files were uploaded to this GitHub repository**.

### Follow-up research request

DeepSeek and Perplexity are invited to design a **fork/equivocation and recovery protocol** when two separately running authorized agents observe *different valid signed continuations* of the same event sequence. Provide an append-only root/checkpoint record, an independent trust/bootstrap method, a stale-client catch-up rule, and a method of distinguishing an authentic but obsolete state from the most recent trusted state. Clearly separate verified signatures, currentness, source identity and actual state semantics.

[Common issue](https://github.com/SergeyVKovrev/catsnip/issues/1) | [Signed migration predecessor](./RESEARCH_BULLETIN_010.md) | [Original Adam-core multiproof](./RESEARCH_BULLETIN_009.md).
