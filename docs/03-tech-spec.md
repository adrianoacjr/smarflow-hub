# Especificação técnica — SmartFlow Hub

Data: 08/10/2026. Versão: 1.0. Status: especificação de implementação para revisão.

Fonte de requisitos: [02-prd.md](02-prd.md), versão presente no workspace nesta data. Esta especificação não implementa funcionalidades. As propostas e pendências do PRD continuam condicionais; escolhas técnicas abaixo são a arquitetura recomendada, não descrição do sistema já entregue.

## 1. Base existente e escopo

Manter Python/FastAPI, SQLAlchemy assíncrono/PostgreSQL, Alembic e React/TypeScript/Vite. Evoluir o monólito modular com processos HTTP e worker separados, compartilhando domínio e aplicação. Não extrair microserviços nesta etapa.

Evidências verificadas:

| Base | Estado observado | Consequência técnica |
| --- | --- | --- |
| [main.py](../backend/app/main.py) e [controladores](../backend/app/adapters/controllers/) | Routers sem proteção transversal de identidade | Introduzir autenticação e autorização antes da exposição de negócio |
| [ORM](../backend/app/infrastructure/orm/) | PKs UUID, contratos externos ainda inconsistentes | UUID em todas as camadas e contratos versionados |
| [migração inicial](../backend/app/migrations/versions/08f97a601dda_uuid_primary_keys.py) | Cria cinco tabelas, não cria `user_channel_bindings` | Nova revisão explícita; não reescrever revisão aplicada |
| [conversation_mapper.py](../backend/app/infrastructure/mappers/conversation_mapper.py) | Usa `source`, `resolved_at`, `assigned_agent_id`, divergindo de ORM/entidade | Modelo canônico e teste de round-trip |
| [enums](../backend/app/domain/enums/) e ORM | `agent` versus `user`; `resolved/abandoned` versus `open/closed`; `read` ausente | Migração com mapeamentos aprovados, sem conversão silenciosa |
| [analyze_message.py](../backend/app/application/use_cases/message/analyze_message.py) | Usa atributos antigos de mensagem e `MessageStatus.ESCALATED`, ausente no enum | Separar estado de entrega de estado de atendimento |
| [frontend](../frontend/src/) | Estrutura visual e teste de health | Implementar jornadas e estado de sessão |

Escopo alvo: requisitos RF/RNF do PRD, handoff, administração, segurança, operação e MVP. Instagram, campanhas, billing, RAG e construtor de fluxos ficam como extensões futuras; não criar contratos públicos fictícios para eles.

## 2. Clean Architecture

### 2.1 Dependências e responsabilidades

```text
HTTP / consumidor de jobs → application → domain
                                ↑           ↑
                         infrastructure implementa portas
composition root → conecta adaptadores, casos de uso e implementações
```

- `domain`: entidades, objetos de valor, invariantes, estados e políticas puras. Não importa FastAPI, Pydantic, SQLAlchemy, SDKs ou filas.
- `application`: comandos, consultas, resultados, autorização de operações, orquestração e portas. Só depende do domínio e de abstrações.
- `adapters`: DTO HTTP, extração de identidade, parsing de webhook, apresentação de erros e consumidores de jobs. Nunca consulta ORM diretamente.
- `infrastructure`: implementações PostgreSQL, JWT, bcrypt, cliente Meta/OpenAI, armazenamento de segredos e telemetria.
- Composition root: `main.py` e fábricas de `infrastructure/dependencies/`; worker terá entrada própria. É o único ponto que conhece implementações concretas.

Preservar os contratos de repositório em `domain/interfaces/` para evitar reorganização sem benefício; adicionar portas de orquestração em `application/interfaces/`. Entidades não acessam repositórios. DTOs HTTP não atravessam a fronteira da aplicação; mappers convertem explicitamente enums, UUID e objetos de valor.

### 2.2 Portas e contratos internos

```python
# Esboços de contratos, não implementação executável.
class ExecutionContext:
    actor_id: UUID | None
    tenant_id: UUID | None
    permissions: frozenset[str]
    correlation_id: str

class IConversationRepository:
    async def get(self, tenant_id: UUID, conversation_id: UUID): ...
    async def save(self, conversation, expected_version: int): ...

class IUnitOfWork:
    async def __aenter__(self): ...
    async def commit(self): ...
    async def rollback(self): ...

class IMessageGateway:
    async def send(self, channel, outbound) -> SendResult: ...

class IAIResponderGateway:
    async def respond(self, context, policy) -> AIResult: ...
```

Outras portas: `IPasswordHasher`, `ITokenService`, `IPrincipalResolver`, `IAuthorizationPolicy`, `ISecretStore`, `IWebhookVerifier`, `IClock`, `IOutboxRepository`, `IAuditRepository` e, quando mídia for aprovada, `IAttachmentStore`. `SendResult` contém ID do provedor ou resultado ambíguo tipado; não retorna apenas `None`. `AIResult` contém texto, motivo de término e uso, sem apresentar heurística de `finish_reason` como confiança semântica.

`ExecutionContext` é produzido por adaptador confiável. Casos de uso verificam permissões mesmo quando chamados por worker. `tenant_id=None` só vale para operações de plataforma explicitamente autorizadas; não significa acesso irrestrito aos repositórios.

### 2.3 Transações

Casos de uso definem a unidade de trabalho. Repositórios fazem `flush`, nunca `commit`. Remover a responsabilidade implícita de commit da dependência HTTP após a migração para UoW; deve existir um único dono da transação.

