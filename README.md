# MagicBot

## Português (Brasil)

MagicBot é um bot do telegram que analisa fontes da Magic Island Robotics (FRC 5800). Ele responde usando os documentos em `data/` usando um modelo local servido pelo LM Studio.

### O que ele faz

```text
Pergunta no Telegram → documentos relevantes da equipe → LM Studio → resposta + nomes dos arquivos-fonte
```

O bot propositalmente **não** usa conhecimento geral para responder perguntas sobre a equipe. Se os documentos não tiverem a resposta, ele deve avisar em vez de tentar adivinhar.

### Configuração inicial

1. Instale o Python 3.10+ e o LM Studio.
2. No LM Studio, carregue um modelo de chat/instruções e inicie o servidor local compatível com a API da OpenAI (normalmente na porta 1234).
3. Crie um bot no BotFather do Telegram e copie o token.
4. Crie sua configuração local:

   ```bash
   cp .env.example .env
   ```

   Coloque o token do BotFather em `TELEGRAM_BOT_TOKEN`. Nunca envie o arquivo `.env` para o Git.

5. Crie e ative um ambiente virtual; depois, instale as dependências:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

6. Inicie o bot a partir da raiz do projeto:

   ```bash
   python bot.py
   ```

O modelo de embeddings é baixado na primeira execução. O índice de busca gerado é salvo em `storage/` e recriado automaticamente quando algum documento-fonte é alterado.

### Como interagir

- Conversa privada: envie uma pergunta normalmente.
- Grupo: use `/ask sua pergunta` ou marque o bot.
- `/agenda`: eventos e prazos atuais.
- `/links`: recursos oficiais da equipe.
- `/onboarding`: primeiros passos para novos membros.
- `/help`: resumo de uso.

### Mantendo as respostas corretas

`data/knowledge_base.txt` contém o relatório de outreach. `data/team/` serve para as informações atualizadas da equipe.
Ainda a serem preenchidos: 

- `calendar.md` — datas, horários, locais e calendário oficial.
- `quick_links.md` — recursos oficiais aprovados.
- `onboarding.md` — checklist real da primeira semana.

Adicione arquivos Markdown separados para cada assunto, por exemplo `data/team/safety.md`, `data/team/programming.md` ou `data/team/faq.md`. Comece cada um com `Updated: AAAA-MM-DD`. Não coloque informações confidenciais em `data/`: o bot pode citá-las em qualquer chat ao qual tenha acesso.

Quando uma informação mudar, atualize o arquivo correspondente, revise-o com o responsável e reinicie o bot caso ele já esteja em execução. Na próxima inicialização, o índice de busca será recriado.

### Mapa do projeto

- `bot.py` — inicia o polling do Telegram.
- `config.py` — lê o `.env` e os caminhos do projeto.
- `handlers.py` — comandos, comportamento em grupos/conversas privadas e divisão segura de mensagens longas.
- `rag.py` — indexação de documentos, busca e prompt de IA baseado em fontes.
- `data/` — documentos editáveis que servem como fonte de verdade.
- `tests/` — testes simples de regressão.

### Solução de problemas

- **"TELEGRAM_BOT_TOKEN is missing"**: crie `.env` a partir de `.env.example` e adicione o token.
- **O bot não consegue responder**: confirme que o LM Studio está em execução, há um modelo carregado e a URL do servidor corresponde a `LM_STUDIO_URL`.
- **Uma marcação no grupo é ignorada**: confira o nome de usuário do bot no Telegram; reinicie o bot após uma mudança de nome ou defina `BOT_USERNAME` como alternativa.
- **A resposta está desatualizada ou incorreta**: corrija o arquivo-fonte, em vez de tentar corrigir a resposta pelo chat.

### Testes

```bash
python -m unittest discover -s tests
```

---

## English

MagicBot is a source-grounded Telegram assistant for Magic Island Robotics (FRC 5800). It answers from the documents in `data/`, using a local model served by LM Studio.

## What it does

```text
Telegram question → relevant team documents → LM Studio → answer + source filenames
```

The bot intentionally does **not** use general knowledge for team questions. If the documents do not support an answer, it should say so rather than guess.

## First-time setup

1. Install Python 3.10+ and LM Studio.
2. In LM Studio, load a chat/instruct model and start its OpenAI-compatible local server (normally port 1234).
3. Create a Telegram bot with BotFather and copy its token.
4. Create your local configuration:

   ```bash
   cp .env.example .env
   ```

   Put the BotFather token in `TELEGRAM_BOT_TOKEN`. Never commit `.env`.

5. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

6. Start the bot from the project root:

   ```bash
   python bot.py
   ```

The embedding model downloads on its first run. The generated search index is stored in `storage/` and is rebuilt automatically whenever a source document changes.

## How members use it

- Private chat: send a normal question.
- Group chat: use `/ask your question` or tag the bot.
- `/agenda`: current events and deadlines.
- `/links`: approved team resources.
- `/onboarding`: first steps for a new member.
- `/help`: usage summary.

## Keeping answers accurate

`data/knowledge_base.txt` contains the outreach report. `data/team/` is for living team information. Fill in its three starter files before sharing the bot with members:

- `calendar.md` — dates, times, locations, official calendar.
- `quick_links.md` — approved public resources.
- `onboarding.md` — the actual first-week checklist.

Add separate Markdown files for each topic, for example `data/team/safety.md`, `data/team/programming.md`, or `data/team/faq.md`. Begin each with `Updated: YYYY-MM-DD`. Do not place confidential information in `data/`: the bot may quote it to any chat it can access.

When information changes, update the relevant file, review it with the responsible lead, and restart the bot if it is already running. The next startup rebuilds its search index.

## Project map

- `bot.py` — starts Telegram polling.
- `config.py` — reads `.env` and paths.
- `handlers.py` — commands, group/private routing, and safe Telegram-sized replies.
- `rag.py` — document indexing, retrieval, and source-grounded AI prompt.
- `data/` — editable source-of-truth documents.
- `tests/` — small regression checks.

## Troubleshooting

- **"TELEGRAM_BOT_TOKEN is missing"**: create `.env` from `.env.example` and add the token.
- **The bot cannot answer**: ensure LM Studio is running, a model is loaded, and its server URL matches `LM_STUDIO_URL`.
- **A group mention is ignored**: verify the bot's Telegram username; restart after a rename, or set `BOT_USERNAME` as a fallback.
- **The answer is outdated or wrong**: correct the source file rather than trying to fix the answer in chat.

## Tests

```bash
python -m unittest discover -s tests
```
