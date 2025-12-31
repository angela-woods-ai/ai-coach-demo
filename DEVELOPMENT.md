# Development Guide

## Clone & Install
git clone https://github.com/angela-woods-ai/ai-coach-demo.git
cd ai-coach-mvp
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Node & UI Requirements

This project includes two JavaScript layers:

- **Node.js API** (Express / middleware layer)
- **Next.js UI** (React frontend)

### Required versions
- **Node.js**: `>= 20.9.0`
- **npm**: `>= 9.x`

> Next.js requires Node 20+.  
> If you see `EBADENGINE` warnings, upgrade Node before continuing.

### Recommended setup (macOS)
- nvm install 20
- nvm use 20
- cd node
- npm install
- cd web
- npm install

Your **Node API layer** should already contain these in `package.json`:

```json
{
  "dependencies": {
    "express": "^4.19.0",
    "cors": "^2.8.5",
    "dotenv": "^16.4.0",
    "node-fetch": "^3.3.2"
  },
  "devDependencies": {
    "typescript": "^5.x",
    "ts-node": "^10.x",
    "nodemon": "^3.x"
  },
  "scripts": {
    "dev": "nodemon src/server.ts"
  }
}
```

Your **UI layer** (created via create-next-app) already includes everything required:
```json
{
  "dependencies": {
    "next": "^14.x",
    "react": "^18.x",
    "react-dom": "^18.x"
  }
}
```

## Environment Setup
- Copy .env.example to .env
- Set USE_PINECONE and/or USE_CLAUDE true (optional), if true, you must also set PINECONE_API_KEY and ANTHROPIC_API_KEY to your own API keys

## Project Structure
- /ai          → Python FastAPI coaching engine
- /node        → NodeJS API
- /web         → NextJS frontend

## Run the test harness (AI layer only from command line)
- python -m ai.test_driver

## Run the full demo

### Terminal1 (FASTAPI AI Layer)
- source .venv/bin/activate
- uvicorn ai.app:app --reload
- (optional) Test calls via swagger http://127.0.0.1:8000/docs

### Terminal2 (NodeJS)
- source .venv/bin/activate
- cd node
- npm run dev
- NodeJS should now be running on http://localhost:3001
- (optional) Test health from a Terminal with: curl http://localhost:3001/api/health 

### Terminal3 (NextJS UI)
- source .venv/bin/activate
- cd web
- npm run dev
- Access the web UI at http://localhost:3000/

### Demo Sequence
Submit these user reflections one at a time in the web UI
- Work deadlines have been overwhelming lately.
- Deadlines make it hard for me to relax, even after hours.
- I’ve been enjoying learning new technical skills.
- Even though work is stressful, learning helps me feel grounded.
Try your own reflections!

### Shutdown
- CTRL+C in each terminal window
   