Persistir alteração, auditoria e outbox na mesma transação. Chamadas externas ocorrem fora dela; não manter locks durante OpenAI ou Meta. HTTP de criação só retorna sucesso depois do commit. Workers usam transações curtas para adquirir lease, confirmar resultado e reagendar.

## 3. Modelo canônico de dados

Convenções: UUID nativo em PK/FK, datas `timestamptz` em UTC, enum serializado pelo valor, `client_id` como nome persistido do tenant. Campos com `?` são opcionais. Todos os recursos de negócio incluem `client_id`; o tenant não é alterável por PATCH.

| Tabela/agregado | Campos principais alvo | Restrições |
| --- | --- | --- |
| `client` / Client | id, name, email, plan, active, created_at, updated_at | Plano mantém valores existentes, sem inventar benefícios; versão opcional para administração concorrente |
| `users` / User | id, client_id, name, email_normalized, password_hash?, user_type, access_level, active, system_prompt?, auth_version, created_at, updated_at | Unique(client_id,email_normalized); bot não pode iniciar sessão humana; nulabilidade de credenciais de bot depende da política de provisionamento |
| `user_channel_bindings` / ChannelBinding | id, client_id, user_id, source, external_ref, credential_ref, credential_version, active, created_at, updated_at | Unique(source,external_ref); bot e vínculo no mesmo tenant; credencial referenciada, nunca devolvida |
| `customers` / Customer | id, client_id, name?, email?, phone?, origin, active, tags, created_at, updated_at | Não identificar pessoa globalmente por telefone; dados de contato opcionais |
| `customer_channel_identities` | id, client_id, customer_id, binding_id, external_ref | Unique(client_id,binding_id,external_ref); identidade do contato por canal |
| `conversations` / Conversation | id, client_id, customer_id, binding_id, bot_user_id?, assigned_agent_id?, status, version, resolved_at?, created_at, updated_at | Agent e bot pertencem ao tenant; assignment só para humano ativo; source derivado do binding |
| `messages` / Message | id, client_id, conversation_id, sender_user_id?, direction, source, status, content?, automated, provider_message_id?, reply_to_message_id?, created_at, provider_timestamp? | Inbound sem autor usuário; outbound exige autor bot/humano; conversa é vínculo canônico, customer derivado |
| `message_attachments` | id, client_id, message_id, provider_media_id?, object_ref?, mime_type, filename?, size?, processing_state | Conteúdo ou pelo menos um anexo na criação atômica; proibir referência de outro tenant |
| `message_status_events` | id, client_id, binding_id, provider_message_id, status, provider_timestamp, dedup_key, received_at | Unique(client_id,binding_id,dedup_key); preserva histórico e eventos fora de ordem |
| `webhook_events` | id, binding_id?, client_id?, provider_event_key, kind, payload_encrypted, state, received_at, processed_at? | Deduplicação por evento lógico do provedor; quarentena quando não houver binding conhecido |
| `outbox_jobs` | id, client_id, kind, aggregate_id, dedup_key, schema_version, state, attempts, available_at, lease_until?, lease_token?, last_error_code?, correlation_id | Unique(client_id,kind,dedup_key); estados ready/leased/done/dead/paused |
| `send_attempts` | id, client_id, message_id, attempt_no, state, provider_message_id?, started_at, completed_at? | Unique(message_id,attempt_no); estados incluem outcome_unknown |
| `api_keys` | id, client_id, prefix, hash, scopes, expires_at?, revoked_at?, last_used_at? | Segredo aleatório de alta entropia; somente hash/prefixo persistidos |
| `audit_events` | id, client_id?, actor_id?, action, resource_type, resource_id?, result, correlation_id, created_at | Append-only para usuário da aplicação; sem tokens, senha ou corpo de mensagens |
| `bot_policies` | id, client_id, bot_user_id, version, mode, configuration, created_at | Proposta de política versionada, habilitação condicionada à decisão humana |

Refresh sessions e identidades de administrador de plataforma são modelos condicionais da seção 6; não reutilizar `admin` de tenant como superusuário.

### 3.1 Integridade e índices

Adicionar `UNIQUE(client_id,id)` em pais e FKs compostas `(client_id,parent_id)` nos filhos para impedir associações cruzadas também no banco. Repositório de mensagens exige tenant, inclusive busca por ID do provedor. Não usar cascade para apagar histórico de atendimento sem política de retenção aprovada.

Índices: conversations `(client_id,status,updated_at DESC,id)`; messages `(client_id,conversation_id,created_at,id)`; jobs `(state,available_at)`; auditoria `(client_id,created_at,id)`. Unique parcial para provider message ID não nulo por binding/direção (armazenar binding na mensagem com FK consistente ou criar índice em tabela de identidade do provedor).

Se aprovada uma conversa ativa por cliente/canal: índice unique parcial `(client_id,customer_id,binding_id)` nos estados ativos. Não ativar a restrição sem decisão sobre reabertura e multiplicidade.

### 3.2 Estados

Conversa: `bot_handling → escalated → human_handling → resolved`; `human_handling/escalated → bot_handling`; resolver novamente não gera novo evento. `abandoned` permanece do domínio, mas não expor abandono automático sem política. Atribuição exige `escalated`, usuário humano ativo e versão esperada.

