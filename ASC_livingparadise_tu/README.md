# 생활낙원 프로젝트

생활낙원 프로젝트를 위한 파이선 장고 기반의 코드

## 기능

- 네이버 쇼핑에서 키워드를 기준으로 상위 첫번째 자사 제품 그리고 상위 3가지 경쟁사 제품 스크롤링
- 쿠팡 쇼핑에서 키워드를 기준으로 상위 첫번째 자사 제품 그리고 상위 3가지 경쟁사 제품 스크롤링
- 키워드 검색수 업데이트
- 각 크롤링 한제품의 가격 평점 정보 업데이트


## 사용법

```bash
$ pip install pipenv
$ pipenv install --dev
$ pipenv run python manage.py makemigrations
$ pipenv run python manage.py migrate
$ pipenv run python manage.py runserver
```
$ pipenv run pip freeze > requirements.txt  >> 프로젝트에 사용된 패키지 이름과 버전을 담아주는 명령어
$ pipenv run pip install -r requirements.txt  >> 프로젝트에 사용된 패키지 설치 (현재없는 패키지만 빠르게 설치됨)
관리자 개정을 생성하기 위한 명령어

```bash
$ pipenv run python manage.py createsuperuser
```

콘솔에서 등록된 잡을 실행 시키는 명령어

```bash
$ pipenv run python manage.py count_beans 100
$ pipenv run python manage.py count_beans_threaded 100
```

## 환경변수

공통 환경 변수 `ENVIRONMENT` 에 할당가능한 세가지 형태의 개발 환경 설정 `DEVELOPMENT`, `STAGING`, `PRODUCTION`.

```
ENVIRONMENT='DEVELOPMENT'
DJANGO_SECRET_KEY='dont-tell-eve'
DJANGO_DEBUG='yes'
```

다음 변수는 staging과 production에서먼 사용

```
DJANGO_SESSION_COOKIE_SECURE='yes'
DJANGO_SECURE_BROWSER_XSS_FILTER='yes'
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF='yes'
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS='yes'
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SECURE_REDIRECT_EXEMPT=''
DJANGO_SECURE_SSL_HOST=''
DJANGO_SECURE_SSL_REDIRECT='yes'
DJANGO_SECURE_PROXY_SSL_HEADER='HTTP_X_FORWARDED_PROTO,https'
```

## 배포

어떤 클라우드 서버나 자체 서버에서 배포 가능합니다.


## License

The MIT License (MIT)

Copyright (c) 2012-2017 José Padilla

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
