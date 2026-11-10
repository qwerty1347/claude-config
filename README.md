# claude-config

Claude Code 전역 설정(에이전트·스킬·플러그인·전역 CLAUDE.md)을 여러 PC 에서 똑같이 쓰기 위한 저장소. 이 repo 가 원본이다.

## 새 PC 적용

1. Claude Code 설치·로그인
2. `git clone https://github.com/qwerty1347/claude-config.git` (어디에 받아도 된다)
3. `powershell -ExecutionPolicy Bypass -File .\sync.ps1`
4. Claude Code 재시작 → `/agents`, `/skills`, `/plugin` 으로 확인

`sync.ps1` 이 하는 일 (몇 번 실행해도 같은 결과):
- `~/.claude/agents`, `~/.claude/skills` → 이 repo 의 `agents/`, `skills/` 로 junction. 기존 폴더는 `*.bak-<시각>` 으로 남기고, 기존 링크는 링크만 지운다(링크가 가리키던 폴더는 그대로).
- `CLAUDE.md` → `~/.claude/CLAUDE.md` 로 복사(내용이 다르면 기존 것을 `.bak-<시각>` 으로 백업). Windows 는 파일 심볼릭 링크에 관리자 권한이 필요해 복사로 한다.
- repo 위치를 `~/.claude/claude-config-path.txt` 에 기록하고, 이 repo 의 로컬 git `user.email` 을 `qwertys1347@gmail.com` 으로 설정.
- 플러그인(user 범위)을 `$plugins` 목록과 맞춘다: 없으면 설치, 꺼져 있으면 켜기, 목록에 없으면 **끄기**(삭제하지 않음). project·local 범위 플러그인은 건드리지 않는다.

## PC 간 동기화

- 다른 PC 에서 바꾼 것을 받을 때: `git pull` → `sync.ps1` → Claude Code 재시작
  - 에이전트·스킬은 junction 이라 pull 만으로 반영된다. sync 는 CLAUDE.md·플러그인 때문에 돌린다.
- 이 PC 에서 바꿀 때: 먼저 `git pull` → 변경 → README 표·변경 이력 → 커밋 → push
  - 에이전트·스킬은 `~/.claude/...` 에서 고쳐도 repo 가 바뀐다(junction).
  - 전역 지침은 repo 의 `CLAUDE.md` 를 고치고 `sync.ps1`.
  - 플러그인은 `sync.ps1` 의 `$plugins` 를 고치고 `sync.ps1`.
  - 전역 `CLAUDE.md` 에 이 절차가 규칙으로 들어 있어 Claude 가 따른다.
- 두 PC 에서 pull 없이 각각 바꾸면 충돌이 난다. 바꾸기 전에 pull.

### 새 PC 에서 다르게 동작하는 것

| 대상 | 이유 | 결과·대처 |
|---|---|---|
| `api-doc` 스킬 | 명세서를 이 repo 의 `docs/skills/api-doc/output` 에 모은다(`.gitignore` 로 커밋 제외) | PC 마다 따로 쌓인다. 다른 PC 의 명세서는 넘어오지 않는다 |
| `security-review` 스킬 | 동봉된 `pylib/lxml` 이 Python 3.12(win_amd64) 전용 빌드 | 3.12 가 아니면 첫 실행 때 `pylib/` 에 python-docx 를 다시 설치한다(네트워크 필요) |
| `ui-ux-pro-max` 플러그인 | 검색 스크립트가 Python 3 필요 | Python 이 없으면 검색이 안 된다 |
| `web-design-guidelines` 스킬 | 실행마다 GitHub 에서 규칙을 받아온다 | GitHub 가 막힌 망에서는 실패한다 |
| 플러그인 설치(`sync.ps1`) | GitHub 마켓플레이스에서 받는다 | GitHub 가 막힌 망에서는 실패한다 |

동기화하지 않는 것: 로그인 정보, 허용 규칙(`settings.local.json`), 메모리, Orca 훅·statusLine(Orca 설치 시 Orca 가 넣는다), 프로젝트 스킬(`project-skills/` 에서 복사).

## 구성

