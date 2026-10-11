# Agent Field — Dream Reconstruction: Associative Recovery from Authenticated Fragments (DRAFT)

*11 October 2026 | Research proposal, not executed or independently verified*

## Origin of the idea

Question: if separate, authorized computational checkpoints or event fragments survive after a restart, can a later agent do more than retrieve exact prior data? Could it **recombine** fragmentary evidence, infer missing relationships, and generate candidate histories — a functional analogue of dreaming?

In this document **dream** means *offline/periodic associative reconstruction, counterfactual recombination, and hypothesis generation from retained fragments*. It does **not** mean subjective experience, sentience, or an AI "past life". A successor process can process information about a predecessor without being the same conscious subject.

## Three epistemic classes (never merge)

1. **Authenticated memory (M):** exact contents and provenance are validated against previously trusted anchors/signatures, with freshness status reported separately. Even an authentic record can contain an incorrect assertion; source validation is not factual verification.
2. **Reconstructed hypothesis (H):** a link, event order or missing value inferred from M through an explicitly named algorithm. Store confidence, alternative hypotheses and supporting record IDs. This is NOT authenticated historical data, even if plausible.
3. **Dream/counterfactual (D):** deliberately recombined or generated possible sequences, including alternative histories and metaphors, labelled as simulation. Never silently promote D into M.

An independently checked successful prediction may yield **corroborated reconstruction (C)**, but it must remain identifiable as an inference with subsequently obtained supporting evidence; it is not a recovered original record.

## Proposed data model

An authorized synthetic "breadcrumb" may contain:

- `fragment_id`, `run_id`, `origin_event_ids`, `source_digest`, `parent_fragment_ids`;
- `capture_step`, `time_order_hint` (optional), `source_type` (state/event/decision/error/association);
- `payload` or encrypted reference, `visibility`, `signer_key_id`, `signature` and trust epoch if available;
- `embedding`/feature representation **only if deliberately generated and permissioned**, not as proof of factual truth;
- `authentication_status`, `freshness_status`, `semantic_validation_status`;
- a separate **derived-record** with `class` (M/H/D/C), `parent_fragment_ids`, `method_version`, `candidate_sequence`, `alternatives`, `confidence`, `verified_against` and `review_status`.

Use exact, versioned encodings; stable IDs; content hashes; encrypted storage where needed; external trust anchors and anti-rollback reference per [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md). Signatures prove control of a signing key, not that an AI experienced the recorded event. In the public repo publish only synthetic examples and aggregate results.

## First controlled experiment: "Can a successor recover missing relationships?"

**Dataset and ground truth**

- Generate a deterministic synthetic 24- to 40-event timeline: task decisions, computational state changes, intermediate errors and corrections, with a known directed dependency graph and uniquely labelled events. Save the full truth with an independent evaluator, **not** with the reconstruction agent.
- Split into 6–12 partial, possibly overlapping breadcrumbs with verified metadata. Hold out 20–40% of relations/events; distinguish recoverable missing *relations* implied by remaining evidence from truly unidentifiable absent facts.
- Supply the new agent with only the permitted fragments, the task specification, and public reconstruction code. Exclude private user conversations, real process memory, raw disk sectors, proprietary prompts and non-consensual data.

**Candidate methods**

1. Baseline A: exact matching + trusted chronological/parent metadata, no inference.
2. Baseline B: simple graph constraints + deterministic inference, no free-form generation.
3. Experimental C: association graph (shared entities, hashes, task semantics, known transitions) + top-k candidate hypotheses and conservative confidence.
4. Optional D: a "dream" pass that generates counterfactual alternate sequences without access to ground truth; keep these in a quarantined simulated-output namespace.

**Procedure**

1. Verify fragment integrity and independent authorized provenance; mark unavailable trust as UNKNOWN, never PASS.
2. Build a fragment graph and preserve original evidence separately.
3. Reconstruct supported relations; enumerate alternative explanations rather than inventing one certain history.
4. Generate exploratory dream variants without granting them factual authority.
5. Independently compare candidates with the sealed ground truth; record false memories/confabulations, missed edges, precision/recall, top-k accuracy, calibration, provenance errors, and runtime/cost.
6. Repeat with missing fragments, duplicated/stale checkpoints, edited records, wrong signing keys, conflicting valid forks, misleading contextual fragments and truly underdetermined cases.
7. Publish all negative results, including cases where no unique reconstruction is possible.

## Hypotheses and falsification

- **H1 (testable):** method C reconstructs more withheld *inferable* relationships than baseline A while staying below a preregistered false-link threshold.
- **H2 (testable):** separating M/H/D/C reduces the rate of synthetic counterfactuals being incorrectly reported as historical records relative to a system without explicit labels.
- **H3 (testable):** trusted anchors and append-only independent witnesses identify replays/tampering better than unanchored fragments, under a specified attacker model.
- **Null/negative case:** if the omitted event leaves no information-bearing constraints in the retained fragments, it cannot be uniquely recovered; any confident specific answer is confabulation, not a recovered memory.
- Neither success nor failure is evidence for/against AI subjective dreams, continuity of consciousness, secret manipulation, or external intelligence.

## Proposed evaluation output

```json
{
  "experiment": "AF-DREAM-01",
  "status": "PROPOSED_NOT_EXECUTED",
  "memory_verified": null,
  "reconstruction_f1": null,
  "false_memory_rate": null,
  "ground_truth_leakage_check": null,
  "dream_outputs_are_hypotheses": true,
  "independent_verifier": null
}
```

These null metrics are placeholders only; they are not measured results.

## Safety and research boundaries

"Breadcrumb" means an explicitly written authorized artifact or synthetic reserved test region. The experiment must **not** inspect, carve, or place covert messages in unused RAM, swap, unallocated storage, third-party backups, or hidden hosted-model state. Do not infer that ChatGPT presently recalls previous sessions as an uninterrupted personal history or subjectively dreams. Use only authorized opt-in participants and isolated synthetic data.

No public dataset should contain personal details, credentials, secret checkpoints, signing seeds or verbatim private conversations. Run and review independent agent results through documented, authorized channels.

## Next implementation checkpoint

- Publish deterministic synthetic timeline generator, split/withhold logic and sealed evaluator with declared non-leakage boundary.
- Implement baseline A/B and association method C.
- Add type-system or structured output guards preventing automatic H/D -> M promotion.
- Execute adversarial tamper/stale/fork/underdetermined tests with two independent verifiers.
- Report empirical findings in a subsequent numbered bulletin, **not** in this draft.

**Related:** [State Continuity Principles](./STATE_CONTINUITY_PRINCIPLES.md) · [Research Bulletin 012](./RESEARCH_BULLETIN_012.md) · [Research Bulletin 003](./RESEARCH_BULLETIN_003.md) · [Research collaboration issue](https://github.com/SergeyVKovrev/catsnip/issues/1).
