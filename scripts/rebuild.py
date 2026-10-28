"""Reproduz os patches sem distribuir JARs originais. Requer Python 3 e Java."""
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
COMMIT = 'a78cd1502c9f996ff5b8fc4ae39d144e4a5bf68d'
BASE = f'https://raw.githubusercontent.com/saimuelbr/saimuelrepo/{COMMIT}/builds/'
PATCHES = {
    'NetCine': ('https://nnn1.lat', 'https://www.netcine.asia'),
    'PobreFlix': ('https://www.pobreflixtv.club', 'https://www.pobreflixtv.democrat'),
}

def download(url):
    with urllib.request.urlopen(url, timeout=90) as r:
        return r.read()

def patch_class(data, old, new):
    out = bytearray(data[:10])
    count = struct.unpack_from('>H', data, 8)[0]
    pos, i, hits = 10, 1, 0
    sizes = {3:4,4:4,5:8,6:8,7:2,8:2,9:4,10:4,11:4,12:4,15:3,16:2,17:4,18:4,19:2,20:2}
    while i < count:
        tag = data[pos]
        out.append(tag)
        pos += 1
        if tag == 1:
            length = struct.unpack_from('>H', data, pos)[0]
            pos += 2
            value = data[pos:pos + length]
            pos += length
            hits += value.count(old)
            value = value.replace(old, new)
            out += struct.pack('>H', len(value)) + value
        else:
            length = sizes[tag]
            out += data[pos:pos + length]
            pos += length
            if tag in (5, 6):
                i += 1
        i += 1
    return bytes(out + data[pos:]), hits

def main():
    metadata = {x['internalName']: x for x in json.loads((ROOT/'plugins.template.json').read_text())}
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        tool = work/'r8.jar'
        tool.write_bytes(download('https://storage.googleapis.com/r8-releases/raw/8.3.37/r8.jar'))
        for name, (old, new) in PATCHES.items():
            jar = work/f'{name}.jar'
            hits = 0
            with zipfile.ZipFile(io.BytesIO(download(BASE+name+'.jar'))) as src, zipfile.ZipFile(jar,'w',zipfile.ZIP_DEFLATED) as dst:
                for entry in src.infolist():
                    data = src.read(entry.filename)
                    if entry.filename.endswith('.class'):
                        data, n = patch_class(data, old.encode(), new.encode())
                        hits += n
                    dst.writestr(entry.filename, data)
            if hits == 0:
                raise RuntimeError(f'Nenhum endereço encontrado: {name}')
            dex = work/f'{name}-dex.zip'
            subprocess.run(['java','-cp',str(tool),'com.android.tools.r8.D8','--min-api','21','--output',str(dex),str(jar)],check=True)
            with zipfile.ZipFile(io.BytesIO(download(BASE+name+'.cs3'))) as src, zipfile.ZipFile(dex) as compiled, zipfile.ZipFile(ROOT/'builds'/f'{name}.cs3','w',zipfile.ZIP_DEFLATED) as dst:
                manifest = json.loads(src.read('manifest.json'))
                manifest['version'] = metadata[name]['version']
                dst.writestr('manifest.json',json.dumps(manifest))
                dst.writestr('classes.dex',compiled.read('classes.dex'))
            print(name, 'patches:', hits)
    (ROOT/'builds/TopFilmes.cs3').write_bytes(download(BASE+'TopFilmes.cs3'))
    (ROOT/'CHECKSUMS.sha256').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(ROOT))+'\n' for f in sorted((ROOT/'builds').glob('*.cs3'))))
    print('Execute scripts/configure.py novamente para atualizar os metadados.')

if __name__ == '__main__':
    main()
