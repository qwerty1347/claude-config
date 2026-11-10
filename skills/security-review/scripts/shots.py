# 코드 발췌를 HTML 로 그려 Chrome/Edge headless 로 PNG 저장 (보안성 검토 근거 스크린샷)
# 사용: python shots.py <spec.json> <출력폴더>
# spec.json: [{"item": "2-6", "caption": "설명", "shown": "표시 경로", "path": "실제 파일 경로",
#              "start": 1, "end": 20, "highlight": [5, 6] 또는 "부분문자열|부분문자열"}]
import html, json, os, subprocess, sys, tempfile
from collections import Counter

# 파일명 = "<항목번호> <체크리스트 docx 상세항목 요약>-<순번>" (예: 2-6 타 이용자 권한 도용 방지-1). 내용 설명은 caption 에.
TITLES = {
    '1-1': '규정검토', '1-2': '개인정보 수집 동의 절차', '1-3': '개인정보 파기 및 보존 정책',
    '1-4': '개인정보보호 책임자 지정', '1-5': '주민번호 미수집', '1-6': '만14세 아동 법정대리인 동의',
    '1-7': '개인정보 제3자 제공 위탁 절차', '1-8': '위탁 및 제3자 제공 동의', '1-9': '개인정보처리방침 공개',
    '1-10': '이용약관 동의 및 공개', '1-11': '취급위탁 사항 공개', '1-12': '계약서 보안 의무조항',
    '1-13': '외부 사용자 접근통제 및 권한제한', '1-14': '업무정의 및 직무분리',
    '1-15': '정보의 조회 출력 다운로드 업무별 접근통제', '1-16': '계정 생성 변경 삭제 규칙',
    '1-17': '전산자료 관리책임자 지정', '1-18': '계정관리자 지정', '1-19': '슈퍼 계정관리자 지정',
    '1-20': '가용성 확보조치', '1-21': '백업관리 정책', '1-22': '장애 예방 및 성능 모니터링',
    '2-1': '비밀번호 입력 마스킹', '2-2': '개인정보 조회 출력 마스킹', '2-3': '회원DB 탈퇴DB 분리',
    '2-4': '주민번호 외 본인확인', '2-5': '권한상승 방지', '2-6': '타 이용자 권한 도용 방지',
    '2-7': 'API 악용 방지', '2-8': '메모리 보호', '2-9': '중요정보 화면 미표시', '2-10': '프로그램 무결성 검증',
    '2-11': '입력정보 위변조 보호', '2-12': 'SQL 인젝션 방지', '2-13': 'XSS 방지', '2-14': '다중세션 취약점 방지',
    '2-15': '업로드 취약점 방지', '2-16': '역분석 방지', '2-17': '안전한 알고리즘 암호화',
    '2-18': '인증정보 개인정보 송수신 암호화', '2-19': '이용자 비밀번호 실패 확인 조치',
    '2-20': '이용자 패스워드 복잡도', '2-21': '본인확인 후 비밀번호 변경', '2-22': '비밀번호 재사용 금지',
    '2-23': '사용자 비밀번호 실패 접근통제', '2-24': '사용자 비밀번호 복잡도', '2-25': '계정 접속기록 자동생성',
    '2-26': '개인정보 처리내역 이용내역 기록', '2-27': '이용자 정보 조회 시 자동 기록',
}
assert len(TITLES) == 49

BROWSERS = [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']
BROWSER = next((b for b in BROWSERS if os.path.exists(b)), None)

CSS = """
body{margin:0;background:#1e1e1e;font-family:'D2Coding','Consolas','Malgun Gothic',monospace;}
.cap{background:#2d2d30;color:#ffd866;padding:10px 16px;font:600 14px 'Malgun Gothic',sans-serif;}
.path{background:#252526;color:#9cdcfe;padding:6px 16px;font-size:13px;border-bottom:1px solid #3c3c3c}
table{border-collapse:collapse;width:100%;font-size:14px;line-height:21px}
td{padding:0 12px;white-space:pre;color:#d4d4d4;vertical-align:top}
td.n{color:#858585;text-align:right;width:44px;border-right:1px solid #3c3c3c}
tr.hl td{background:#5a1d1d}
tr.hl td.n{color:#ff8080}
"""


def render(s, out, tmp):
    lines = open(s['path'], encoding='utf-8').read().split('\n')
    a, b, hl = s['start'], min(s['end'], len(lines)), s.get('highlight', [])
    rows = []
    for no in range(a, b + 1):
        t = lines[no - 1]
        on = any(k in t for k in hl.split('|')) if isinstance(hl, str) else no in hl
        rows.append(f'<tr class="{"hl" if on else ""}"><td class="n">{no}</td><td>{html.escape(t) or " "}</td></tr>')
    src = os.path.join(tmp, 'shot.html')
    open(src, 'w', encoding='utf-8').write(
        f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
        f'<div class="cap">{html.escape(s["caption"])}</div><div class="path">{html.escape(s["shown"])}</div>'
        f'<table>{"".join(rows)}</table></body></html>')
    width = max(900, min(1500, 140 + 8 * max(len(lines[i - 1]) for i in range(a, b + 1))))
    height = 80 + 21 * (b - a + 1) + 12
    png = os.path.join(out, s['name'] + '.png')
    subprocess.run([BROWSER, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1.5',
                    f'--window-size={width},{height}', f'--screenshot={png}', 'file:///' + src.replace('\\', '/')],
                   check=True, capture_output=True)
    assert os.path.getsize(png) > 1000, png
    print('OK', s['name'])


if __name__ == '__main__':
    assert BROWSER, 'Chrome/Edge 를 찾지 못함'
    spec, out = json.load(open(sys.argv[1], encoding='utf-8')), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        seq = Counter()
        for s in spec:
            seq[s['item']] += 1
            s['name'] = f"{s['item']} {TITLES[s['item']]}-{seq[s['item']]}"
            render(s, out, tmp)
