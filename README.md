# claude-config

이 PC 의 Claude Code 전역 설정(에이전트·스킬·플러그인·전역 CLAUDE.md)을 다른 PC 에 똑같이 옮기기 위한 저장소.

## 새 PC 적용

1. Claude Code 설치·로그인
2. `git clone https://github.com/qwerty1347/claude-config.git`
3. `powershell -ExecutionPolicy Bypass -File .\import.ps1`
   - `~/.claude` 의 `agents`, `skills`, `CLAUDE.md` 를 이 repo 내용으로 바꾼다. 기존 것은 `*.bak-<시각>` 으로 남는다.
   - 대상이 junction·심볼릭 링크면 건너뛴다(링크 너머 다른 repo 를 덮어쓰지 않도록).
   - repo 위치를 `~/.claude/claude-config-path.txt` 에 기록한다(전역 CLAUDE.md 의 기록 규칙이 이 경로를 쓴다). 어디에 clone 해도 된다.
   - 이 repo 의 로컬 git `user.email` 을 `qwertys1347@gmail.com` 으로 설정한다.
   - 이어서 `plugins.ps1` 로 플러그인을 설치한다.
4. Claude Code 재시작 → `/agents`, `/skills`, `/plugin` 으로 확인

업데이트: `git pull` 후 3번부터 다시.

## 이 PC 에서 바꾼 뒤

`powershell -ExecutionPolicy Bypass -File .\export.ps1` → 아래 표·변경 이력 갱신 → 커밋.
(전역 `~/.claude/CLAUDE.md` 에 이 절차가 규칙으로 적혀 있다.)

## 구성

| 경로 | 내용 |
|---|---|
| `agents/` | `~/.claude/agents` 전체 |
| `skills/` | `~/.claude/skills` 전체 (`synced`, `__pycache__` 제외) |
| `CLAUDE.md` | 전역 `~/.claude/CLAUDE.md` 복사본 |
| `project-skills/` | 프로젝트에 복사해 쓰는 스킬 원본 (전역 설치 안 함, export 대상 아님) |
| `plugins.ps1` | 플러그인·마켓플레이스 목록(설치 명령) |
| `export.ps1` / `import.ps1` | 이 PC → repo / repo → 새 PC |

## 에이전트 (33개)

### 원본에서 바꾼 것

원본: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

| 에이전트 | 바꾼 내용 |
|---|---|
| `ui-designer` | 본문 174줄 → 30줄(없는 context-manager 프로토콜 제거, 기존 토큰·컴포넌트 우선). `skills:` 에 `frontend-design:frontend-design`, `emil-design-eng` |
| `fastapi-developer` | 본문 287줄 → 32줄(공식 FastAPI 문서 우선). `skills:` 에 `fastapi` |

- `fastapi` 스킬은 전역이 아니라 프로젝트 스킬이라(아래 「프로젝트 스킬」) 그 프로젝트 밖에서는 미리 로드가 건너뛰어진다.
- `skills:` 는 YAML 리스트로 쓴다. `skills: a, b` 쉼표 형식은 인식되지 않았다.

### 직접 만든 것

리팩토링 파이프라인: `legacy-analyzer`(진단) → `refactoring-strategist`(전략) → `refactoring-engineer`(실행) → `modernization-reviewer`(검토)

### 원본 그대로 (27개)

agent-installer, agent-organizer, ai-writing-auditor, api-documenter, architect-reviewer, code-reviewer, context-manager, dependency-manager, deployment-engineer, docker-expert, error-coordinator, knowledge-synthesizer, memory-curator, microservices-architect, multi-agent-coordinator, performance-engineer, performance-monitor, prompt-engineer, qa-expert, readme-generator, refactoring-specialist, security-auditor, task-distributor, test-automator, ui-ux-tester, webhook-engineer, workflow-orchestrator

## 전역 스킬 (7개)

