from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles         # use to serve static files. Remember to install `aiofiles` first
from fastapi.templating import Jinja2Templates      # use to render HTML templates. Remember to install `jinja2` first
from fastapi.responses import HTMLResponse
from search_util import search_collocation

# create app
app = FastAPI()

# publish static files on server. `directory` should be the path to your static files folder
# name is used for template access
app.mount("/static", StaticFiles(directory="static/css"), name="static")

# set up template path. `directory` should be the path where you place templates
templates = Jinja2Templates(directory="templates")

# --- HTML template sample --- #
# `response_class` and `Request` object is required for HTML rendering
@app.get("/show-html", response_class=HTMLResponse)
async def renderHTML(request: Request, word: str, limit: int = None):
    results = search_collocation(word, limit)

    # render template. Specify data you need in jinja template in the second dict. 
    # "request" is necessary for template rendering
    return templates.TemplateResponse("index.html", {"request": request, "word": word, "results": results})

# --- pure API sample --- #
@app.get("/search")
async def search(word: str, limit: int = None):
    return search_collocation(word, limit)

# --- sanity check --- #
@app.get("/")
async def health_check():
    return {}
