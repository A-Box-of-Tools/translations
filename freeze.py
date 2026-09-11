"""Make the translations archive out of the live site and the website sources.

    python freeze.py <dist checkout> <website checkout at the frozen commit> <out>

Writes <out>/site/<lang>/ - each frozen language exactly as it is deployed, with
its own copies of the seven frame scripts it used to load from the site root -
and <out>/source/locales/<lang>/, the translation sources it was built from.
Every edit asserts what it found, so a tree that is not the one this was written
against fails loudly instead of being half-frozen.
"""

import re
import shutil
import sys
from pathlib import Path

FROZEN = ['ar', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja', 'ko', 'nl', 'pt', 'tr', 'zh-TW']
FRAME = ['lang', 'lang-keep', 'handoff', 'feedback', 'page-md', 'offline', 'hub-filter']
ROOT_SCRIPT = re.compile(r'''(["'])/(%s)\.js''' % '|'.join(re.escape(n) for n in FRAME))

dist, website, out = (Path(p).resolve() for p in sys.argv[1:4])
assert (dist / 'sitemap.xml').is_file(), f'{dist} is not a dist checkout'
assert (website / 'build.py').is_file(), f'{website} is not a website checkout'
if out.exists():
    shutil.rmtree(out)

total_files = total_refs = 0
for lang in FROZEN:
    src = dist / lang
    dst = out / 'site' / lang
    assert src.is_dir(), f'{lang} is not in the deployed tree'
    shutil.copytree(src, dst)

    for name in FRAME:
        own = dst / f'{name}.js'
        assert not own.exists(), f'{lang}/{name}.js already exists; the copy would overwrite it'
        shutil.copyfile(dist / f'{name}.js', own)

    refs = 0
    for page in dst.rglob('*.html'):
        text = page.read_bytes().decode('utf-8')
        new, n = ROOT_SCRIPT.subn(lambda m: f'{m.group(1)}/{lang}/{m.group(2)}.js', text)
        if n:
            page.write_bytes(new.encode('utf-8'))
            refs += n
    assert refs, f'{lang}: no page loaded a frame script from the root, which is not the tree this expects'
    left = [p for p in dst.rglob('*.html') if ROOT_SCRIPT.search(p.read_bytes().decode('utf-8'))]
    assert not left, f'{lang}: still loads from the root: {left[:3]}'

    shutil.copytree(website / 'locales' / lang, out / 'source' / 'locales' / lang)
    files = sum(1 for p in dst.rglob('*') if p.is_file())
    total_files += files
    total_refs += refs
    print(f'{lang}: {files} files, {refs} frame-script references pointed at its own copies')

print(f'total: {total_files} files, {total_refs} references')
