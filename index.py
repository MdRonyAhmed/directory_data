import asyncio
from time import sleep
from playwright.async_api import async_playwright
import requests
from sympy import E


async def run(playwright):
    try:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=False)
        page = await browser.new_page()
        # Subscribe to "request" and "response" events.
        # page.on("request", lambda request: print(">>", request.method, request.url))
        # page.on("response", lambda response: print("<<", response.status, response.url))

        await page.goto("https://www.truevalue.com/storelocator")
        print('loading done--')
        sleep(6)

        element = await page.wait_for_selector('iframe[id="storelocator"]')
        frame = await element.content_frame()
        await frame.type('input[name="addressline"]', "newyork", delay=200)
        sleep(5)
        async with page.expect_response("**storelocator.truevalue.com/rest/locatorsearch**") as response_info:
            await frame.click('button[class="button-search SaveBTN"]')
        response = await response_info.value

        app_key = await frame.get_attribute('a[title="Send to Email"]', "data-url")
        app_key = app_key.split('appkey=', 1)
        app_key = app_key[1].split('&', 1)
        app_key = app_key[0]
        print(app_key)

        url_api = response.url
        print(url_api)

        payload = {"request": {"appkey": f"{app_key}", "formdata": {"geoip": "false", "dataview": "store_default", "limit": 40, "geolocs":{"geoloc": [{"addressline": "newyork", "country": "US", "latitude": 40.7127753, "longitude": -74.0059728, "state": "NY", "province": "", "city": "New York", "address1": "", "postalcode": ""}]}, "searchradius": "40|50|80", "stateonly": 1, "where": {"truevaluebranded": {"eq": "Branded"}, "excluded": {"distinctfrom": "1"}, "ecommurl": {"ne": ""}, "or": {"giftcard": {"eq": ""}, "tvpaint": {"eq": ""}, "creditcard": {"eq": ""}, "localad": {"eq": ""}, "ja": {"eq": ""}, "tvr": {"eq": ""}, "main_id": {"eq": ""}, "programcode": {"in": ""}}}, "false": "0"}}}
        
        headers = {
            'Content-Type': 'text/plain'
        }

        response = requests.request(
            "POST", url_api, headers=headers, data=payload)

        print(response.text)

        sleep(9999)
    except E:
        print(E)
        sleep(9999)
        # await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
