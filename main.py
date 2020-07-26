from typing import Optional
from fastapi import FastAPI
import tweetimg
import urllib.parse
from fastapi.responses import HTMLResponse,FileResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/tweet/")
async def read_tweeturl(q: Optional[str] = None):
    url_ = urllib.parse.unquote(q)
    file_name = "tweet"
    tweetimg.get_tweet(url_,file_name)
    await tweetimg.asyc_screenshot(file_name)
    path = tweetimg.autocrop(file_name)
    # return { "q": q, "tweet_url_path": path}
    return FileResponse(path)