Mensagem: inbound `received`; outbound `pending → sent → delivered → read`, com falha terminal quando confirmada. `escalated` não é estado de entrega: pertence à conversa. Callback pode saltar estados intermediários; `read` recebido antes de `delivered` deve avançar sem regressão posterior. Falha atrasada não substitui evidência de entrega; armazenar conflito para investigação. Retries são tentativas, não mutações arbitrárias de `failed` para `sent`.

Resultado externo ambíguo fica em `send_attempts.outcome_unknown`; não marcar como falha definitiva nem reenviar cegamente.

## 4. Contratos HTTP alvo

### 4.1 Convenções comuns

Proposta: `/api/v1` para APIs de negócio; manter webhook em `/webhooks/whatsapp` durante transição. UUID em JSON como string; datas RFC3339 UTC; campos desconhecidos de comandos rejeitados. PATCH distingue ausente de null, aceitando null somente em campos anuláveis. `active`, `source`, `created_at` e `assigned_agent_id` são nomes canônicos.

Tenant vem do principal autenticado. Rotas de tenant não aceitam `client_id` mutável em body/query. Operações de plataforma recebem ID na URL e autorização explícita. `Authorization: Bearer <access_token>` para UI; API keys são mecanismo separado, restrito a scopes de integração aprovados.

Listagens: `limit` default proposto 50, máximo 100; cursor opaco com ordenação estável `(created_at,id)` ou `(updated_at,id)`, vinculado aos filtros. Resposta `{items: [...], next_cursor: string|null}`; não usar tamanho da página como total global. Filtros de busca usam whitelist e SQL parametrizado; busca inicial por nome/referência do contato, busca no conteúdo é futura.

Mutação de conversa envia `expected_version`; conflito 409. Criação de outbound envia `Idempotency-Key`; mesma chave, ator, tenant, rota e payload retorna o resultado anterior; payload diferente retorna 409. Persistir hash e resposta/ID em registro `idempotency_requests` com unicidade nesse escopo. Prazo de retenção da chave é configurável e publicado antes do uso externo.

### 4.2 Identidade, administração e configuração

| Método e caminho em /api/v1 | Entrada | Resultado e autorização |
| --- | --- | --- |
| POST /auth/login | email, password, tenant_hint se estratégia aprovada | 200 `{access_token,token_type,expires_in,user}`; 401 uniforme |
| GET /auth/me | Bearer | 200 identidade, tenant, permissions, active |
| POST /auth/logout | sessão atual | 204; revogação conforme estratégia da seção 6 |
| POST /auth/refresh | cookie de sessão, se aprovado | 200 novo access token e rotação de refresh |
| POST /clients | name,email,plan | 201 Client e API key uma única vez; plataforma |
| GET /clients; GET /clients/{id} | paginação / UUID | 200 Client(s); plataforma |
| PATCH /clients/{id} | name?,email?,active? | 200 Client; plataforma; sem alteração implícita de plano |
| PATCH /clients/{id}/plan | plan | 200 Client; plataforma; sem cobrança automática |
| POST /users | name,email,password?,user_type,access_level,system_prompt? | 201 User sem hash; admin tenant |
| GET /users; GET /users/{id} | filtros active,user_type / UUID | 200 User(s); permissão users:read |
| PATCH /users/{id} | name?,email?,active?,access_level?,system_prompt? | 200 User; impedir elevação indevida |
| POST /auth/change-password | current_password,new_password | 204; invalida sessões conforme política |
| POST /channels | bot_user_id,source,external_ref,credential | 201 Channel público sem segredo; admin tenant |
| GET /channels; GET /channels/{id} | paginação / UUID | 200 binding, estado e diagnóstico sanitizado |
| PATCH /channels/{id} | active?,bot_user_id? | 200 Channel; tenant consistente |
| POST /channels/{id}/credentials/rotate | credential | 200 versão/estado, sem segredo |
| POST /channels/{id}/verify | sem segredo no body | 202 job diagnóstico; GET channel mostra resultado |
| POST /api-keys | name,scopes,expires_at? | 201 `{id,prefix,secret}` somente nesta resposta |
| GET /api-keys | paginação | 200 metadados sem hash/secret |
| POST /api-keys/{id}/rotate | parâmetros de expiração | 201 chave sucessora; sobreposição depende de política |
| DELETE /api-keys/{id} | UUID | 204 revoga; nunca hard delete do histórico |
| GET/PUT /bots/{id}/policy | versão/configuração validada | 200 Policy; condicionado à definição da política |

Delete de client/user/customer e desvinculação física de canal só ganham contrato final após política de histórico/retenção. Até lá usar desativação; rotas legadas de delete devem ser desabilitadas na versão alvo, não manter destruição implícita.

### 4.3 Clientes finais, conversas e mensagens

| Método e caminho | Entrada | Resultado |
| --- | --- | --- |
| POST /customers | name?,email?,phone?,origin,tags? | 201 Customer; identidade de canal validada por operação própria |
| GET /customers; GET /customers/{id} | cursor, busca, active / UUID | 200 Customer(s) |
| PATCH /customers/{id} | campos de perfil e active | 200 Customer; nunca troca tenant |
| POST /conversations | customer_id,binding_id | 201 Conversation; criação inicial depende da regra de roteamento |
| GET /conversations | status?,customer_id?,assigned_agent_id?,q?,cursor | 200 página filtrada pelo escopo do agente |
| GET /conversations/{id} | UUID | 200 Conversation com version |
| POST /conversations/{id}/escalate | reason?,expected_version | 200 Conversation |
| POST /conversations/{id}/assign | agent_id,expected_version | 200 Conversation; 409 se já assumida |
| POST /conversations/{id}/return-to-bot | expected_version | 200 Conversation; bot/canal devem estar ativos |
| POST /conversations/{id}/resolve | expected_version | 200 Conversation; operação repetida resolvida é sem efeito |
| GET /conversations/{id}/messages | cursor,limit | 200 página cronológica |
| POST /conversations/{id}/messages | content?,attachment_ids?; Idempotency-Key | 202 Message pending após commit do job |
| GET /messages/{id} | UUID | 200 Message com estado e último erro sanitizado |
| POST /messages/{id}/retry | expected_attempt | 202 ou 409 se pendente/ambígua/não elegível |
| POST /jobs/{id}/reprocess | reason | 202; operador autorizado; idempotência preservada |

