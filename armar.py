"""Arma index.html a partir de fuente/: mete los datos, las fotos y los logos dentro de la página."""
import json, base64, os

def b64(p, m):
    return 'data:%s;base64,%s' % (m, base64.b64encode(open(p, 'rb').read()).decode())

d = json.load(open('fuente/data.json', encoding='utf8'))
MIME = {'avif': 'image/avif', 'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
data = [dict(i=i, s=p['s'], n=p['n'], b=p.get('b', ''), c=p['c'], t=p['t'], notes=p['notes'],
             fam=p.get('fam', []), ing=p.get('ing', '')) for i, p in enumerate(d)]
imgs = {i: b64('fuente/fotos/' + p['foto'], MIME[p['foto'].rsplit('.', 1)[1]]) for i, p in enumerate(d) if p.get('foto')}
t = open('fuente/plantilla.html', encoding='utf8').read()
t = (t.replace('__LOGO__', b64('fuente/logo.png', 'image/png'))
      .replace('__FIRST_IMG__', next(iter(imgs.values()), ''))
      .replace('__DATA__', json.dumps(data, ensure_ascii=False))
      .replace('__IMGS__', json.dumps(imgs)))
# logos de marcas: fuente/logos/<nombre>.png se usa en la plantilla como __BRAND_<nombre>__
for f in sorted(os.listdir('fuente/logos')):
    if f.endswith('.png'):
        t = t.replace('__BRAND_%s__' % f[:-4], b64('fuente/logos/' + f, 'image/png'))

# vista previa al compartir el link (WhatsApp, Instagram, X): og.png vive aparte en la raíz del repo, con URL absoluta
SITIO = 'https://mateocipres.github.io/griyata-web/'
HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Perfumes árabes originales. Catálogo con precios y pedidos por WhatsApp. Retiro en Malabrigo, Santa Fe.">
<meta property="og:title" content="Griyata Parfums">
<meta property="og:description" content="Perfumes árabes originales. Catálogo con precios y pedidos por WhatsApp.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Griyata Parfums">
<meta property="og:locale" content="es_AR">
<meta property="og:url" content="__SITIO__">
<meta property="og:image" content="__SITIO__og.png">
<meta property="og:image:secure_url" content="__SITIO__og.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo de Griyata Parfums sobre fondo bordó">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Griyata Parfums">
<meta name="twitter:description" content="Perfumes árabes originales. Catálogo con precios y pedidos por WhatsApp.">
<meta name="twitter:image" content="__SITIO__og.png">
<meta name="twitter:image:alt" content="Logo de Griyata Parfums sobre fondo bordó">
<meta name="theme-color" content="#52131e">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
""".replace('__SITIO__', SITIO)

# la plantilla empieza con <title>, los <link> y el <style>: eso va en <head>; el resto en <body>
cut = t.index('</style>') + len('</style>')
page = HEAD + t[:cut] + '\n</head>\n<body>\n' + t[cut:] + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf8').write(page)
print(len(page) // 1024, 'KB')
