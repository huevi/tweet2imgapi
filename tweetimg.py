import asyncio
from pyppeteer import launch
import os
from PIL import Image
import numpy as np
import requests
import json

# import uvloop


# file_name="new_tweet.html"
# file_path=os.path.dirname(os.path.realpath(file_name))+f"/{file_name}"

async def asyc_screenshot(file_name):
    file_path=os.path.abspath(f"./data/{file_name}.html")
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080, 'deviceScaleFactor' :2})
    await page.goto(f"file:{file_path}",({ "waitUntil": 'networkidle0' }))

    await page.screenshot({'path': f'./data/{file_name}.png','fullPage':'true','omitBackground': 'true'})
    await browser.close()


def screenshot(file_name):
    asyncio.get_event_loop().run_until_complete(asyc_screenshot(file_name))
    # asyncio.run(asyc_screenshot(file_name)) 
# uvloop.install()
# asyncio.run(main())
    # pass
# call()

def get_tweet(tweet_url,file_name):
    oemb_tweet_api="https://publish.twitter.com/oembed?url="
    tweet_post=oemb_tweet_api+tweet_url+"&theme=dark"
    page=requests.get(tweet_post)
    html_string=json.loads(page.text)["html"]
    with open (f"./data/{file_name}.html","w") as file:
        file.write(html_string)
        
def autocrop(file_name):
    img_path = f"./data/{file_name}.png"
    image=Image.open(img_path)
    image.load()
    image_data = np.asarray(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
    new_image = Image.fromarray(image_data_new)
    new_image.save(f'./data/{file_name}_crop.png')
    return f'./data/{file_name}_crop.png'