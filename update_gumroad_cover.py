import urllib.request, json

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'
BASE_URL = 'https://cartoonasd00488-lab.github.io/thaitools'

products = [
    {
        'id': 'hVi9IV0OqNpF8RlFEAEzAA==',
        'name': 'Prompt Pack 50+ สูตรใช้ AI ทำงาน',
        'cover': BASE_URL + '/assets/covers/prompt-pack.svg',
        'desc': (
            '50+ Prompts สำเร็จรูป สำหรับ ChatGPT, Claude, Gemini\n\n'
            '🎯 หมวดหมู่:\n'
            '- งานเอกสารและเขียนเนื้อหา (5 prompts)\n'
            '- การตลาดและโซเชียลมีเดีย (5 prompts)\n'
            '- ไอเดียและวางแผน (5 prompts)\n'
            '- โค้ดดิ้งและการพัฒนา (5 prompts)\n'
            '- เทรนนิ่งและการเรียนรู้ (5 prompts)\n\n'
            '💡 เหมาะสำหรับ:\n'
            '✓ Content Creator\n'
            '✓ นักการตลาด\n'
            '✓ นักพัฒนา\n'
            '✓ นักเรียนนักศึกษา\n'
            '✓ เจ้าของธุรกิจ\n\n'
            'ภาษาไทย 100% ใช้กับทุก AI ได้ทันที\n'
            'เมื่อซื้อแล้วคุณจะได้รับไฟล์ PDF พร้อมใช้งาน'
        )
    },
    {
        'id': 'ULR_k1q00sYbwsMhREdgDQ==',
        'name': 'คู่มือเริ่มต้นใช้ AI สำหรับคนไทย (E-book)',
        'cover': BASE_URL + '/assets/covers/ebook.svg',
        'desc': (
            '📘 E-book สอนใช้ AI Tools ตั้งแต่เริ่มต้น จนถึงใช้งานจริงในชีวิตประจำวัน\n\n'
            '🎯 เหมาะสำหรับ:\n'
            '- คนที่ไม่เคยใช้ AI มาก่อน\n'
            '- อยากเริ่มใช้ AI แต่ไม่รู้จะเริ่มยังไง\n'
            '- อยากทำงานให้เร็วขึ้นด้วย AI\n\n'
            '📖 เนื้อหาภายในเล่ม:\n'
            '▶︎ AI คืออะไร? เข้าใจง่าย\n'
            '▶︎ แนะนำ ChatGPT, Claude, Gemini\n'
            '▶︎ วิธีเขียน Prompt อย่างมืออาชีพ\n'
            '▶︎ การประยุกต์ใช้ AI ในชีวิตประจำวัน\n'
            '▶︎ เคล็ดลับและเทคนิคขั้นสูง\n\n'
            'ภาษาไทย อ่านง่าย เข้าใจเร็ว\n'
            'ใช้ได้จริง 100%'
        )
    },
    {
        'id': 't2YGHAsEnRsv1MhI-tkKmQ==',
        'name': 'Notion Template จัดการงานด้วย AI',
        'cover': BASE_URL + '/assets/covers/notion-template.svg',
        'desc': (
            '📊 ระบบจัดการงานส่วนตัว + AI Assistant แบบ all-in-one\n\n'
            '🎯 เหมาะสำหรับ:\n'
            '- Freelancer\n'
            '- Content Creator\n'
            '- นักเรียน นักศึกษา\n'
            '- คนทำงานทั่วไป\n\n'
            '📋 มีอะไรใน Template:\n'
            '✓ Dashboard จัดการงาน\n'
            '✓ ระบบติดตามเป้าหมาย\n'
            '✓ AI Prompts ในตัว\n'
            '✓ ระบบบันทึกการเงิน\n'
            '✓ Template จดบันทึก\n\n'
            'ติดตั้งพร้อมใช้ทันที\n'
            'แค่ Duplicate ไปใช้ก็เริ่มทำงานได้เลย'
        )
    }
]

def update_product(pid, name, cover_url, description):
    body = json.dumps({
        'access_token': TOKEN,
        'name': name,
        'description': description,
        'preview_url': cover_url
    }).encode()
    req = urllib.request.Request(
        f'https://api.gumroad.com/v2/products/{pid}',
        data=body,
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
        method='PUT'
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        if result.get('success'):
            print(f'  ✅ {name}')
            print(f'     Cover: {cover_url}')
        else:
            print(f'  ❌ {name}: {result}')
    except urllib.error.HTTPError as e:
        print(f'  ❌ {name}: Error {e.code}: {e.read().decode()[:200]}')

print('🔄 กำลังอัปเดตสินค้าบน Gumroad...')
print()
for p in products:
    update_product(p['id'], p['name'], p['cover'], p['desc'])
    print()

print()
print('✅ เสร็จสิ้น!')
print(f'🌐 ร้านค้า: https://cartoonist376.gumroad.com/')
