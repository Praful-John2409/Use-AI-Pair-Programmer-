from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribe/")
async def transcribe_audio(request: Request):
    data = await request.json()
    transcript = data.get("transcript")
    
    # Summarize and extract entities using GPT-4o
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Summarize and extract entities from the transcript using the predefined schema."},
            {"role": "user", "content": transcript}
        ]
    )
    summary = response.choices[0].message['content']
    return {"summary": summary}