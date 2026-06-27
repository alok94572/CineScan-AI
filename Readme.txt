🎬 CineScan AI

An AI-powered movie information extractor built with LangChain, Llama 3.1 (Ollama), Pydantic, and Streamlit.

Paste any unstructured movie description, review, or paragraph, and CineScan AI automatically extracts structured movie information such as title, release year, genres, cast, director, rating, and summary.

Features
AI-powered movie information extraction
Structured JSON output using Pydantic
Interactive Streamlit dashboard
Session-based movie library
Download extracted data as JSON
Quick links to IMDb, YouTube trailers, and Rotten Tomatoes
Runs locally using Ollama (No external API required)
Tech Stack
Python
LangChain
Ollama
Llama 3.1
Streamlit
Pydantic
Project Workflow
User enters an unstructured movie description.
LangChain formats the prompt.
Llama 3.1 extracts movie information.
Pydantic validates the response.
Streamlit displays structured results.
Users can save and export extracted movies.
Extracted Information
Movie Title
Release Year
Genre
Director
Cast
Rating
Summary
Installation
git clone https://github.com/yourusername/CineScan-AI.git

cd CineScan-AI

pip install -r requirements.txt

Start Ollama:

ollama run llama3.1

Run the application:

streamlit run app.py
Example Input

Christopher Nolan directed Inception in 2010. The film stars Leonardo DiCaprio, Joseph Gordon-Levitt, and Elliot Page. It is a science fiction thriller with an IMDb rating of 8.8.

Example Output
{
  "title": "Inception",
  "release_year": 2010,
  "genre": ["Science Fiction", "Thriller"],
  "director": "Christopher Nolan",
  "cast": [
    "Leonardo DiCaprio",
    "Joseph Gordon-Levitt",
    "Elliot Page"
  ],
  "rating": 8.8,
  "summary": "A skilled thief enters dreams to steal secrets but faces his most difficult mission yet."
}
Future Improvements
Movie poster integration
Multiple movie extraction
PDF export
TMDB API integration
Search history
Dark/Light mode
Advanced analytics dashboard
Author

Alok Mishra

Built while learning Generative AI, LangChain, Prompt Engineering, and Local LLM application development.