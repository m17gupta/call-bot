from openai import OpenAI
import os

def suggest_description_from_row(row):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Suggest a product description from: {row}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
