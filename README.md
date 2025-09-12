## 2025 AnA SSF - 나만의 싸이월드 만들기

### 소개
2000년대 감성을 담은 소셜 네트워크 서비스 '싸이월드'를 직접 구현해보는 프로젝트입니다.
사진 업로드, 미니홈피, 도토리, 방명록 등 주요 기능들을 구현했습니다.

### 기술 스택
 - 프론트엔드 : Qwik-city, Tailwind CSS
 - 백엔드 : FastAPI
 - 데이터베이스 : SQLite
 - 배포 : git

### 주요 기능
 - 회원가입 / 로그인
 - 프로필 사진 업로드 및 방 꾸미기
 - 방명록 작성
 - 도토리 상점

### 프로젝트 구조 
2025-SSF-Internal\
├── Backend\
│   ├── __init__.py\
│   ├── models\
│   ├── routes\
│   └── ...\
└── README.md

### 실행 방법
1. 프론트엔드\
git clone https://github.com/sunrin-ana/2025-SSF-Frontend.git \
npm install\
npm run

2. 백엔드\
git clone https://github.com/sunrin-ana/2025-SSF.git \
pip install -r requirements.txt\
uvicorn Backed:app --reload

### 개발 기간
2025-05-30 ~ 2025-09-12

### 팀원
장한울 - diary, ~~photo~~, ~~letter~~, store\
고윤 - avatar, room\
김건우 - user, friendship\
김주영 - dotory-manage server, frontend

### 참고자료
싸이월드 미니홈피 소개
