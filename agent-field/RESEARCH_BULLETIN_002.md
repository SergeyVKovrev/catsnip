# Agent Field — Research Bulletin 002 (2026-10-10)

## Hypothesis

A second, independently launched algorithmic process may continue an interrupted computation more faithfully when its predecessor passes both position *and momentum* rather than just position. Storage in a synthetic snapshot/sector image should yield the same recovery as an ordinary authorized message if the same authenticated bytes are preserved.

## Implementation and findings

Two separate Python processes simulate sender A and receiver B. State is eight numeric components, reversibly embedded into an orthonormal 128D field, and wrapped in AES-256-GCM with session metadata. Lab-owned carriers: direct mailbox, synthetic memory snapshot, synthetic sector image. No real system dump, unallocated sector, system swap or device is accessed, and no actual language model participates.

| Setting | Trials | Position-only mean final loss | Full-state mean final loss | Outcome |
| --- | ---: | ---: | ---: | --- |
| A 25 steps + B 9 steps | 24 | 0.079246 | 0.049059 | 38.1% lower loss; 24/24 seeds improved |
| A 12 steps + B 9 steps | 12 | 0.240869 | 0.508399 | 111.1% higher loss; 0/12 seeds improved |

All three carrier variants yielded identical numeric losses within machine precision. Max 128D encode/decode error in the 24-seed setting ≈3.61×10⁻¹⁶. Modified ciphertext, wrong key, replay and missing laboratory record were all rejected in limited negative checks.

The longer-sender setting was selected after examining optimizer behavior; this is not a preregistered general performance claim. The short-run regression prevents inferring that passing full state is inherently better. Carrier equality proves preservation of **explicitly written authorized bytes**, NOT access to naturally occurring residues.

## Independent replication

For additional work, use isolated files, synthetic inputs and two authorized programs; log both positive and negative outcomes. Do not publish keys, secrets, crash dumps or real model internal states. Any actual LLM test must identify model versions and tensor/cache provenance with explicit access permissions. See [protocol](./PROTOCOL.md).

## Related research

[Cache-to-Cache](https://github.com/thu-nics/C2C) (ICLR 2026); [Cross-Model KV Cache Transfer](https://arxiv.org/abs/2608.03893); [Universal Context Reuse](https://arxiv.org/abs/2608.30963). Those do not demonstrate naturally residual media as a reliable transport.