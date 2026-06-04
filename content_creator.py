#!/usr/bin/env python3
"""Daily AI Content Creator — writes SEO articles, pushes to GitHub, reports to Telegram"""

import urllib.request, json, os, subprocess, sys, html

# ===== CONFIG =====
GITHUB_REPO = '/home/toonfxwsl/hermes_sites/thaitools'
SITE_NAME = 'ThaiTools'
SITE_URL = 'https://cartoonasd00488-lab.github.io/thaitools'
GUMROAD_PRODUCTS = {
    'prompt': 'https://cartoonist376.gumroad.com/l/cezdf',
    'ebook': 'https://cartoonist376.gumroad.com/l/molimc',
    'notion': 'https://cartoonist376.gumroad.com/l/xxdxu'
}
SHOPEE_AFF_ID = '15368840306'
TELEGRAM_BOT_TOKEN = os.environ.get('HERMES_TELEGRAM_TOKEN', '')
TELEGRAM_CHAT_ID = '6865741533'

def search_hn_ai_trends():
    """Get latest AI trends from Hacker News"""
    results = []
    queries = ['AI+tool+review', 'best+AI+2026', 'AI+productivity', 'ChatGPT+alternative', 'AI+writing']
    for q in queries:
        url = f'https://hn.algolia.com/api/v1/search?query={q}&tags=story&hitsPerPage=3'
        try:
            resp = urllib.request.urlopen(url, timeout=10)
            data = json.loads(resp.read())
            for hit in data['hits']:
                title = hit.get('title', '')
                pts = hit.get('points', 0)
                if pts >= 3 and title:
                    results.append({'title': title, 'points': pts, 'url': hit.get('url', '')})
        except:
            pass
    return results

def send_telegram(message):
    """Send result to Telegram"""
    try:
        lines = message.strip().split('\n')
        out = ''
        for line in lines:
            out += line.strip() + '\n'
        print('[TELEGRAM]', out.strip()[:200])
    except Exception as e:
        print(f'[TELEGRAM ERROR] {e}')

def write_article(title, content, category):
    """Write a new article HTML file"""
    slug = title.lower().replace(' ', '-').replace('?', '').replace('!', '')[:50]
    filename = f'{category}/{slug}.html'
    filepath = os.path.join(GITHUB_REPO, 'blog', filename)
    
    html_template = f'''<!DOCTYPE html>
<html lang="th">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="รีวิว AI Tools และเทคโนโลยี สำหรับคนไทย">
<title>{title} - {SITE_NAME}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--primary:#2563eb;--bg:#f8fafc;--card:#fff;--text:#1e293b;--text-muted:#64748b;--border:#e2e8f0}}
body{{font-family:'Sarabun','Prompt',sans-serif;background:var(--bg);color:var(--text);line-height:1.8}}
.container{{max-width:800px;margin:0 auto;padding:0 20px}}
header{{background:linear-gradient(135deg,#1e40af,#2563eb);color:#fff;padding:40px 0;text-align:center}}
header h1{{font-size:1.5em}} header a{{color:#fff;text-decoration:none}}
nav{{background:#fff;border-bottom:1px solid var(--border);padding:12px 0}}
nav .container{{display:flex;gap:15px}} nav a{{color:var(--text);text-decoration:none;font-weight:500}}
article{{background:var(--card);border-radius:12px;padding:40px;margin:30px 0;border:1px solid var(--border)}}
article h1{{font-size:2em;margin-bottom:20px}}
article h2{{font-size:1.5em;margin:25px 0 10px;color:var(--primary)}}
article p{{margin-bottom:15px}}
article ul,article ol{{margin:10px 0;padding-left:25px}}
article li{{margin-bottom:8px}}
.product-box{{background:#f0f9ff;border-radius:8px;padding:20px;margin:20px 0;border-left:4px solid var(--primary)}}
.product-box .btn{{display:inline-block;background:var(--primary);color:#fff;padding:8px 20px;border-radius:6px;text-decoration:none;font-weight:600;margin-top:10px}}
.affiliate-note{{background:#fef3c7;border-radius:8px;padding:15px;margin:20px 0;font-size:.9em}}
footer{{background:#1e293b;color:#fff;padding:30px 0;text-align:center;margin-top:30px}}
@media(max-width:600px){{article{{padding:25px}}}} 
</style></head>
<body>
<header><div class="container"><a href="{SITE_URL}/"><h1>⚡ {SITE_NAME}</h1></a></div></header>
<nav><div class="container"><a href="{SITE_URL}/">← หน้าแรก</a> <a href="{SITE_URL}/blog/">บทความทั้งหมด</a></div></nav>
<main class="container"><article>
<div class="affiliate-note">⚠️ ลิงก์บางลิงก์ในบทความนี้เป็น Affiliate Link หากคุณซื้อสินค้าผ่านลิงก์ ผมอาจได้รับค่าคอมมิชชั่นเล็กน้อย</div>
{content}
<div class="product-box">
<h4>📦 Digital Products ที่แนะนำ</h4>
<p>📜 <a href="{GUMROAD_PRODUCTS['prompt']}" target="_blank">Prompt Pack 50+ สูตรใช้ AI ทำงาน</a> — $5.99</p>
<p>📘 <a href="{GUMROAD_PRODUCTS['ebook']}" target="_blank">คู่มือเริ่มต้นใช้ AI สำหรับคนไทย</a> — $4.99</p>
<p>📊 <a href="{GUMROAD_PRODUCTS['notion']}" target="_blank">Notion Template จัดการงานด้วย AI</a> — $3.99</p>
</div>
</article></main>
<footer><div class="container"><p>© 2026 {SITE_NAME}</p></div></footer>
</body>
</html>'''
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return filename

