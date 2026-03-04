# ProseiAê!

Este repositório contém uma aplicação web de conversa em tempo real. Você pode criar salas de chat, conversar com outros usuários via WebSockets e gerenciar suas conversas em uma interface responsiva.

## O que a aplicação faz

O site público exibe a página inicial e permite que usuários autenticados criem salas de chat, entrem em conversas em tempo real e editem ou saiam de salas. As mensagens são enviadas e recebidas instantaneamente via WebSockets. A área de contas, com django-allauth, oferece login, cadastro, recuperação de senha e gestão de e-mail.

## Stack tecnológica

- **Framework**: Django 6 com Python 3.14+
- **Tempo real**: Django Channels com Daphne e Redis como channel layer
- **Banco de dados**: SQLite (configurável via `DATABASE_URL`)
- **Cache e canais**: Redis (django-redis e channels-redis)
- **Autenticação**: django-allauth (login por e-mail, cadastro, recuperação de senha)
- **Front-end**: templates Django, HTMX (django-htmx), Tailwind CSS (django-tailwind) e Heroicons
- **Configuração**: django-environ para variáveis de ambiente

## Configuração

Para configurar o projeto, copie `.env.example` para `.env` e ajuste os valores. No mínimo, defina uma `SECRET_KEY` forte, configure `DEBUG` (ON/OFF), `ALLOWED_HOSTS` (valores separados por vírgula), `DATABASE_URL` (por exemplo `sqlite:///db.sqlite3`) e `REDIS_URL` (por exemplo `redis://localhost:6379/0`). O Redis é necessário para os WebSockets e o cache; em desenvolvimento você pode subir o serviço com Docker: `docker compose up -d redis`.

## Executando localmente

É recomendável usar um ambiente virtual. Os exemplos abaixo assumem que você está na raiz do projeto.

Instale as dependências:

```bash
uv sync
```

Ou, se usar pip:

```bash
pip install -e .
```

Suba o Redis (se ainda não estiver rodando):

```bash
docker compose up -d redis
```

Aplique as migrações:

```bash
python manage.py migrate
```

Para desenvolvimento, inicie o servidor e o Tailwind com um único comando:

```bash
python manage.py tailwind dev
```

Acesse `http://127.0.0.1:8000` no navegador.

A página inicial fica em `/`, e as salas de chat em `/chat/`. O painel administrativo Django fica em `/admin/`. As contas (login, cadastro, etc.) ficam em `/accounts/`.

## URLs

Em desenvolvimento o site fica em `http://127.0.0.1:8000`. Principais rotas:

- `/` — Página inicial
- `/chat/home/` — Início do chat (listagem de conversas)
- `/chat/create/` — Criar nova sala
- `/chat/<identifier>/` — Sala de conversa
- `/chat/users/@<username>/` — Iniciar chat com usuário
- `/chat/edit/<identifier>/` — Editar sala
- `/chat/leave/<identifier>/` — Sair da sala
- `/chat/delete/<identifier>/` — Excluir sala
- `/accounts/` — Login, cadastro, recuperação de senha e gestão de conta
- `/admin/` — Painel administrativo Django

## Como se tornar administrador

O login e o cadastro são feitos pelo django-allauth em `/accounts/`. Para acessar o painel em `/admin/`, é preciso ser um usuário com status de *staff* (e, para acesso total, *superuser*). O único jeito de conceder isso é pelo shell do Django:

```bash
python manage.py shell
```

No shell:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(email="email@exemplo.com")  # Use o e-mail da conta
u.is_staff = True
u.is_superuser = True  # Opcional, para acesso total ao admin
u.save()
```

## Licença

Esta aplicação está licenciada sob a licença [CC BY-NC-ND 4.0](./LICENSE).
