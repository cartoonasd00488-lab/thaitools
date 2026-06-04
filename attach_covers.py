import json, urllib.request

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'
BASE = 'https://cartoonasd00488-lab.github.io/thaitools'

updates = [
    ('hVi9IV0OqNpF8RlFEAEzAA==', 'Prompt Pack 50+ สูตรใช้ AI ทำงาน',
     'https://raw.githubusercontent.com/cartoonasd00488-lab/thaitools/main/assets/covers/prompt-pack.png'),
    ('ULR_k1q00sYbwsMhREdgDQ==', 'คู่มือเริ่มต้นใช้ AI สำหรับคนไทย (E-book)',
     'https://raw.githubusercontent.com/cartoonasd00488-lab/thaitools/main/assets/covers/ebook.png'),
    ('t2YGHAsEnRsv1MhI-tkKmQ==', 'Notion Template จัดการงานด้วย AI',
     'https://raw.githubusercontent.com/cartoonasd00488-lab/thaitools/main/assets/covers/notion-template.png'),
]

for pid, name, cover_url in updates:
    body = json.dumps({
        'access_token': TOKEN,
        'name': name,
        'preview_url': cover_url
    }).encode()
    req = urllib.request.Request(
        f'https://api.gumroad.com/v2/products/{pid}',
        data=body, headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
        method='PUT'
    )
    resp = urllib.request.urlopen(req, timeout=20)
    result = json.loads(resp.read())
    if result.get('success'):
        print(f'  ✅ {name}')
        print(f'     Cover: {cover_url}')
    else:
        print(f'  ❌ {name}: {result}')

print('\n✅ เสร็จสิ้น!')
