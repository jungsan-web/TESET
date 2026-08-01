import os
import requests
from playwright.sync_api import sync_playwright


WEBHOOK_URL = os.getenv("WEBHOOK_URL")


BOARD_URL = "https://www.fmkorea.com/index.php?mid=stock"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        user_agent=(
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
        )
    )


    page.goto(
        BOARD_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )


    page.wait_for_timeout(5000)


    print("====================")
    print("페이지 제목")
    print(page.title())
    print("====================")


    # 화면에 표시되는 텍스트 출력
    text = page.locator("body").inner_text()


    print(text[:3000])


    browser.close()
