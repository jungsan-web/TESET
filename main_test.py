import os
import requests
from bs4 import BeautifulSoup
import urllib.parse


WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# 테스트 닉네임
NICKNAME = "doetlho"

# FMKorea 주식 게시판
BOARD_URL = "https://www.fmkorea.com/index.php?mid=stock"


if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL이 없습니다.")


headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_discord(message):
    requests.post(
        WEBHOOK_URL,
        json={
            "content": message
        }
    )


# 게시판 가져오기
response = requests.get(
    BOARD_URL,
    headers=headers
)

response.encoding = "utf-8"

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


posts = soup.select(
    "table.bd_lst tbody tr"
)


found = False


for post in posts:

    # 제목
    title_tag = post.select_one(
        ".title a"
    )

    if not title_tag:
        continue


    title = title_tag.text.strip()

    link = title_tag.get("href")


    # 작성자
    writer = post.select_one(
        ".author"
    )


    if not writer:
        continue


    writer_name = writer.text.strip()


    if writer_name == NICKNAME:

        found = True


        if link.startswith("/"):
            link = "https://www.fmkorea.com" + link


        message = f"""
🔔 FMKorea 새 글 발견

작성자 : {NICKNAME}
제목 : {title}

{link}
"""


        send_discord(message)

        break



if not found:

    send_discord(
        f"현재 {NICKNAME} 작성 글 없음"
    )


print("확인 완료")