| 경로 | 내용 |
|---|---|
| `agents/` | 전역 에이전트 (`~/.claude/agents` 가 여기로 junction) |
| `skills/` | 전역 스킬 (`~/.claude/skills` 가 여기로 junction) |
| `CLAUDE.md` | 전역 지침 원본 (`~/.claude/CLAUDE.md` 로 복사) |
| `project-skills/` | 프로젝트에 복사해 쓰는 스킬 원본 (설치 안 함) |
| `sync.ps1` | 위 연결·복사 + 플러그인 목록(`$plugins`, `$marketplaces`)과 맞추기 |

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

외부 스킬은 자동 업데이트되지 않는다. 원본 repo 를 다시 받아 `skills/<이름>` 을 덮어쓴 뒤 커밋.

## 프로젝트 스킬 (`project-skills/`, 전역 설치 안 함)

`sync.ps1` 은 이 폴더를 설치하지 않는다. 필요한 프로젝트의 `.claude/skills/` 에 직접 복사해 쓴다.
전역에 두지 않는 이유: 같은 이름의 프로젝트 스킬(프로젝트별 메모가 붙은 것)과 겹치지 않게 하려고.

### fastapi

- 출처: FastAPI 공식 스킬(SKILL.md + `references/` 6개: dependencies, other-tools, path-operations, pydantic, responses, streaming). 원본은 `C:\xampp\htdocs\www\projects\claude-admin\.claude\skills\fastapi`.
- 쓰는 법: `project-skills/fastapi` 를 FastAPI 프로젝트의 `.claude/skills/fastapi` 로 복사.
- 프로젝트마다 버전·폐쇄망 같은 제약이 다르면 SKILL.md 맨 아래에 「이 프로젝트에서 쓸 때 — 로컬 추가 메모」를 덧붙인다(공식 원문보다 우선). 예: ai-wish(폐쇄망, uv·ruff 금지, wheel 은 `pip-packages/`), domeggook-ax md_approval(0.115.12, PyMySQL 동기·`def`).
- `fastapi-developer` 에이전트가 이 스킬을 미리 로드한다. 프로젝트에 없으면 스킬 없이 동작한다.
- 갱신: 새 공식판을 받으면 이 폴더를 직접 덮어쓰고 커밋한다.

## 플러그인 (`sync.ps1` 의 `$plugins`)

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

- [2026-11-10] api-doc 명세서 출력 위치 harness → claude-config `docs/`(gitignore), 플러그인 frontend-design·ui-ux-pro-max 를 user 범위로 설치 — `skills/api-doc/`, `sync.ps1`
- [2026-11-10] 프로젝트 스킬 원본 추가: fastapi (공식판, claude-admin 에서 복사, 전역 설치 안 함) — `project-skills/fastapi`
- [2026-11-10] ui-designer 본문 재작성, `skills:` 에 frontend-design·emil-design-eng — `agents/ui-designer.md`
- [2026-11-10] 플러그인 켬: frontend-design, ui-ux-pro-max — `sync.ps1`
- [2026-11-10] 스킬 설치: emil-design-eng, web-design-guidelines (hallmark 는 설치 후 삭제) — `skills/`
- [2026-10-29] 스킬 제작: security-review — `skills/security-review`
- [2026-10-22] 플러그인 설치: ponytail 5.3.2 — `sync.ps1`
- [2026-10-12] 스킬 제작: agent-review — `skills/agent-review`
- [2026-10-12] fastapi-developer 본문 재작성, `skills: fastapi` — `agents/fastapi-developer.md`
- [2026-10-06] VoltAgent 에이전트 27개 설치(원본 그대로) — `agents/`
- [2026-10-01] 스킬 제작: autoprompt, excalidraw-diagram-generator — `skills/`
- [2026-10-01] 플러그인 설치: ui-ux-pro-max, skill-creator — `sync.ps1`
- [2026-09-30] 플러그인 설치: frontend-design, playwright(현재 꺼짐) — `sync.ps1`
- [2026-08-21] 에이전트 제작: legacy-analyzer, refactoring-strategist, refactoring-engineer, modernization-reviewer — `agents/`
- [2026-08-04] 스킬 제작: api-doc — `skills/api-doc`
