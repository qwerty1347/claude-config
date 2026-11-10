# 사내 체크리스트 docx 서식(assets/checklist_template.docx)을 복사해 반영여부·사유 칸만 채운다
# 사용: python checklist.py <rows.json> <서비스명> <출력.docx>
# rows.json: 49개 [["Y", ""], ["N/A", "랜딩페이지에서 처리"], ...] — 1-1~1-22, 2-1~2-27 순서
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', 'pylib')
sys.path.insert(0, LIB)
try:
    from docx import Document
except ImportError:  # 처음 한 번만 스킬 폴더 안에 설치 (전역 site-packages 안 건드림)
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '--target', LIB, 'python-docx'], check=True)
    import importlib
    importlib.invalidate_caches()  # 설치 전 없던 pylib 경로가 import 캐시에 '없음'으로 남아 있음
    from docx import Document

TEMPLATE = os.path.join(HERE, '..', 'assets', 'checklist_template.docx')
TEMPLATE_NAME = '꾹AI:Designer'  # 템플릿 제목에 들어 있는 원래 서비스명


def set_text(cell, text):
    p = cell.paragraphs[0]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ''
    else:
        p.add_run(text)


rows_path, service, out = sys.argv[1:4]
rows = json.load(open(rows_path, encoding='utf-8'))
assert len(rows) == 49, f'49개여야 함: {len(rows)}'
doc = Document(TEMPLATE)
for p in doc.paragraphs:
    for r in p.runs:
        r.text = r.text.replace(TEMPLATE_NAME, service)
table = doc.tables[0]
assert len(table.rows) == 50, len(table.rows)
for row, (yn, why) in zip(table.rows[1:], rows):
    set_text(row.cells[3], yn)
    set_text(row.cells[4], why)
doc.save(out)
print('OK', out)
