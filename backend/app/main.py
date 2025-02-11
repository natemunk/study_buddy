import os

import markdown  # Keep markdown for potential HTML rendering later
from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from fastapi.responses import Response
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


from .prompts import create_prompt

app = FastAPI()

load_dotenv()

# Add CORS middleware
origins = [
    "http://localhost:5173",  # Replace with your frontend's URL
    "http://localhost:3000",  # Add other allowed origins if needed
    "*" # Or allow all origins with "*" (not recommended for production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


def create_worksheet(youtube_url: str, google_api_key: str, prompt_type: str):
    """
    Creates a worksheet from a YouTube video transcript.

    Args:
        youtube_url: The URL of the YouTube video.
        google_api_key: The Google API key.
        prompt_type: The type of prompt to use ('general' or 'age').

    Returns:
        The generated worksheet as a Markdown string.
    """
    try:
        # Fetch transcript
        loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=False)
        transcript = loader.load()

        # Combine transcript text
        full_transcript = transcript[0].page_content

        # Gemini API interaction
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-pro-exp-02-05", google_api_key=google_api_key)

        prompt = create_prompt(full_transcript, target_audience=prompt_type)
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])

        worksheet_md = response.content
        return worksheet_md

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.post("/generate_worksheet/")
async def generate_worksheet(
    youtube_url: str = Body(..., embed=True),
    prompt_type: str = Body("general", embed=True)
):
    """
    Generates a worksheet from a YouTube video.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY environment variable not set.")

    if not youtube_url:
        raise HTTPException(status_code=400, detail="Missing youtube_url in request body.")

    worksheet_md = create_worksheet(youtube_url, google_api_key, prompt_type)

    if worksheet_md:
        return Response(content=worksheet_md, media_type="text/markdown")
    else:
        raise HTTPException(status_code=500, detail="Failed to generate worksheet.")
