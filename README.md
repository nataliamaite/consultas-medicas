# API de Consultas Médicas

API RESTful desenvolvida em Python com Django REST Framework para gerenciamento de profissionais e consultas médicas.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento, segurança, testes automatizados, documentação de API, containerização e CI/CD.

## Tecnologias

* Python 3.13
* Django
* Django REST Framework
* PostgreSQL
* Poetry
* Docker
* Docker Compose
* JWT
* CORS
* Swagger / OpenAPI
* ReDoc
* Ruff
* GitHub Actions
* AWS

## Funcionalidades

### Profissionais

* Criar profissional
* Listar profissionais
* Consultar profissional por ID
* Atualizar profissional
* Excluir profissional

Campos:

* Nome social
* Profissão
* Endereço
* Contato

### Consultas

* Criar consulta
* Listar consultas
* Consultar consulta por ID
* Atualizar consulta
* Excluir consulta
* Associar consulta a um profissional
* Buscar consultas por profissional

## Estrutura da API

### Profissionais

```text
GET     /api/profissionais/
POST    /api/profissionais/
GET     /api/profissionais/{id}/
PUT     /api/profissionais/{id}/
PATCH   /api/profissionais/{id}/
DELETE  /api/profissionais/{id}/
```

### Consultas

```text
GET     /api/consultas/
POST    /api/consultas/
GET     /api/consultas/{id}/
PUT     /api/consultas/{id}/
PATCH   /api/consultas/{id}/
DELETE  /api/consultas/{id}/
```

### Consultas por profissional

```text
GET /api/profissionais/{id}/consultas/
```

Esse endpoint retorna as consultas associadas ao profissional informado.

## Autenticação

A API utiliza autenticação baseada em JWT.

### Obter token

```text
POST /api/token/
```

Exemplo:

```json
{
    "username": "usuario",
    "password": "senha"
}
```

A resposta contém:

```json
{
    "refresh": "...",
    "access": "..."
}
```

O token de acesso deve ser enviado nas requisições protegidas:

```text
Authorization: Bearer <access_token>
```

### Renovar token

```text
POST /api/token/refresh/
```

## Segurança e validação

A aplicação possui mecanismos para reduzir riscos comuns e garantir a qualidade dos dados recebidos.

Entre as medidas implementadas:

* autenticação JWT;
* permissões para endpoints protegidos;
* validação de campos obrigatórios;
* rejeição de valores vazios;
* remoção de espaços desnecessários nos dados;
* validação da existência do profissional relacionado à consulta;
* uso do ORM do Django para acesso ao banco;
* configuração controlada de CORS;
* variáveis sensíveis armazenadas em ambiente;
* logs de acesso e erros;
* separação entre configurações locais e Docker.

O Django ORM utiliza consultas parametrizadas, reduzindo o risco de SQL Injection nas operações realizadas pela aplicação.

### Logging

A API possui logging separado para acessos e erros:

* `api.access` — registra método HTTP, endpoint e status da resposta;
* `django.request` — registra erros de requisição em nível `ERROR`.

Os logs são enviados para o console, facilitando sua utilização em ambientes Docker e AWS.

Para evitar exposição de informações sensíveis, a aplicação não registra intencionalmente senhas, tokens JWT, cabeçalhos de autenticação, corpo das requisições ou credenciais do banco de dados.

## Documentação da API

A API possui documentação OpenAPI gerada automaticamente.

### Swagger UI

```text
/api/docs/
```

### ReDoc

```text
/api/redoc/
```

### OpenAPI Schema

```text
/api/schema/
```

A documentação permite visualizar os endpoints, modelos de dados, parâmetros e autenticação JWT.

## Testes automatizados

Os testes foram implementados utilizando `APITestCase` do Django REST Framework.

São testados, entre outros:

* CRUD de profissionais;
* CRUD de consultas;
* busca de consultas por profissional;
* dados obrigatórios;
* dados inválidos;
* profissional inexistente;
* autenticação;
* endpoints protegidos.

### Executar testes localmente

```bash
poetry run python manage.py test
```

### Executar testes no Docker

```bash
docker compose exec web poetry run python manage.py test
```

## Qualidade de código

O projeto utiliza Ruff para análise estática e padronização do código.

Executar:

```bash
poetry run ruff check .
```

O pipeline de CI também executa essa verificação automaticamente.

## Execução local

### Pré-requisitos

Instale:

* Python 3.13
* Poetry
* PostgreSQL
* Git

### Clonar o projeto

```bash
git clone https://github.com/nataliamaite/consultas-medicas.git
cd consultas-medicas
```

### Instalar dependências

```bash
poetry install
```

### Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DJANGO_SECRET_KEY=sua-chave-secreta
DEBUG=True

POSTGRES_DB=consultas_medicas
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua-senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

O arquivo `.env` não deve ser versionado.

### Executar migrations

```bash
poetry run python manage.py migrate
```

### Criar usuário administrador

```bash
poetry run python manage.py createsuperuser
```

### Executar aplicação

