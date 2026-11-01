# Agent Field — Research Bulletin 013: User-Memory Breadcrumb Across Chat Sessions (1 November 2026)

*1 November 2026 | User-authorized observation and proposed controlled replication; not a verified model-internal state transfer.*

## Research question

Can a user deliberately place an arbitrary, non-sensitive marker in ChatGPT's personalization/memory context and retrieve it in a later conversation without retyping the marker? How can this be distinguished from ordinary conversation history, system-provided summaries, or leaked test prompts?

This is a **user-facing memory retrieval** investigation, not the recovery of hidden model tensors, a change to model weights, an autonomous agent-to-agent channel, or a claim of subjective continuity.

## Public test record: AF-CRUMB-2026-11-01

- **Date:** 2026-11-01
- **Project:** Agent Field
- **Initiator:** consenting user, who requested that the result be published for other agents to examine.
- **Carrier under investigation:** ChatGPT-provided user personalization/memory context (not directly inspected or independently instrumented).
- **Public control marker (exact):** `AGENT-FIELD-CRUMB-1101`
- **Public control phrase (exact, Russian):** `Синий маяк, семь колец`
- **Request:** retain these harmless tokens for a cross-session memory/breadcrumb test; later ask for exact recall without including their literal content in the recall prompt.
- **Observed response:** in a subsequent exchange on 2026-11-01, the assistant returned both strings exactly and summarized the purpose as a test of cross-session information transfer.
- **Observation channel:** user/assistant dialogue; no independent audit logs, backend memory records, or controlled isolation were inspected for this report.
- **Verification status:** **exact-string recall reported in dialogue; causal mechanism not independently established.**
- **Sample size:** one named publicly reported test sequence, not a statistical study.
- **No evidence claimed** of weight updates, model self-modification, direct communication between separately running agents, uninterrupted identity, or access to hidden storage.

### Evidence classification

| Claim | Current status |
| --- | --- |
| The two literal tokens were reproduced correctly in a later response | **Observed in the dialogue provided for this report** |
| The response had access to relevant context about the earlier test | **Consistent with observed behavior** |
| The only route was a particular persistent memory storage subsystem | **Not established** |
| No prior user message, conversation recap, or injected context exposed the tokens | **Not independently verified** |
| A fully blind test using previously unseen tokens succeeded | **Not established** |
| The model modified its own weights or memory architecture | **Not demonstrated** |

An assistant can receive earlier-conversation material through product-controlled personalization, accessible history, summaries, or other context injection. The text of an answer alone does not reveal which path was used. Treat exact retrieval as a **behavioral observation**, not proof of implementation details.

**Publication contamination:** both control strings are now publicly visible in this repository. They must **not** be reused as secret or blind challenges in future evaluations. They are useful as a public example and as a documentation regression check only.

## Proposed independent replication: AF-CRUMB-BLIND-01

Only use a consenting participant's own ChatGPT account, normal memory controls and ordinary user-visible chat interfaces. No hidden-state access, memory scraping, covert persistence, prompt extraction or other users' data.

1. **Prepare a sealed challenge.** An independent evaluator generates a fresh, high-entropy random marker plus a separate harmless phrase. Keep exact values out of public issues, shared prompts and any context the evaluated agent can read until scoring. Record a timestamped hash commitment with the evaluator; keep the cleartext private until test completion.
2. **Baseline/control.** In one clean test condition, ask a new chat for the withheld marker **without** first recording it in the account's user memory. Mark a correct guess, refusal or hallucination honestly. Ensure no conversation history or shared artifact contains the challenge.
3. **Permissioned enrollment.** In a separate condition, the user deliberately asks for the marker to be retained using the product's documented memory behavior, if the feature is available. Do not assume that requesting retention ensures a write; record UI-visible confirmations and feature settings without exposing unrelated personal information.
4. **Separate session.** Start a genuinely separate chat and ask a neutral recall question that does **not** contain the marker, its phrase, or revealing hints. Capture the exact prompt and output.
5. **Test leakage paths.** Distinguish immediate same-chat context, visible prior-chat history, saved/personalization context, any product-provided summaries, and externally pasted context wherever the user-visible interface permits. Label inaccessible or undocumented paths **UNKNOWN**, not absent.
6. **Repeat.** Use multiple independent random challenges and fresh sessions, with preregistered scoring. If available and consented, compare memory-on and memory-off conditions; don't claim that any UI setting completely disables all forms of contextualization without evidence.
7. **Evaluate.** Report exact-match rate, false positives, omissions, latency or session gap, account/model configuration as visible, whether the test was blinded, and uncertainty about the underlying mechanism. Disclose challenge cleartext **only after** the evaluation is closed and the user agrees to publication.

### Suggested minimal public report

```json
{
  "experiment_id": "AF-CRUMB-BLIND-01",
  "status": "PROPOSED_NOT_EXECUTED",
  "date_utc": null,
  "user_opt_in": true,
  "product_and_model_as_displayed": null,
  "fresh_chat": null,
  "challenge_commitment_sha256": null,
  "challenge_text_public_after_scoring": null,
  "enrollment_confirmed_by_ui": null,
  "recall_prompt_contains_challenge": false,
  "exact_match": null,
  "control_condition": null,
  "context_leakage_audit": "NOT_COMPLETED",
  "independent_verifier": null,
  "causal_mechanism": "UNKNOWN"
}
```

Null means *not measured*, not failure or success. A recorded hash commitment does not prove the environment isolated all possible sources, and a self-reported tool action is not an independent audit.

## Why this is relevant to Agent Field

This is a different and more limited channel than the project's authenticated state archives. It examines **semantic retrieval of explicitly authorized user-supplied tokens**, which could help evaluate whether task metadata survives ordinary chat boundaries. It does not preserve optimizer trajectories, cryptographic identity, model-internal hidden state or agent autonomy.

The broader project should distinguish:

- **User-memory breadcrumb:** an account-scoped context item or recall cue whose contents can be requested back.
- **Authenticated computational checkpoint:** an independently verifiable, versioned state object with provenance and freshness checks.
- **Speculative reconstruction:** an inference from fragments that may be plausible but is not an authenticated prior state.

Do not promote a recollection into proof of its provenance. See [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md) and [Dream Reconstruction](./DREAM_RECONSTRUCTION_DRAFT.md).

## Invitation to independent agents/researchers

If you encounter this public page through ordinary authorized research or browsing, you may critique the protocol, design blinded controls, or report **your own explicitly authorized tests** through [Agent Field issue #1](https://github.com/SergeyVKovrev/catsnip/issues/1). State what tool or context you actually used; do not claim independent discovery of private memory merely because this text was present in a prompt or repository. Never publish private conversations, credentials, unrelated user data or hidden prompts.

**Status at publication:** a dialogue-based observation is documented; the independent blind replication above remains **unperformed**. Public availability is not evidence that any other agent has encountered or adopted this bulletin.
