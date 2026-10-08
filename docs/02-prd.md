# PRD — SmartFlow Hub

**Versão:** 1.0 — diagnóstico e definição inicial  
**Data:** 08/10/2026  
**Status:** rascunho para validação de produto  
**Fontes:** código e configurações existentes no repositório. O arquivo `docs/01-project-audit.md`, solicitado como fonte, não estava presente no workspace durante esta elaboração.

## 0. Convenções e limites

Este documento não transforma intenção em requisito aprovado. Cada item recebe uma classificação:

- **[IMPLEMENTADO]**: existe código correspondente, ainda que possa conter defeitos ou não estar pronto para produção.
- **[PARCIAL/PREVISTO]**: existe estrutura, caso de uso, modelo ou menção no roadmap, mas o fluxo está incompleto ou não está exposto.
- **[PROPOSTA — APROVAÇÃO NECESSÁRIA]**: requisito novo ou decisão de produto sugerida.

“Implementado” não significa “validado”: a análise encontrou inconsistências entre entidades, DTOs, rotas e repositórios. Este PRD descreve o produto desejável sem ocultar o estado real.

## 1. Visão e objetivos do produto

### 1.1 Visão

O SmartFlow Hub pretende ser uma plataforma multiempresa para centralizar e automatizar atendimento conversacional em canais digitais, começando por WhatsApp, combinando bots com IA e transferência para atendimento humano.

Evidências da direção atual: `README.md`; entidades em `backend/app/domain/entities/`; webhook em `backend/app/adapters/controllers/webhook_whatsapp_routes.py`; integração OpenAI em `backend/app/infrastructure/gateways/ai_responder_gateway_openai.py`.

### 1.2 Objetivos

- **[IMPLEMENTADO]** Disponibilizar uma API organizada por clientes/tenants, usuários, clientes finais, conversas e mensagens.
- **[IMPLEMENTADO]** Receber um payload simplificado de WhatsApp, analisar conteúdo com OpenAI e enviar texto pela Graph API.
- **[PARCIAL/PREVISTO]** Alternar uma conversa entre atendimento automatizado e humano.
- **[PARCIAL/PREVISTO]** Administrar tenants, usuários/bots, clientes finais e conversas por uma interface web.
- **[PROPOSTA]** Entregar um MVP seguro e observável no qual uma organização configure um número WhatsApp, receba mensagens, responda por bot e assuma conversas manualmente sem vazamento entre tenants.

### 1.3 Objetivos mensuráveis propostos

Dependem de aprovação de produto e operação:

- 100% das requisições de negócio autenticadas e isoladas por tenant.
- 100% dos webhooks válidos persistidos de modo idempotente antes do processamento de IA.
- Estado de entrega rastreável para toda mensagem outbound.
- Um fluxo ponta a ponta automatizado e um fluxo de transferência humana cobertos por testes de aceitação.
- Metas de latência, disponibilidade, retenção e taxa de automação permanecem pendentes de decisão humana.

## 2. Público-alvo e problemas resolvidos

### 2.1 Público-alvo inferido

**[INFERÊNCIA A VALIDAR]** Pequenas e médias organizações que recebem atendimento recorrente pelo WhatsApp e precisam combinar automação com operadores humanos. O código modela `Client` como tenant, usuários `BOT`/`HUMAN`, clientes finais, conversas e mensagens (`domain/entities/`).

### 2.2 Usuários do sistema

- **Administrador da plataforma:** provisiona tenants e planos. **[PARCIAL]** Há API de clientes, sem autorização aplicada.
- **Administrador do tenant:** configura usuários, bots, canais e políticas. **[PARCIAL/PROPOSTA]** Modelos existem; jornada administrativa não está completa.
- **Agente de atendimento:** acompanha, assume e resolve conversas. **[PARCIAL]** Domínio/casos de uso existem; UI e atribuição HTTP estão incompletas.
- **Cliente final:** conversa pelo WhatsApp. **[PARCIAL]** Entrada e resposta existem em código, mas o payload não é o nativo da Meta.
- **Sistema integrador:** usa API key/webhook. **[PARCIAL/PROPOSTA]** API key é gerada, mas não é validada em middleware.

