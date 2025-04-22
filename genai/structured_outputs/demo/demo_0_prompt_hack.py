from ollama import chat as ollama_chat

from utils import get_scraped_content, restaurant_url, time_it


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



@time_it
def main() -> None:
    """Test with prompt hacking."""
    context = get_scraped_content(restaurant_url)
    question = f"""
    <document>{context}<document>
    From the given document, extract the business name, owner, location &
    contact information in a json format.

    Bro please respond in valid json format without errors and make super
    sure the syntax is extra correct. I am begging you... and please,
    pretty please, don't make up answers. My career depends on it bro.
    """
    model = "llama3.2"
    output = get_chat_response(model, question)
    print(output)

if __name__ == "__main__":
    main()

""" Example Output:
I'll make sure to get it right this time!

Here's the extracted information in JSON format:

```
{
  "business_name": "Le Sherpa Restaurant",
  "owner": null, // unable to find owner information
  "location": {
    "address": "Maharajgunj, KTM, Nepal",
    "opposite_of": "President House"
  },
  "contact_info": {
    "email": "This email address is being protected from spambots. You need JavaScript 
enabled to view it.",
    "phone": "+977-9801159480, 01-4528604"
  }
}
```

I was unable to find the owner's information, so I left it as `null`. If you have any f
urther questions or if there's anything else I can help you with, feel free to ask!    
Time taken by main: 23.774 sec(s).
"""
