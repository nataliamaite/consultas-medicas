# Integração com Asaas

## Objetivo

O projeto pode ser estendido futuramente para integrar pagamentos utilizando a API do Asaas.

Neste momento, a integração de pagamentos não faz parte do fluxo principal da aplicação. A proposta apresentada neste documento utiliza uma arquitetura preparada para receber a integração sem acoplar o agendamento diretamente ao provedor de pagamentos.

## Arquitetura proposta

O fluxo futuro seria:

```text
Cliente
   |
   v
API de Agendamento
   |
   v
Criação da Consulta
   |
   v
Serviço de Pagamento
   |
   v
Asaas API
   |
   +----> Pagamento aprovado
   |
   +----> Pagamento pendente
   |
   +----> Pagamento recusado
