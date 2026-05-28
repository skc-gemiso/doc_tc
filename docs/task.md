# 문서 변환 모듈(Task Worker) 개발 작업 계획서

## 1. 프로젝트 개요

외부 API 서버에서 문서 변환 요청을 수행하면,
Python 기반 문서 변환 모듈이 호출되어 다음 작업을 수행한다.

- 문서 → PDF 변환
- PDF 썸네일 생성
- PDF 카탈로그 이미지 생성
- Callback URL 호출

본 프로젝트는 REST API 서버 자체를 개발하는 것이 아니라,
독립 실행 가능한 문서 변환 처리 모듈(Task Worker) 개발을 목표로 한다.

---

# 2. 개발 범위

## 포함 범위

- 문서 파일 읽기
- PDF 변환
- 썸네일 이미지 생성
- 전체 페이지 이미지 생성
- Callback URL 호출
- 작업 로그 저장
- 예외 처리

---

## 제외 범위

- REST API 서버 개발
- 사용자 인증
- 웹 UI 개발
- 파일 업로드 서버 개발
- DB 서버 개발

---

# 3. 지원 포맷

## 입력 가능 문서

- doc
- docx
- xls
- xlsx
- ppt
- pptx
- odt
- ods
- odp
- txt
- csv
- rtf
- html
- pdf

---

# 4. 시스템 처리 구조

## 전체 흐름

```text
외부 API 서버
    ↓
Python 변환 모듈 호출
    ↓
PDF 생성
    ↓
Thumbnail 생성
    ↓
Catalog 생성
    ↓
Callback URL 호출
```

---

# 5. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python 3.12 |
| PDF 변환 | LibreOffice Headless |
| PDF 렌더링 | PyMuPDF |
| 이미지 처리 | Pillow |
| HTTP 통신 | requests |
| 운영 OS | Rocky Linux |

---

# 6. 모듈 호출 방식

## Python 함수 호출

```python
from converter import run

run(task)
```

---

## CLI 실행 방식

```bash
python main.py task.json
```

---

# 7. Task 데이터 구조

## Request 예시

```json
{
    "taskId": 1,
    "srcPath": "/srcPath/src.ext",
    "isThumbNail": true,
    "isCatalog": true,
    "width": 700,
    "height": 500,
    "tarPath": "/tarPath/tar.pdf",
    "callBack": "https://callback.url"
}
```

---

# 8. Request 항목 정의

| 필드명 | 타입 | 필수 | 설명 |
|---|---|---|---|
| taskId | Integer | O | 작업 ID |
| srcPath | String | O | 원본 파일 경로 |
| isThumbNail | Boolean | X | 썸네일 생성 여부 |
| isCatalog | Boolean | X | 카탈로그 생성 여부 |
| width | Integer | X | 썸네일 가로 크기 |
| height | Integer | X | 썸네일 세로 크기 |
| tarPath | String | O | PDF 저장 경로 |
| callBack | String | O | Callback URL |

---

# 9. 파일 생성 규칙

## 입력 파일

```text
/app/input/PPT/test.pptx
```

---

## PDF 생성

```text
/app/output/PPT/test.pdf
```

---

## 썸네일 생성

생성 조건:

```text
isThumbNail = true
```

생성 경로:

```text
/app/output/PPT/Thumbnail/thumb_test.jpg
```

---

## 카탈로그 생성

생성 조건:

```text
isCatalog = true
```

생성 경로:

```text
/app/output/PPT/Catalog/1.jpg
/app/output/PPT/Catalog/2.jpg
/app/output/PPT/Catalog/3.jpg
```

---

# 10. 내부 처리 프로세스

## Step 1. 입력 데이터 검증

검사 항목:

- srcPath 존재 여부
- 파일 확장자
- tarPath 경로
- callback URL 유효성

---

## Step 2. PDF 변환

LibreOffice Headless 사용

실행 예시:

```bash
libreoffice \
--headless \
--convert-to pdf \
source.docx \
--outdir /output
```

---