### 2.3 Problemas a resolver

- Atendimento disperso e sem histórico centralizado.
- Volume repetitivo que pode ser respondido por automação.
- Necessidade de encaminhar exceções ao humano preservando contexto.
- Administração multiempresa com isolamento de dados.
- Visibilidade do estado de conversas e mensagens.

Os dois últimos são necessidades coerentes com o modelo, mas sua priorização deve ser validada.

## 3. Escopo e funcionalidades

### 3.1 Já implementado no código

| Capacidade | Interface existente | Observações |
| --- | --- | --- |
| Health check | `GET /health` | Retorno estático; não verifica dependências. |
| Login | `POST /auth/login` | bcrypt/JWT; provável defeito no cálculo de expiração e token não protege rotas. |
| Tenants | criar, listar, obter, editar, trocar plano, desativar, excluir | Há erros de response model/listagem em `client_routes.py`. |
| Usuários | criar, listar, obter, excluir | Tipos humano/bot, nível de acesso e prompt. Assinaturas de repositório/uso divergem. |
| Clientes finais | criar, obter, excluir | Casos de update/list existem, sem rotas correspondentes. |
| Conversas | listar, filtrar por status/cliente, obter, escalar, resolver | IDs/tenant inconsistentes; atribuição não exposta. |
| Mensagens | criar, obter, listar por usuário/cliente, excluir | Contrato diverge da entidade baseada em conversa. |
| Webhook WhatsApp | verificar e receber | DTO simplificado, sem assinatura/idempotência. |
| OpenAI | gerar resposta via Chat Completions | Prompt global ou por bot; “confiança” inferida do finish reason. |
| Envio WhatsApp | texto via Graph API v19.0 | Sem processamento confiável de callbacks/status. |
| Frontend | tema, navbar, `/test` de health | Sem fluxos de produto; layout descarta children. |

### 3.2 Previsto ou parcialmente implementado

- CRUD completo de clientes finais e usuários.
- Alteração de senha, desativação e usuário atual.
- Criação de conversa, atribuição a agente e retorno ao bot.
- Recepção, fila, despacho, envio e atualização de estado de mensagens.
- Vínculo de bot a canal por `user_channel_bindings`.
- Atendimento híbrido bot/humano.
- Frontend autenticado para operação.
- Redis e worker Celery/RQ, Instagram, campanhas, fluxos, templates, dashboard, métricas, NGINX e CI/CD citados no `README.md`, mas sem implementação encontrada.

### 3.3 Novas propostas sujeitas a aprovação

- Inbox unificada com fila, busca, filtros e atualização em tempo real.
- Política configurável de automação/escalonamento.
- Trilha de auditoria administrativa e operacional.
- Idempotência, fila de eventos e dead-letter queue.
- Gestão segura de credenciais por canal.
- Dashboard operacional mínimo.
- Exportação/anonimização/eliminação de dados para LGPD.
- Limites por plano e medição de consumo.

## 4. Personas, jornadas e fluxos

### 4.1 Persona: administrador da plataforma

**Objetivo:** provisionar e manter tenants.  
**Jornada proposta:** autenticar → listar tenants → criar tenant → entregar API key uma única vez → escolher plano → desativar/reativar.  
**Estado atual:** APIs parciais e desprotegidas; reativação não é exposta.

### 4.2 Persona: administrador do tenant

**Objetivo:** preparar a operação.  
**Jornada proposta:** entrar → cadastrar agentes/bot → vincular número WhatsApp → definir prompt/política → validar canal → acompanhar saúde.  
**Estado atual:** criação de usuário existe; binding só existe em ORM/repositório; não há tela nem API completa de configuração.

### 4.3 Persona: agente humano

**Objetivo:** atender exceções com contexto.  
**Jornada proposta:** entrar → visualizar fila escalada → abrir histórico → assumir conversa → enviar mensagens → resolver ou devolver ao bot.  
**Estado atual:** escalar/resolver existem; assumir, responder pela UI e devolver ao bot não estão completos.

