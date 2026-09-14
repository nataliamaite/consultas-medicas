# Problemas Encontrados e Soluções

## 1. Conexão com PostgreSQL local

### Problema

Durante a configuração inicial do PostgreSQL, a porta padrão `5432` já estava sendo utilizada por outro banco/projeto.

### Solução

Foi utilizado o PostgreSQL local na porta `5433`.

No ambiente Docker, o PostgreSQL continua utilizando a porta interna padrão `5432`, pois a comunicação entre os containers ocorre pela rede interna do Docker.

### Resultado

Foi possível manter o banco local e o banco utilizado pelo Docker separados.

---

## 2. Conflito entre Docker e Podman

### Problema

Em alguns momentos, o comando `docker` estava tentando utilizar o socket do Podman:

```text
unix:///run/user/1000/podman/podman.sock
```

Isso impedia comandos como `docker compose exec` de acessar o Docker Engine.

### Solução

Foi removida temporariamente a variável `DOCKER_HOST` da sessão:

```bash
unset DOCKER_HOST
```

E o contexto padrão do Docker foi selecionado:

```bash
docker context use default
```

### Resultado

O Docker voltou a utilizar o socket correto do Docker Engine.

### Melhoria futura

A configuração do ambiente deverá ser revisada para evitar que `DOCKER_HOST` volte a apontar automaticamente para o Podman.

---

## 3. Falha inicial no GitHub Actions

### Problema

O pipeline de CI falhou durante a instalação das dependências com o erro relacionado à instalação do próprio projeto:

```text
The current project could not be installed:
No file/folder found for package api-consultas-medicas
```

### Causa

O Poetry estava tentando instalar o projeto como um pacote Python, embora a aplicação não estivesse estruturada como uma biblioteca Python distribuível.

### Solução

Foi utilizado:

```bash
poetry install --no-interaction --no-root
```

A opção `--no-root` impede que o Poetry tente instalar o projeto como pacote.

### Resultado

O pipeline passou a instalar corretamente as dependências e o CI foi executado com sucesso.

---

## 4. Porta 8000 ocupada

### Problema

Ao tentar executar:

```bash
poetry run python manage.py runserver
```

foi apresentada a mensagem:

```text
Error: That port is already in use.
```

### Investigação

Foi utilizado:

```bash
sudo lsof -nP -iTCP:8000 -sTCP:LISTEN
```

A investigação mostrou que a porta estava sendo utilizada pelo Docker.

### Causa

O Docker Compose já estava expondo:

```yaml
ports:
  - "8000:8000"
```

Portanto, uma segunda instância do Django não poderia utilizar a mesma porta.

### Solução

A aplicação foi acessada através do container já em execução.

---

## 5. Erro na geração do OpenAPI

### Problema

Após a instalação do `drf-spectacular`, a interface do Swagger carregava, mas `/api/schema/` retornava HTTP 500.

### Erro identificado

O erro indicava:

```text
Incompatible AutoSchema used on View
```

e recomendava configurar o `DEFAULT_SCHEMA_CLASS`.

### Solução

Foi adicionada ao `REST_FRAMEWORK` a configuração:

```python
"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
```

### Resultado

O schema OpenAPI passou a ser gerado corretamente e o Swagger UI foi disponibilizado.

---

## 6. Configuração de autenticação no Swagger

### Problema

O Swagger inicialmente não possuía uma definição visual para autenticação JWT.

### Solução

Foi configurado um esquema de segurança Bearer JWT no `SPECTACULAR_SETTINGS`.

Isso permitiu utilizar o botão `Authorize` diretamente no Swagger.

### Resultado

Foi possível:

1. obter um token JWT;
2. autorizar o Swagger;
3. executar endpoints protegidos;
4. receber respostas autenticadas.

---

## 7. GET aparentemente vazio no Swagger

### Problema

Durante os testes, o endpoint de listagem de profissionais parecia retornar:

```json
[]
```

mesmo existindo profissionais no banco.

### Investigação

Foi verificado:

* banco PostgreSQL;
* quantidade de registros;
* `ProfissionalViewSet`;
* `ProfissionalSerializer`;
* autenticação JWT;
* documentação Swagger.

A consulta direta pelo Django ORM confirmou que os registros existiam e que o serializer os retornava corretamente.

### Causa

O endpoint GET consultado no Swagger não era o endpoint correto.

### Resultado

Após selecionar o endpoint correto, a listagem dos profissionais funcionou normalmente.

### Aprendizado

A investigação demonstrou a importância de validar cada camada da aplicação separadamente:

```text
Banco → Model → Serializer → ViewSet → URL → Autenticação → Cliente
```

---

## 8. Separação entre banco local e banco Docker

### Problema

Foi necessário compreender por que dados existentes no PostgreSQL local não apareciam automaticamente na aplicação executada pelo Docker.

### Causa

O Docker Compose utiliza um serviço PostgreSQL próprio:

```yaml
db:
  image: postgres:17
```

Esse serviço possui seu próprio volume persistente.

### Solução

Foi mantida a separação entre:

* PostgreSQL local;
* PostgreSQL utilizado pelo Docker.

### Resultado

O ambiente Docker tornou-se reproduzível sem depender do banco instalado diretamente na máquina.

---

## 9. Práticas adotadas após os problemas

A partir dos problemas encontrados, foram adotadas algumas práticas:

* verificar logs antes de alterar código;
* utilizar comandos de diagnóstico para identificar processos e portas;
* testar componentes isoladamente;
* manter banco local e Docker separados;
* utilizar CI para validar lint, testes e build;
* evitar armazenamento de secrets no Git;
* documentar problemas e respectivas soluções;
* utilizar imagens Docker versionadas no processo de deploy.
