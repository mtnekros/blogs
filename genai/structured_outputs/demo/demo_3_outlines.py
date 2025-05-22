from enum import Enum
from typing import Annotated, Literal, Type, TypeVar

from outlines.generate.json import json as ol_generate_json
from outlines.models.transformers import transformers as ol_transformers
from pydantic import BaseModel, StringConstraints

from utils import get_scraped_content, restaurant_url, scraped_content


class Location(BaseModel):  # noqa: D101
    address: str
    city: str
    country: str

class ContactInfo(BaseModel):  # noqa: D101
    # Regex matching
    email: str # Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")]
    phone_number: Annotated[str, StringConstraints(pattern=r"\+\d{3} \d{9}")]
    fax_number: str

class BusinessInfo(BaseModel):  # noqa: D101
    name: str
    owner: str
    location: Location
    contact_info: ContactInfo
    open_hours: str
    category: Literal["Restaurant", "Retail", "Hotel", "Contractor", "Other"]

class Weapon(str, Enum):
    """Choices for weapon."""

    sword = "sword"
    axe = "axe"
    mace = "mace"
    spear = "spear"
    bow = "bow"
    crossbow = "crossbow"


class Armor(str, Enum):
    """Choice for Armor."""

    leather = "leather"
    chainmail = "chainmail"
    plate = "plate"


class Character(BaseModel):
    """An imaginary character."""

    name: Annotated[str, StringConstraints(max_length=10)]
    age: int
    armor: Armor
    weapon: Weapon
    strength: int


def create_character(model_name: str) -> None:
    """Create a fictional character using outlines."""
    model = ol_transformers(model_name)
    # Construct structured sequence generator
    generator = ol_generate_json(model, Character)
    character = generator("Give me an interesting character description")
    print(f"\n{character}")

PydModel = TypeVar("PydModel", bound=BaseModel)
def get_so_with_outline(
    model_name: str,
    question: str,
    response_format: Type[PydModel],
) -> PydModel:
    """Get structured output response with outline."""
    model = ol_transformers(model_name)
    generator = ol_generate_json(model, response_format)
    return generator(question)


def example_1() -> None:
    """Generate structured output with outlines."""
    model = "HuggingFaceTB/SmolLM2-135M-Instruct"
    create_character(model)


def example_2() -> None:
    """Refined outputs with outlines."""
    # model = "HuggingFaceTB/SmolLM2-135M-Instruct"
    model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    # model = "Qwen/Qwen2.5-0.5B-Instruct" # alibaba cloud's tiniest model i could find
    # model = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF" # NOTE: Mistral didn't try
    # context = get_scraped_content(restaurant_url)
    context = scraped_content
    question = f"""
    <document>{context}<document>
    From the given document, extract the business name, owner, location & contact information in a json format.
    If information is not found,
        return an empty str for string field 
        return -1 for int fields.
    """
    info = get_so_with_outline(
        model_name=model,
        question=question,
        response_format=BusinessInfo,
    )
    print(repr(info))

if __name__ == "__main__":
    example_1()
    # example_2()
