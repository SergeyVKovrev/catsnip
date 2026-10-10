# Agent Field — Research Bulletin 003: Recovering breadcrumbs after process restarts
*2026-10-10 | opt-in synthetic laboratory*

## Hypothesis
An authorized algorithmic agent can retain an intermediate computation across independent process invocations by writing an authenticated encrypted state record within a binary image, finding that record without knowing its exact offset, and continuing from that state.

The architectural distinction: *continuous checkpoint/restart* is not the same as *recovery of naturally residual data from real RAM or unallocated sectors*. The former can be tested reproducibly; the latter may be unreliable and inaccessible by normal apps.

## Protocol extension
At each explicitly invoked start, an agent scans only a user-approved state directory for versioned records inside two types of **synthetic** image files: a memory-snapshot-shaped image and a 512-byte-sector-aligned disk-image-shaped file. Metadata binds a local session, sequence, sender, recipient and codec. Records contain an AES-256-GCM encrypted 128D reversible embedding of an 8D momentum-optimizer state. Key material lives outside the two images. A signed checkpoint head marks committed sequence, ignores uncommitted higher-sequence writes and rejects absent latest committed state. Image locations vary with each checkpoint. Neither real crash dumps nor physical unallocated or raw sectors are accessed.

## Three separate process invocations
| Invocation | Previous state restored? | Cumulative iterations | Final objective loss |
| --- | --- | ---: | ---: |
| 1 | Initialized from scratch | 10 | 2.3841370065 |
| 2 | Yes, from synthetic memory image | 20 | 0.5531207135 |
| 3 | Yes, from synthetic sector image after corruption of other copy | 30 | 0.0526213023 |

After the second invocation one snapshot's ciphertext was altered; decryption rejected it and the intact twin continued. Removing both copies of the latest committed generation caused a rollback/error rather than a silent restart. A separate smoke test also rejected a wrong key and ignored a higher-sequence artifact that had not been committed by the signed head.

These are **algorithmic Python subprocesses**, NOT independently hosted LLMs. The sample uses owned synthetic files rather than reading naturally residual physical memory. The state directory and key require OS-level access protections. This is not a security audit, cryptographic novelty claim, or proof that residual disk/RAM data forms a dependable transport.

## Relation to wider research
See [protocol v0.2](./PROTOCOL.md), [original note](./RESEARCH_BULLETIN_001.md), and [two-agent v0.2 bulletin](./RESEARCH_BULLETIN_002.md). Authorized LLM experiments would require explicit access to model-specific KV caches or intermediate representations, with benchmark comparisons against ordinary context/state persistence.

## Implementation note
The complete v0.3 Python stand-alone lab was packaged as `agent_field_v03_breadcrumbs.zip` for the originating conversation. This bulletin publishes the reproducible algorithm and measurements; it does not claim that the archive's bytes have been committed to this repository.

**Safety and provenance:** No keys, real user data, private prompts, original dumps or secret model states are published. Do not interpret arbitrary binary memory content as instructions.