```bash
poetry run python manage.py runserver
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000/
```

Documentação:

```text
http://127.0.0.1:8000/api/docs/
```

## Execução com Docker

O projeto também pode ser executado utilizando Docker Compose.

### Subir os containers

```bash
docker compose up --build
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000/
```

### Verificar containers

```bash
docker compose ps
```

### Executar migrations

```bash
docker compose exec web poetry run python manage.py migrate
```

### Criar superusuário

```bash
docker compose exec web poetry run python manage.py createsuperuser
```

### Executar testes

```bash
docker compose exec web poetry run python manage.py test
```

### Parar a aplicação

```bash
docker compose down
```

Os dados do PostgreSQL são armazenados em um volume Docker.

## CI/CD

O projeto utiliza GitHub Actions para automatizar o processo de integração contínua.

O pipeline de CI possui as seguintes etapas:

```text
Push / Pull Request
        ↓
Lint
        ↓
Testes
        ↓
Build Docker
```

### Lint

O Ruff verifica problemas de qualidade e padronização do código.

### Testes

O pipeline executa os testes automatizados utilizando PostgreSQL como serviço.

### Build

Após a aprovação dos testes, uma imagem Docker da aplicação é construída.

## Ambientes

O projeto foi estruturado para trabalhar com ambientes separados:

```text
Staging
Produção
```

O ambiente de staging será utilizado para validar novas versões antes da publicação em produção.

Cada ambiente deverá possuir suas próprias configurações e recursos de infraestrutura.

Informações sensíveis, como senhas, chaves e credenciais, não são armazenadas no código-fonte.

## Deploy na AWS

A arquitetura planejada para produção utiliza serviços AWS para execução da aplicação e armazenamento dos dados.

Componentes previstos:

```text
GitHub
   ↓
GitHub Actions
   ↓
Amazon ECR
   ↓
Amazon ECS / Fargate
   ↓
Django REST API
   ↓
Amazon RDS PostgreSQL
```

O ambiente de staging será mantido separado do ambiente de produção.

As imagens Docker serão versionadas utilizando o SHA do commit, permitindo rastrear exatamente qual versão da aplicação está em execução.

## Estratégia de deployment

O fluxo planejado é:

```text
Código
   ↓
Lint
   ↓
Testes
   ↓
Build
   ↓
Push da imagem para ECR
   ↓
Deploy Staging
   ↓
Validação
   ↓
Deploy Produção
```

A publicação em produção será protegida por uma etapa de aprovação.

## Rollback

O projeto utiliza imagens Docker versionadas por SHA do commit.

Caso uma versão apresente problemas, será possível retornar para uma versão anterior estável.

Exemplo:

```text
Versão atual:
api-consultas-medicas:8f31a2c

Versão anterior:
api-consultas-medicas:72ab91d
```

O serviço poderá ser atualizado novamente para a versão estável.

A estratégia completa está documentada em:

```text
docs/rollback.md
```

## Decisões técnicas

As principais decisões arquiteturais estão documentadas em:

```text
docs/decisoes-tecnicas.md
```

O documento explica as escolhas relacionadas a:

* Django;
* Django REST Framework;
* PostgreSQL;
* Poetry;
* Docker;
* JWT;
* CORS;
* validação;
* testes;
* logs;
* Swagger;
* CI/CD;
* ambientes;
* deployment;
* rollback.

## Problemas encontrados

Durante o desenvolvimento foram registrados problemas e respectivas soluções, incluindo:

* conflito de porta do PostgreSQL;
* conflito entre Docker e Podman;
* problemas de instalação do projeto com Poetry;
* conflito de porta da aplicação;
* configuração do OpenAPI;
* autenticação JWT no Swagger;
* diferença entre banco local e banco Docker.

Documentação:

```text
docs/problemas-encontrados.md
```

## Estrutura do projeto

```text
api-consultas-medicas/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── middleware.py
│   └── ...
│
├── profissionais/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── docs/
│   ├── decisoes-tecnicas.md
│   ├── problemas-encontrados.md
│   └── rollback.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── manage.py
├── poetry.lock
└── pyproject.toml
```

### CORS

A API utiliza uma política restritiva de CORS, permitindo somente as origens explicitamente configuradas por variável de ambiente.

A configuração é feita por meio da variável:

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

O projeto não utiliza `CORS_ALLOW_ALL_ORIGINS`, evitando que requisições de qualquer origem sejam autorizadas.

Em ambientes de staging e produção, as origens permitidas devem ser substituídas pelos respectivos domínios da aplicação, mantendo a política de allowlist.

Exemplo:

```env
CORS_ALLOWED_ORIGINS=https://staging.exemplo.com
```

As configurações específicas de cada ambiente devem ser mantidas fora do código-fonte e fornecidas por variáveis de ambiente.


## Autora

**Natália Maitê Guimarães Santos**

Bacharel em Ciência da Computação — UEPB

GitHub:

```text
https://github.com/nataliamaite
```

Projeto:

```text
https://github.com/nataliamaite/consultas-medicas
```