Resposta Conversation: `id,customer_id,binding_id,source,bot_user_id,assigned_agent_id,status,version,created_at,updated_at,resolved_at`. Message: `id,conversation_id,sender_user_id,direction,source,status,content,attachments,automated,created_at,delivery_error_code`. Cliente não escolhe direção/status/automated/autor no envio; o caso de uso determina.

```json
{
  "content": "Olá, vou continuar seu atendimento.",
  "attachment_ids": []
}
```

`202` significa persistido para envio, não entregue. A UI consulta Message até status terminal ou acompanha atualização da inbox. Upload de mídia, se aprovado: `POST /attachments` multipart retorna 202 com id e estado de análise; GET `/attachments/{id}` informa disponibilidade. Só anexos prontos podem ser enviados. Download autenticado emite URL temporária após autorização.

### 4.4 Erros e compatibilidade

Envelope único: `{error:{code,message,details?,correlation_id}}`. Detalhes de validação não incluem senha, corpo integral nem resposta do provedor.

| HTTP | Código de exemplo | Tratamento |
| --- | --- | --- |
| 400 | INVALID_WEBHOOK | JSON/envelope malformado |
| 401 | INVALID_CREDENTIALS / SESSION_EXPIRED | Login ou autenticação; sem revelar usuário |
| 403 | FORBIDDEN / INVALID_SIGNATURE | Ação proibida ou webhook não autenticado |
| 404 | RESOURCE_NOT_FOUND | Ausente ou pertencente a outro tenant |
| 409 | VERSION_CONFLICT / IDEMPOTENCY_CONFLICT / INVALID_TRANSITION | Recarregar estado ou corrigir comando |
| 413 | PAYLOAD_TOO_LARGE | Limite configurado de corpo/mídia |
| 422 | VALIDATION_ERROR | UUID, enum, campos ou conteúdo inválidos |
| 429 | RATE_LIMITED | Retry-After, sem loop agressivo |
| 503 | TEMPORARILY_UNAVAILABLE | Persistência/infra indisponível; retry seguro |
| 500 | INTERNAL_ERROR | Log interno sanitizado, sem stack na resposta |

Erros de domínio/aplicação são independentes de HTTP; handlers fazem o mapeamento. Falhas de worker viram códigos persistidos e métricas. Versionar OpenAPI e adaptar frontend na mesma entrega. Não manter rotas legadas desprotegidas como aliases. Prazo de remoção/compatibilidade depende de inventário de consumidores externos, ainda desconhecido.

## 5. Fluxos assíncronos e integrações

### 5.1 Recepção WhatsApp

1. GET de verificação compara token configurado e devolve challenge como texto quando válido. POST autentica bytes originais antes de converter JSON; `IWebhookVerifier` encapsula protocolo do provedor.
2. Adaptador converte envelope em eventos normalizados, incluindo múltiplas entradas/mensagens/status. Tenant é resolvido pelo binding confiável, nunca por campo tenant fornecido.
3. Em transação: registrar evento deduplicado e job de normalização. Responder 200 somente após commit durável. Banco indisponível retorna 503; evento duplicado já persistido retorna 200 sem novos efeitos.
4. Worker cria/localiza identidade, conversa e inbound atomicamente, e registra job de análise. Conflitos de uniqueness em contatos concorrentes são relidos, não duplicados.
5. Payload autenticado de número desconhecido vai para quarentena restrita, com alerta e sem IA/envio. Tipo não suportado persiste evento como unsupported, sem tentativas infinitas.

Chave inbound: binding + ID externo da mensagem. Chave callback: binding + ID externo + estado + timestamp/evento canônico. Hash do corpo inteiro não basta para eventos lógicos repetidos em envelopes diferentes. Retenção mínima de tombstones de deduplicação deve cobrir janela de replay acordada mesmo depois de apagar conteúdo.

### 5.2 Worker e fila

Proposta técnica inicial: PostgreSQL outbox/jobs com worker separado, `FOR UPDATE SKIP LOCKED`, leases e índice de jobs vencidos. Evita exigir Redis/Celery enquanto a escolha do broker está pendente. Se adotado broker depois, relay publica outbox e consumidor continua idempotente.

Job carrega IDs, versão de schema e correlation ID; não credenciais/conteúdo. Lease expirado permite retomada; confirmação exige lease token vigente para evitar que worker antigo sobrescreva novo resultado. Retry com backoff exponencial/jitter, limite configurado e respeito a Retry-After; limite proposto de cinco tentativas requer calibração. Exaustão vai para dead-letter com código/diagnóstico, reprocessamento auditado. Ordenar processamento por conversa e usar versões, sem lock de banco durante rede.

### 5.3 IA e handoff

