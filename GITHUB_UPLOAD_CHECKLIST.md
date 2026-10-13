# GitHub 업로드 전 체크리스트

## 프로젝트 루트에 둘 파일
- README.md
- .gitignore
- requirements.txt

## GitHub에 올려도 되는 파일
- Python 소스 코드
- 합성(Mock) 입력 데이터
- 정답 CSV
- standards.json (테스트용 모의 기준값)
- README.md

## 올리지 않는 파일
- __pycache__/
- .venv/, venv/
- .env
- 실제 기관 내부자료
- 개인정보/민감정보
- 생성된 output/*.xlsx

## requirements 설치

```powershell
python -m pip install -r requirements.txt
```

## Ollama는 pip 패키지가 아님

별도로 설치해야 합니다.

사용 모델:

```powershell
ollama pull qwen2.5:3b
```

설치 확인:

```powershell
ollama --version
```

## Git 기본 명령 예시

```powershell
git init
git add .
git status
git commit -m "Initial commit: AI soil analysis automation prototype"
```

그 다음 GitHub에서 새 저장소를 만든 뒤 GitHub가 안내하는 remote 명령을 연결합니다.
