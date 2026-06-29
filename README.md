# tech_summary

Gemini API와 GitHub Actions를 활용해 매일 한국 시간 12시에 최신 IT 테크 트렌드를 이메일로 자동 발송하는 뉴스레터 봇입니다.

## 트러블슈팅

### 503 UNAVAILABLE - Gemini API 서버 과부하

**증상**: GitHub Actions 실행 중 아래 에러가 발생하며 뉴스레터가 누락됨

```
google.genai.errors.ServerError: 503 UNAVAILABLE
```

**원인**: Gemini API 서버의 일시적인 과부하

**해결**: `app.py`에 Exponential Backoff 재시도 로직 추가
- 503 에러 발생 시 최대 3회까지 자동 재시도
- 재시도 대기 시간: 30초 → 60초 → 120초
- 3회 모두 실패 시 Actions job 실패 처리