import urllib.request, json, urllib.parse, os, sys

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'

def gumroad_api(method, path, data_dict):
    url = f'https://api.gumroad.com/v2{path}'
    body = json.dumps(data_dict).encode()
    req = urllib.request.Request(url, data=body, headers={
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:500]}

def upload_file_to_gumroad(filepath, filename=None):
    """Upload a file to Gumroad and return its URL"""
    if not filename:
        filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    # Step 1: Get presigned URL
    presign_data = urllib.parse.urlencode({
        'access_token': TOKEN,
        'filename': filename,
        'file_size': filesize,
        'content_type': 'text/markdown'
    }).encode()
    
    req = urllib.request.Request(
        'https://api.gumroad.com/v2/files/presign',
        data=presign_data,
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    )
    presign = json.loads(urllib.request.urlopen(req, timeout=30).read())
    
    if not presign.get('success'):
        return None, f"Presign failed: {presign}"
    
    upload_id = presign['upload_id']
    key = presign['key']
    part_url = presign['parts'][0]['presigned_url']
    
    # Step 2: Upload to S3
    with open(filepath, 'rb') as f:
        file_data = f.read()
    
    s3_req = urllib.request.Request(part_url, data=file_data, headers={
        'Content-Type': 'text/markdown'
    }, method='PUT')
    s3_resp = urllib.request.urlopen(s3_req, timeout=60)
    etag = s3_resp.headers.get('ETag', '').strip('"')
    
    # Step 3: Complete upload
    complete_body = json.dumps({
        'access_token': TOKEN,
        'upload_id': upload_id,
        'key': key,
        'parts': [{'part_number': 1, 'etag': etag}]
    })
    complete_req = urllib.request.Request(
        'https://api.gumroad.com/v2/files/complete',
        data=complete_body.encode(),
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
    )
    complete = json.loads(urllib.request.urlopen(complete_req, timeout=30).read())
    
    if not complete.get('success'):
        return None, f"Complete failed: {complete}"
    
    return complete['file_url'], None

def create_product(name, description, price_cents, filepath=None, tags=None):
    """Create a new Gumroad product"""
    data = {
        'access_token': TOKEN,
        'name': name,
        'description': description,
        'price': price_cents,
        'currency': 'usd',
        'tags': tags or []
    }
    
    if filepath:
        file_url, err = upload_file_to_gumroad(filepath)
        if err:
            return None, f"File upload failed: {err}"
        data['files'] = [{'url': file_url}]
    
    return gumroad_api('POST', '/products', data), None

# Create Prompt Pack product
print("=" * 60)
print("สร้าง Digital Products บน Gumroad")
print("=" * 60)

# Product 1: Prompt Pack (already exists, just publish)
print("\n📦 Product 1: Prompt Pack 50+")
result = gumroad_api('PUT', '/products/hVi9IV0OqNpF8RlFEAEzAA==', {
    'access_token': TOKEN,
    'published': 'true'
})
if 'error' in result:
    print(f"  ❌ Publish error: {result.get('body')}")
else:
    prod = result.get('product', {})
    print(f"  ✅ Published: {prod.get('published')}")
    print(f"  🔗 URL: {prod.get('short_url')}")

# Product 2: E-book
print("\n📦 Product 2: E-book คู่มือ AI")
result2 = create_product(
    name='คู่มือเริ่มต้นใช้ AI สำหรับคนไทย (E-book)',
    description=(
        '📘 E-book สอนใช้ AI Tools ตั้งแต่เริ่มต้น จนถึงใช้งานจริงในชีวิตประจำวัน\n\n'
        '🎯 เหมาะสำหรับ:\n'
        '- คนที่ไม่เคยใช้ AI มาก่อน\n'
        '- อยากเริ่มใช้ AI แต่ไม่รู้จะเริ่มยังไง\n'
        '- อยากทำงานให้เร็วขึ้นด้วย AI\n\n'
        '📖 เนื้อหา:\n'
        '- AI คืออะไร? เข้าใจง่าย\n'
        '- แนะนำ ChatGPT, Claude, Gemini\n'
        '- วิธีเขียน Prompt อย่างมืออาชีพ\n'
        '- การประยุกต์ใช้ AI ในชีวิตประจำวัน\n'
        '- เคล็ดลับและเทคนิคขั้นสูง\n\n'
        'ภาษาไทย อ่านง่าย เข้าใจเร็ว'
    ),
    price_cents=499
)
if result2[0]:
    prod = result2[0].get('product', {})
    print(f"  ✅ Created: {prod.get('name')}")
    print(f"  🔗 URL: {prod.get('short_url')}")
    print(f"  💰 Price: ${prod.get('price',0)/100}")
else:
    print(f"  ❌ {result2[1]}")

# Product 3: Notion Template
print("\n📦 Product 3: Notion Template")
result3 = create_product(
    name='Notion Template จัดการงานด้วย AI',
    description=(
        '📊 ระบบจัดการงานส่วนตัว + AI Assistant แบบ all-in-one\n\n'
        '🎯 เหมาะสำหรับ:\n'
        '- Freelancer\n'
        '- Content Creator\n'
        '- นักเรียน นักศึกษา\n'
        '- คนทำงานทั่วไป\n\n'
        '📋 รวม:\n'
        '- Dashboard จัดการงาน\n'
        '- ระบบติดตามเป้าหมาย\n'
        '- AI Prompts ในตัว\n'
        '- ระบบบันทึกการเงิน\n'
        '- Template จดบันทึก\n\n'
        'ติดตั้งพร้อมใช้ทันที'
    ),
    price_cents=399
)
if result3[0]:
    prod = result3[0].get('product', {})
    print(f"  ✅ Created: {prod.get('name')}")
    print(f"  🔗 URL: {prod.get('short_url')}")
    print(f"  💰 Price: ${prod.get('price',0)/100}")
else:
    print(f"  ❌ {result3[1]}")

print("\n" + "=" * 60)
print("✅ เสร็จสิ้น!")
