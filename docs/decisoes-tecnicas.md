# Decisões Técnicas

## 1. Objetivo do projeto

A API de Consultas Médicas foi desenvolvida para disponibilizar operações de gerenciamento de profissionais e consultas médicas por meio de uma API RESTful.

A aplicação permite:

* cadastrar, consultar, atualizar e remover profissionais;
* cadastrar, consultar, atualizar e remover consultas;
* associar consultas a profissionais;
* consultar as consultas vinculadas a um profissional;
* autenticar usuários por JWT;
* validar e sanitizar dados de entrada;
* executar testes automatizados;
* executar a aplicação em ambiente Docker;
* disponibilizar documentação interativa da API.

---

## 2. Python e Django

Foi utilizado Python com Django por oferecer uma estrutura consolidada para desenvolvimento de aplicações web, além de fornecer recursos de segurança, ORM, gerenciamento de configurações e organização modular.

O Django ORM também permite trabalhar com o banco de dados por meio de consultas parametrizadas, reduzindo a necessidade de construção manual de SQL e contribuindo para a prevenção de SQL Injection.

---

## 3. Django REST Framework

O Django REST Framework foi utilizado para implementar a API REST.

A escolha foi motivada pela integração com Django e pela disponibilidade de recursos como:

* serializers;
* ViewSets;
* routers;
* autenticação;
* permissões;
* respostas HTTP;
* suporte a testes de APIs.

Os `ModelViewSet` foram utilizados para reduzir código repetitivo na implementação das operações CRUD.

---

## 4. PostgreSQL

O PostgreSQL foi escolhido como banco de dados relacional por oferecer:

* consistência dos dados;
* suporte a relacionamentos entre entidades;
* integridade referencial;
* bom suporte para aplicações backend;
* compatibilidade com Django.

A relação entre profissionais e consultas é representada por uma chave estrangeira.

---

## 5. Poetry

O Poetry foi utilizado para gerenciamento das dependências e do ambiente Python.

As dependências do projeto são declaradas no `pyproject.toml` e o arquivo `poetry.lock` permite reproduzir versões consistentes das dependências utilizadas no projeto.

---

## 6. Docker

A aplicação foi containerizada utilizando Docker.

Foram definidos dois serviços principais:

* `web`: aplicação Django;
* `db`: PostgreSQL.

O Docker Compose permite executar os serviços de forma integrada e reproduzir o ambiente local com maior facilidade.

O banco utilizado pelo container é separado do PostgreSQL instalado diretamente na máquina.

---

## 7. Autenticação JWT

A API utiliza JSON Web Token (JWT) para autenticação.

Foi escolhido JWT por ser adequado para APIs REST e permitir autenticação sem manter uma sessão tradicional no servidor.

Os endpoints da API exigem autenticação, enquanto os endpoints de obtenção e renovação do token são utilizados para iniciar e manter a sessão de acesso.

Endpoints relacionados:

* `POST /api/token/`
* `POST /api/token/refresh/`

---

## 8. CORS

Foi utilizado `django-cors-headers` para controlar as origens que podem realizar requisições à API.

Durante o desenvolvimento local são permitidas as origens utilizadas pela aplicação local.

A configuração evita utilizar `CORS_ALLOW_ALL_ORIGINS=True`, reduzindo a exposição desnecessária da API.

Em ambientes de staging e produção, as origens deverão ser configuradas especificamente para os domínios autorizados.

---

## 9. Validação e sanitização

Os serializers do Django REST Framework são responsáveis pela validação dos dados recebidos pela API.

Foram implementadas validações para:

* campos obrigatórios;
* valores vazios;
* espaços em branco;
* tamanho máximo dos campos;
* existência do profissional relacionado a uma consulta.

Valores com espaços no início e no final são tratados antes da persistência.

A aplicação utiliza o ORM do Django para acesso ao banco, evitando a construção manual de consultas SQL a partir de entradas do usuário.

---

## 10. Logs

Foi implementado middleware para registrar informações básicas das requisições:

* método HTTP;
* caminho acessado;
* código de status da resposta.

Os logs não devem armazenar informações sensíveis, como senhas, tokens JWT ou dados completos das requisições.

---

## 11. Testes automatizados

Foram utilizados testes do `APITestCase` do Django REST Framework.

Os testes cobrem:

* criação de profissionais;
* listagem de profissionais;
* consulta individual;
* atualização;
* exclusão;
* criação de consultas;
* listagem de consultas;
* atualização e exclusão;
* busca de consultas por profissional;
* dados obrigatórios ausentes;
* profissional inexistente;
* acesso sem autenticação.

Os testes são executados localmente e também no pipeline de CI.

---

## 12. Ruff

O Ruff foi utilizado para análise estática e padronização do código Python.

O pipeline de CI executa o Ruff antes dos testes, permitindo identificar problemas de estilo e possíveis erros antes da construção da imagem Docker.

---

## 13. Documentação da API

Foi utilizado `drf-spectacular` para geração da documentação OpenAPI.

A API disponibiliza:

* Swagger UI: `/api/docs/`;
* Redoc: `/api/redoc/`;
* OpenAPI Schema: `/api/schema/`.

A documentação permite visualizar e testar os endpoints diretamente pelo navegador, incluindo autenticação JWT.

---

## 14. CI/CD

O projeto utiliza GitHub Actions para automação do processo de integração contínua.

O pipeline atual executa:

1. Lint;
2. Testes automatizados;
3. Build da imagem Docker.

O objetivo da etapa de CI é impedir que alterações com problemas de qualidade, testes quebrados ou falhas na construção da imagem avancem para o processo de deploy.

A etapa de CD será responsável posteriormente pelos deployments nos ambientes de staging e produção da AWS.

---

## 15. Separação entre staging e produção

Os ambientes de staging e produção serão mantidos separados.

Cada ambiente deverá possuir suas próprias configurações e recursos, incluindo banco de dados e variáveis sensíveis.

As credenciais e configurações específicas de cada ambiente não serão armazenadas no código-fonte.

---

## 16. Gerenciamento de configurações

Informações sensíveis e configurações dependentes do ambiente são obtidas por variáveis de ambiente.

O arquivo `.env` é utilizado apenas no ambiente local e está incluído no `.gitignore`.

Em CI/CD e AWS, essas configurações deverão ser fornecidas por mecanismos seguros de gerenciamento de secrets e variáveis de ambiente.

---

## 17. Estratégia de deploy

A aplicação será distribuída como imagem Docker.

A estratégia planejada é utilizar um registry de imagens e um serviço de containers na AWS, permitindo que a mesma imagem validada pelo pipeline seja promovida entre os ambientes.

A identificação das imagens por commit permite rastrear exatamente qual versão está sendo executada em cada ambiente.

---

## 18. Estratégia de rollback

O rollback será baseado em versões imutáveis da imagem Docker.

Cada build de deploy deverá ser associado ao SHA do commit correspondente.

Caso uma versão apresente problemas em produção, a infraestrutura poderá retornar para a versão anterior conhecida como estável.

O procedimento detalhado está documentado em:

`docs/rollback.md`

---

## 19. Decisões futuras

Algumas funcionalidades podem ser adicionadas posteriormente:

* integração com Asaas para pagamentos e split;
* melhoria da observabilidade;
* utilização de HTTPS com domínio próprio;
* configuração de escalabilidade;
* pipeline de deploy com aprovação para produção;
* estratégias mais avançadas de deployment, como Blue/Green.

Essas funcionalidades não devem comprometer a simplicidade e a segurança da versão inicial.
