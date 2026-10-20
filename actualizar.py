"""Trae el catálogo de la planilla de Google y actualiza fuente/data.json y fuente/fotos/.

Lee solo las hojas publicadas "Catálogo" y "Fotos" (como CSV). Nunca la hoja Stock.
Si algo falla o la planilla viene vacía, no toca nada: la página queda como estaba.
"""
import csv, hashlib, io, json, os, re, sys, urllib.request

CONFIG = json.load(open('fuente/planilla.json', encoding='utf8'))
LINEAS = ('MUJER', 'UNISEX', 'HOMBRE')
FOTOS_DIR = 'fuente/fotos'


def bajar(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (griyata-web)'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()


def leer_csv(url_o_archivo):
    if url_o_archivo.startswith('http'):
        texto = bajar(url_o_archivo).decode('utf-8-sig')
        if texto.lstrip().startswith('<'):
            sys.exit('La planilla devolvió una página web en vez de datos. ¿Está publicada como CSV?')
    else:
        texto = open(url_o_archivo, encoding='utf-8-sig').read()
    return list(csv.reader(io.StringIO(texto)))


def precio(celda):
    digitos = re.sub(r'\D', '', celda or '')
    return int(digitos) if digitos else None


def clave_foto(url):
    m = re.search(r'\.(\d+)\.(avif|jpg|jpeg|png|webp)', url)
    return m.group(1) if m else hashlib.sha1(url.encode()).hexdigest()[:12]


def extension(url):
    m = re.search(r'\.(avif|jpg|jpeg|png|webp)(?:\?|$)', url.lower())
    return m.group(1).replace('jpeg', 'jpg') if m else 'jpg'


# ---------- hoja Fotos: nombre → link, notas, marca ----------
fotos = {}
for fila in leer_csv(CONFIG['fotos_csv'])[1:]:
    fila += [''] * (4 - len(fila))
    nombre, link, notas, marca = (x.strip() for x in fila[:4])
    if nombre:
        fotos[nombre.lower()] = {'link': link, 'notas': notas, 'marca': marca}

# ---------- hoja Catálogo: líneas y perfumes disponibles ----------
perfumes, linea = [], None
for fila in leer_csv(CONFIG['catalogo_csv']):
    fila += [''] * (5 - len(fila))
    nombre = fila[1].strip()
    if nombre.upper() in LINEAS:
        linea = nombre.upper()
        continue
    contado, tarjeta = precio(fila[2]), precio(fila[3])
    if not linea or not nombre or contado is None or tarjeta is None:
        continue
    extra = fotos.get(nombre.lower(), {})
    perfumes.append({'s': linea, 'n': nombre, 'c': contado, 't': tarjeta,
                     'notes': fila[4].strip() or extra.get('notas', ''),
                     'b': extra.get('marca', ''), 'img': extra.get('link', '')})

if len(perfumes) < 3:
    sys.exit('La planilla trajo %d perfumes; parece un error, no actualizo nada.' % len(perfumes))

# ---------- fotos: bajar solo las nuevas ----------
os.makedirs(FOTOS_DIR, exist_ok=True)
for p in perfumes:
    p['foto'] = ''
    if not p['img']:
        print('Sin foto en la hoja Fotos:', p['n'])
        continue
    archivo = '%s.%s' % (clave_foto(p['img']), extension(p['img']))
    ruta = os.path.join(FOTOS_DIR, archivo)
    if not os.path.exists(ruta):
        try:
            contenido = bajar(p['img'])
            if len(contenido) < 500 or contenido[:1] == b'<':
                raise ValueError('no es una imagen')
            open(ruta, 'wb').write(contenido)
            print('Foto nueva:', p['n'])
        except Exception as e:
            print('No pude bajar la foto de %s (%s)' % (p['n'], e))
            continue
    p['foto'] = archivo

nuevo = json.dumps(perfumes, ensure_ascii=False, indent=1)
viejo = open('fuente/data.json', encoding='utf8').read() if os.path.exists('fuente/data.json') else ''
if nuevo != viejo:
    open('fuente/data.json', 'w', encoding='utf8').write(nuevo)
    print('Catálogo actualizado: %d perfumes.' % len(perfumes))
else:
    print('Sin cambios en la planilla.')
