# Multi-Store Bot

Bot de monitoramento de precos que suporta multiplas lojas, com interface web, autenticacao, banco de dados e notificacoes por email.

## O que faz

- Multi-loja: suporta sites estaticos (requests) e dinamicos (Playwright)
- Cadastro de produtos: cada usuario cadastra seus produtos
- Monitoramento automatico: roda a cada X minutos e salva o historico
- Alertas por email: avisa quando o preco baixa do valor alvo
- Historico de precos: guarda todas as variacoes
- Backup do banco: copia de seguranca dos dados
- Multi-usuario: login com email + senha (bcrypt)
- Interface web: Flask + HTML + CSS
- Isolamento: roda em Docker
- Logs: registra tudo com rotacao automatica

## Tecnologias

- Python 3.14
- Flask (framework web)
- Flask-Login (autenticacao)
- bcrypt (hash de senhas)
- SQLite (banco de dados)
- requests (requisicoes HTTP)
- BeautifulSoup4 (parsing de HTML)
- Playwright (automacao de navegador)
- schedule (agendamento)
- Docker (isolamento)

## Como rodar

Com Docker:

    docker-compose up

Acessa http://localhost:5000

Sem Docker:

    pip install -r requirements.txt
    python app.py

## Configuracao

Crie um arquivo .env na raiz do projeto:

    EMAIL_USER=seuemail@gmail.com
    EMAIL_PASS=sua_senha_de_app
    EMAIL_TO=seuemail@gmail.com

Importante: use uma senha de app do Gmail, nao a senha normal.

## Estrutura

    multi-store-bot/
      app.py
      auth.py
      bank.py
      config.py
      mail.py
      security.py
      stores/
      templates/
      static/
      Dockerfile
      docker-compose.yml
      requirements.txt

## Seguranca

- Senhas com bcrypt
- Validacao de URLs com lista branca
- SQL com parametros contra injecao
- Bloqueio de requisicoes externas no Playwright
- Docker isola o ambiente
- .env nao sobe pro Git

## Lojas suportadas

- Books to Scrape (estatico): titulo + preco
- Quotes to Scrape (estatico): frase + autor
- Quotes JS (dinamico): frase + autor

## Autor

SlinkierBook - https://github.com/SlinkierBook

## Licenca

Este projeto e de uso livre para estudo e portfolio.