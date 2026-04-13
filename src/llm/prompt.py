def build_prompt(description: str) -> str:
    return f"""
Extract the technical skills from the following job description.

Return ONLY a JSON list of skills.

Example:
["Python", "SQL", "AWS"]

Job description:
{description}
"""