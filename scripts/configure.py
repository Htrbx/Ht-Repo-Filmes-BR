"""Gera URLs para o dono/repositório e branch reais, sem serviços externos."""
import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

def configure(repository, branch):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Informe USUARIO/REPOSITORIO')
    if not branch or any(c in branch for c in '\r\n'):
        raise ValueError('Branch inválida')
    base = f'https://raw.githubusercontent.com/{repository}/{quote(branch, safe="/")}'
    plugins = json.loads((ROOT / 'plugins.template.json').read_text())
    for p in plugins:
        p['url'] = f'{base}/builds/{p["internalName"]}.cs3'
        p['repositoryUrl'] = f'https://github.com/{repository}'
        p['fileSize'] = (ROOT / 'builds' / f'{p["internalName"]}.cs3').stat().st_size
    def write(path, value):
        path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    write(ROOT / 'builds/plugins.json', plugins)
    write(ROOT / 'repo.json', {
        'name': 'BR Filmes e Séries — testes',
        'description': 'TopFilmes original + NetCine e PobreFlix experimentais. Sem extensões dedicadas a anime.',
        'manifestVersion': 1,
        'pluginLists': [f'{base}/builds/plugins.json'],
    })
    link = f'{base}/repo.json'
    (ROOT / 'LINK_DO_REPOSITORIO.txt').write_text(link + '\n')
    print(link)
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a') as f:
            f.write(f'## Link para adicionar no CloudStream\n\n```text\n{link}\n```\n\nReprodução das versões de teste ainda não confirmada.\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', nargs='?', default=os.environ.get('GITHUB_REPOSITORY'))
    parser.add_argument('--branch', default=os.environ.get('GITHUB_REF_NAME', 'main'))
    args = parser.parse_args()
    configure(args.repository or '', args.branch)