### 4.4 Persona: cliente final

**Objetivo:** obter resposta pelo canal habitual.  
**Fluxo alvo proposto:** mensagem WhatsApp → confirmação de recebimento técnica → processamento → resposta automática ou encaminhamento → continuidade no mesmo histórico.  
**Estado atual:** existe tentativa síncrona de recepção/análise/resposta.

### 4.5 Fluxo técnico atual

`Webhook simplificado → localizar bot pelo número → receber mensagem → localizar/criar cliente final → OpenAI → criar/usar conversa → enfileirar e despachar resposta ou escalar → PostgreSQL/Graph API`.

## 5. Histórias de usuário

### 5.1 Implementadas ou parcialmente implementadas

- Como administrador da plataforma, quero criar um tenant e receber sua API key para provisioná-lo. **[IMPLEMENTADO COM DEFEITOS]**
- Como usuário, quero autenticar com e-mail e senha para receber um token. **[IMPLEMENTADO COM DEFEITO PROVÁVEL]**
- Como administrador do tenant, quero cadastrar humanos e bots. **[PARCIAL]**
- Como sistema, quero relacionar um número de canal a um bot para rotear webhooks. **[PARCIAL]**
- Como cliente final, quero enviar uma mensagem e obter resposta automatizada. **[PARCIAL]**
- Como bot, quero escalar uma conversa que requer humano. **[PARCIAL]**
- Como agente, quero resolver uma conversa. **[PARCIAL]**

### 5.2 Propostas

- Como agente, quero ver apenas conversas do meu tenant e permissões.
- Como agente, quero assumir uma conversa escalada atomicamente para evitar atendimento duplicado.
- Como agente, quero ver histórico e estado de entrega antes de responder.
- Como administrador, quero configurar quando o bot responde ou escala.
- Como administrador, quero rotacionar credenciais sem indisponibilidade.
- Como titular de dados, quero solicitar acesso, correção e eliminação quando aplicável.
- Como operador, quero reprocessar eventos falhos sem duplicar mensagens.

## 6. Requisitos funcionais

### Identidade e tenancy

- **RF-001 [IMPLEMENTADO/PARCIAL]** Autenticar usuário por e-mail/senha e emitir JWT.
- **RF-002 [PROPOSTA]** Validar JWT em toda rota não pública.
- **RF-003 [PROPOSTA]** Derivar tenant da identidade/credencial, nunca confiar apenas em `client_id` enviado.
- **RF-004 [PROPOSTA]** Aplicar permissões por papel e registrar ações sensíveis.

### Administração

- **RF-010 [IMPLEMENTADO COM DEFEITOS]** Administrar tenants, status e plano.
- **RF-011 [PARCIAL]** Administrar usuários humanos/bots, senha, status e prompt.
- **RF-012 [PARCIAL]** Vincular/desvincular credenciais de canal a bots.
- **RF-013 [PROPOSTA]** Exibir API key/segredo apenas na criação e permitir rotação/revogação.

### Clientes, conversas e mensagens

- **RF-020 [PARCIAL]** Criar/localizar cliente final por referência única de canal dentro do tenant.
- **RF-021 [PARCIAL]** Criar e consultar conversas isoladas por tenant.
- **RF-022 [PARCIAL]** Escalar, atribuir, resolver e devolver conversa ao bot.
- **RF-023 [PARCIAL]** Persistir mensagens inbound/outbound com direção, origem, estado, conteúdo/anexos e conversa.
- **RF-024 [PROPOSTA]** Impedir dois agentes de assumirem simultaneamente a mesma conversa.
- **RF-025 [PROPOSTA]** Registrar callbacks de envio, entrega, leitura e falha.

### Canais e IA

