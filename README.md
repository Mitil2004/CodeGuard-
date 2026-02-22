CodeGuard 🛡️ | AI-Powered SEC-OPS Intelligence

CodeGuard is a professional-grade automated security auditing platform designed to identify critical vulnerabilities in source code using Large Language Models (LLMs). By implementing a "Shift Left" security approach, CodeGuard allows developers to catch logic flaws, backdoors, and OWASP Top 10 vulnerabilities during the development phase rather than after deployment.

🚀 Key Features

Heuristic AI Audits: Powered by Gemini 2.5 Flash to understand code logic, not just syntax.

SEC-OPS Dashboard: High-contrast, terminal-inspired interface with dark/light mode support.

Persistent History: Integrated MongoDB Atlas archive for tracking security audits over time.

Professional Exports: Generate and download cryptographically "signed" PDF security certificates.

Real-time Connectivity: Live "Heartbeat" monitoring for backend health status.

Responsive Design: Fully optimized for mobile and desktop security reviews.

🛠️ Technical Stack

Backend

Framework: Python 3.12 (FastAPI)

Engine: Google Gemini 2.5 Flash

Database: MongoDB Atlas (NoSQL)

Async Driver: Motor (Non-blocking I/O)

Frontend

Library: React.js (Vite)

Styling: Tailwind CSS

Iconography: Lucide-React

Utilities: React-Markdown, jsPDF

🏗️ Architecture & Workflow

Input: User submits source code via the React terminal.

Analysis: FastAPI receives the payload and executes a prompt-engineered request to the Gemini 2.5 engine.

Persistence: The audit result is simultaneously stored in MongoDB and returned to the client.

Rendering: The UI renders the report using a recursive typing effect and provides a PDF export option.

🚦 Local Setup Instructions

1. Prerequisites

Python 3.11+

Node.js & npm

Google AI Studio API Key

MongoDB Atlas Cluster

2. Backend Setup

cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt


Create a .env file in the backend folder:

GEMINI_API_KEY=your_gemini_api_key
MONGODB_URL=your_mongodb_atlas_url


Run the API:

uvicorn main:app --reload


3. Frontend Setup

cd backend/frontend
npm install
npm run dev


🌐 Deployment Configuration

Backend (Render)

Root Directory: backend

Build Command: pip install -r requirements.txt

Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Frontend (Vercel)

Root Directory: backend/frontend

Framework Preset: Vite

Environment Variable: VITE_API_URL (Point to your Render URL)

🛡️ Security Acknowledgements

This tool is intended for educational and internal audit purposes. While the AI engine is highly sophisticated, it should be used alongside traditional Static Application Security Testing (SAST) and manual code review for production environments.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