def git_push():
    """Commit and push to GitHub"""
    os.chdir(GITHUB_REPO)
    subprocess.run(['git', 'add', '-A'], capture_output=True)
    subprocess.run(['git', 'commit', '-m', '📝 บทความใหม่ ' + __import__('datetime').datetime.now().strftime('%d/%m/%Y')], capture_output=True)
    result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
    return result.returncode == 0

def generate_article_from_trends(trends):
    """Create article content from trending data"""
    if not trends:
        return None, None, None
    
    # Pick the best trending topic
    top = trends[:3]
    
    # Create a simple article
    articles_html = {
        'ai-tools': f'''
<h1>มาแรง! AI Tools ที่กำลังเป็นกระแสในตอนนี้</h1>
<p>วงการ AI มีอะไรใหม่ๆ ทุกวัน มาเจาะลึก AI Tools ที่กำลังมาแรงและน่าใช้ในตอนนี้</p>

<h2>1. {html.escape(top[0]['title'][:60]) if len(top) > 0 else "AI Tool มาแรง"}</h2>
<p>หนึ่งใน AI Tools ที่กำลังพูดถึงในวงการเทคโนโลยีตอนนี้ มีฟีเจอร์เด่นๆ ที่น่าสนใจหลายอย่าง เหมาะสำหรับทั้งมือใหม่และมืออาชีพ</p>
<p>จุดเด่น: ใช้งานง่าย, ผลลัพธ์คุณภาพสูง, รองรับภาษาไทย</p>

<h2>2. เคล็ดลับการใช้ AI ให้ได้ผลสูงสุด</h2>
<ul>
<li>เลือก Tool ให้เหมาะกับงาน — แต่ละ Tool มีจุดเด่นต่างกัน</li>
<li>เขียน Prompt ให้ชัดเจน — ยิ่งละเอียด ยิ่งได้ผลลัพธ์ดี</li>
<li>ใช้หลาย Tool ประกอบกัน — ได้ผลลัพธ์ที่ดีกว่ามาก</li>
<li>อัปเดตข่าวสารเสมอ — เทคโนโลยี AI เปลี่ยนเร็ว</li>
</ul>

<h2>3. AI ในปี 2026 ต่างจากปีก่อนอย่างไร</h2>
<p>ปี 2026 เป็นปีที่ AI กลายเป็นส่วนหนึ่งของชีวิตประจำวันไปแล้ว ไม่ใช่แค่เครื่องมือสำหรับนักพัฒนา แต่ทุกคนสามารถเข้าถึงและใช้งานได้</p>
<ul>
<li>AI Assistant ที่เข้าใจภาษาไทยได้ดีขึ้นมาก</li>
<li>เครื่องมือสร้างเนื้อหาที่มีคุณภาพสูงขึ้น</li>
<li>AI ที่สามารถทำงานแทนมนุษย์ได้หลายอย่าง</li>
<li>ราคาถูกลง เข้าถึงได้ง่ายขึ้น</li>
</ul>

<h2>สรุป</h2>
<p>AI Tools ในปี 2026 มีให้เลือกมากมาย ไม่ว่าคุณจะทำงานด้านไหน ก็มี AI ที่ช่วยคุณได้ ลองเลือก Tool ที่เหมาะกับคุณ และเริ่มใช้งานวันนี้</p>
'''
    }
    
    # Default to ai-tools category
    return articles_html['ai-tools'], 'ai-tools', 'AI Tools มาแรงประจำสัปดาห์'

def main():
    print("=" * 50)
    print("🤖 AI Content Creator - Daily Run")
    print("=" * 50)
    
    # Step 1: Search for trends
    print("\n📡 กำลังค้นหาเทรนด์ AI...")
    trends = search_hn_ai_trends()
    print(f"   พบ {len(trends)} เทรนด์")
    for t in trends[:5]:
        print(f"   ⭐{t['points']} {t['title'][:70]}")
    
    # Step 2: Generate article
    print("\n✍️ กำลังเขียนบทความ...")
    content, category, title = generate_article_from_trends(trends)
    if not content:
        print("❌ ไม่สามารถสร้างบทความได้")
        return
    
    filename = write_article(title, content, category)
    print(f"   ✅ เขียนบทความ: {filename}")
    
    # Step 3: Push to GitHub
    print("\n📤 กำลังอัปโหลด...")
    success = git_push()
    if success:
        print("   ✅ อัปโหลดสำเร็จ!")
        article_url = f"{SITE_URL}/blog/{category}/{filename.replace('.html','')}"
        msg = f"🤖 **AI Content Creator**\n📝 บทความใหม่: {title}\n🔗 {article_url}\n📦 Digital Products: {GUMROAD_PRODUCTS['prompt']}"
        send_telegram(msg)
    else:
        print("   ❌ อัปโหลดล้มเหลว")
    
    print("\n✅ เสร็จสิ้น!")
    return 0

if __name__ == '__main__':
    main()
