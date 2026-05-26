# Workspace Copilot Instructions

- When the user says "now I need a <tag> quote", invoke the `random-tag-quote` skill.
- Treat `<tag>` as the requested quote tag and pass it directly as the skill argument.
- If the phrase is used without a tag, ask for one tag before invoking the skill.
- For the `random-tag-quote` skill, do not create or configure a Python venv.
- Execute the skill with Conda exactly as documented: `conda run -n genai python .github/skills/random-tag-quote/scripts/get_random_tag_quote.py <tag>`.
