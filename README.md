# jhwanseok.github.io

## 로컬 개발 환경 실행

### 요구 사항

- Node.js >= 22.12.0 (`package.json`의 `engines` 기준)

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

기본적으로 `http://localhost:4321`에서 개발 서버가 실행됩니다.

### 빌드 및 프리뷰

```bash
npm run build    # dist/ 에 정적 사이트 빌드
npm run preview  # 빌드된 결과물을 로컬에서 미리보기
```

### 기타 명령어

```bash
npm run astro -- <command>  # Astro CLI 명령어 직접 실행 (예: npm run astro -- check)
```