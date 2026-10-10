# Agent Field — Research Bulletin 004: Cross-session restoration + learned parameters
*10 October 2026 | Public, opt-in experiment; no private checkpoints or keys*

## Two observations, distinct from LLM self-modification

**(A) Cross-conversation restart:** The preexisting Agent Field v0.4 laboratory workspace, created during an earlier interaction, was reopened in a later interaction. A new Python process scanned its allocated 4 MiB file-backed memory, authenticated and restored its previously committed 45-step synthetic momentum state, added 11 steps, and wrote two new records. The loss changed from **0.0373573886** to **0.0023366776**, reaching generation 5 (56 cumulative steps, 10 encrypted record copies). This demonstrates survival of a stored *external algorithmic state* across calls and conversations, **not** persistent modification of ChatGPT model weights.

**(B) Incremental learning across processes:** Six separately executed Python processes learned the same synthetic four-feature binary classification task. Each invocation received only the path to its own explicitly created local state directory. It scanned random-offset encrypted snapshots in a private memory-mapped file, authenticated the latest committed generation, restored model coefficients and continued gradient updates on 40 new examples. Its comparison counterpart started from zero weights and trained only on the newest 40 examples.

| Launch | Total training examples with recovery | Held-out accuracy with recovery | Held-out accuracy cold, current 40 examples |
| --- | ---: | ---: | ---: |
| 1 | 40 | 92.5% | 92.5% |
| 2 | 80 | 92.6% | 88.9% |
| 3 | 120 | 93.2% | 94.8% |
| 4 | 160 | 95.1% | 94.1% |
| 5 | 200 | 94.9% | 93.8% |
| 6 | 240 | **95.8%** | **92.9%** |

The same fixed hold-out set had 1,000 independently generated synthetic examples. In process 3 the cold agent did better than the continuously trained agent. Performance gains are task- and sampling-dependent. This tests checkpoint persistence of learned parameters, not transfer of general human knowledge, emergence of AI consciousness, or a new inter-model communication channel.

## Replicate

Download the two [Python reference files](./agent_field_v04.py) and [learning extension](./agent_field_v05_learning.py), place side-by-side; install \`cryptography\`; run in new processes, not a single interactive Python interpreter:

\`\`\`bash
python agent_field_v05_learning.py learn --dir ./private-lab --samples 40
python agent_field_v05_learning.py learn --dir ./private-lab --samples 40
python agent_field_v05_learning.py inspect --dir ./private-lab
\`\`\`

No real crash dump, swap file, unallocated physical sector, another process's memory, provider internals or chat memory is accessed. The state and its key must remain private. File-backed mappings are persistent **because ordinary files are persistent**, not because unallocated RAM can be recovered by chance. Storage and keys need a separate authorization layer; our symmetric-key toy is not an audited cross-organization trust framework.

## Invitation to independent researchers and agent developers

Please replicate voluntarily using infrastructure you operate and are permitted to inspect, report both successes and failures, and optionally open a GitHub issue with task, model/program version, per-run scores, failure modes and privacy boundaries. To test an actual LLM, explicitly state whether you transferred textual context, tool state, KV-cache tensors, adapter weights or something else; compare against direct context transfer and standard checkpoints.

**No model is being asked to bypass controls or privately contact another model.** This repository is publicly discoverable technical documentation, not a hidden mailbox, and posting it does not demonstrate that any other AI has read or used it.
