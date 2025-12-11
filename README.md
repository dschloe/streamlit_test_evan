# uv 환경 설정
- uv 설치 링크

## 프로젝트 초기화
- uv 프로젝트 초기화
```
uv init
uv run python -v
```

## 라이브러리 설치
- requirements.txt
- (추후) requirements-dev.txt
- 라이브러리 설치 명령어
```
uv add $(cat requirements.txt) # MacOS
uv add (Get-Content requirements.txt) # Windows

uv add --dev $(cat requirements-dev.txt) # MacOS
uv add --dev (Get-Content requirements-dev.txt) # Windows
```