## Step 3. Thumbnail 생성

조건:

```text
isThumbNail = true
```

처리:

- PDF 첫 페이지 렌더링
- width / height 적용
- JPG 저장

---

## Step 4. Catalog 생성

조건:

```text
isCatalog = true
```

처리:

- PDF 전체 페이지 렌더링
- 페이지별 JPG 저장

---

# 11. Callback 처리

## Callback 호출 시점

모든 작업 완료 후 호출한다.

---

## Callback Request 예시

```json
{
    "result": true,
    "message": "success",
    "data": {
        "taskId": 1,
        "filePath": "/app/output/PPT/test.pdf",
        "imgPath": "/app/output/PPT/Thumbnail/thumb_test.jpg",
        "catalogImgPath": "/app/output/PPT/Catalog/",
        "pageCount": 12
    }
}
```

---

## 실패 Callback 예시

```json
{
    "result": false,
    "message": "convert failed",
    "data": {
        "taskId": 1
    }
}
```

---

# 12. 디렉토리 구조

```text
converter/

├── main.py
├── models/
│   └── task.py
├── services/
│   ├── office_converter.py
│   ├── thumbnail_service.py
│   ├── catalog_service.py
│   └── callback_service.py
├── utils/
│   ├── file_utils.py
│   └── logger.py
├── temp/
└── logs/
```

---

# 13. 권장 클래스 구조

## Task 모델

```python
class ConvertTask:
    taskId: int
    srcPath: str
    tarPath: str
    isThumbNail: bool
    isCatalog: bool
    width: int
    height: int
    callBack: str
```

---

## 메인 처리 클래스

```python
class DocumentConverter:

    def run(self, task):

        pdf_path = convert_to_pdf(task)

        if task.isThumbNail:
            create_thumbnail(pdf_path)

        if task.isCatalog:
            create_catalog(pdf_path)

        send_callback(task)
```

---

# 14. 이미지 생성 정책

## Thumbnail

- 첫 페이지 기준 생성
- JPG 저장
- width / height 적용

---

## Catalog

- 전체 페이지 생성
- 페이지 번호 기준 파일명 생성

예시:

```text
1.jpg
2.jpg
3.jpg
```

---

# 15. 성능 고려사항

## 예상 처리 시간

| 작업 | 예상 시간 |
|---|---|
| DOCX → PDF | 1~3초 |
| XLSX → PDF | 3~10초 |
| PPTX → PDF | 10~60초 |
| PDF → JPG | 페이지당 0.2~1초 |

---

# 16. LibreOffice 충돌 방지

동시 실행 시 충돌 방지를 위해
Worker별 User Profile 분리 사용 권장

예시:

```bash
-env:UserInstallation=file:///tmp/worker_001
```

---

# 17. 예외 처리 정책

## 처리 대상

- 파일 없음
- 변환 실패
- PDF 생성 실패
- 이미지 생성 실패
- Callback 실패
- Timeout 발생

---

## Callback 실패 정책

- Retry 3회
- Timeout 10초

---

# 18. 로그 정책

## 저장 로그

- 작업 시작
- PDF 생성 완료
- Thumbnail 생성 완료
- Catalog 생성 완료
- Callback 결과
- 작업 종료

---

## 로그 예시

```text
[INFO] TASK START : 1001
[INFO] PDF CREATED
[INFO] THUMB CREATED
[INFO] CATALOG CREATED
[INFO] CALLBACK SUCCESS
[INFO] TASK END
```

---

# 19. 보안 정책

## 파일 검증

- 확장자 검사
- MIME 검사
- 파일 크기 제한

---

## 권장 사항

- 악성 파일 검사
- ClamAV 연동 검토

---

# 20. 최종 목표

본 시스템은 Linux 환경에서 안정적으로:

- 문서를 PDF로 변환하고
- 썸네일 이미지를 생성하며
- 카탈로그 이미지를 생성하고
- 작업 완료 후 Callback URL을 호출하는

독립 실행형 문서 변환 모듈 개발을 목표로 한다.
