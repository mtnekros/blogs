from ollama import chat as ollama_chat

model = "phi"

response = ollama_chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": """
            Tell me the benefits of giving presentations teaching things we learn every week in json format.
            """
        },
    ],
)

print(response.message.content)

