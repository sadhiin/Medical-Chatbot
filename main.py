from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# importing cros origin resource
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["chat_bot"],
    allow_headers=["*"],
)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={'message': 'Hello World!'}, media_type="text/html"
    )

@app.post('/api/chat')
async def chat_bot():
    return {"bot": "Hello World"}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=2)