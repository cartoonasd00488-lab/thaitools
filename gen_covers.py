"""Create PNG covers and save to files, then push to GitHub"""
import struct, zlib, os

OUTPUT_DIR = '/home/toonfxwsl/hermes_sites/thaitools/assets/covers'

def create_gradient_png(width, height, r, g, b):
    """Create gradient RGBA PNG"""
    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            grad = int((y / height) * 50)
            pr, pg, pb = max(0,r-grad), max(0,g-grad), max(0,b-grad)
            raw += struct.pack('BBBB', pr, pg, pb, 255)
    comp = zlib.compress(raw)
    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    return png

covers = [
    ('prompt-pack.png', 45, 55, 145),
    ('ebook.png', 10, 100, 70),
    ('notion-template.png', 200, 100, 30),
]

for name, r, g, b in covers:
    png = create_gradient_png(300, 400, r, g, b)
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, 'wb') as f:
        f.write(png)
    print(f'✅ {name} ({len(png)} bytes)')
