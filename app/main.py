from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from .models import StoryRequest, StoryResponse, StoryLog, DashboardData

# Load environment variables
load_dotenv()

# --- Constants ---
BADGE_CATEGORIES = {
    "Science": "🔬", "Math": "🧮", "History": "📜", "Geography": "🌍",
    "Art": "🎨", "Music": "🎵", "Literature": "📚", "Technology": "💻",
    "Nature": "🌳", "Health": "❤️"
}

LEARNING_PATH_THRESHOLDS = {
    "Beginner": 0,
    "Intermediate": 5,
    "Advanced": 15,
    "Expert": 30
}

# In-memory "database" for story logs
story_logs: list[StoryLog] = []

# --- FastAPI App Initialization ---
app = FastAPI(title="MagicQuest")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- AI Configuration ---
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Helper Functions ---
def get_learning_path_badge(num_questions: int) -> str:
    """Determine the learning path badge based on the number of questions asked."""
    badge = "Beginner"
    for level, threshold in LEARNING_PATH_THRESHOLDS.items():
        if num_questions >= threshold:
            badge = level
    return badge

def generate_story(question: str) -> StoryResponse:
    """Generate a story and learning badge based on the child's question."""
    badge_list = ", ".join(BADGE_CATEGORIES.keys())
    prompt = f"""
    You are a creative and friendly storyteller for children.
    Create a short, child-friendly story (3-4 sentences) based on this question: "{question}"
    The story should be educational, safe, and positive.
    Also, provide a "learning point" for a parent and a "badge" category.
    The badge MUST be one of these exact categories: {badge_list}.
    Return a JSON object with three keys: "story", "learning_point", and "badge".
    """
    
    response = model.generate_content(prompt)
    
    try:
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(cleaned_response)
        
        badge = data.get("badge", "Creativity")
        if badge not in BADGE_CATEGORIES:
            badge = "Creativity" # Fallback for safety
            
        badge_icon = BADGE_CATEGORIES.get(badge, "✨")
        
        learning_path_badge = get_learning_path_badge(len(story_logs) + 1)
        
        story_log = StoryLog(**data, question=question, badge_icon=badge_icon)
        story_logs.append(story_log)
        
        return StoryResponse(
            story=data["story"],
            learning_point=data["learning_point"],
            badge=badge,
            badge_icon=badge_icon,
            learning_path_badge=learning_path_badge
        )
    except (json.JSONDecodeError, KeyError):
        return StoryResponse(
            story="Once upon a time, a curious explorer asked a wonderful question!",
            learning_point="Explored creative thinking and curiosity.",
            badge="Creativity",
            badge_icon="✨",
            learning_path_badge=get_learning_path_badge(len(story_logs) + 1)
        )

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask", response_model=StoryResponse)
async def ask_question(story_request: StoryRequest):
    """Handle text-based questions and return a story."""
    return generate_story(story_request.question)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Display the parental dashboard with story logs and badge counts."""
    badge_counts = {}
    for log in story_logs:
        badge_counts[log.badge] = badge_counts.get(log.badge, 0) + 1
        
    learning_path_badge = get_learning_path_badge(len(story_logs))
    
    dashboard_data = DashboardData(
        stories=story_logs, 
        badge_counts=badge_counts,
        learning_path_badge=learning_path_badge
    )
    return templates.TemplateResponse("dashboard.html", {"request": request, "dashboard_data": dashboard_data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
