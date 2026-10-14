# 부산보건고등학교 교사 AI 업무 심화 연수

무료 계정 중심의 120분 연수용 정적 웹사이트입니다. AI 업무 선택, NotebookLM 공개 자료 검색과 인용 확인, 공식·사용자 제작 스킬, 근거를 담은 문서 작업 요청, Word/PPT/Excel 실습을 제공합니다.

## 배포

GitHub Pages: `main` 브랜치 `/docs` 폴더. 외부 AI API나 키를 사용하지 않습니다. 사이트 입력은 브라우저에서만 처리되며 제출 서버가 없습니다. 학습 체크 상태만 localStorage에 저장됩니다.

## 자료

`docs/references/`: 공식 공개 자료와 검색용 변환본. 원문 URL, 적용일, 수집일, 파일 해시는 공개 자료 목록에 기록합니다. 학교 원본 공개 자료와 법령·교육청 지침을 구분하고 최신본 여부는 원문에서 재확인합니다. 학교 내부 자료·개인 학생 자료는 포함하지 않습니다.

`docs/assets/notebook/`: 로그인된 실제 서비스에서 공개 자료로 진행한 NotebookLM 실습 캡처. 사이트에 표시한 기준일의 화면이며, 실제 도구 UI와 기능은 변경될 수 있습니다.

`docs/downloads/`: 공개 자료 묶음, 가상 예산 CSV 등.

## 디자인

OpenDesign 공식 사이트의 밝은 작업 공간 구성과 [Clean 디자인 시스템](https://github.com/nexu-io/open-design/blob/main/design-systems/clean/DESIGN.md)을 참고해 독립적인 HTML/CSS로 제작했습니다. OpenDesign 로고·제품 화면·소스 코드는 복제하지 않았습니다.

## 검증

`scripts/check-site.cjs`: 링크/파일 존재, 자료 목록, JS 구문 검사.
`scripts/serve.cjs`: 로컬 개발 HTTP 서버. 기본 포트 4173.
`artifacts/`: 배포 및 화면 검증 증거(커밋하지 않음).

라이선스: 직접 제작한 사이트 코드 MIT. 외부 스킬 및 공공 자료의 이용 조건은 각 원문을 따릅니다. 공식 스킬 원문을 이 저장소에 재배포하지 않습니다.
