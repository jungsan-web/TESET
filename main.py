import os
import requests

# GitHub Secret에서 Discord Webhook 주소 가져오기
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not WEBHOOK_URL:
    raise Exception("WEBHOOK_URL이 설정되지 않았습니다.")

# Discord로 테스트 메시지 전송
response = requests.post(
    WEBHOOK_URL,
    json={
        "content": "✅ FMKorea 알림 봇 연결 테스트 성공!"
    }
)

print(response.status_code)
print("메시지 전송 완료")
