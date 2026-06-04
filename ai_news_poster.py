#!/usr/bin/env python3
"""Daily AI News Poster — researches AI trends, writes Facebook posts, delivers to Telegram"""

import urllib.request, json, datetime, html, textwrap

TELEGRAM_CHAT = '6865741533'

def search_trends():
    """Get latest AI trends from Hacker News"""
    results = []
    queries = [
        'AI+news+2026', 'artificial+intelligence+breakthrough', 
        'ChatGPT', 'Claude+AI', 'Gemini+AI',
        'AI+tool+launch', 'machine+learning', 'LLM',
        'AI+startup', 'open+source+AI'
    ]
    seen = set()
    for q in queries:
        url = f'https://hn.algolia.com/api/v1/search?query={q}&tags=story&hitsPerPage=5&numericFilters=points>3'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            for hit in data['hits']:
                title = hit.get('title', '')
                pts = hit.get('points', 0)
                url_str = hit.get('url', '') or f"https://news.ycombinator.com/item?id={hit['objectID']}"
                if title and title not in seen and pts >= 5:
                    seen.add(title)
                    results.append({'title': title, 'points': pts, 'url': url_str, 'author': hit.get('author', '')})
        except:
            pass
    results.sort(key=lambda x: x['points'], reverse=True)
    return results[:8]  # Top 8 news

def generate_post(trends, day_name):
    """Generate a Facebook post in Thai"""
    if not trends:
        return None
    
    today = datetime.datetime.now().strftime('%d/%m/%Y')
    
    post = f"""📡 **AI NEWS ประจำวันที่ {today}** 🇹🇭

มาแล้ว! ข่าว AI ร้อนๆ ประจำวันนี้ อัปเดตจากวงการทั่วโลก 👇

"""
    for i, t in enumerate(trends[:5], 1):
        title = html.unescape(t['title'])
        post += f"{i}. {title}\n"
    
    post += f"""
🔗 อ่านเต็มๆ ที่ต้นทาง: {trends[0]['url']}

---

💡 **AI Tips ประจำวัน**
ลองใช้ AI ช่วยทำงานซ้ำๆ เช่น สรุปอีเมล ค้นหาข้อมูล หรือเขียน Draft เนื้อหา — ประหยัดเวลาได้ชั่วโมงต่อวัน!

---

✅ กดติดตามเพจไว้ เจอข่าว AI ใหม่ทุกวัน!
💬 คอมเมนต์ว่าเพื่อนใช้ AI อะไรกันอยู่บ้าง?

#AI #AINews #เทคโนโลยี #AIไทย #ArtificialIntelligence"""
    
    return post

def main():
    print("🤖 AI News Poster")
    print("=" * 40)
    
    day_name = ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์'][datetime.datetime.now().weekday()]
    
    print(f"\n📡 กำลังค้นหาข่าว AI (วัน{day_name})...")
    trends = search_trends()
    print(f"   พบ {len(trends)} ข่าวเด่น")
    
    post = generate_post(trends, day_name)
    if post:
        print(f"\n📝 โพสต์ที่เตรียมไว้:\n")
        print(post[:200] + "...")
        print()
        print("=" * 40)
        print("✅ พร้อมโพสต์! คัดลอกข้อความด้านบนไปลง Facebook")
        
        # Output clearly for cron job parsing
        print("\n---START_POST---")
        print(post)
        print("---END_POST---")
    else:
        print("❌ ไม่พบข่าว")

if __name__ == '__main__':
    main()
