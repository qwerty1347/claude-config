# 전역 지침

## 프론트엔드 UI 작업

- **프론트엔드 UI 작업은 기존 디자인 토큰·컴포넌트를 따른다.**
  - 일반 수정(스타일·문구·작은 컴포넌트 변경)은 메인 세션에서 `frontend-design` 스킬 기준으로 한다.
  - 새 화면·새 컴포넌트 작성, 화면 단위 개편만 `ui-designer` 에이전트(Agent 도구, `subagent_type: "ui-designer"`)에 맡긴다.
  - MR 전 UI 검토는 `web-design-guidelines` 스킬로 한다.
  - 색·폰트·전체 스타일을 새로 정할 때는 `ui-ux-pro-max` 를 직접 호출한다.

## 에이전트·스킬 변경 기록

에이전트·스킬·플러그인을 추가·삭제·수정하면(에이전트의 `skills:` 변경, 플러그인 켜기·끄기 포함) 같은 작업 안에서 claude-config repo 를 갱신하고 커밋까지 한다.

**repo 위치**: `~/.claude/claude-config-path.txt` 에 적힌 경로(`import.ps1` 이 기록한다). 파일이 없으면 `D:\projects\claude-config`. 둘 다 없으면 작업하지 말고 알린다. 아래 `<repo>` 는 이 경로다.

1. `powershell -ExecutionPolicy Bypass -File <repo>\export.ps1` 실행 (agents·skills·이 CLAUDE.md 복사)
2. 플러그인을 바꿨으면 `plugins.ps1` 의 목록도 고친다.
3. `README.md` 의 표(에이전트·스킬·플러그인)를 현재 상태에 맞게 고친다.
4. 「변경 이력」 **맨 위**에 한 줄 추가: `- [YYYY-MM-DD] 무엇을 설치·삭제·변경했는지 — 바뀐 파일 경로`
   - 에이전트·스킬·플러그인 자체의 변경만 적는다. 이 문서·repo·규칙 관리 같은 메타 작업은 적지 않는다.
5. 커밋한다(계정 규칙은 아래). 커밋 메시지는 이력에 적은 한 줄을 그대로 쓴다. push 는 요청받을 때만 한다.

대상: `~/.claude/agents`, `~/.claude/skills`(PC 에 따라 다른 repo 로의 junction 일 수 있다), 플러그인. 프로젝트 `.claude/` 안의 에이전트·스킬은 대상이 아니다.
repo 의 `project-skills/`(프로젝트에 복사해 쓰는 스킬 원본, 예: fastapi)는 export 대상이 아니므로 직접 갱신하고 README 「프로젝트 스킬」에 적는다.

## claude-config 저장소 커밋 계정

claude-config repo(`<repo>`)의 git 커밋은 **항상 `qwertys1347` 계정**(`qwertys1347@gmail.com`)으로 한다.
- 커밋 전에 `git -C <repo> config user.email` 이 `qwertys1347@gmail.com` 인지 확인하고, 아니면 커밋하지 말고 알린다.
- 전역 git 설정(`--global`)은 바꾸지 않는다. 다르게 해야 하면 이 저장소의 로컬 설정만 쓴다.
