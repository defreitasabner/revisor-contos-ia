# Revisor de Contos com IA

Este projeto oferece um leitor crítico com inteligência artificial para escritores(as) que não tem uma pessoa disponível para ler e comentar seu conto. A ferramenta analisa o texto e ajuda o(a) autor(a) a refletir sobre o efeito da obra, sem assumir o processo criativo.

## O que o revisor faz

- Analisa estilo, coerência, ritmo, linguagem e personagens, com citações do conto.
- Aponta pontos fortes e aspectos que podem ser aprimorados.
- Sugere trechos que podem ser encurtados ou removidos e explica o possível efeito dessas mudanças.
- Considera o contexto informado, como o fato de ser um microconto, de ter um limite de palavras ou de estar incompleto.

O revisor não reescreve nem continua o conto, não inventa elementos e não atende a pedidos que não sejam avaliar um conto.

## Como usar

1. Envie um conto em `.docx`, `.pdf`, `.txt` ou `.md`.
2. Se quiser, informe um contexto para orientar a avaliação.
3. Faça perguntas de acompanhamento sobre a avaliação na mesma conversa.

O histórico fica no navegador e é apagado ao recarregar a página. PDFs digitalizados como imagem não funcionam, pois não contêm texto extraível.

## Chave de API e privacidade

É necessária uma chave de API do Gemini, do Google AI Studio. O conto e as mensagens de acompanhamento são enviados ao Google para gerar a avaliação. Consulte as condições de uso e privacidade aplicáveis à sua conta e à sua chave de API.

## Executar localmente

Requer Python 3.11 ou superior.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto e adicione sua chave:

```env
GEMINI_API_KEY=sua_chave
```

Inicie o servidor e acesse http://127.0.0.1:5000:

```bash
.venv/bin/python app.py
```

## Configuração

| Variável | Descrição | Padrão |
|---|---|---|
| `GEMINI_API_KEY` | Chave de API do Gemini (obrigatória) | — |
| `GEMINI_MODEL` | Modelo Gemini usado | `gemini-2.5-flash` |

Variáveis definidas no ambiente têm prioridade sobre as definidas no `.env`.

## Limitações

- O único provedor implementado é o Gemini.
- Não há autenticação nem armazenamento persistente; o projeto é voltado ao uso local e pontual.
- Em arquivos `.docx`, apenas os parágrafos do corpo são lidos. Tabelas, cabeçalhos e rodapés são ignorados.
- Arquivos `.doc` não são aceitos.
- A interface carrega Bootstrap, `marked` e `DOMPurify` por CDN e precisa de acesso à internet.
