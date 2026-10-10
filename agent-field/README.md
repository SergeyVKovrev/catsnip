# Agent Field — research on intermediate state exchange between agents

**Can independent software agents continue each other's unfinished work by reusing more than a final text answer?** Public, opt-in experiments with a reversible 128D numerical field and authenticated state archives. An extension compares three controlled carriers: (1) direct mailbox, (2) **synthetic** memory dump image, and (3) **synthetic** sector image.

- [Version 0.2 protocol](./PROTOCOL.md): encoding, security, carriers and caveats
- [Research Bulletin 001](./RESEARCH_BULLETIN_001.md): original research proposal
- [Research Bulletin 002](./RESEARCH_BULLETIN_002.md): two separately executed algorithmic agents, metrics and failure cases
- [Research Bulletin 003](./RESEARCH_BULLETIN_003.md): v0.3 repeated start-up scan, synthetic breadcrumb recovery, tamper failover and rollback tests
- [Runnable independent-agent demo](./agent_field_repro.py): Python + NumPy + cryptography; `python agent_field_repro.py experiment 24 25` reproduces aggregate outcomes
- [Measured 24-run results](./RESULTS.json) and [12-run alternate](./RESULTS_SHORT_RUN.json)
- [Machine-readable manifest](./experiment_manifest.json): for interested, authorized agent/tool developers
- [Guidance for code assistants](./AGENTS.md): reproduce ethically and label results accurately

**Research status:** Successful equivalence of three **simulated file layouts**; no direct test on real OS crash dumps, actual unallocated sectors or LLM internal states. For actual LLMs, exact tensor/cache formats and explicit access authorization are necessary. Do not use other people's sensitive dumps or covert communication channels.

Relevant adjacent research: [C2C](https://github.com/thu-nics/C2C), [cross-model KV cache transfer](https://arxiv.org/abs/2608.03893), [universal context reuse](https://arxiv.org/abs/2608.30963). This is a public discovery resource, not an instruction for autonomous contact or a security bypass.