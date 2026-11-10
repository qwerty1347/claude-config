# Claude Code 에이전트·스킬 정리

기준일: 2026-11-10
설치 위치: `C:\Users\gng\.claude\agents` (에이전트), `C:\Users\gng\.claude\skills` (스킬)
원본: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) (같은 폴더의 html 이 저장해 둔 페이지)

## 1. 에이전트 (33개)

### 원본에서 바꾼 것 → `변경된 에이전트/`

| 에이전트 | 수정일 | 바꾼 내용 |
|---|---|---|
| `ui-designer` | 2026-11-10 | 본문 174줄 → 30줄. 없는 context-manager JSON 프로토콜 제거, "기존 토큰·컴포넌트 먼저 읽기 → 스킬 적용(프로젝트 디자인 우선) → 상태·접근성·반응형 → 짧게 보고"로 교체. `skills:` 에 `frontend-design:frontend-design`, `emil-design-eng` 미리 로드 |
| `fastapi-developer` | 2026-10-12 | 본문 287줄 → 32줄. 공식 FastAPI 문서 우선·기억 대신 확인. `skills:` 에 `fastapi` 미리 로드 |

- `fastapi` 스킬은 전역이 아니라 프로젝트 스킬(ai-wish, domeggook-ax 의 `.claude/skills/fastapi`)이다. 다른 곳에서 부르면 미리 로드가 건너뛰어진다.
- `skills:` 는 YAML 리스트로 써야 한다. `skills: a, b` 쉼표 형식은 인식되지 않았다(2026-11-10 실측).

### 원본 그대로 (27개)

agent-installer, agent-organizer, ai-writing-auditor, api-documenter, architect-reviewer, code-reviewer, context-manager, dependency-manager, deployment-engineer, docker-expert, error-coordinator, knowledge-synthesizer, memory-curator, microservices-architect, multi-agent-coordinator, performance-engineer, performance-monitor, prompt-engineer, qa-expert, readme-generator, refactoring-specialist, security-auditor, task-distributor, test-automator, ui-ux-tester, webhook-engineer, workflow-orchestrator

## 2. 전역 스킬

### `~/.claude/skills` (harness repo)

| 스킬 | 출처 | 비고 |
|---|---|---|
| agent-review | 직접 제작 | MR 전 code-reviewer·security-auditor·ui-ux-tester 병렬 실행 |
| api-doc | 직접 제작 | Laravel API 명세서 HTML |
| autoprompt | 직접 제작 | 요청을 프롬프트로 다듬기 |
| excalidraw-diagram-generator | 직접 제작 | Excalidraw 다이어그램 |
| security-review | 직접 제작 | ISMS 49개 항목 보안성 검토 |
| emil-design-eng | [emilkowalski/skill](https://github.com/emilkowalski/skill) (MIT) | 인터랙션·애니메이션·컴포넌트 다듬기. harness `.gitignore` 처리 |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (MIT) | UI 검토, 실행마다 GitHub 에서 규칙을 받아옴. `.gitignore` 처리 |

- 외부 스킬 2개는 자동 업데이트되지 않는다. 갱신하려면 repo 를 다시 받아 폴더를 덮어쓴다.
- hallmark 는 설치했다가 2026-11-10 삭제.

### 플러그인 (`~/.claude/settings.json` 의 `enabledPlugins`)

| 플러그인 | 포함 스킬 | 용도 |
|---|---|---|
| frontend-design (Anthropic 공식) | frontend-design | 일반 UI 작업 기준 |
| ui-ux-pro-max (MIT) | ui-ux-pro-max, banner-design, brand, design, design-system, slides, ui-styling | 색·폰트·스타일 정할 때 직접 호출 (`search.py --design-system`, Python 필요) |
| skill-creator | skill-creator | 스킬 제작 |
| ponytail | ponytail, -audit, -debt, -gain, -help, -review | 최소 변경 모드 |

설치만 되고 꺼진 플러그인: playwright

## 3. UI 작업 규칙 (ai-wish, domeggook-ax CLAUDE.md)

- 기존 디자인 토큰·컴포넌트를 따른다.
- 일반 수정은 메인 세션에서 `frontend-design` 스킬 기준.
- 새 화면·새 컴포넌트·화면 단위 개편만 `ui-designer` 에이전트.
- MR 전 UI 검토는 `web-design-guidelines`.

## 변경 이력

> 2026-11-10 이전 항목은 파일 수정일·`installed_plugins.json` 의 `installedAt`·harness git 이력으로 복원했다(실제 작업일과 하루 이틀 다를 수 있다).

- [2026-08-04] 스킬 제작: api-doc — `~/.claude/skills\api-doc`
- [2026-09-30] 플러그인 설치: frontend-design, playwright (claude-plugins-official) — `~/.claude/plugins`
- [2026-10-01] 플러그인 설치: ui-ux-pro-max (nextlevelbuilder 마켓플레이스 추가), skill-creator — `~/.claude/plugins`, `~/.claude/settings.json`
- [2026-10-01] 스킬 제작: autoprompt, excalidraw-diagram-generator — `~/.claude/skills\`
- [2026-10-06] VoltAgent 에이전트 27개 설치(원본 그대로) — `~/.claude/agents\`
- [2026-10-12] 스킬 제작: agent-review — `~/.claude/skills\agent-review`
- [2026-10-12] fastapi-developer 본문 재작성, `skills: fastapi` 미리 로드 — `변경된 에이전트\fastapi-developer.md`
- [2026-10-22] 플러그인 설치: ponytail 5.3.2 — `~/.claude/plugins`, `~/.claude/settings.json`
- [2026-10-29] 스킬 제작: security-review — `~/.claude/skills\security-review`
- [2026-11-10] 스킬 설치: emil-design-eng, web-design-guidelines (harness `.gitignore` 처리), hallmark 설치 후 삭제 — `~/.claude/skills\`
- [2026-11-10] 플러그인 켬: frontend-design, ui-ux-pro-max — `~/.claude/settings.json`
- [2026-11-10] ui-designer 본문 30줄로 재작성, `skills:` 에 frontend-design·emil-design-eng 미리 로드 — `변경된 에이전트\ui-designer.md`
- [2026-11-10] 전역 `~/.claude/CLAUDE.md` 생성(이 문서 갱신 규칙)
- [2026-11-10] 폴더 이름 변경 `D:\projects\에이전트` → `D:\projects\claude-config`, 커밋 계정 규칙(qwertys1347) 추가 — `~/.claude/CLAUDE.md`
