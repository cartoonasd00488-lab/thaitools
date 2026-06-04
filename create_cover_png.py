"""Create simple gradient PNG images for product covers using pure Python + zlib"""
import struct, zlib, base64, urllib.request, json

TOKEN = 'IFvqJG3lgjY2iXIZZsRE6cnseOLXnREx2OYVgd5qAoo'
BASE_URL = 'https://cartoonasd00488-lab.github.io/thaitools'

def create_simple_png(width, height, r, g, b, text_name=""):
    """Create a minimal colored PNG with gradient"""
    # Create raw pixel data (RGBA)
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'  # filter byte
        for x in range(width):
            # Simple gradient
            grad = int((y / height) * 60)
            pr = max(0, r - grad)
            pg = max(0, g - grad)
            pb = max(0, b - grad)
            raw_data += struct.pack('BBBB', pr, pg, pb, 255)
    
    # Compress
    compressed = zlib.compress(raw_data)
    
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
    
    png = b'\x89PNG\r\n\x1a\n'  # PNG signature
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))  # RGBA
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    
    return png

def update_with_base64(pid, name, png_bytes):
    """Upload PNG as cover via base64 data URI"""
    b64 = base64.b64encode(png_bytes).decode()
    data_uri = f'data:image/png;base64,{b64}'
    
    body = json.dumps({
        'access_token': TOKEN,
        'name': name,
        'preview_url': data_uri
    }).encode()
    
    req = urllib.request.Request(
        f'https://api.gumroad.com/v2/products/{pid}',
        data=body,
        headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'},
        method='PUT'
    )
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

products = [
    ('hVi9IV0OqNpF8RlFEAEzAA==', 'Prompt Pack 50+ สูตรใช้ AI ทำงาน'),
    ('ULR_k1q00sYbwsMhREdgDQ==', 'คู่มือเริ่มต้นใช้ AI สำหรับคนไทย (E-book)'),
    ('t2YGHAsEnRsv1MhI-tkKmQ==', 'Notion Template จัดการงานด้วย AI'),
]

colors = [(45, 55, 145), (10, 100, 70), (200, 100, 30)]  # Blue, Green, Orange

print('🔄 กำลังอัปโหลดภาพปก...')
for (pid, name), (r, g, b) in zip(products, colors):
    print(f'\n📦 {name}')
    png = create_simple_png(200, 266, r, g, b)
    print(f'   PNG size: {len(png)} bytes')
    result = update_with_base64(pid, name, png)
    if result.get('success'):
        print(f'   ✅ อัปโหลดสำเร็จ!')
    else:
        print(f'   ❌ ล้มเหลว: {result}')

print('\n✅ เสร็จสิ้น!')
print('🌐 ไปที่ https://app.gumroad.com/products แล้วกด Publish อีกครั้งครับ')
