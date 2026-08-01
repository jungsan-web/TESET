import os
import requests
from playwright.sync_api import sync_playwright


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# 테스트 닉네임
NICKNAME = "doetlho"

BOARD_URL = "https://www.fmkorea.com/index.php?mid=stock"


if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL 없음")


def send_discord(message):
    requests.post(
        WEBHOOK_URL,
        json={
            "content": message
        }
    )


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page(
        viewport={
            "width": 1280,
            "height": 2000
        },
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    )


    print("FMKorea 접속 시작")


    page.goto(
        BOARD_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )


    page.wait_for_timeout(5000)


    print(
        "페이지 제목:",
        page.title()
    )


    # 게시글 영역 확인
    rows = page.locator(
        "table.bd_lst tbody tr"
    )


    count = rows.count()


    print(
        "게시글 수:",
        count
    )


    found = False


    for i in range(count):

        row = rows.nth(i)

        text = row.inner_text()


        if NICKNAME in text:

            title = row.locator(
                ".title a"
            ).inner_text()


            link = row.locator(
                ".title a"
            ).get_attribute(
                "href"
            )


            if link.startswith("/"):
                link = (
                    "https://www.fmkorea.com"
                    + link
                )


            send_discord(
                f"""
🔔 FMKorea 새 글 발견

작성자 : {NICKNAME}
제목 : {title}

{link}
"""
            )


            found = True
            break


    browser.close()



if not found:

    send_discord(
        f"현재 {NICKNAME} 작성 글 없음"
    )


print("확인 완료")
