"""Search Google and extract AI-related keyword ideas for Thai content"""
import requests, re, json, urllib.parse, time

def search_google(query, num=5):
    """Search Google and return results"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'th,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    }
    try:
        resp = requests.get(
            f'https://www.google.com/search?q={urllib.parse.quote(query)}&hl=th&num={num}',
            headers=headers, timeout=10
        )
        html = resp.text
        
        # Extract search result titles and snippets
        results = []
        # Try various patterns
        titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
        snippets = re.findall(r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        
        for i, title in enumerate(titles[:num]):
            clean_title = re.sub(r'<[^>]*>', '', title).strip()
            snippet = ''
            if i < len(snippets):
                snippet = re.sub(r'<[^>]*>', '', snippets[i]).strip()
            if clean_title:
                results.append({'title': clean_title, 'snippet': snippet})
        
        return results
    except Exception as e:
        return [{'error': str(e)}]

def find_keyword_ideas():
    """Find keyword ideas for Thai AI content"""
    seed_keywords = [
        'AI tools รีวิว', 'ChatGPT ภาษาไทย', 'AI ทำงาน', 'วิธีใช้ AI',
        'AI productivity', 'best AI tools 2026', 'AI สร้างรายได้',
        'AI content', 'tools AI ฟรี', 'AI สำหรับธุรกิจ'
    ]
    
    all_keywords = {}
    
    for keyword in seed_keywords:
        print(f'\n🔍 ค้นหา: {keyword}')
        results = search_google(keyword)
        if results and len(results) > 0 and 'error' not in results[0]:
            for r in results:
                title = r.get('title', '')
                snippet = r.get('snippet', '')
                words = re.findall(r'[\w]+', title.lower())
                for w in words:
                    if len(w) > 3 and w not in ['this', 'that', 'with', 'from', 'have', 'been']:
                        all_keywords[w] = all_keywords.get(w, 0) + 1
                print(f'   📌 {title[:80]}')
        elif results and len(results) > 0:
            print(f'   ❌ {results[0].get("error", "No results")}')
        else:
            print(f'   ⚠️ ไม่มีผลลัพธ์ (Google อาจบล็อค)')
        time.sleep(1)
    
    # Sort by frequency
    sorted_kw = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)
    print(f'\n{"="*50}')
    print('📊 Top Keywords Found:')
    for kw, count in sorted_kw[:30]:
        print(f'   {kw}: {count} times')

if __name__ == '__main__':
    print('🔍 Thai AI Keyword Research')
    print('=' * 50)
    find_keyword_ideas()
