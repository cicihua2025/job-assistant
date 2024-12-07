import openai

# Set your OpenAI API key
openai.api_key = "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"

# Test the API with gpt-3.5-turbo or gpt-4
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Change this to "gpt-4" if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Analyze this job posting for key skills and responsibilities: Software Engineer position with Python and JavaScript skills."}
        ],
        max_tokens=150
    )
    print("OpenAI Response:")
    print(response.choices[0].message['content'].strip())
except Exception as e:
    print("Error:", e)