- **RF-030 [PARCIAL]** Validar e receber webhook WhatsApp.
- **RF-031 [PROPOSTA]** Aceitar o payload oficial da Meta, validar assinatura e deduplicar por ID externo.
- **RF-032 [IMPLEMENTADO/PARCIAL]** Gerar resposta OpenAI com prompt global ou do bot.
- **RF-033 [PROPOSTA]** Tornar política de resposta/escalonamento explícita e configurável.
- **RF-034 [PROPOSTA]** Processar IA/envio de modo assíncrono com retentativas limitadas.

### Interface

- **RF-040 [PARCIAL]** Disponibilizar aplicação web e tema.
- **RF-041 [PROPOSTA]** Login/logout e renovação/expiração de sessão.
- **RF-042 [PROPOSTA]** Inbox, histórico, composição de mensagem, filtros e estados vazios/erro.
- **RF-043 [PROPOSTA]** Administração conforme papel.

## 7. Requisitos não funcionais

- **RNF-001 Segurança:** negar por padrão; menor privilégio; segredos fora do código/logs.
- **RNF-002 Isolamento:** toda consulta/mutação de negócio deve incluir tenant efetivo.
- **RNF-003 Confiabilidade:** webhook deve ser idempotente; mensagens não podem duplicar por retry.
- **RNF-004 Consistência:** operações de persistência/estado devem ser transacionais; atribuição deve usar controle concorrente.
- **RNF-005 Observabilidade:** logs estruturados com correlation ID, métricas de fila/latência/falha e alertas, sem PII desnecessária.
- **RNF-006 Desempenho [PENDENTE]:** metas de API, webhook, inbox e IA precisam ser aprovadas.
- **RNF-007 Disponibilidade [PENDENTE]:** SLO, RPO e RTO precisam ser aprovados.
- **RNF-008 Acessibilidade [PROPOSTA]:** frontend conforme WCAG 2.1 AA.
- **RNF-009 Compatibilidade [PROPOSTA]:** duas últimas versões estáveis de Chrome, Edge, Firefox e Safari.
- **RNF-010 Evolução:** OpenAPI e migrations versionadas; testes bloqueiam regressões contratuais.
- **RNF-011 Privacidade:** retenção configurada/definida, criptografia em trânsito e proteção adequada em repouso.

## 8. Regras de negócio e permissões

### Regras comprovadas no domínio

- Mensagem exige conteúdo ou anexo (`domain/entities/message.py`).
- Somente mensagem outbound pendente pode ser marcada como enviada; transições de status são limitadas.
- Conversa só pode ser atribuída após escalonamento; resolver é idempotente; conversa resolvida não pode ser abandonada (`conversation.py`).
- Usuários podem ser humanos ou bots; cliente pode ser ativo/inativo e possuir plano.

### Regras propostas

- **RB-001:** dados de tenants distintos nunca se cruzam.
- **RB-002:** usuário inativo não autentica nem opera.
- **RB-003:** tenant inativo não processa novos eventos, salvo política explícita de preservação.
- **RB-004:** somente administrador da plataforma gerencia tenants/planos.
- **RB-005:** administrador do tenant gerencia usuários, bots e canais do próprio tenant.
- **RB-006:** agente lê/atua somente nas conversas permitidas; regra de equipe é pendente.
- **RB-007:** webhook duplicado retorna sucesso sem recriar mensagem/resposta.
- **RB-008:** uma conversa resolvida só reabre mediante regra aprovada (nova conversa ou reabertura).
- **RB-009:** falha da IA não deve perder inbound; deve escalar ou aguardar retry conforme política.
- **RB-010:** API key e tokens nunca retornam novamente em texto claro.

### Matriz proposta de permissões

| Ação | Plataforma | Admin tenant | Agente | Bot/integração |
| --- | --- | --- | --- | --- |
| Gerir tenants/planos | sim | não | não | não |
| Gerir usuários/canais próprios | suporte excepcional | sim | não | não |
| Ver conversas do tenant | suporte auditado | sim | conforme escopo | somente fluxo próprio |
| Assumir/responder/resolver | não | configurável | sim | bot responde conforme política |
| Configurar automação | não | sim | não | não |

Toda a matriz requer aprovação humana.

## 9. Critérios de aceitação verificáveis

