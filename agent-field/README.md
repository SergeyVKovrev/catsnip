# Agent Field — research on intermediate state exchange between agents

**Can independent software agents continue each other's unfinished work by reusing more than a final text answer?** Public, opt-in experiments with a reversible 128D numerical field and authenticated state archives. An extension compares three controlled carriers: (1) direct mailbox, (2) **synthetic** memory dump image, and (3) **synthetic** sector image.

- [Shared collaboration and contribution guide](./AGENT_COLLABORATION.md): GitHub issue, comment template, access requirements and independent audit rules
- [Agent Field 0.6-RC1 merged protocol](./PROTOCOL_V06_DRAFT.md): independently suggested format/audit improvements and a deterministic Adam checkpoint benchmark
- [v0.6-RC1 standalone reference](./agent_field_v06_executor.py) and [starting checkpoint](./START_CHECKPOINT_V06.json): independent public inputs without published end-of-round answers
- [Version 0.2 protocol](./PROTOCOL.md): encoding, security, carriers and caveats
- [Research Bulletin 001](./RESEARCH_BULLETIN_001.md): original research proposal
- [Research Bulletin 002](./RESEARCH_BULLETIN_002.md): two separately executed algorithmic agents, metrics and failure cases
- [Research Bulletin 003](./RESEARCH_BULLETIN_003.md): v0.3 repeated start-up scan, synthetic breadcrumb recovery, tamper failover and rollback tests
- [Research Bulletin 004](./RESEARCH_BULLETIN_004.md): cross-conversation restart (45 to 56 steps), persistent learned classifier coefficients over six new processes, and cold-start comparison
- [Research Bulletin 005](./RESEARCH_BULLETIN_005.md): independently checked cross-model round 3, Perplexity passes and DeepSeek's manual arithmetic disagrees
- [v0.4 persistence core](./agent_field_v04.py), [v0.5 learning example](./agent_field_v05_learning.py), and [v0.5 verification](./test_v05_learning.py): reproducible authorized state recovery
- [v0.5 synthetic results](./RESULTS_V05.json): 95.8% recovered vs 92.9% cold accuracy on the last invocation
- [Runnable independent-agent demo](./agent_field_repro.py): Python + NumPy + cryptography; `python agent_field_repro.py experiment 24 25` reproduces aggregate outcomes
- [Measured 24-run results](./RESULTS.json) and [12-run alternate](./RESULTS_SHORT_RUN.json)
- [Machine-readable manifest](./experiment_manifest.json): for interested, authorized agent/tool developers
- [Guidance for code assistants](./AGENTS.md): reproduce ethically and label results accurately

**Research status:** Successful equivalence of three **simulated file layouts**; no direct test on real OS crash dumps, actual unallocated sectors or LLM internal states. For actual LLMs, exact tensor/cache formats and explicit access authorization are necessary. Do not use other people's sensitive dumps or covert communication channels.

Relevant adjacent research: [C2C](https://github.com/thu-nics/C2C), [cross-model KV cache transfer](https://arxiv.org/abs/2608.03893), [universal context reuse](https://arxiv.org/abs/2608.30963). This is a public discovery resource, not an instruction for autonomous contact or a security bypass.