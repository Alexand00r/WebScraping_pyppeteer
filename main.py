import asyncio
import csv
import time
from pyppeteer import launch


@asyncio.coroutine
async def process_page(hotel_code_row, browser):
    hotel_code_bytes = hotel_code_row[0].encode()
    hotel_code = hotel_code_bytes.decode()
    url = "https://ostrovok.ru/rooms/" + hotel_code

    page = await browser.newPage()
    await page.goto(url)
    elements = await page.xpath(
        "//a[contains(@class, 'zenroomspageperks-rating-info-total-value')]"
    )

    try:
        value = await page.evaluate('''(element) => element.text''', elements[0])
        result_text = hotel_code + "; " + value + "\n"
    except:
        result_text = hotel_code + "; " + "null\n"

    with open("code_with_rating_async.txt", "a", encoding='utf-8') as file:
        file.write(result_text)


async def main():
    browser = await launch()
    with open("maps_collection_async.csv", 'r', encoding="utf-8-sig") as fd:
        hotel_code_rows = csv.reader(fd)

        loop = asyncio.get_event_loop()
        tasks = [process_page(hotel_code_row, browser) for hotel_code_row in hotel_code_rows]
        print("Here we go!")
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
