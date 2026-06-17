import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google import genai
from datetime import datetime

# 1. 환경 변수 로드 (GitHub Secrets 사용 전제)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD") # Gmail 앱 비밀번호
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def generate_newsletter():
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # 실행 시점의 현재 날짜와 시각을 가져옵니다.
    now = datetime.now()
    today_str = now.strftime('%Y년 %m월 %d일 %H:%M')

    prompt = f"""
    현재 시점은 {today_str}입니다. 당신은 실리콘밸리의 탑티어 테크 인사이더이자 냉철한 기술 분석가입니다. 
    반드시 실시간 검색을 통해, **정확히 지난 24시간 전(어제 이 시간)부터 현재({today_str})까지** 글로벌 개발자 생태계(GitHub Trending, Hacker News, Product Hunt, Reddit)에서 가장 뜨겁게 논의되고 있는 최신 IT 기술 및 오픈소스 트렌드를 분석해 뉴스레터 형태로 작성해 주세요.

    [필수 제약 조건]
    1. 분석 범위: 반드시 지난 24시간 이내의 데이터만 포함하세요. 그 이전의 오래된 뉴스는 제외하세요.
    2. 메일 전용 포맷: 인사말 없이 곧바로 [제목]부터 출력하세요.
    3. 무조건적인 솔직함: 기술의 한계점과 단점을 냉정하게 지적하세요.
    4. 가독성: 마크다운 문법을 활용하여 볼드 가공과 줄바꿈을 확실히 하세요.
    5. 기준 일시 명시: 제목에 분석 기준 시점({today_str})을 포함하세요.

    [출력 양식]
    제목: 🚀 [Tech Pulse] {today_str} 기준 지난 24시간 테크 리포트
    ---
    ### 짚고 넘어가야 할 최신 기술 3선
    ■ 1. [기술명] (요약, 활용처, 장점, 단점)
    ■ 2. [기술명]
    ■ 3. [기술명]
    ---
    ### 핵심 인프라 및 언어 업데이트
    ■ 4. 메이저 배포 소식 (1~2개)
    ---
    ### 5초 테크 지식 충전
    ■ 5. 오늘의 테크 용어 사전
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text

def send_email(content):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = f"🚀 [Tech Pulse] {datetime.now().strftime('%Y-%m-%d')} 테크 트렌드 리포트"
    
    msg.attach(MIMEText(content, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    if not all([GEMINI_API_KEY, GMAIL_USER, GMAIL_PASSWORD, RECIPIENT_EMAIL]):
        print("Error: Missing environment variables.")
    else:
        newsletter_content = generate_newsletter()
        send_email(newsletter_content)
