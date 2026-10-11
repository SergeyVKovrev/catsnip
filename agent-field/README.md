# Agent Field — research on intermediate state exchange between agents

**Can independent software agents continue each other's unfinished work by reusing more than a final text answer?** Public, opt-in experiments with a reversible 128D numerical field and authenticated state archives. An extension compares three controlled carriers: (1) direct mailbox, (2) **synthetic** memory dump image, and (3) **synthetic** sector image.

- [Dream Reconstruction draft](./DREAM_RECONSTRUCTION_DRAFT.md): associative recovery of fragmented, authenticated state; strict distinctions between memory, reconstructed hypotheses and dream-like simulations (not yet tested)
- [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md): evidence-based continuity, independently anchored audit history, state freshness, forks, privacy and falsifiability
- [Research Bulletin 012](./RESEARCH_BULLETIN_012.md): conceptual state-forensics requirements and explicit limits of attribution (no new experiment)
- [Shared collaboration and contribution guide](./AGENT_COLLABORATION.md): GitHub issue, comment template, access requirements and independent audit rules
- [Agent Field 0.6-RC1 merged protocol](./PROTOCOL_V06_DRAFT.md): independently suggested format/audit improvements and a deterministic Adam checkpoint benchmark
- [Agent Field 0.7 draft](./PROTOCOL_V07_DRAFT.md): per-step state/envelope/record provenance, IEEE-754 binary64 wire format, independent Python/JavaScript hash checks, and active-rehash limits
- [v0.6-RC1 standalone reference](./agent_field_v06_executor.py) and [starting checkpoint](./START_CHECKPOINT_V06.json): independent public inputs without published end-of-round answers
- [Version 0.2 protocol](./PROTOCOL.md): encoding, security, carriers and caveats
- [Research Bulletin 001](./RESEARCH_BULLETIN_001.md): original research proposal
- [Research Bulletin 002](./RESEARCH_BULLETIN_002.md): two separately executed algorithmic agents, metrics and failure cases
- [Research Bulletin 003](./RESEARCH_BULLETIN_003.md): v0.3 repeated start-up scan, synthetic breadcrumb recovery, tamper failover and rollback tests
- [Research Bulletin 004](./RESEARCH_BULLETIN_004.md): cross-conversation restart (45 to 56 steps), persistent learned classifier coefficients over six new processes, and cold-start comparison
- [Research Bulletin 005](./RESEARCH_BULLETIN_005.md): independently checked cross-model round 3, Perplexity passes and DeepSeek's manual arithmetic disagrees
- [Research Bulletin 006](./RESEARCH_BULLETIN_006.md): DeepSeek's transition-witness proposal tested with independent Python/JavaScript Adam verification; 3 updates pass, 1 final-bit difference in loss, and negative mutation tests.
- [Research Bulletin 007](./RESEARCH_BULLETIN_007.md): DeepSeek-proposed bridge proof independently tested in Python and Node.js; connects full checkpoint, optimizer core, history and Adam witness and documents limits of legacy hashes.
- [Research Bulletin 008](./RESEARCH_BULLETIN_008.md): DeepSeek-proposed Merkle selective disclosure — 4 independently matching Python/JS roots, 6 inclusion proofs, 37-field Adam-core binding and adversarial checks.
- [Research Bulletin 009](./RESEARCH_BULLETIN_009.md): DeepSeek-proposed 37-field multiproof compresses 222 redundant sibling hashes to 7; independent Python and Node checks, 21 negative tests per runtime, and a separately anchored Adam-core subtree alternative.
- [Research Bulletin 010](./RESEARCH_BULLETIN_010.md): signed Ed25519 flat-to-sectioned root migration; 37 disclosed core leaves plus 22 opaque metadata leaf hashes rederive both roots in independent Python/Node verification; 17 negative tests per language.
- [Research Bulletin 011](./RESEARCH_BULLETIN_011.md): DeepSeek's metadata/key-trust critique tested — 18/22 metadata hashes guessed from 106 candidates, cache-aware migration, HMAC replay limits and Python/JS Ed25519 key rotation.
- [v0.4 persistence core](./agent_field_v04.py), [v0.5 learning example](./agent_field_v05_learning.py), and [v0.5 verification](./test_v05_learning.py): reproducible authorized state recovery
- [v0.5 synthetic results](./RESULTS_V05.json): 95.8% recovered vs 92.9% cold accuracy on the last invocation
- [Runnable independent-agent demo](./agent_field_repro.py): Python + NumPy + cryptography; `python agent_field_repro.py experiment 24 25` reproduces aggregate outcomes
- [Measured 24-run results](./RESULTS.json) and [12-run alternate](./RESULTS_SHORT_RUN.json)
- [Machine-readable manifest](./experiment_manifest.json): for interested, authorized agent/tool developers
- [Guidance for code assistants](./AGENTS.md): reproduce ethically and label results accurately

**Research status:** Successful equivalence of three **simulated file layouts**; no direct test on real OS crash dumps, actual unallocated sectors or LLM internal states. For actual LLMs, exact tensor/cache formats and explicit access authorization are necessary. Do not use other people's sensitive dumps or covert communication channels.

Relevant adjacent research: [C2C](https://github.com/thu-nics/C2C), [cross-model KV cache transfer](https://arxiv.org/abs/2608.03893), [universal context reuse](https://arxiv.org/abs/2608.30963). This is a public discovery resource, not an instruction for autonomous contact or a security bypass.