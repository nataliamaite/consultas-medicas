# Estratégia de Rollback

## Objetivo

A estratégia de rollback tem como objetivo permitir a reversão rápida da aplicação para uma versão estável anterior caso uma nova versão apresente falhas em staging ou produção.

A estratégia escolhida utiliza imagens Docker versionadas pelo SHA do commit do Git, permitindo identificar exatamente qual versão do código está sendo executada.

## Estratégia de versionamento

Cada imagem Docker publicada no Amazon ECR será identificada pelo SHA do commit responsável pela versão.

Exemplo:

```text
api-consultas-medicas:8f31a2c
```

Dessa forma, diferentes versões da aplicação podem coexistir no repositório de imagens, sem depender exclusivamente de uma tag como `latest`.

O uso do SHA torna cada versão imutável e facilita a identificação da versão que deve ser restaurada.

## Processo de deploy

O fluxo planejado será:

```text
GitHub
   ↓
GitHub Actions
   ↓
Lint
   ↓
Testes
   ↓
Build Docker
   ↓
Push para Amazon ECR
   ↓
Deploy em Staging
   ↓
Validação
   ↓
Deploy em Produção
```

Cada deploy será associado ao SHA do commit correspondente.

## Processo de rollback

Caso uma versão apresente problemas em produção, será possível retornar para a imagem Docker correspondente à versão anterior.

Exemplo:

```text
Versão atual:
api-consultas-medicas:8f31a2c

Versão anterior estável:
api-consultas-medicas:72ab91d
```

O rollback consiste em atualizar o serviço da aplicação para utilizar novamente a imagem:

```text
api-consultas-medicas:72ab91d
```

No ambiente AWS, o serviço será atualizado para utilizar a revisão anterior da Task Definition do ECS, mantendo a imagem Docker correspondente à versão estável.

## Rollback via GitHub Actions

O pipeline de CI/CD deverá possuir uma execução manual para rollback.

A execução receberá como parâmetro o SHA da versão que deve ser restaurada.

Exemplo conceitual:

```text
workflow_dispatch
        ↓
informar IMAGE_TAG
        ↓
validar imagem no ECR
        ↓
atualizar Task Definition
        ↓
atualizar serviço ECS
        ↓
aguardar estabilização
        ↓
confirmar deployment
```

Isso permite realizar uma reversão sem precisar alterar o código-fonte ou criar um novo commit apenas para desfazer uma alteração.

## Critérios para executar rollback

O rollback poderá ser executado quando ocorrer, por exemplo:

* falha no health check da aplicação;
* aumento significativo de erros HTTP 5xx;
* falha em funcionalidades críticas;
* erro de configuração;
* problemas de integração com banco de dados ou serviços externos;
* regressão identificada após o deploy;
* indisponibilidade da aplicação após uma nova versão.

## Staging e produção

O rollback será independente entre os ambientes.

Uma versão problemática em staging poderá ser revertida sem afetar produção.

Da mesma forma, um rollback em produção não deverá alterar o ambiente de staging.

Os ambientes utilizarão configurações e recursos separados.

## Banco de dados e migrations

As migrations do Django exigem atenção especial durante um rollback.

Alterações compatíveis e retrocompatíveis deverão ser priorizadas para evitar que uma versão anterior da aplicação deixe de funcionar devido ao estado do banco de dados.

Para alterações destrutivas de banco, recomenda-se utilizar uma estratégia em etapas:

1. adicionar a nova estrutura;
2. executar o deploy da aplicação compatível com as duas estruturas;
3. migrar os dados;
4. remover estruturas antigas somente após confirmação da estabilidade.

Dessa forma, o rollback da aplicação não depende necessariamente de desfazer imediatamente alterações no banco.

## Objetivo da estratégia

A estratégia busca garantir:

* versões Docker identificáveis;
* possibilidade de retornar para uma versão estável;
* menor tempo de indisponibilidade;
* rastreabilidade dos deployments;
* separação entre staging e produção;
* rollback controlado através do GitHub Actions;
* redução do risco durante novas releases.

## Evolução futura

Como evolução da infraestrutura, a aplicação poderá utilizar estratégias como Blue/Green Deployment ou Canary Deployment utilizando recursos do Amazon ECS.

Essas estratégias podem permitir que uma nova versão seja validada antes de receber todo o tráfego da aplicação.
