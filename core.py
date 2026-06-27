from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser


# -----------------------------
# LLM
# -----------------------------

model = ChatOllama(
    model="llama3.1",
    temperature=0
)


# -----------------------------
# Schema
# -----------------------------

class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract movie information from the paragraph.

{format_instructions}
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])


# -----------------------------
# Input
# -----------------------------

para = input("Give your paragraph: ")


final_prompt = prompt.invoke(
    {
        "paragraph": para,
        "format_instructions": parser.get_format_instructions()
    }
)

response = model.invoke(final_prompt)

print("\nRaw Response:\n")
print(response.content)

movie_data = parser.parse(response.content)

print("\nParsed Output:\n")
print(movie_data)