import openai
from decouple import config

# Set your OpenAI API Key securely
openai.api_key = config("OPENAI_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def gpt_fallback(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mixtral-8x7b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"I'm having trouble reaching the AI service right now. Error: {e}"
