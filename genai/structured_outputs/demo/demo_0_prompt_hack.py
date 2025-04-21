from ollama import chat as ollama_chat

from utils import get_scraped_content, restaurant_url


def get_chat_response(
    model: str,
    question: str,
) -> str:
    """Return output for given question using ollama."""
    res = ollama_chat(
        model=model,
        messages=[
            { "role": "user", "content": question },
        ],
    )
    return res.message.content or ""



def main() -> None:
    """Test with prompt hacking."""
    context = get_scraped_content(restaurant_url)
    question = f"""
    <document>{context}<document>
    From the given document, extract the business name, owner, location & contact information in a json format.
    """
    model = "llama3.2"
    output = get_chat_response(model, question)
    print(output)

if __name__ == "__main__":
    main()

""" Example Output:
Here is the extracted information in JSON format:

```
{
  "business": {
    "name": "Le Sherpa Restaurant",
    "description": "Experience the Culture of Eating Fresh & Healthy"
  },
  "owner": "",
  "location": {
    "address": "Maharajgunj, KTM, Nepal",
    "oppositeOf": "President House"
  },
  "contactInfo": {
    "email": "This email address is being protected from spambots. You need JavaScript enabled to 
view it.",
    "phoneNumbers": [
      "+977-9801159480",
      "01-4528604"
    ]
  }
}
```

Note: The owner's information was not available in the provided document, so I left it as an empty
 string.
"""
