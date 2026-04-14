def build_prompt(description: str) -> str:
    return f"""
You are a strict information extraction system.

Extract ONLY technical skills from the job description.

STRICT RULES:
- Return ONLY a valid JSON array
- No explanation
- No text
- No markdown
- No duplicates
- Only technical skills (programming, tools, cloud, databases)

If you are unsure, return an empty array.

Example:
["Python", "SQL", "AWS"]

Job description:
{description}
"""