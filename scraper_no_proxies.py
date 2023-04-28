import asyncio
from pyppeteer import launch

## Main declarations
h = "https://"
out = "out/output_no_proxies.txt"
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

##  Main
async def main():
    data = {}

    #   UI: General Start
    print("============================ Start =============================")

    parameters = {
        "head": get_headless_value(),
        "debug": get_debug_value(),
    }

    #   UI: Main Part Start
    print("============================= Main =============================")

    #   Mainloop
    for site in sites:
        if site not in data:
            if parameters["debug"]:
                print(f"→ Scraping site: {site}")

            #   Browser arguments
            browser_args = {}
            browser_args["args"] = []

            #   Scraping
            browser = await launch(headless=parameters["head"], **browser_args)
            try:
                page = await browser.newPage()
                await page.goto(h + site)
                current_data = await page.content()
                data[site] = current_data
                await page.close()

                # Success response
                if parameters['debug']:
                    print(f"    • Scraped site {site} successfully.")
            #   Error handling
            except Exception as e:
                print(f"    • Caught exception: {e}")
            #   End
            finally:
                await browser.close()
    
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
