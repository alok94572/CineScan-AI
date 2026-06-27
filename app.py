import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
import json
import urllib.parse

# --- Page Config ---
st.set_page_config(page_title="CineScan AI", page_icon="🍿", layout="wide")

# --- Custom CSS for a Cinematic Look ---
st.markdown("""
    <style>
    .main { background-color: #0b0d11; }
    .movie-card {
        background-color: #161b22;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #e50914;
        margin-bottom: 20px;
    }
    .genre-pill {
        background-color: #3d444d;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 5px;
        border: 1px solid #e50914;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff0a16;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic: Model & Schema ---
class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    release_year: Optional[int] = Field(description="Year of release")
    genre: List[str] = Field(description="Genres")
    director: Optional[str] = Field(description="Director name")
    cast: List[str] = Field(description="Main actors")
    rating: Optional[float] = Field(description="Rating out of 10")
    summary: str = Field(description="Short summary")

parser = PydanticOutputParser(pydantic_object=Movie)
model = ChatOllama(model="llama3.1", temperature=0)

# Initialize Session State for "My Library"
if "library" not in st.session_state:
    st.session_state.library = []

# --- UI Header ---
st.markdown("<h1 style='text-align: center; color: #e50914;'>🎬 CINE-SCAN AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Transform messy text into cinematic structured data</p>", unsafe_allow_html=True)
st.write("---")

# --- Layout ---
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader("📽️ Input Source")
    para = st.text_area(
        "Paste movie descriptions, reviews, or scripts here:",
        placeholder="Example: Christopher Nolan directed Inception in 2010. Starring Leonardo DiCaprio, this sci-fi heist thriller has a rating of 8.8...",
        height=300
    )
    
    extract_btn = st.button("PROCESS DATA")

with right_col:
    st.subheader("📊 Extraction Results")
    
    if extract_btn and para:
        with st.spinner("Analyzing frames..."):
            try:
                # Prompt Engineering
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "Extract movie details precisely. {format_instructions}"),
                    ("human", "{paragraph}")
                ])
                final_prompt = prompt.invoke({"paragraph": para, "format_instructions": parser.get_format_instructions()})
                
                # LLM Call
                response = model.invoke(final_prompt)
                movie_data = parser.parse(response.content)
                
                # Store in session library
                st.session_state.library.append(movie_data.dict())

                # Display Modern Result Card
                st.markdown(f"""
                    <div class="movie-card">
                        <h2 style='margin-top:0;'>{movie_data.title.upper()} ({movie_data.release_year or 'N/A'})</h2>
                        <p style='color: #8b949e;'>Directed by <b>{movie_data.director or 'Unknown'}</b></p>
                    </div>
                """, unsafe_allow_html=True)

                # Rating with a progress bar
                r = movie_data.rating or 0.0
                st.write(f"**Critic Score:** {r}/10")
                st.progress(r / 10)

                # Summary & Cast
                st.info(f"**Summary:** {movie_data.summary}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**🎭 Cast**")
                    for actor in movie_data.cast:
                        st.markdown(f"- {actor}")
                with c2:
                    st.write("**🏷️ Genres**")
                    genre_html = "".join([f'<span class="genre-pill">{g}</span>' for g in movie_data.genre])
                    st.markdown(genre_html, unsafe_allow_html=True)

                st.write("---")
                
                # Amazing Feature: External Quick Links
                st.write("🔗 **Quick Explore**")
                search_query = urllib.parse.quote(movie_data.title)
                link_cols = st.columns(3)
                link_cols[0].markdown(f"[IMDb](https://www.imdb.com/find?q={search_query})")
                link_cols[1].markdown(f"[Trailer](https://www.youtube.com/results?search_query={search_query}+trailer)")
                link_cols[2].markdown(f"[Rotten Tomatoes](https://www.rottentomatoes.com/search?search={search_query})")

            except Exception as e:
                st.error(f"Failed to parse movie data. Error: {e}")
    elif not extract_btn:
        st.info("Waiting for input... The results will appear here.")

# --- Bottom Section: Saved Library ---
st.write("---")
if st.session_state.library:
    st.subheader("📂 My Extracted Library")
    
    # Download Data Feature
    json_data = json.dumps(st.session_state.library, indent=4)
    st.download_button(
        label="Download Library as JSON",
        data=json_data,
        file_name="movie_library.json",
        mime="application/json"
    )
    
    # Simple table view of history
    st.table(st.session_state.library)

# --- Footer ---
st.markdown("<br><hr><center>Powered by Llama 3.1 & Streamlit Magic</center>", unsafe_allow_html=True)