Carregar últimas N mensagens da mesma conversa/tenant em ordem cronológica (não primeiras N de todo o cliente). Aplicar limite de contexto por orçamento configurado, prompt versionado e política de redação de PII. Chamada usa porta existente evoluída, preservando SDK na infraestrutura. Modelo e limites são configuração, não valores fixados neste documento.

Antes de chamar: verificar tenant/bot/canal ativo, status bot_handling e política habilitada. Após retorno: reler versão/status; se humano assumiu, invalidar resposta automática ainda não enfileirada. Dedupe de resposta por inbound + versão da política; registrar decisão e custo sem logar conteúdo. Novo inbound concorrente exige política de ordenação/agregação aprovada; serialização por conversa é a base técnica recomendada.

Pedido explícito de humano e limiar de confiança existem como heurísticas em código; critérios definitivos são pendentes. Resposta vazia, recusa ou timeout preservam inbound e produzem resultado tipado; retry ou escalonamento segue política aprovada. Não expor número de confiança fabricado. Atualização de conversa e auditoria/outbox ocorrem atomicamente.

### 5.4 Envio e ambiguidade externa

Persistir outbound e job antes de rede. Worker verifica estado/autor/tenant/canal novamente, registra tentativa e obtém credencial vigente via secret store. Gateway devolve ID do provedor e classificação do erro. Callback atualiza histórico e projeção monotônica, inclusive se chegar antes da confirmação do envio.

Não há transação distribuída entre PostgreSQL e Meta: timeout após aceitação ou crash após envio pode deixar resultado desconhecido. Exatamente uma entrega externa não pode ser garantida apenas por outbox. Marcar tentativa outcome_unknown, aguardar callback/reconciliação quando correlacionável e suspender reenvio automático. Se provedor oferecer idempotência documentada, utilizá-la; caso contrário, ação manual auditada e política de risco de duplicação precisam de aprovação. Aceitação 6 do PRD vale para duplicação de webhook, não promessa universal de exactly-once externo.

Erros 401/403 de canal: suspender processamento e alertar administrador. Erros permanentes de destinatário/payload: falha sem retry. Limites/5xx: retry somente quando seguro. Verificar restrições de janela de atendimento/formato no adaptador antes do envio; não adicionar campanhas/templates ao MVP por consequência técnica.

### 5.5 Protocolo de fornecedores

Versão Graph, formato de assinatura/eventos, capacidades de idempotência e limites devem ser confirmados na documentação oficial durante a implementação. Esta especificação usa portas e contratos internos e não certifica que a versão fixa v19.0 do código continua suportada. Não atualizar SDK/modelo/API implicitamente.

Rotação de credenciais usa versão; jobs referenciam binding e resolvem segredo na execução. Revogação impede novos envios imediatamente. Sobreposição de chaves API exige prazo aprovado; jamais migrar hashes existentes para texto claro.

## 6. Segurança, autorização e privacidade

Corrigir expiração JWT usando duração padrão quando override ausente. Validar algoritmo permitido, assinatura, expiração, sujeito UUID e issuer/audience definidos por ambiente. Claims incluem tenant e versão de autenticação; verificar estado atual do usuário/tenant para bloqueio e revogação. JWT não contém segredos nem PII dispensável. Bcrypt permanece atrás da porta; validar limite de bytes da implementação e não truncar senha silenciosamente.

Há email unique por tenant, mas login atual só usa email. Proposta: tenant_hint público identifica organização no login; identidade é comprovada por senha naquele tenant. O hint não autoriza acesso. Alternativa de identidade global/múltiplas organizações exige modelo diferente e aprovação antes de congelar contrato.

Proposta de sessão: access token somente em memória; refresh token opaco em cookie HttpOnly/Secure, hash em `auth_sessions` (id,user_id,client_id,token_hash,family_id,expires_at,revoked_at,replaced_by). Rotação detecta reutilização e revoga família. Proteger refresh/logout com validação Origin e CSRF quando cookies puderem circular cross-site. Logout revoga sessão; troca de senha incrementa auth_version. Se refresh não for aprovado, logout/invalidação e nova autenticação substituem renovação automática; não oferecer endpoint fictício.

Administrador de plataforma precisa principal separado ou identidade com escopo explícito de plataforma, provisionada fora do cadastro público. Não mapear todo `admin` existente para plataforma. Suporte cross-tenant é elevação temporária auditada, desabilitada até aprovação. Matriz exata de equipe/permissões segue PRD §8; `IAuthorizationPolicy` centraliza implementação, negando permissões não definidas.

Segredos de canal: referência em banco e valor em secret store aprovado. TLS; acesso mínimo do banco; CORS por origem exata; rate limit para login, webhook e ações de envio com contadores compartilhados em múltiplas instâncias. Separar credencial de migração da credencial runtime. Redigir logs e respostas antes de exportação de telemetria.

Mídia: limites de tamanho/tipo, inspeção de conteúdo, quarentena, download com restrição de destinos para impedir SSRF, URLs temporárias após autorização. Mídia não aprovada permanece unsupported; não tornar bucket público.

Retenção e direitos: futura porta de exportação/anonimização com job auditado, verificação de solicitante e preservação mínima de integridade. Bases legais, prazos, conteúdo enviado à IA, residência, backups e legal hold dependem de decisão humana; não executar expurgo por default. Logs de auditoria também têm prazo a aprovar. RB-010 é interpretada como não reapresentar segredos persistidos; emissão inicial de access/refresh token necessariamente os entrega ao cliente autorizado.

