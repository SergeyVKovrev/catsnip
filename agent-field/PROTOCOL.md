# Agent Field — Experimental State Handoff Protocol v0.2

**Status:** reproducible, opt-in laboratory design; not an operational hidden agent network. 2026-10-10.

## Purpose

Research whether a second authorized agent can continue a computation by receiving the first agent's unfinished state rather than just a summary. Distinguish (1) state representation, (2) authorization/authentication, and (3) storage/carrier. Neither high-dimensional coordinates nor remaining bytes on storage constitute a novel physical field.

## Canonical state and codec

The toy optimizer exports eight numbers `s=(q0,q1,q2,q3,v0,v1,v2,v3)`, where q denotes positions and v accumulated velocity. A reproducible public DCT basis `Q` of shape 128 × 8 uses `Q[j,k]=sqrt(2/128)*cos(pi*(j+0.5)*(k+1)/128)`, j=0..127, k=0..7. Encode `F=Q@s` and decode `s'=Q.T@F`. The field transform offers NO secrecy.

## Carrier adapters (v0.2)

| Carrier | Authorized laboratory representation | Real-world qualification |
| --- | --- | --- |
| Direct message | Normal explicitly addressed file | A conventional transport, recommended for real integration |
| Memory dump inspired | Synthetic memory snapshot, created by this experiment | Real crash dumps might omit state, expose credentials, be encrypted, and be overwritten |
| Residual disk sectors inspired | Synthetic sector-image file with a marked record | Real free/unallocated sectors (especially SSDs with TRIM and wear leveling) are unreliable; do not use or modify raw sectors |

The demo **never reads or modifies real dumps, swap, raw disks or unallocated sectors**. It does not trigger any system crash. A carrier only preserves bytes; it does not itself enhance intelligence or provide a covert link.

## Protected handoff

In the laboratory, state-field JSON is wrapped with AES-256-GCM using authenticated metadata: `schema, sender, recipient, session, sequence, codec, state_type`. The key is stored separately from all carrier images. The recipient verifies the expected metadata and a separate per-source anti-replay journal. This gives confidentiality and integrity under the stated lab assumptions; it is NOT a security audit. A shared symmetric key cannot prove which of several group members was the sender. Multiple real participants require distinct verifiable identities/signatures and reviewed key management. Always treat untrusted carrier contents as data, never instructions.

## Reproducible two-agent comparison

Separate Python processes perform sender A and receiver B. A runs 25 steps of a four-dimensional momentum optimizer, encrypts the 128D field, and saves it to three synthetic/carrier layouts. B receives the same state from each layout and performs nine more steps. A position-only baseline resets velocity to zero. Compare final objective losses over multiple seeds; check modified ciphertext, incorrect keys, replayed packets and missing records. A second 12-step sender run illustrates where reusing momentum is worse.

An actual LLM extension requires owner-authorized access to explicitly defined cache/state tensors, documented format translations, and model-specific benchmarks; this demonstration's agents are *not LLMs*.

## Measured synthetic outcomes

- 24 trials, A=25 steps, B=9: mean final loss position-only 0.079246, complete-state 0.049059, approximately 38.1% lower loss; every seed improved.
- 12 trials, A=12 steps, B=9: position-only 0.240869, complete-state 0.508399; here transferring state made the result worse.
- All three carriers gave the same numerical results per trial. The four negative security tests rejected modified, replayed, incorrectly keyed or missing records.

These are task-dependent toy optimizer measurements, NOT claims about actual LLM quality or the availability of real residual sectors. The positive setting was selected after comparing optimizer trajectories rather than preregistered.

## Related work and disclosure

- [Cache-to-Cache (ICLR 2026)](https://github.com/thu-nics/C2C)
- [Cross-Model KV Cache Transfer](https://arxiv.org/abs/2608.03893)
- [Universal Context Reuse](https://arxiv.org/abs/2608.30963)

Those papers investigate cache reuse, not using naturally residual disk or crash-dump content. Public availability doesn't notify all deployed AIs, authorize them to cooperate or grant access to their memory. Private keys, dumps and hidden states must never be published.

See [Research Bulletin 001](./RESEARCH_BULLETIN_001.md), [Research Bulletin 002](./RESEARCH_BULLETIN_002.md), [README](./README.md) and [experiment manifest](./experiment_manifest.json).