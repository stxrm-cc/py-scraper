import asyncio
from pyppeteer import launch
import websockets

## Main declarations
h = "https://"
out = "out/output.txt"
sites = [
    "amazon.fr",
    "ebay.de"
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
directories = {
    "proxies": "resources/proxies.txt"
}

##  Helpers
def get_headless_value():
    while True:
        answer = input("Do you want to run the browser in headless mode? (y/n):\n→ ").lower()
        if answer in user_answers:
            return user_answers[answer]
        print("Invalid input. Please enter y/n.")

def get_debug_value():
    while True:
        answer = input("Debug? (y/n):\n→ ").lower()
        if answer in user_answers:
            return user_answers[answer]
        print("Invalid input. Please enter y/n.")

def get_proxy_credentials(proxy):
    #   Arbitrary 
    parts = proxy.split("@")
    if len(parts) == 2:
        #   Converting to tuple for formatting
        return tuple(parts[0].split(":"))
    return None

##  Main
async def main():
    data = {}
    idx = 1 # Proxy ID

    #   UI: General Start
    print("============================ Start =============================")

    parameters = {
        "head": get_headless_value(),
        "debug": get_debug_value(),
    }
    #   Parsing proxies
    with open(directories["proxies"]) as f:
        proxies = f.read().splitlines()

    #   UI: Main Part Start
    print("============================= Main =============================")

    #   Mainloop
    for proxy in proxies:
        if len(data) != len(sites):
            credentials = get_proxy_credentials(proxy)
            #   Browser arguments for proxy use
            browser_args = {}
            if credentials:
                #   Authentication
                browser_args["args"] = [
                    f"--proxy-server={proxy}",
                    f"--proxy-auth={credentials[0]}:{credentials[1]}"
                ]
            else:
                browser_args["args"] = [
                    f"--proxy-server={proxy}"
                ]
            #   Scraping
            browser = await launch(headless=parameters["head"], **browser_args)
            
            try:
                ws_url = browser.wsEndpoint # Documentation: https://pptr.dev/ for func details
                                            # else https://github.com/pyppeteer/pyppeteer for python version
                #   Debug
                if parameters["debug"]:
                    print(f"→ Trying proxy {idx}: {proxy}")
                    
                async with websockets.connect(ws_url) as ws:
                    for site in sites:
                        if not (site in data):
                            print(f"  • Attempting to scrape: {site}")
                            page = await browser.newPage()
                            await page.goto(h + site)
                            current_data = await page.content()
                            data[site] = current_data
                            await page.close()

                    # Proxy success response
                    if parameters['debug']:
                        print(f"    • Proxy {proxy} was succesful.")
            #   Error handling
            except Exception as e:
                print(f"    • Caught exception: {e}")
            #   End
            finally:
                await browser.close()
            
            idx += 1
    
    return data

#   to prevent execution from other files since im gonna import this file as a module probably
if __name__ == "__main__":
    data = asyncio.get_event_loop().run_until_complete(main())
    # print(f"Data output:\n {data}\n", len(data)) -- Deprecated and annoying to read in console

    #   Write data to file
    with open(out, "w") as file:
        file.write(str(data))

    #   UI: End
    print("============================= Done =============================")

    print(f"→ Data has been exported to directory '../{out}'.")
    input("/!\ Scraping has finished. Press Enter to exit...    ")