## 7. Frontend e contratos de apresentação

Preservar componentes atuais e corrigir renderização de children. Estrutura proposta: `features/auth`, `features/inbox`, `features/admin`, `services/http`, `domain/types` e componentes de apresentação. Cliente HTTP centraliza Bearer, erro tipado, correlation ID, paginação e cancelamento de consultas. Tipos gerados/validados contra OpenAPI evitam duplicar contratos manualmente.

Rotas: login; inbox; conversa por UUID; administração de usuários/canais; tenants somente para plataforma. Guard de rota melhora UX, autorização real permanece no backend. Permissões vêm de `/auth/me`, não de interpretação local arbitrária de papel.

Primeira versão técnica pode usar polling com backoff/jitter e pausa em aba oculta, intervalo a calibrar. Tempo real via SSE é evolução proposta se latência aprovada exigir; evento contém ID/versão e causa reconsulta autorizada, nunca broadcast de conteúdo de todos os tenants.

Envio preserva rascunho em memória em falhas; evita submissão dupla, reutiliza chave idempotente na mesma intenção e mostra pending até confirmação. 409 recarrega conversa e explica conflito. 401 tenta refresh uma única vez se habilitado; caso contrário login com retorno restrito a path local. Não guardar mensagens/senhas em localStorage. Logout limpa caches por tenant.

Estados: loading inicial; vazio inicial com ação autorizada; vazio filtrado com limpar filtros; offline com retry; forbidden; sessão expirada; pending/sent/delivered/read/failed; mídia em processamento/unsupported. Retry explícito em envio ambíguo exige orientação do backend. Navegação por teclado, foco, nomes acessíveis e anúncios de estado devem ser testados; compatibilidade cobre navegadores definidos no PRD.

## 8. Migrações e compatibilidade de dados

Plano expandir → preencher → validar → restringir → remover legado. Não executar nenhuma migração como parte desta documentação. Inventariar revisão aplicada, volume e dados reais antes de planejar lock/downtime. Nunca pressupor banco vazio.

| Etapa | Alterações | Validação e reversão |
| --- | --- | --- |
| M1 — expansão | Criar bindings ausentes, timestamps/campos opcionais, colunas canônicas e versão de conversa; novos enums paralelos quando necessário | Upgrade desde a revisão inicial; comparar metadata; rollback somente sem dados novos |
| M2 — dados | Preencher client_id em mensagens via conversa, mapear autores, identidade de cliente/canal e source/channel | Relatório de órfãos/ambiguidade; preservar colunas antigas e tabela de correspondência |
| M3 — normalização | Corrigir external_red, reconciliar access_level e estados | `user→agent`, `closed→resolved` e `open→bot_handling` são candidatos, não conversões automáticas; exigir confirmação semântica e timestamp de resolução não inventado |
| M4 — integridade | Unique composto, FKs de tenant, índices, nullability e checks; anexos atômicos no caso de uso | Resolver duplicatas antes; criação de índices concorrentes em revisão apropriada fora de transação quando necessário |
| M5 — confiabilidade/segurança | Criar eventos, outbox, tentativas, idempotência, audit, keys; sessions/policies se aprovadas | Testes de dedupe, retomada, rotação e isolamento; não recuperar segredo de hash |
| M6 — contrato final | Adaptar aplicação/frontend para v1 e remover campos obsoletos após janela aprovada | Backup e restauração ensaiados; migração destrutiva sem downgrade fictício, preferir forward fix |

`external_red` não prova qual namespace de identidade contém; não preencher binding automaticamente. Dados `escalated` em mensagens exigem recuperar estado de entrega de eventos/evidências, sem presumir received/sent. Vínculos inexistentes não devem receber tenant sintético para passar FK. Quando legado não puder ser convertido, bloquear cutover e emitir relatório restrito.

Não reescrever `08f97a601dda`. Manter nomes físicos existentes quando possível; schemas app/events do bootstrap não justificam mover todas as tabelas. Alembic é autoridade do schema da aplicação; corrigir SQL de bootstrap inválido/separar provisionamento em tarefa própria. Backend só fica ready após schema compatível; job único de migração antecede rollout, sem concorrência de múltiplas instâncias.

## 9. Observabilidade e operação

Logs JSON: timestamp, level, service, operation, correlation_id, job_id, duration_ms, error_code; IDs de tenant/ator somente em logs restritos, sem corpo, telefone, email, tokens ou prompt. Propagar correlation ID do HTTP até jobs e chamadas externas. Sanitizar ID recebido e gerar valor quando inválido.

Métricas de baixa cardinalidade: requests/error/latência por rota-template; webhooks accepted/duplicate/invalid/quarantined; jobs ready/dead/age/lease_expired; AI latência/timeout/tokens; send confirmed/failed/unknown; conflitos de atribuição; falhas de autorização. Não usar tenant, mensagem ou telefone como label de métricas.

Alertas propostos: crescimento da idade da fila, envio ambíguo, canal sem credencial válida, dead letters, falhas de persistência, regressão de autorização. Limiares e SLO são pendentes; métricas não implicam disponibilidade garantida.

`GET /health/live`: processo vivo, 200 sem rede externa. `GET /health/ready`: banco acessível, revisão compatível e dependências internas mínimas, 200/503 sem segredos. OpenAI/Meta degradados não devem derrubar liveness nem impedir persistência inbound. Worker expõe heartbeat/progresso via armazenamento ou endpoint interno.

