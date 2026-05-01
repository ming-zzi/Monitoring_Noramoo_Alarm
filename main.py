import requests
from bs4 import BeautifulSoup
import os

# 환경 변수에서 정보 가져오기 (보안)
TG_TOKEN = os.environ.get("8626248654:AAE1iQdxYuMyOhvGb-DacC4mzLqiqdsJAVY")
TG_CHAT_ID = os.environ.get("8311000374")
TARGET_URL = "https://www.fmkorea.com/search.php?mid=stock&category=&search_keyword=%EB%85%B8%EB%9D%BC%EB%AC%B4&search_target=nick_name"

def check_new_post():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # 검색 결과의 첫 번째 글 선택
        first_post = soup.select_one('ul.search_result_list li dl dt a')
        
        if not first_post: return
        
        title = first_post.text.strip()
        link = "https://www.fmkorea.com" + first_post['href']
        post_id = first_post['href'].split('document_srl=')[-1].split('&')[0]

        # 이전 글 ID 확인 (GitHub에 저장된 파일 읽기)
        last_id = ""
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                last_id = f.read().strip()

        if post_id != last_id:
            # 텔레그램 알림 전송
            msg = f"🚨 노라무 새 글 발견!\n\n제목: {title}\n링크: {link}"
            send_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={msg}"
            requests.get(send_url)
            
            # 새로운 ID 저장
            with open("last_id.txt", "w") as f:
                f.write(post_id)
            return True
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    if check_new_post():
        print("New post found and notified!")
    else:
        print("No new posts.")
