import requests
from bs4 import BeautifulSoup
import os

# 환경 변수 설정 확인
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
TARGET_URL = "https://www.fmkorea.com/search.php?mid=stock&category=&search_keyword=%EB%85%B8%EB%9D%BC%EB%AC%B4&search_target=nick_name"

def check_new_post():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        first_post = soup.select_one('ul.search_result_list li dl dt a')
        
        if not first_post:
            print("게시글 없음")
            return False
        
        title = first_post.text.strip()
        link = "https://www.fmkorea.com" + first_post['href']

        # [테스트 모드] ID 비교 없이 무조건 메시지 전송
        msg = f"🔔 테스트 알림입니다!\n\n제목: {title}\n링크: {link}"
        send_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={msg}"
        
        response = requests.get(send_url)
        print(f"텔레그램 응답: {response.status_code}") # 200이 나오면 성공
        return True
            
    except Exception as e:
        print(f"에러 발생: {e}")
    return False

if __name__ == "__main__":
    check_new_post()