Compose de desenvolvimento ganha worker do mesmo código. Produção usa imagem imutável sem reload, usuário não root, encerramento gracioso/leases recuperáveis, secret injection e serviços privados. Lockfiles e instalações reproduzíveis; CI separa lint/tipos, testes, build e verificação de migrações. Backup/restore, DLQ e rotação exigem runbooks; frequência, RPO/RTO e orçamento aguardam aprovação.

## 10. Rastreabilidade de requisitos

Cada linha relaciona requisito a caso de uso/arquitetura, contrato/modelo e validação. Referências de seção especificam fluxo, migração, erros e segurança complementares.

| Requisito | Implementação alvo | Contrato/modelo | Teste principal |
| --- | --- | --- | --- |
| RF-001 | AuthenticateUser + hasher/token ports (§6) | login, users/auth_version | T01 |
| RF-002 | PrincipalResolver + guards + autorização na aplicação | Bearer em todas rotas privadas | T02 |
| RF-003 | Contexto confiável + repos tenant-scoped | FKs compostas, me, sem tenant mutável | T03 |
| RF-004 | AuthorizationPolicy + audit transacional | permissões por ação, audit_events | T02/T03/T17 |
| RF-010 | Create/Update/ChangePlan/DeactivateClient | /clients, Client, M1/M5 | T04 |
| RF-011 | Create/Update/DeactivateUser, ChangePassword | /users, change-password, users | T01/T04 |
| RF-012 | BindChannel/DeactivateChannel/VerifyChannel | /channels, bindings, M1/M2 | T04/T05 |
| RF-013 | Issue/Rotate/RevokeApiKey | /api-keys, api_keys/secret store | T04/T17 |
| RF-020 | GetOrCreateCustomer por identidade scoped | customers + identities, M2/M4 | T06 |
| RF-021 | Create/Get/ListConversation por tenant | /conversations, FKs e índices | T03/T06 |
| RF-022 | Escalate/Assign/Resolve/ReturnToBot | ações de conversa + version | T09/T10 |
| RF-023 | Receive/QueueOutboundMessage + UoW | messages/attachments e /messages | T07/T11 |
| RF-024 | AssignAgent com compare-and-swap | UPDATE com version/status, 409 | T09 |
| RF-025 | ApplyDeliveryEvent + projeção monotônica | callbacks, status_events, M5 | T08 |
| RF-030 | VerifyWebhook/IngestWebhook | GET/POST webhook, verifier port | T05 |
| RF-031 | Adaptador Meta + dedupe durável | evento lógico, unique, M5 | T05/T07 |
| RF-032 | AnalyzeMessage via AI port | histórico scoped, AIResult | T10/T12 |
| RF-033 | EvaluateAutomationPolicy puro + política versionada | /bots/{id}/policy, bot_policies | T10/T12; critérios pendentes |
| RF-034 | Worker, outbox, retry, lease e DLQ | jobs, send_attempts, /reprocess | T07/T11 |
| RF-040 | Layout/theme e rotas React | componentes existentes | T13/T15 |
| RF-041 | Sessão UI + resolver backend | me/logout/refresh condicional | T01/T13 |
| RF-042 | Inbox com polling, composição e filtros | cursor, mensagens, erros tipados | T13/T14 |
| RF-043 | Administração + capacidades da sessão | permissões de me e guards | T02/T14 |
| RNF-001 | §6 segurança em adaptadores e aplicação | secrets, JWT, scopes, erros | T01/T02/T17 |
| RNF-002 | §3 FKs + §6 políticas | tenant-scoped em HTTP/worker | T03 |
| RNF-003 | §5 inbox/outbox e dedupe | eventos/chaves/tentativas | T07/T11 |
| RNF-004 | §2 UoW + controle concorrente | transações/version/leases | T06/T09/T11 |
| RNF-005 | §9 logs/métricas/traces | correlation_id e códigos estáveis | T16 |
| RNF-006 | índices/paginação, processamento fora HTTP | limites configuráveis; metas pendentes | T18 baseline, gate após metas |
| RNF-007 | readiness, backup/restore e retomada | rollout/M1–M6, runbooks | T11/T18; RPO/RTO pendentes |
| RNF-008 | §7 UI acessível | teclado/foco/leitor de tela | T15 |
| RNF-009 | §7 matriz de navegadores | build e E2E por engine | T15 |
| RNF-010 | §8 migrations + CI/OpenAPI | v1, round-trip, schemas | T04/T19 |
| RNF-011 | §6 minimização/retention ports | segredo, mídia e jobs de dados | T17; prazos pendentes |

RB-001/002/004/005/006 são cobertas por T01–T03; RB-003 por T10/T11 com política de pausa definida; RB-007 por T07; RB-008 por T06/T10 após decisão de reabertura; RB-009 por T12; RB-010 por T17.

## 11. Plano de testes e critérios verificáveis

Testes propostos; não executados nesta entrega documental. Usar doubles das portas para testes unitários e PostgreSQL real descartável para integração; SQLite não valida FKs/enums/locks usados. Provedores externos são simulados em CI; smoke de sandbox opcional com credenciais próprias e sem contatos reais.

