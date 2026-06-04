import json, urllib.request, os

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'

# Create English version of Prompt Pack
prompt_en_product = {
    'access_token': TOKEN,
    'name': 'Ultimate AI Prompt Pack - 50+ Prompts for ChatGPT, Claude & Gemini',
    'description': (
        '🚀 **50+ Professional AI Prompts** — Instantly improve your work with ChatGPT, Claude, and Gemini\n\n'
        '📂 **Categories:**\n'
        '• Writing & Content Creation\n'
        '• Marketing & Social Media\n'
        '• Business & Strategy\n'
        '• Coding & Development\n'
        '• Learning & Education\n\n'
        '✅ **What you get:**\n'
        '✓ 50+ ready-to-use prompts (PDF)\n'
        '✓ Works with ChatGPT, Claude, Gemini\n'
        '✓ Copy-paste, no editing needed\n'
        '✓ Covers 5 categories\n'
        '✓ Instant download after purchase\n\n'
        '💡 **Perfect for:**\n'
        '• Content Creators\n'
        '• Marketers\n'
        '• Developers\n'
        '• Students\n'
        '• Business Owners\n\n'
        '👉 Download instantly after purchase!'
    ),
    'price': 799,  # $7.99
    'currency': 'usd',
    'published': True,
    'tags': ['AI', 'Prompts', 'ChatGPT', 'Claude', 'Productivity', 'English']
}

# Create English E-book
ebook_en_product = {
    'access_token': TOKEN,
    'name': 'AI for Beginners: Complete Guide to ChatGPT, Claude & Gemini',
    'description': (
        '📘 **AI for Beginners** — Your complete guide to mastering AI tools\n\n'
        '🎯 **Who this is for:**\n'
        '• Complete beginners who\'ve never used AI\n'
        '• Professionals who want to work faster\n'
        '• Anyone feeling overwhelmed by AI\n\n'
        '📖 **What you\'ll learn:**\n'
        '✓ What AI is and how it works (simple explanation)\n'
        '✓ ChatGPT, Claude, Gemini — which to use and when\n'
        '✓ How to write prompts like a pro\n'
        '✓ AI for work: emails, reports, presentations\n'
        '✓ AI for creative: writing, art, music\n'
        '✓ Advanced tips & tricks\n\n'
        '🌍 English version — accessible worldwide\n'
        '📥 Instant PDF download\n\n'
        'Start your AI journey today!'
    ),
    'price': 699,  # $6.99
    'currency': 'usd',
    'published': True,
    'tags': ['AI', 'Beginner', 'Guide', 'ChatGPT', 'Ebook', 'English']
}

products = [prompt_en_product, ebook_en_product]

def create_product(data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        'https://api.gumroad.com/v2/products',
        data=body,
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        if result.get('success'):
            p = result['product']
            print(f'  ✅ {p["name"]}')
            print(f'     URL: {p.get("short_url", "")}')
            print(f'     Price: ${p.get("price",0)/100}')
            return p
        else:
            print(f'  ❌ {data["name"]}: {result}')
    except urllib.error.HTTPError as e:
        print(f'  ❌ Error {e.code}: {e.read().decode()[:200]}')
    return None

print('🔄 Creating English Digital Products on Gumroad')
print('=' * 60)

for p in products:
    result = create_product(p)
    print()

print('=' * 60)
print('✅ Done! English products created.')
print('🌐 Store: https://cartoonist376.gumroad.com/')
