import json, urllib.request

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'

product_ids = [
    'hVi9IV0OqNpF8RlFEAEzAA==',
    'ULR_k1q00sYbwsMhREdgDQ==',
    't2YGHAsEnRsv1MhI-tkKmQ=='
]

for pid in product_ids:
    url = f'https://api.gumroad.com/v2/products/{pid}?access_token={TOKEN}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    p = data.get('product', {})
    print(f'ชื่อ: {p.get("name")}')
    print(f'มีไฟล์: {"Yes" if p.get("files") else "No"}')
    print(f'Preview URL: {p.get("preview_url","no preview")}')
    print(f'Thumbnail: {p.get("thumbnail_url","no thumbnail")}')
    print(f'Published: {p.get("published", False)}')
    print('---')
