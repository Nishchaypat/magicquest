# MagicQuest 🌟

An interactive, multi-page storytelling application that sparks children's curiosity with AI-generated tales and provides insightful analytics for parents.

## Features

- **Interactive Storytelling**: Children can ask any question and receive a unique, age-appropriate story in return.
- **Parental Dashboard**: A separate view for parents to track their child's activity, including questions asked and stories read.
- **Learning Badges**: Each story comes with a "learning badge" (e.g., Science, History, Art) to highlight the educational theme.
- **Badge Analytics**: The dashboard provides a summary of all badges earned, offering insights into a child's interests.
- **Modern UI**: A clean, engaging, and responsive interface built with TailwindCSS.
- **Safe Content Generation**: Powered by Google's Gemini Pro, with prompts designed for safe, child-friendly content.

## Project Structure
```
/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI main application, endpoints
│   └── models.py       # Pydantic data models
├── static/             # Static files (CSS, JS, images)
├── templates/
│   ├── index.html      # Main storytelling page
│   └── dashboard.html  # Parental dashboard page
├── .env                # Environment variables (API keys)
├── requirements.txt    # Python dependencies
└── README.md
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd magicquest
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. **Configure your API key:**
   Create a `.env` file in the root directory and add your Google API key:
   ```
   GOOGLE_API_KEY="your_google_api_key_here"
   ```
4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Open your browser** and navigate to `http://localhost:8000`.

## How It Works

1. A child asks a question on the main page.
2. The FastAPI backend sends the question to the Google Gemini Pro model.
3. The model generates a story, a learning point, and a relevant badge.
4. The story is displayed to the child, and the interaction is logged.
5. Parents can visit the `/dashboard` page to see a summary of all interactions and badges earned.

## Technologies Used

- **Backend**: FastAPI, Uvicorn
- **AI Model**: Google Gemini Pro
- **Data Validation**: Pydantic
- **Frontend**: Jinja2, TailwindCSS, Vanilla JavaScript
- **Environment**: Python 3.9+

## Contributing

Feel free to submit issues and enhancement requests!
