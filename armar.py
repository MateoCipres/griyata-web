"""Arma index.html a partir de fuente/: mete los datos, las fotos y el logo dentro de la página."""
import json, base64

def b64(p, m):
    return 'data:%s;base64,%s' % (m, base64.b64encode(open(p, 'rb').read()).decode())

d = json.load(open('fuente/data.json', encoding='utf8'))
MIME = {'avif': 'image/avif', 'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
data = [dict(i=i, s=p['s'], n=p['n'], b=p.get('b', ''), c=p['c'], t=p['t'], notes=p['notes']) for i, p in enumerate(d)]
imgs = {i: b64('fuente/fotos/' + p['foto'], MIME[p['foto'].rsplit('.', 1)[1]]) for i, p in enumerate(d) if p.get('foto')}
t = open('fuente/plantilla.html', encoding='utf8').read()
t = (t.replace('__LOGO__', b64('fuente/logo.png', 'image/png'))
      .replace('__FIRST_IMG__', next(iter(imgs.values()), ''))
      .replace('__DATA__', json.dumps(data, ensure_ascii=False))
      .replace('__IMGS__', json.dumps(imgs)))

HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Perfumes árabes originales, sellados de fábrica. Catálogo con precios y pedidos por WhatsApp. Retiro en Malabrigo, Santa Fe.">
<meta property="og:title" content="Griyata Parfums">
<meta property="og:description" content="Perfumes árabes originales, sellados de fábrica. Catálogo con precios y pedidos por WhatsApp.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#e7e8ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#262830" media="(prefers-color-scheme: dark)">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""

# la plantilla empieza con <title>, los <link> y el <style>: eso va en <head>; el resto en <body>
cut = t.index('</style>') + len('</style>')
page = HEAD + t[:cut] + '\n</head>\n<body>\n' + t[cut:] + '\n</body>\n</html>\n'
open('index.html', 'w', encoding='utf8').write(page)
print(len(page) // 1024, 'KB')
