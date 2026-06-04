import urllib.request, json

token = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'

url = 'https://api.gumroad.com/v2/products?access_token=' + token
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=15)
data = json.loads(resp.read())
products = data.get('products', [])
print('Products found:', len(products))
for p in products:
    name = p.get('name', 'N/A')
    published = p.get('published', False)
    short_url = p.get('short_url', 'N/A')
    price = p.get('price', 0)
    pid = p.get('id', 'N/A')
    print(f'Name: {name}')
    print(f'Published: {published}')
    print(f'URL: {short_url}')
    print(f'Price: ${price/100}')
    print(f'ID: {pid}')
    print('---')
