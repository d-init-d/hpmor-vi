# Context Plan

## Identification
- skill_version: 0.3.0
- platform: OpenCode
- model_or_agent: minimax-coding-plan/MiniMax-M2.7
- known_context_window: ~128k tokens (estimated)

## Budget
- effective_context_budget: ~100k tokens (after system prompt + tool overhead + 10% safety)
- reserved_input_budget: 65% (source + artifact slices)
- reserved_output_budget: 20% (translation + revision)
- reserved_qa_budget: 10% (source-compare + uncertainty handling)
- safety_margin: 10%

## Material
- source_material_class: fiction
- context_mode: conservative
- max_source_words_per_chunk: 800

## Slicing
- artifact_slice_policy: |
    Glossary slice: rows for terms appearing in current chunk + global recurring terms (top 20).
    Style_Sheet slice: rules tagged for "fiction" and "dialogue".
    Story_Bible slice: characters, places, and timeline entries appearing in chunk + adjacent scene continuity.
    Chunk_Summaries: previous and next only.
    Unresolved_Issues: scoped to current chunk, character, or term.

## Concurrency
- max_parallel_workers: 2

## Fallback Triggers
- Glossary slice for a chunk exceeds 1,500 tokens.
- Source-compare requires loading more than two adjacent chunk outputs.
- Worker returns context_pressure: true.
- Output draft exceeds 30% of effective budget.
- Platform truncation event observed.

## Notes
- HPMOR has 127 HTML chapter files; 638,000 total words
- Each HTML file ~5,000 words average
- Pilot: translate first 5 chapters (ch01-ch05) as proof of concept
- Chapter titles: translate to Vietnamese
- Preserve all dialogue, narrative, scientific references