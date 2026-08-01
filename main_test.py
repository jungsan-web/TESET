import os
import requests
from bs4 import BeautifulSoup


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# 테스트 닉네임
NICKNAME = "doetlho"

BOARD_URL = "https://www.fmkorea.com/index.php?mid=stock"


if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL 없음")


headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def send_discord(message):
    requests.post(
        WEBHOOK_URL,
        json={
            "content": message
        }
    )


response = requests.get(
    BOARD_URL,
    headers=headers
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


# FMKorea 게시글 영역 확인
articles = soup.select(
    "li.li"
)


print(
    "게시글 개수:",
    len(articles)
)


found = False


for article in articles:

    title = article.select_one(
        ".title"
    )

    if not title:
        continue


    writer = article.select_one(
        ".author"
    )

    if not writer:
        continue


    writer_name = writer.get_text(
        strip=True
    )


    if writer_name == NICKNAME:

        link = title.get("href")

        if link.startswith("/"):
            link = (
                "https://www.fmkorea.com"
                + link
            )


        send_discord(
            f"""
🔔 FMKorea 새 글 발견

작성자 : {NICKNAME}
제목 : {title.text.strip()}

{link}
"""
        )

        found = True
        break



if not found:

    send_discord(
        f"현재 {NICKNAME} 작성 글 없음"
    )


print("FMKorea 확인 완료")
