import os
import json
import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# 테스트할 닉네임
NICKNAME = "doetlho"

# FMKorea 주식 게시판
SEARCH_URL = (
    "https://www.fmkorea.com/search.php"
    "?mid=stock"
    "&search_target=nick_name"
    f"&search_keyword={NICKNAME}"
)


if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL이 설정되지 않았습니다.")


headers = {
    "User-Agent": "Mozilla/5.0"
}


response = requests.get(
    SEARCH_URL,
    headers=headers
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


# 검색 결과 첫 번째 글 확인
post = soup.select_one(
    "table.bd_lst tbody tr"
)


if post:

    title = post.select_one(
        ".title a"
    ).text.strip()

    link = post.select_one(
        ".title a"
    )["href"]

    message = f"""
🔔 FMKorea 새 글 발견

작성자 : {NICKNAME}
제목 : {title}

https://www.fmkorea.com{link}
"""

else:

    message = (
        f"현재 {NICKNAME} 님의 새 글이 없습니다."
    )


requests.post(
    WEBHOOK_URL,
    json={
        "content": message
    }
)


print(message)
