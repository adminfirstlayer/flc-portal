#!/usr/bin/env python3
"""Build every client portal page from c/<slug>/data.json.

Usage:  python3 tools/build.py            (rebuild all)
        python3 tools/build.py <slug>     (rebuild one)
        python3 tools/build.py --new "Client Name"   (create a new client folder, prints the slug)

data.json fields:
  client, welcome, booking_url,
  next_drop: {label, date (ISO with Z or +00:00), note},
  plan: {name, cycle, delivered, total, revisions, drops, extras},
  docs: [{slug, title, date, html, pdf, approve, approved, approved_on}]   (newest first)
Document files live in c/<slug>/docs/<doc-slug>.html and .pdf; use relative paths "docs/<doc-slug>.html".
"""
import json, os, re, secrets, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(ROOT, 'tools', 'portal_template.html')).read()
LOGO = open(os.path.join(ROOT, 'tools', 'logo.b64')).read().strip()

def build(slug):
    d = os.path.join(ROOT, 'c', slug)
    data = json.load(open(os.path.join(d, 'data.json')))
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    open(os.path.join(d, 'index.html'), 'w').write(T.replace('{{LOGO}}', LOGO).replace('{{DATA_JSON}}', js))
    print('built', slug)

def new(name):
    base = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    slug = f"{base}-{secrets.token_hex(3)}"
    d = os.path.join(ROOT, 'c', slug); os.makedirs(os.path.join(d, 'docs'))
    json.dump({"client": name, "plan": {}, "next_drop": {}, "docs": []}, open(os.path.join(d, 'data.json'), 'w'), indent=2)
    build(slug); print(slug)

if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--new']: new(' '.join(a[1:]))
    elif a: build(a[0])
    else:
        for s in sorted(os.listdir(os.path.join(ROOT, 'c'))):
            if os.path.exists(os.path.join(ROOT, 'c', s, 'data.json')): build(s)
