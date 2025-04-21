import json
from typing import Literal

from ollama import chat
from pydantic import BaseModel, Field, StringConstraints

from utils import get_scraped_content, restaurant_url


class Location(BaseModel):  # noqa: D101
    address: str
    city: str
    country: str

class ContactInfo(BaseModel):  # noqa: D101
    email: str
    # NOTE: that email is just a string. We can't do pattern matching . :( or
    # with openai as for now
    # Only if we could do something like there:
    # email: Annotated[str, StringConstraints(pattern=r"^$|^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}")]
    phone_number: str
    fax_number: str

class BusinessInfo(BaseModel):  # noqa: D101
    name: str = Field(description="Name of the business.")
    owner: str = Field(description="Business Owner. Will be empty string if not found")
    location: Location
    contact_info: ContactInfo
    category: Literal["Restaurant", "Retail", "Hotel", "Contractor", "Other"]

def main() -> None:
    """Extract business info using ollama's structured output api."""
    context = get_scraped_content(restaurant_url)
    print(context)
    question = f"""
    <document>{context}<document>
    From the given document, extract the business name, owner, location & contact information in a json format.
    If information is not found, just leave an empty str for string field or -1 for int fields.
    """
    model = "llama3" # phi llama3.2
    response = chat(
        messages=[ { 'role': 'user', 'content': question } ],
        model=model,
        format=BusinessInfo.model_json_schema(),
    )

    # biz_info = BusinessInfo.model_validate_json(response.message.content or "")
    # print(repr(biz_info))
    print(response.message.content)


if __name__ == "__main__":
    main()
