import json, base64
def b64(p, m): return 'data:%s;base64,%s' % (m, base64.b64encode(open(p, 'rb').read()).decode())
d = json.load(open('fuente/data.json', encoding='utf8'))
data = [dict(i=i, s=p['s'], n=p['n'], c=p['c'], t=p['t'], notes=p['notes']) for i, p in enumerate(d)]
imgs = {i: b64('fuente/fotos/%d.avif' % i, 'image/avif') for i in range(len(d))}
t = open('fuente/plantilla.html', encoding='utf8').read()
t = (t.replace('__LOGO__', b64('fuente/logo.png', 'image/png'))
      .replace('__FIRST_IMG__', imgs[0])
      .replace('__DATA__', json.dumps(data, ensure_ascii=False))
      .replace('__IMGS__', json.dumps(imgs)))
open('index.html', 'w', encoding='utf8').write(t)
print(len(t) // 1024, 'KB')
