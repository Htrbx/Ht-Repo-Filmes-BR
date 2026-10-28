# BR Filmes e Séries — pacote experimental

Este pacote reaproveita plugins do Saimuel. Não é uma nova implementação dos extratores.
NetCine e PobreFlix receberam SOMENTE troca de endereço e recompilação para Android.
Isso NÃO comprova que catálogo, busca, episódios ou reprodução funcionem no CloudStream.

## Colocar no GitHub pelo celular ou computador

1. Extraia o ZIP. Não envie o ZIP fechado ao GitHub.
2. Abra um repositório PÚBLICO seu. Envie todo o conteúdo extraído diretamente na raiz.
3. Inclua a pasta oculta `.github` e suas subpastas. Não deixe tudo dentro de outra pasta.
4. Abra **Actions → Configurar repositorio**. A execução inicia no envio; se necessário, use **Run workflow**.
5. Quando terminar com marca verde, abra **LINK_DO_REPOSITORIO.txt**, criado na raiz.
6. Copie o link para **CloudStream → Configurações → Extensões → Adicionar repositório**.
7. Instale as extensões que quiser. Para testar NetCine/PobreFlix, desinstale antes suas cópias do Saimuel, pois preservam as mesmas classes internas.

O link depende do seu usuário, nome do repositório e branch: o workflow configura tudo automaticamente.
O arquivo repo.json inicial tem lista vazia de propósito: só estará pronto depois da configuração.
Se a Action falhar com erro de permissão, abra **Settings → Actions → General → Workflow permissions → Read and write permissions** e execute novamente.
Não precisa ativar GitHub Pages, criar token pessoal ou fornecer senha ao pacote.
Se já usa esse repositório com outros plugins, faça backup e integre as listas; enviar estes arquivos substitui a configuração de mesmo nome.

## Conteúdo

| Extensão | Alteração | Validação real |
|---|---|---|
| TopFilmes | Binário original preservado | Usuário relatou reprodução; não testada aqui |
| NetCine BR (teste) | `https://nnn1.lat` → `https://www.netcine.asia` | Catálogo e página de filme acessíveis em teste anterior; sem reprodução confirmada |
| PobreFlix BR (teste) | `https://www.pobreflixtv.club` → `https://www.pobreflixtv.democrat` | Catálogo e página de filme acessíveis em teste anterior; sem reprodução confirmada |

Não inclui extensões dedicadas a anime. Os sites de catálogo misto podem ainda listar animes: este pacote não implementa filtro completo de conteúdo.
Não inclui UltraCine, MegaFlix ou fontes do Liet: as verificações não sustentaram uma correção funcional para elas.
PobreFlix mostrou redirecionamentos variáveis: o domínio aplicado pode mudar novamente.
Se o catálogo aparecer mas o play falhar, é preciso corrigir o extrator; trocar domínio não basta.

## Proveniência e limitações técnicas

Origem: https://github.com/saimuelbr/saimuelrepo
Commit: `a78cd1502c9f996ff5b8fc4ae39d144e4a5bf68d`
Créditos: saimuelbr, Phisher98 e autores indicados nos metadados originais.
A licença GPL-3.0 é declarada no README de origem, preservado em CREDITOS_ORIGINAIS.md.
Consulte o projeto original para código-fonte e condições de redistribuição; este pacote não contém o código Kotlin original, que não estava presente no checkout examinado.
As alterações deste pacote são documentadas e reproduzíveis em scripts/rebuild.py.
O script de configuração e a documentação deste pacote são oferecidos sob GPL-3.0.

DEX gerado com D8 8.3.37, min API 21. O compilador avisou sobre referências externas de CloudStream/Kotlin ausentes do classpath; elas são esperadas no app, mas a compatibilidade em execução NÃO foi validada.
Foram verificadas a estrutura ZIP, checksums DEX, manifests e URLs geradas. Não foi feito teste no aplicativo Android.

Para configurar sem Actions, com Python instalado:

```bash
python3 scripts/configure.py SEU_USUARIO/SEU_REPOSITORIO --branch main
```

Envie então os arquivos gerados para a mesma branch.
