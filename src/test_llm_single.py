from llm.client import call_llm

prompt = """
Extract explicit technical skills from the following job description.

Return only a valid JSON array of strings.

Rules:
- No explanation
- No markdown
- No extra text
- No objects
- No levels
- Only explicit technical skills mentioned in the text
- Do not invent skills
- Do not use the job title as a skill
- Keep the original wording when possible

Job description:
We are looking for a Data Engineer with experience in Python, SQL, Apache Spark, Docker, Airflow, and AWS.
"""

response = call_llm(prompt)
print(response)