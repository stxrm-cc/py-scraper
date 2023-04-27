import asyncio
from pyppeteer import launch
import websockets

##  Helpers
h = "https://"
sites = [
    "amazon.fr"
]
user_answers = {
    "y": True,
    "yes": True,
    "t": True,
    "true": True,
    "n": False,
    "no": False,
    "f": False,
    "false": False
}

# directories = {
#     'proxies': 'proxies.txt'
# }

def get_headless_value():
    while True:
        answer = input("Do you want to run the browser in headless mode? (y/n):\n-> ").lower()
        if answer in user_answers:
            return user_answers[answer]
        print("Invalid input. Please enter y/n.")

##  Main
async def main():
    data = []
    #   Other browser paremeters
    browser_args = {
        'args': []
    }

    #   Mainloop
    browser = await launch(headless=get_headless_value(), **browser_args)
    try:
        ws_url = browser.wsEndpoint
        async with websockets.connect(ws_url) as ws:
            for site in sites:
                page = await browser.newPage()
                await page.goto(h + site)
                current_data = await page.content()
                data.append([site, current_data])
                await page.close()
    #   Error handling
    except Exception as e:
        print(e)
    #   End
    finally:
        await browser.close()
        
    return data

#   to prevent execution from other files since im gonna import this file as a module probably
if __name__ == "__main__":
    data = asyncio.get_event_loop().run_until_complete(main())
    print(data)