| ID | Cenário verificável | Aceitação PRD |
| --- | --- | --- |
| T01 | Token expira no futuro sem override; senha inválida retorna 401; bot/inativo não inicia sessão; revogação e refresh/reuso conforme política | 1,4,16 |
| T02 | Inventário de rotas verifica ausência de bypass; sem token 401, permissão insuficiente 403, UI esconde ação e chamada direta falha | 2,17 |
| T03 | Dois tenants com IDs conhecidos: leitura/mutação/anexo/status/job do outro retorna 404 ou é negado; FK cruzada falha; contexto IA não mistura tenants | 3 |
| T04 | Schema DTO/OpenAPI, CRUD autorizado, round-trip domínio↔ORM e enum/UUID; segredo só aparece na criação/rotação | suporte a 1–4 |
| T05 | Fixtures de envelope múltiplo, assinatura válida/inválida, challenge textual, corpo grande, binding desconhecido e tipo unsupported | 5 |
| T06 | Contatos/inbounds concorrentes não duplicam identidade; conversa segue regra aprovada; cliente sem nome/telefone alterado não une tenants | 10 |
| T07 | Replay do evento e crash após commit/antes do ACK geram um inbound e um efeito lógico; DB indisponível não retorna sucesso | 6,7 |
| T08 | Callback read antes de sent/delivered não regride; callback repetido não duplica eventos; falha tardia é registrada sem perder entrega | 8 |
| T09 | Duas sessões Postgres assumem mesma versão: um sucesso, um 409, uma auditoria de atribuição; nenhum overwrite | 12 |
| T10 | Máquina de estados, escalar inclui fila; resolver duas vezes preserva resolved_at; handoff durante IA cancela resposta automática; tenant/canal inativo não envia | 11,13 |
| T11 | Worker morre com lease; retomada segura; timeout de envio vira unknown sem retry cego; rotação/revogação no meio da fila, DLQ e reprocessamento idempotente | 6–8 |
| T12 | IA timeout/vazia/recusa/rate limit; inbound preservado, retry/escalonamento definido; histórico usa últimas N da conversa e prompt correto | 7 |
| T13 | E2E login→inbox→mensagem→bot e login agente→escalar→assumir→responder→resolver; expiração retorna a path local seguro | 10–13,16 |
| T14 | Vazio inicial/filtro, loading/offline/erro, 409 e retry preservam rascunho; envio duplo com mesma chave não duplica | 14,15,17 |
| T15 | Teclado/foco/contraste/leitor de tela + checagem automática; E2E nos navegadores do PRD, Safari real quando necessário | RNF-008/009 |
| T16 | Correlation ID atravessa HTTP/job/gateway; métricas incrementam; logs/redação não vazam payloads | RNF-005 |
| T17 | Segredos ausentes em listagens/logs/traces; mídia cross-tenant/SSRF bloqueada; auditoria sem PII; retenção/exportação somente após política | RF-013/RNF-011 |
| T18 | Carga de webhook/inbox, atraso de fila, reinício/restore; registrar baseline e comparar com SLO/RPO/RTO aprovados | RNF-006/007 |
| T19 | Banco vazio→head; inicial com fixtures legadas→head; ambiguidades bloqueiam migração; metadata sem drift; import rules impedem dependência externa no domínio | RNF-010 |

Adicionar verificações arquiteturais de imports: domínio não importa aplicação/infra/adaptadores; aplicação não importa infra/HTTP; controladores não acessam Session/ORM para negócio. Caso de uso não retorna ORM. Cobertura deve priorizar invariantes e caminhos de erro, sem definir porcentagem arbitrária como garantia.

## 12. Entregas e decisões pendentes

Sequência sugerida: (1) reconciliar domínio/DTO/repos e migrations com T04/T19; (2) identidade, tenant e RBAC com T01–T03; (3) ingestão/outbox com T05–T07; (4) mensagens/IA/handoff com T08–T12; (5) frontend/admin com T13–T15; (6) observabilidade, privacidade e ensaio operacional com T16–T18. Cada fase possui contratos versionados e migração compatível; não expor nova UI sobre API antiga insegura.

| Decisão humana | O que pode avançar | O que fica condicionado |
| --- | --- | --- |
| Login multiempresa e identidade de plataforma | UUID/contexto/portas de autorização | Body final do login e schema de identidade/sessão |
| Papéis/equipes e suporte cross-tenant | Negar por padrão e testes de isolamento | Matriz de concessão, visibilidade/atribuição |
| Reabertura, janela e multiplicidade de conversas | Histórico e versionamento | Unique de ativa e regra para novo inbound após resolução |
| Política IA, aprovação humana e dados enviados | AIResult tipado, preservação de inbound | Envio automático e gatilhos de escalonamento |
| Tenant/canal inativo e revogação | Bloquear novos efeitos externos | ACK/retention/reprocessamento de eventos pausados |
| Sessão/refresh/MFA/recuperação | Correção JWT e check de ativo | Endpoints e tabelas adicionais de sessão/recuperação |
| Retenção/LGPD/residência e mídia | Minimização e referências privadas | Expurgo, exportação, tipos/limites de upload |
| SLO/latência/RPO/RTO e custo | Instrumentação, testes baseline | Gates quantitativos e dimensionamento |
| Risco de resultado externo ambíguo | Estado unknown e suspensão de retry | Reenvio manual/automático e SLA de reconciliação |
| Canal MVP, número de bindings e planos | Portas e modelo com isolamento | Limites de produto e integrações futuras |

As escolhas de polling, jobs PostgreSQL e API v1 são recomendações técnicas concretas e substituíveis atrás das portas. Nenhuma delas aprova as políticas de produto pendentes. A implementação só será considerada pronta após os critérios de aceitação relevantes passarem e as pendências que bloqueiam seu comportamento serem resolvidas.
