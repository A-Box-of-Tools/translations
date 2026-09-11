"""Prove the archive is the deployed site, changed only where freeze.py says.

    python verify_freeze.py <dist checkout> <archive>
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

FROZEN = ['ar', 'de', 'es', 'fr', 'hi', 'id', 'it', 'ja', 'ko', 'nl', 'pt', 'tr', 'zh-TW']
FRAME = ['lang', 'lang-keep', 'handoff', 'feedback', 'page-md', 'offline', 'hub-filter']

dist, archive = (Path(p).resolve() for p in sys.argv[1:3])
listing = subprocess.run(['git', 'ls-tree', '-r', '-z', 'HEAD'], cwd=dist,
                         capture_output=True, encoding='utf-8', check=True).stdout
deployed = {}
for entry in listing.split('\0'):
    if entry:
        info, path = entry.split('\t', 1)
        deployed[path] = info.split()[2]


def blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def blob_at(path):
    return subprocess.run(['git', 'cat-file', 'blob', deployed[path]], cwd=dist,
                          capture_output=True, check=True).stdout


same = rewritten = added = 0
problems = []
for lang in FROZEN:
    site = archive / 'site' / lang
    here = {p.relative_to(archive / 'site').as_posix(): p for p in site.rglob('*') if p.is_file()}
    theirs = {p for p in deployed if p.startswith(lang + '/')}
    for missing in sorted(theirs - set(here)):
        problems.append(f'missing from the archive: {missing}')
    for name, path in sorted(here.items()):
        data = path.read_bytes()
        if name in deployed:
            if blob(data) == deployed[name]:
                same += 1
                continue
            undone = re.sub(rb'(["\'])/' + re.escape(lang.encode()) + rb'/(%s)\.js'
                            % b'|'.join(re.escape(n.encode()) for n in FRAME), rb'\1/\2.js', data)
            if name.endswith('.html') and blob(undone) == deployed[name]:
                rewritten += 1
            else:
                problems.append(f'changed beyond the script paths: {name}')
        else:
            frame = name.split('/', 1)[1]
            if frame.endswith('.js') and frame[:-3] in FRAME and blob(data) == deployed[frame]:
                added += 1
            else:
                problems.append(f'not in the deployed tree and not a frame copy: {name}')

print(f'{same} identical, {rewritten} pages with only the script paths changed, {added} frame copies')
print('\n'.join(problems[:20]) if problems else 'no other differences')
sys.exit(1 if problems else 0)
