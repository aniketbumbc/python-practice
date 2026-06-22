from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates= Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse,include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=True)
def home():
    return f"<h1>{'hello how are you? '} </h1>"



@app.get("/home/template",include_in_schema=True)
def home(request:Request):
    return templates.TemplateResponse(request, "home.html")