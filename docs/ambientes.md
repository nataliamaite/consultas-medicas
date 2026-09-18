# Ambientes da Aplicação

## Visão geral

O projeto utiliza ambientes separados de acordo com a finalidade de cada etapa do ciclo de desenvolvimento.

| Ambiente | Finalidade | Status |
|---|---|---|
| Local | Desenvolvimento e testes durante a implementação | Disponível |
| Staging | Validação da aplicação antes da produção | Planejado |
| Produção | Execução da aplicação para uso real | Disponível |

## Ambiente Local

O ambiente local é utilizado durante o desenvolvimento.

Principais características:

- Django + Django REST Framework
- PostgreSQL local
- Execução com Poetry
- Docker/ Docker Compose para reprodução do ambiente
- Testes automatizados
- Ruff para análise de código
- Swagger e Redoc para documentação da API

As configurações locais são armazenadas em `.env` e não são versionadas.

## Ambiente de Staging

O ambiente de staging será utilizado para validar uma versão da aplicação antes de sua publicação em produção.

A proposta é manter uma infraestrutura independente da produção, incluindo:

- banco de dados próprio;
- variáveis de ambiente próprias;
- serviço ECS separado;
- recursos de armazenamento/logs separados;
- imagem Docker específica da versão candidata.

Fluxo planejado:

```text
develop
   ↓
GitHub Actions
   ↓
Lint
   ↓
Testes
   ↓
Build
   ↓
Deploy Staging
   ↓
Validação
   ↓
main