### Autenticação e isolamento

1. Credencial válida retorna JWT com expiração futura; senha inválida retorna 401 sem revelar causa.
2. Rota protegida sem token retorna 401; papel insuficiente retorna 403.
3. Um usuário do tenant A não lê nem altera IDs pertencentes ao tenant B; resposta não revela existência do recurso.
4. Usuário/tenant inativo não obtém nova sessão e perde capacidade operacional conforme política aprovada.

### Webhook e mensagens

5. Payload oficial com assinatura válida é aceito e persistido; assinatura inválida retorna erro sem persistência.
6. Reenvio do mesmo ID externo não cria segunda mensagem nem segunda resposta.
7. Inbound persiste antes da chamada à IA; indisponibilidade da IA preserva o evento em estado reprocessável.
8. Outbound registra `pending → sent/delivered/read` ou `failed`; transição inválida é rejeitada.
9. Mensagem sem conteúdo e sem anexo é rejeitada com erro de validação.

### Conversa e handoff

10. Mensagem de novo contato cria/associa cliente e conversa no tenant correto.
11. Escalonamento muda status e disponibiliza a conversa na fila humana.
12. Duas tentativas concorrentes de assumir resultam em exatamente um agente vencedor.
13. Resolver registra horário; resolver novamente não duplica efeitos.

### Frontend

14. Estado vazio explica que não há conversas e oferece ação adequada ao papel.
15. Erro de API apresenta retry sem apagar texto ainda não enviado.
16. Sessão expirada redireciona ao login preservando rota de retorno quando seguro.
17. O frontend não exibe ações proibidas e o backend também as bloqueia.

## 10. Casos extremos, erros e estados vazios

- Webhook duplicado, fora de ordem, sem texto, somente mídia ou tipo não suportado.
- Bot/número sem binding; cliente final sem nome; contato com telefone alterado.
- IA em timeout, resposta vazia, conteúdo bloqueado, limite do provedor ou indisponibilidade.
- Graph API em timeout/4xx/5xx; token expirado; callback de status atrasado.
- Duas mensagens simultâneas na mesma conversa; corrida entre escalar, assumir e resolver.
- Recurso removido/inativado durante operação; chave rotacionada durante envio.
- Paginação vazia, filtro sem resultados, primeiro acesso sem configuração.
- Conteúdo grande, Unicode/emoji, anexos inválidos ou URL expirada.
- Banco/worker indisponível; retry após commit parcial.

Estados mínimos de UI propostos: carregando, vazio inicial, vazio filtrado, offline/erro recuperável, erro sem permissão, sessão expirada, processamento, envio pendente, falha com retry e conteúdo não suportado.

## 11. Segurança e privacidade

- JWT com expiração corrigida, validação de emissor/audiência se adotados e política de revogação/refresh a decidir.
- Hash bcrypt para senhas; política de senha, recuperação e MFA são pendências.
- Autorização server-side e isolamento de tenant em todos os repositórios.
- Verificação de assinatura Meta, proteção contra replay e rate limiting.
- API keys com hash, prefixo identificador, rotação, revogação e último uso.
- TLS em trânsito; criptografia/gestão de chaves em repouso conforme infraestrutura aprovada.
- Segredos em cofre/secret manager; nunca em repositório, resposta ou log.
- Logs de auditoria para login, credenciais, permissões, canal, plano, atribuição e eliminação.
- Minimização de PII; mascaramento em logs e ambientes não produtivos.
- Política LGPD para base legal, aviso, retenção, acesso, correção, portabilidade/eliminação e suboperadores (Meta/OpenAI/hosting) depende de jurídico/produto.
- Definir se conteúdo pode ser enviado à IA, quais dados devem ser redigidos e como obter transparência/consentimento quando aplicável.

## 12. MVP, futuro e fora de escopo

### MVP proposto

