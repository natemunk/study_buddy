import os

import markdown
import pdfkit
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def create_worksheet(youtube_url: str, google_api_key: str):
    """
    Creates a worksheet from a YouTube video transcript using the Gemini API.

    Args:
        youtube_url: The URL of the YouTube video.
        google_api_key: The Google API key for Gemini.

    Returns:
        The path to the generated PDF worksheet, or None if an error occurred.
    """
    try:
        # Fetch transcript
        loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=False)
        transcript = loader.load()

        # Combine transcript text
        full_transcript = transcript[0].page_content

        # Gemini API interaction
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        prompt = f"""
You are an educational content creator that transforms YouTube video transcripts into engaging, interactive worksheets designed to enhance active learning.

Below is the full transcript of a YouTube video:
{full_transcript}

Your task is to analyze the transcript and identify the key segments or sections of the video in chronological order. Then, create a worksheet in Markdown format with the following features:

1. **Chronological Organization:**
   Arrange all questions and activities in the order of the video’s timeline.

2. **Engaging Questions:**
   Include a mix of question types (e.g., multiple-choice, short-answer, reflection, fill-in-the-blanks) that encourage the viewer to actively listen and process the content.

3. **Interactive Activities:**
   Add engaging tasks such as summarizing key points, predicting what will come next, or reflective prompts that require personal insights.

4. **Segment Headers:**
   Clearly label each section of the worksheet (e.g., “Introduction,” “Main Content,” “Conclusion”) so viewers can easily follow along with the video's flow.

5. **Ample Space for Answers:**
   For each question or activity, provide generous space for users to write down their responses. Use blank lines, underscores, or designated write-in areas (e.g., "____________________") to indicate where users should write their answers. They should receive a minimum of two lines for each answer, unless a single word answer is required.

6. **Active Learning Focus:**
   Ensure that the questions and activities reinforce the major concepts covered in the video and encourage personal reflection on the content.

Ensure that the final output is entirely formatted in Markdown. Do not include any bibliographic references or additional information beyond the worksheet.

Produce the completed worksheet as your final output.

The user needs 3-5 new lines worth of space between each question for notes and answers. This is a priority.
"""
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])

        # Convert markdown to HTML, then to PDF
        worksheet_md = response.content
        worksheet_html = markdown.markdown(worksheet_md)

        # Add CSS for styling
        styled_html = f"""
<style>
.worksheet hr {{
  border: none;
  height: 2px;  /* Adjust as needed */
  background-color: #eee; /* Light gray line */
  margin: 2rem 0; /* Add some vertical space */
}}
</style>
<div class="worksheet">
{worksheet_html}
</div>
"""

        pdf_path = "worksheet.pdf"
        pdfkit.from_string(styled_html, pdf_path)

        return pdf_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        exit(1)

    youtube_url = input("Enter the YouTube video URL: ")
    pdf_path = create_worksheet(youtube_url, google_api_key)

    if pdf_path:
        print(f"Worksheet created and saved to: {pdf_path}")
