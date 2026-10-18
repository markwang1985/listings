#!/usr/bin/env python3
"""重新產生物件列表首頁 index.html：掃描每個物件資料夾的 index.html，抓標題、租金、格局等資訊。
新增物件後在 repo 根目錄執行：python3 build_index.py"""
import re, json, os, subprocess, html

ROOT = os.path.dirname(os.path.abspath(__file__))
def strip(x): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', (x or '').replace('<small>', ' ').replace('</small>', ' '))).strip()
items = []
for d in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, d, 'index.html')
    if not os.path.isfile(p):
        continue
    s = open(p, encoding='utf-8').read()
    g = lambda pat: (re.search(pat, s, re.S) or [None, ''])[1]
    title = g(r'<title>(.*?)</title>')
    name = re.sub(r'^出租｜|・月租.*$', '', title)
    loc = strip(g(r'<div class="loc">.*?</span>(.*?)</div>'))
    city_dist, _, area = loc.partition('｜')
    stats = re.findall(r'<div class="stat[^"]*"><b>(.*?)</b><span>(.*?)</span>', s)
    dep = strip(g(r'<p class="dep">(.*?)</p>'))
    date = subprocess.run(['git', 'log', '--diff-filter=A', '--format=%cs', '--', f'{d}/index.html'], cwd=ROOT, capture_output=True, text=True).stdout.strip().split('\n')[-1] or ''
    items.append({
        'slug': d, 'name': name, 'district': city_dist.replace('台中市', ''), 'area': area,
        'rent': int(g(r'<div class="price">.*?<b>(.*?)</b>').replace(',', '') or 0),
        'size': strip(stats[0][0]) if stats else '', 'sizeLabel': strip(stats[0][1]) if stats else '',
        'layout': strip(stats[1][0]) if len(stats) > 1 else '', 'floor': strip(stats[2][1]).replace('樓層／', strip(stats[2][0]).replace(' ', '') + '／') if len(stats) > 2 else '',
        'dep': dep, 'date': date,
        'cover': next((f'{d}/img/{f}' for f in ('cover.jpg', 'living.jpg') if os.path.isfile(os.path.join(ROOT, d, 'img', f))), f'{d}/og-image.jpg'),
    })
items.sort(key=lambda x: x['date'], reverse=True)
data = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
tpl = open(os.path.join(ROOT, 'index.template.html'), encoding='utf-8').read()
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(tpl.replace('/*DATA*/[]', data))
print(len(items), 'items:', ', '.join(i['slug'] for i in items))
