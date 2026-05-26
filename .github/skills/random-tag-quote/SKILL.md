---
name: random-tag-quote
description: 'Provide a random quote from Abirate/english_quotes by user-provided tag. Use when users ask for an inspirational, topical, or mood-based quote by tag, especially when they say "now I need a <tag> quote".'
argument-hint: 'tag (example: humor, life, love, success)'
---

# Random Tag Quote

Return one random quote from the Hugging Face dataset `Abirate/english_quotes` using a tag provided by the user.

## When to Use
- User asks for a random quote with a specific tag.
- User wants a quote matching a mood or topic.
- User asks for a quote from `Abirate/english_quotes`.
- User says: "now I need a <tag> quote".


## Procedure
1. Extract the requested tag from the user prompt.
2. If no tag is provided, ask for one tag before continuing.
3. Do not create or configure a virtual environment (venv/virtualenv/pipenv/poetry) for this skill.
4. Run the skill script in the `genai` Conda environment: `conda run -n genai python .github/skills/random-tag-quote/scripts/get_random_tag_quote.py <tag>`.
5. Optional fast path: use local cache only with `--offline` after cache exists.
6. The script normalizes tag comparison with lowercase matching.
7. If no quotes match, the script reports that clearly and suggests nearby options:
   - Show up to 10 available tags from `tags.txt` (if present).
   - Otherwise derive tags from dataset and suggest up to 10 close matches.
8. If matches exist, the script chooses exactly one random item.
9. Return the script result in a concise response with:
   - Quote text
   - Author
   - Matched tag

## Branching Logic
- Missing tag: ask user for one tag and wait.
- Invalid tag: do not fail silently; explain no matches and suggest valid tags.
- Valid tag with matches: return one random quote only.

## Quality Checks
- Confirm the quote comes from filtered results for the requested tag.
- Ensure randomness is applied only after filtering.
- Keep response concise and readable.
- Include attribution (`author`) every time.

## Implementation Notes
- Script entrypoint: [./scripts/get_random_tag_quote.py](./scripts/get_random_tag_quote.py)
- Script options:
   - `conda run -n genai python .github/skills/random-tag-quote/scripts/get_random_tag_quote.py --list-tags`
   - `conda run -n genai python .github/skills/random-tag-quote/scripts/get_random_tag_quote.py humor`
   - `conda run -n genai python .github/skills/random-tag-quote/scripts/get_random_tag_quote.py --offline humor`
