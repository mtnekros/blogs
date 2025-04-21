"""Use instructor & ollama running on localhost to generate structured outputs."""

from pprint import pprint
from textwrap import dedent
from typing import Type, TypeVar

import instructor
from ollama import chat as ollama_chat
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from pydantic import BaseModel, Field

OLLAMA_HOST = "http://localhost:11434/v1"


class ArticleSummary(BaseModel):
    """Summary Schema for the structured output."""

    key_points: list[str] = Field(description="Key points from the articles")
    summary: str = Field(description="Summary of the articles in a few words.")


class TokenTracker(BaseModel):
    """Class to track token & attempts."""

    n_attempts: int = 0
    input_tokens: list[int] = Field(default_factory=list)
    output_tokens: list[int] = Field(default_factory=list)

    def update(self, completion: ChatCompletion) -> None:  # noqa: ANN401
        """Track no of retries & tokens used."""
        self.n_attempts += 1
        print(f"Attemp no: {self.n_attempts}")
        if not completion.usage:
            return
        self.input_tokens.append(completion.usage.prompt_tokens)
        self.output_tokens.append(completion.usage.completion_tokens)


    def summary(self) -> str:
        """Return the summary of attempts."""
        return dedent(f"""
            Num Retries: {self.n_attempts}
            Total Input Token Used: {sum(self.input_tokens)}
            Total Output Token Used: {sum(self.output_tokens)}
            Total Tokens Used: {sum(self.input_tokens) + sum(self.output_tokens)}"
        """)

PydModel = TypeVar("PydModel", bound=BaseModel)

def get_so_with_instructor(
    model: str,
    question: str,
    response_model: Type[PydModel],
    max_retries: int = 4,
) -> PydModel:
    """Get structured output with instructor."""
    tracker = TokenTracker()
    client = instructor.from_openai(
        OpenAI(
            base_url=OLLAMA_HOST,
            api_key="ollama", # required, but unused.
        ),
        mode=instructor.Mode.JSON,
    )
    client.on("completion:response", tracker.update)
    resp = client.chat.completions.create(
        model=model,
        messages=[ { "role": "user", "content": question } ],
        response_model=response_model,
        max_retries=max_retries,
    )
    print(tracker.summary())
    return resp

def get_vanilla_output(
    model: str,
    question: str,
) -> str:
    """Get vanilla response from ollama."""
    response = ollama_chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    return response.message.content or ""

def summarise_new_article_comp() -> None:
    """Comparison between structured output & converstation text using instructor & ollama."""
    context = """
    DHL Express is suspending deliveries to the US worth more than $800 (£603) because of a "significant increase" in red tape at customs following the introduction of Donald Trump's new tariff regime.
    The delivery giant said it will temporarily stop shipments from companies in all countries to American consumers on Monday "until further notice".
    It added that business-to-business shipments will still go ahead, "though they may also face delays".
    Previously, packages worth up to $2,500 could enter the US with minimal paperwork but due to tighter customs checks that came into force alongside Trump's tariffs earlier this month, the threshold has been lowered.
    DHL said that the change "has caused a surge in formal customs clearances, which we are handling around the clock".
    It said that while it is working to "scale up and manage this increase, shipments worth over $800, regardless of origin, may experience multi-day delays".
    The company said it will still deliver packages worth less than $800, which can be sent to the US with minimal checks.
    But the White House is set to clamp down on deliveries under $800 - specifically those sent from China and Hong Kong - on 2 May when it closes a loophole allowing low-value packages to enter the US without incurring any duties.
    The removal of the so-called "de minimis" rule will impact the likes of the fast-fashion firm Shein and Temu, the low-cost retail giant.
    Shein and Temu have both warned that they will increase prices "due to recent changes in global trade rules and tariffs".
    The Trump administration has claimed that "many shippers" in China "hide illicit substances and conceal the true contents of shipments sent to the US through deceptive shipping practices".
    Under an excutive order, the White House said the measures were aimed at "addressing the synthetic opioid supply chain" which it said "play a significant role in the synthetic opioid crisis in the US".
    Beijing has said that the opioid fentanyl is a "US problem" and China has the strictest drug policies in the world.
    Last week, Hongkong Post said it was suspending packages sent to the US by sea and, from 27 April, would stop accepting parcels destined for America.
    It said: "The US is unreasonable, bullying and imposing tariffs abusively."
    """  # noqa: E501
    question = f"""
        <document>{context}</document>
        Give me a summary of the article above & give me the main key points
    """
    # model = "phi"
    model = "llama3"
    summary = get_so_with_instructor(
        model=model,
        question=question,
        response_model=ArticleSummary,
    )
    print(f"Article Summary: {summary.summary}")
    print("Key points:")
    for i, points in enumerate(summary.key_points):
        print(f"   * Fact {i}: {points}")

    vanilla_output = get_vanilla_output(model=model,question=question + " in json format.")
    print("\nVanilla Output:")
    pprint(vanilla_output)


if __name__ == "__main__":
    summarise_new_article_comp()