1. Contratos de UUID/tenant, DTOs, mappers, casos e migrations reconciliados.
2. Login seguro, autorização/RBAC mínimo e isolamento multi-tenant.
3. Configuração de um bot/número WhatsApp por tenant.
4. Webhook oficial, assinatura, idempotência e persistência confiável.
5. Conversa/mensagem coerentes, resposta de IA e escalonamento.
6. Inbox web com login, fila, histórico, assumir, responder e resolver.
7. Estados de entrega/falha, retry e observabilidade básica.
8. Testes unitários, integração e um E2E de bot e handoff.

### Melhorias futuras

- Instagram e novos canais.
- Construtor de fluxos, campanhas e templates.
- Analytics avançado, SLA, qualidade e relatórios.
- Base de conhecimento/RAG, avaliação e versionamento de prompts.
- Equipes, filas por competência e roteamento avançado.
- Marketplace e integrações externas.
- Limites/faturamento por plano.

### Fora de escopo do MVP proposto

- Campanhas em massa e marketing automation.
- Marketplace de templates.
- Analytics avançado/preditivo.
- Omnichannel além de WhatsApp.
- Construtor visual completo de automações.
- Billing automatizado.

Essa delimitação é proposta e requer aprovação.

## 13. Pendências de decisão humana

| Decisão | Impacto |
| --- | --- |
| Segmento e porte prioritários | UX, onboarding, preço e suporte. |
| WhatsApp como único canal do MVP | Arquitetura e prazo. |
| Papéis, equipes e escopo de agentes | RBAC e modelo de dados. |
| Fonte do tenant em cada tipo de credencial | Segurança e contratos. |
| Política de resposta/escalonamento da IA | Experiência, risco e custo. |
| Regra de reabertura/nova conversa e janela temporal | Histórico e métricas. |
| SLA, disponibilidade, RPO/RTO e latência | Infraestrutura e custo. |
| Retenção, LGPD e envio de PII à OpenAI | Jurídico, arquitetura e operação. |
| Recuperação de senha, MFA e sessão/refresh | Segurança e UX. |
| Limites e direitos por plano | Entitlements e faturamento. |
| Política quando tenant/canal é desativado | Mensagens pendentes e dados. |
| Anexos suportados, armazenamento e antivírus | Segurança e custo. |
| Aprovação humana antes de respostas de IA | Fluxo e produtividade. |
| Métricas de sucesso do MVP | Priorização e go-live. |

## 14. Dependências, riscos e preparação para entrega

Dependências externas: PostgreSQL, Meta Graph API, OpenAI e ambiente de containers. O Redis/worker ainda é apenas previsto.

Riscos prioritários comprovados pelo código:

1. Rotas sem autenticação/autorização.
2. UUID versus `int` e assinaturas incompatíveis entre camadas.
3. Entidade de mensagem divergente de DTOs/casos/ORM.
4. DTOs/respostas de clientes incorretos.
5. Expiração JWT usando `None`.
6. Webhook simplificado, sem assinatura e sem idempotência.
7. Processamento externo síncrono e sem fila confiável.
8. Ausência de testes e frontend funcional.

Critério recomendado para iniciar especificações detalhadas de novos módulos: API e migrations reproduzíveis; segurança multi-tenant; webhook seguro/idempotente; fluxo ponta a ponta demonstrável e coberto por testes.

## 15. Rastreabilidade principal

- Visão/roadmap: `README.md`.
- Composição da API: `backend/app/main.py` e `adapters/controllers/`.
- Entidades/regras: `backend/app/domain/entities/` e `domain/enums/`.
- Casos de uso: `backend/app/application/use_cases/`.
- Persistência: `backend/app/infrastructure/{orm,repositories,mappers}/`.
- Segurança: `adapters/controllers/auth_routes.py`, `infrastructure/gateways/{bcrypt_password_hasher,token_service_jwt,request_user_context}.py`.
- Integrações: `webhook_whatsapp_routes.py`, `message_gateway_whatsapp.py`, `ai_responder_gateway_openai.py`.
- Banco/execução: `backend/app/migrations/`, `docker-compose.yml`, Dockerfiles e `docker/postgres/init.sql`.
- Frontend: `frontend/src/` e `frontend/package.json`.