| 스킬 | 출처 | 용도 |
|---|---|---|
| agent-review | 직접 제작 | MR 전 code-reviewer·security-auditor·ui-ux-tester 병렬 실행 |
| api-doc | 직접 제작 | Laravel API 명세서 HTML |
| autoprompt | 직접 제작 | 요청을 프롬프트로 다듬기 |
| excalidraw-diagram-generator | 직접 제작 | Excalidraw 다이어그램 |
| security-review | 직접 제작 | ISMS 49개 항목 보안성 검토 (pylib 동봉) |
| emil-design-eng | [emilkowalski/skill](https://github.com/emilkowalski/skill) (MIT) | 인터랙션·애니메이션·컴포넌트 다듬기 |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT) | UI 검토, 실행마다 GitHub 에서 규칙을 받아옴 |

외부 스킬은 자동 업데이트되지 않는다. 원본 repo 를 다시 받아 `~/.claude/skills/<이름>` 을 덮어쓴 뒤 export.

## 프로젝트 스킬 (`project-skills/`, 전역 설치 안 함)

`import.ps1` 은 이 폴더를 설치하지 않는다. 필요한 프로젝트의 `.claude/skills/` 에 직접 복사해 쓴다.
전역에 두지 않는 이유: 같은 이름의 프로젝트 스킬(프로젝트별 메모가 붙은 것)과 겹치지 않게 하려고.

### fastapi

- 출처: FastAPI 공식 스킬(SKILL.md + `references/` 6개: dependencies, other-tools, path-operations, pydantic, responses, streaming). 원본은 `C:\xampp\htdocs\www\projects\claude-admin\.claude\skills\fastapi`.
- 쓰는 법: `project-skills/fastapi` 를 FastAPI 프로젝트의 `.claude/skills/fastapi` 로 복사.
- 프로젝트마다 버전·폐쇄망 같은 제약이 다르면 SKILL.md 맨 아래에 「이 프로젝트에서 쓸 때 — 로컬 추가 메모」를 덧붙인다(공식 원문보다 우선). 예: ai-wish(폐쇄망, uv·ruff 금지, wheel 은 `pip-packages/`), domeggook-ax md_approval(0.115.12, PyMySQL 동기·`def`).
- `fastapi-developer` 에이전트가 이 스킬을 미리 로드한다. 프로젝트에 없으면 스킬 없이 동작한다.
- 갱신: 새 공식판을 받으면 이 폴더를 직접 덮어쓰고 커밋한다(export 가 갱신하지 않는다).

## 플러그인 (`plugins.ps1`)

| 플러그인 | 포함 스킬 | 용도 |
|---|---|---|
| frontend-design (Anthropic 공식) | frontend-design | 일반 UI 작업 기준 |
| ui-ux-pro-max (MIT) | ui-ux-pro-max, banner-design, brand, design, design-system, slides, ui-styling | 색·폰트·스타일 정할 때 직접 호출 (Python 필요) |
| skill-creator | skill-creator | 스킬 제작 |
| ponytail | ponytail, -audit, -debt, -gain, -help, -review | 최소 변경 모드 |

## UI 작업 규칙

전역 `CLAUDE.md`(이 repo 의 `CLAUDE.md` 가 복사본)의 「프론트엔드 UI 작업」에 있다. 모든 프로젝트에 적용된다.

## 변경 이력

> 2026-11-10 이전 항목은 파일 수정일·플러그인 `installedAt`·git 이력으로 복원했다(실제 작업일과 하루 이틀 다를 수 있다).

- [2026-11-10] 프로젝트 스킬 원본 추가: fastapi (공식판, claude-admin 에서 복사, 전역 설치 안 함) — `project-skills/fastapi`
- [2026-11-10] ui-designer 본문 재작성, `skills:` 에 frontend-design·emil-design-eng — `agents/ui-designer.md`
- [2026-11-10] 플러그인 켬: frontend-design, ui-ux-pro-max — `plugins.ps1`
- [2026-11-10] 스킬 설치: emil-design-eng, web-design-guidelines (hallmark 는 설치 후 삭제) — `skills/`
- [2026-10-29] 스킬 제작: security-review — `skills/security-review`
- [2026-10-22] 플러그인 설치: ponytail 5.3.2 — `plugins.ps1`
- [2026-10-12] 스킬 제작: agent-review — `skills/agent-review`
- [2026-10-12] fastapi-developer 본문 재작성, `skills: fastapi` — `agents/fastapi-developer.md`
- [2026-10-06] VoltAgent 에이전트 27개 설치(원본 그대로) — `agents/`
- [2026-10-01] 스킬 제작: autoprompt, excalidraw-diagram-generator — `skills/`
- [2026-10-01] 플러그인 설치: ui-ux-pro-max, skill-creator — `plugins.ps1`
- [2026-09-30] 플러그인 설치: frontend-design, playwright(현재 꺼짐) — `plugins.ps1`
- [2026-08-21] 에이전트 제작: legacy-analyzer, refactoring-strategist, refactoring-engineer, modernization-reviewer — `agents/`
- [2026-08-04] 스킬 제작: api-doc — `skills/api-doc`
