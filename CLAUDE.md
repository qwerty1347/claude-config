# 전역 지침

## 에이전트·스킬 변경 기록

에이전트·스킬·플러그인을 추가·삭제·수정하면(에이전트의 `skills:` 변경, 플러그인 켜기·끄기 포함) 같은 작업 안에서 `D:\projects\claude-config` 를 갱신하고 커밋까지 한다.

1. `powershell -ExecutionPolicy Bypass -File D:\projects\claude-config\export.ps1` 실행 (agents·skills·이 CLAUDE.md 복사)
2. 플러그인을 바꿨으면 `plugins.ps1` 의 목록도 고친다.
3. `README.md` 의 표(에이전트·스킬·플러그인)를 현재 상태에 맞게 고친다.
4. 「변경 이력」 **맨 위**에 한 줄 추가: `- [YYYY-MM-DD] 무엇을 설치·삭제·변경했는지 — 바뀐 파일 경로`
   - 에이전트·스킬·플러그인 자체의 변경만 적는다. 이 문서·repo·규칙 관리 같은 메타 작업은 적지 않는다.
5. 커밋한다(계정 규칙은 아래). 커밋 메시지는 이력에 적은 한 줄을 그대로 쓴다. push 는 요청받을 때만 한다.

대상: `~/.claude/agents`, `~/.claude/skills`(harness junction), 플러그인. 프로젝트 `.claude/` 안의 에이전트·스킬은 대상이 아니다.

## claude-config 저장소 커밋 계정

`D:\projects\claude-config` 의 git 커밋은 **항상 `qwertys1347` 계정**(`qwertys1347@gmail.com`)으로 한다.
- 커밋 전에 `git -C D:\projects\claude-config config user.email` 이 `qwertys1347@gmail.com` 인지 확인하고, 아니면 커밋하지 말고 알린다.
- 전역 git 설정(`--global`)은 바꾸지 않는다. 다르게 해야 하면 이 저장소의 로컬 설정만 쓴다.
