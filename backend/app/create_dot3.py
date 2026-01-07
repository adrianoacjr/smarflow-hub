colors = {
    # === DOMAIN LAYER ===
    # Tons terrosos/laranja representam a base conceitual sólida do sistema
    'dom_color_A': '"#C0392B"',   # Vermelho escuro (fundamento)
    'dom_color_B': '"#F1948A"',   # Vermelho claro

    # Models – base de entidades, estável e confiável
    'model_color_A': '"#6E2C00"', # Marrom escuro (terra/base)
    'model_color_B': '"#EDBB99"', # Marrom claro

    # Interfaces – conectam, são pontes (amarelo esverdeado)
    'inter_color_A': '"#9A7D0A"', # Amarelo oliva escuro
    'inter_color_B': '"#F7DC6F"', # Amarelo claro

    # === INFRASTRUCTURE LAYER ===
    # Representa a sustentação técnica (tons de cinza/vermelho metálico)
    'infra_color_A': '"#641E16"', # Bordô escuro (profundidade)
    'infra_color_B': '"#C39BD3"', # Lilás metálico suave

    # Repositories – parte técnica, armazenamento (verde, “persistência”)
    'repo_color_A': '"#145A32"',  # Verde escuro
    'repo_color_B': '"#82E0AA"',  # Verde claro

    # Gateways – interfaces externas, conexão com o mundo (azul petróleo)
    'gate_color_A': '"#0E6251"',  # Verde-azulado escuro
    'gate_color_B': '"#48C9B0"',  # Verde-água claro

    # === APPLICATION LAYER ===
    # Camada lógica e de orquestração (roxo — inteligência e abstração)
    'app_color_A': '"#4A148C"',   # Roxo escuro
    'app_color_B': '"#CE93D8"',   # Roxo claro

    # Use cases – a “mente” do sistema (violeta vibrante)
    'use_color_A': '"#512DA8"',   # Roxo médio (já ótimo)
    'use_color_B': '"#B39DDB"',   # Roxo lavanda

    # === PRESENTATION LAYER ===
    # Comunicação com o usuário (vermelho/rosa – energia, interface)
    'pres_color_A': '"#B71C1C"',  # Vermelho forte
    'pres_color_B': '"#F8BBD0"',  # Rosa claro

    # Controllers – controle e entrada (cinza-azulado, neutro e sólido)
    'cont_color_A': '"#263238"',  # Azul petróleo escuro
    'cont_color_B': '"#90A4AE"',  # Cinza-azulado claro

    # DTOs – transporte de dados (laranja, clareza e estrutura)
    'dto_color_A': '"#E65100"',   # Laranja escuro
    'dto_color_B': '"#FFCC80"',   # Laranja claro

    # Dependencies – injeção e ligação (ciano, remete à conexão)
    'dep_color_A': '"#006064"',   # Azul petróleo escuro
    'dep_color_B': '"#80DEEA"',   # Azul claro

    # ORM
    'orm_color_A': '"#0A1F44"',
    'orm_color_B': '"#4DD0E1"',

    # Security - criptografia, proteção, vigilância (azul profundo + ciano neon)
    'sec_color_A': '"#0A1F44"',   # Azul profundo (sensação de blindagem e confiança)
    'sec_color_B': '"#4DD0E1"',   # Ciano luminoso (camada de proteção ativa / “energia de firewall”)

    # === CORE LAYER ===
    'core_color_A': '"#B71C1C"',
    'core_color_B': '"#F8BBD0"',
}


dot = f"""
digraph G {{
  rankdir=LR;
  graph [fontsize=10, bgcolor="#FFFFFF", labelloc="t", label="Smartflow Hub Layers", fontname="Helvetica"];
  node [shape=box, style=filled, fillcolor="#E8F0FF", fontname="Helvetica"];
  edge [color="#666666"];
  splines=spline;
  penwidth=1;
  ranksep=2;
  edge [
    penwidth=3;
    constraint=true;
  ];
  node [
    fillcolor="white";
    penwidth=1;
    fontsize=10;
  ];

  // ===== Domain Layer =====
  subgraph cluster_domain_layer {{
    label="Domain Layer";
    color={colors['dom_color_A']};
    style="filled,rounded";
    fillcolor={colors['dom_color_B']};

    // ===== Models =====
    subgraph cluster_models {{
      label="Entities & Value Objects\n(User, etc.)";
      color={colors['model_color_A']};
      style="filled,rounded";
      fillcolor={colors['model_color_B']};

      "app.domain.models.user";
      "app.domain.models.message";
      "app.domain.models.customer";
    }}
    // ==== Interfaces =====
    subgraph cluster_interfaces {{
      label="Interfaces\n(IUserRepository, etc.)";
      color={colors['inter_color_A']};
      style="filled,rounded";
      fillcolor={colors['inter_color_B']};

      "app.domain.interfaces.user_repository";
      "app.domain.interfaces.message_repository";
      "app.domain.interfaces.customer_repository";
      "app.domain.interfaces.ai_responder_gateway";
      "app.domain.interfaces.message_gateway";
      "app.domain.interfaces.token_service";
    }}
  }}

  // ===== Infrastructure Layer =====
  subgraph cluster_infrastructure_layer {{
    label="Infrastructure Layer";
    color={colors['infra_color_A']};
    style="filled,rounded";
    fillcolor={colors['infra_color_B']};

    // ===== Repositories =====
    subgraph cluster_repositories {{
      label="Repositories Impl\n(UserRepositoryImpl, etc.)";
      color={colors['repo_color_A']};
      style="filled,rounded";
      fillcolor={colors['repo_color_B']};

      "app.infrastructure.repositories.user_repository_postgres";
      "app.infrastructure.repositories.message_repository_postgres";
      "app.infrastructure.repositories.customer_repository_postgres";
    }}

    // ===== Gateways =====
    subgraph cluster_gateways {{
      label="Gateways Impl\n(WhatsAppGatewayImpl, etc.)";
      color={colors['gate_color_A']};
      style="filled,rounded";
      fillcolor={colors['gate_color_B']};

      "app.infrastructure.gateways.ai_responder_gateway_openai";
      "app.infrastructure.gateways.message_gateway_whatsapp";
      "app.infrastructure.gateways.openai_client";
    }}

    // ===== Orm =====
    subgraph cluster_orm {{
      label="Orm";
      color={colors['orm_color_A']}
      style="filled,rounded";
      fillcolor={colors['orm_color_B']};

      "app.infrastructure.orm.base";
      "app.infrastructure.orm.user_orm";
      "app.infrastructure.orm.user_mapper";
      "app.infrastructure.orm.message_orm";
      "app.infrastructure.orm.message_mapper";
      "app.infrastructure.orm.customer_orm";
      "app.infrastructure.orm.customer_mapper";
    }}

    // ===== Security =====
    subgraph cluster_secutiry {{
      label="Security";
      color={colors['sec_color_A']};
      style="filled,rounded";
      fillcolor={colors['sec_color_B']}

      "app.infrastructure.security.jwt_config";
      "app.infrastructure.security.token_service_jwt";
    }}
  }}

  // ===== Application Layer =====
  subgraph cluster_application_layer {{
    label="Application Layer";
    color={colors['app_color_A']};
    style="filled,rounded";
    fillcolor={colors['app_color_B']};

    // ===== dtos =====
    subgraph cluster_dtos {{
      label="DTOs";
      color={colors['dto_color_A']};
      style="filled,rounded";
      fillcolor={colors['dto_color_B']};

      "app.presentation.dtos.user_dto";
      "app.presentation.dtos.message_dto";
      "app.presentation.dtos.customer_dto";
      "app.presentation.dtos.auth_dto";
      "app.presentation.dtos.gpt_dto";
      "app.presentation.dtos.whatsapp_webhook_dto";
    }}

    // ===== User =====
    subgraph cluster_user_application {{
      label="User Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

      "app.application.user.authenticate_user";
      "app.application.user.create_user";
      "app.application.user.delete_user";
      "app.application.user.get_all_users";
      "app.application.user.get_user";
      "app.application.user.update_user.py";
    }}
    // ===== Message =====
    subgraph cluster_message_application {{
      label="Message Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

      "app.application.message.analyze_message";
      "app.application.message.get_all_messages";
      "app.application.message.receive_message";
      "app.application.message.send_message";
      "app.application.message.save_outbound_message";
    }}
    // ===== Customer =====
    subgraph cluster_customer_application {{
      label="Customer Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

      "app.application.customer.create_customer";
      "app.application.customer.delete_customer";
      "app.application.customer.get_all_customers";
      "app.application.customer.get_customer";
      "app.application.customer.update_customer";
    }}
    // ===== Integration =====
    subgraph cluster_integration_application {{
      label="Integration Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

      "app.application.integration.generate_ai_reply";
      "app.application.integration.process_ai_reply";
      "app.application.integration.receive_whatsapp_message";
    }}
  }}

  // ===== Presentation Layer =====
  subgraph cluster_presentation_layer {{
    label="Presentation Layer";
    color={colors['pres_color_A']};
    style="filled,rounded";
    fillcolor={colors['pres_color_B']};

    // ===== Controllers =====
    subgraph cluster_controllers {{
      label="Routers\n(user_router, whatsapp_router, etc.)";
      color={colors['cont_color_A']};
      style="filled,rounded";
      fillcolor={colors['cont_color_B']};

      "app.presentation.controllers.user_routes";
      "app.presentation.controllers.message_routes";
      "app.presentation.controllers.customer_routes";
      "app.presentation.controllers.auth_routes";
      "app.presentation.controllers.gpt_routes";
      "app.presentation.controllers.webhook_whatsapp_routes";
    }}
    // ===== Dependencies =====
    subgraph cluster_dependencies {{
      label="Dependencies";
      color={colors['dep_color_A']};
      style="filled,rounded";
      fillcolor={colors['dep_color_B']};

      "app.presentation.dependencies.di_user";
      "app.presentation.dependencies.di_message";
      "app.presentation.dependencies.di_customer";
      "app.presentation.dependencies.di_auth";
      "app.presentation.dependencies.di_ai";
    }}
    "app.main";
  }}

  // ===== Core Layer =====
  subgraph cluster_core_layer {{
    label="Core Layer";
    color={colors['core_color_A']};
    style="filled,rounded";
    fillcolor={colors['core_color_B']};

    "app.core.config";
    "app.core.database";
  }}

  // ===== Edges =====

  // ===== User Module =====
  "app.main" -> "app.presentation.controllers.user_routes" [color={colors['pres_color_A']}];
  
  "app.presentation.controllers.user_routes" -> "app.presentation.dependencies.di_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.presentation.dtos.user_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.create_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.delete_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.get_all_users" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.get_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.core.database" [color={colors['cont_color_A']}];

  //"app.presentation.dependencies.di_user" -> "app.domain.interfaces.user_repository" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.create_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.get_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.get_all_users" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.delete_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.infrastructure.repositories.user_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.user_repository" -> "app.domain.models.user" [color={colors['inter_color_A']}];

  "app.application.user.create_user" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.create_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.application.user.get_user" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.get_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.application.user.get_all_users" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.get_all_users" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.application.user.delete_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.infrastructure.repositories.user_repository_postgres" -> "app.domain.models.user" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.domain.interfaces.user_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.infrastructure.orm.user_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.infrastructure.orm.user_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.user_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];
  
  "app.infrastructure.orm.user_mapper" -> "app.domain.models.user" [color={colors['orm_color_A']}];
  "app.infrastructure.orm.user_mapper" -> "app.infrastructure.orm.user_orm" [color={colors['orm_color_A']}];

  "app.presentation.dtos.user_dto" -> "app.domain.models.user" [color={colors['dto_color_A']}];

  "app.core.database" -> "app.core.config" [color={colors['core_color_A']}];

  // ===== Message Module =====
  "app.main" -> "app.presentation.controllers.message_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.message_routes" -> "app.presentation.dependencies.di_message" [color={colors['cont_color_A']}];
  "app.presentation.controllers.message_routes" -> "app.presentation.dtos.message_dto" [color={colors['cont_color_A']}];

  //"app.presentation.dependencies.di_message" -> "app.domain.interfaces.message_repository" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_message" -> "app.application.integration.receive_whatsapp_message" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_message" -> "app.infrastructure.repositories.message_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.message_repository" -> "app.domain.models.message" [color={colors['inter_color_A']}];

  "app.application.integration.receive_whatsapp_message" -> "app.domain.models.message" [color={colors['use_color_A']}];
  "app.application.integration.receive_whatsapp_message" -> "app.domain.interfaces.message_repository" [color={colors['use_color_A']}];

  "app.infrastructure.repositories.message_repository_postgres" -> "app.domain.models.message" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.domain.interfaces.message_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.infrastructure.orm.message_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.infrastructure.orm.message_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.message_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];

  "app.infrastructure.orm.message_mapper" -> "app.domain.models.message" [color={colors['orm_color_A']}];
  "app.infrastructure.orm.message_mapper" -> "app.infrastructure.orm.message_orm" [color={colors['orm_color_A']}];

  "app.presentation.dtos.message_dto" -> "app.domain.models.message" [color={colors['dto_color_A']}];

  // ===== Customer Module =====
  "app.main" -> "app.presentation.controllers.customer_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.customer_routes" -> "app.presentation.dependencies.di_customer" [color={colors['cont_color_A']}];
  "app.presentation.controllers.customer_routes" -> "app.presentation.dtos.customer_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.customer_routes" -> "app.application.customer.create_customer" [color={colors['cont_color_A']}];
  "app.presentation.controllers.customer_routes" -> "app.core.database" [color={colors['cont_color_A']}];

  //"app.presentation.dependencies.di_customer" -> "app.domain.interfaces.customer_repository" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_customer" -> "app.application.customer.create_customer" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_customer" -> "app.infrastructure.repositories.customer_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.customer_repository" -> "app.domain.models.customer" [color={colors['inter_color_A']}];

  "app.application.customer.create_customer" -> "app.domain.models.customer" [color={colors['use_color_A']}];
  "app.application.customer.create_customer" -> "app.domain.interfaces.customer_repository" [color={colors['use_color_A']}];

  "app.infrastructure.repositories.customer_repository_postgres" -> "app.domain.models.customer" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.domain.interfaces.customer_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.infrastructure.orm.customer_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.infrastructure.orm.customer_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.customer_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];

  "app.infrastructure.orm.customer_mapper" -> "app.domain.models.customer" [color={colors['orm_color_A']}];
  "app.infrastructure.orm.customer_mapper" -> "app.infrastructure.orm.customer_orm" [color={colors['orm_color_A']}];

  "app.presentation.dtos.customer_dto" -> "app.domain.models.customer" [color={colors['dto_color_A']}];

  // ===== Customer Module =====
  "app.main" -> "app.presentation.controllers.auth_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.auth_routes" -> "app.application.user.authenticate_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.auth_routes" -> "app.presentation.dependencies.di_auth" [color={colors['cont_color_A']}];
  "app.presentation.controllers.auth_routes" -> "app.presentation.dtos.auth_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.auth_routes" -> "app.core.database" [color={colors['cont_color_A']}];

  "app.application.user.authenticate_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];
  "app.application.user.authenticate_user" -> "app.domain.interfaces.token_service" [color={colors['use_color_A']}];

  //"app.presentation.dependencies.di_auth" -> "app.domain.interfaces.user_repository" [color={colors['dep_color_A']}];
  //"app.presentation.dependencies.di_auth" -> "app.domain.interfaces.token_service" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_auth" -> "app.application.user.authenticate_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_auth" -> "app.infrastructure.repositories.user_repository_postgres" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_auth" -> "app.infrastructure.security.token_service_jwt" [color={colors['dep_color_A']}];

  "app.infrastructure.security.token_service_jwt" -> "app.infrastructure.security.jwt_config" [color={colors['sec_color_A']}];

  // ===== Webhook Whatsapp Module =====
  "app.main" -> "app.presentation.controllers.webhook_whatsapp_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.webhook_whatsapp_routes" -> "app.application.integration.receive_whatsapp_message" [color={colors['cont_color_A']}];
  "app.presentation.controllers.webhook_whatsapp_routes" -> "app.presentation.dependencies.di_message" [color={colors['cont_color_A']}];
  "app.presentation.controllers.webhook_whatsapp_routes" -> "app.presentation.dtos.whatsapp_webhook_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.webhook_whatsapp_routes" -> "app.core.database" [color={colors['cont_color_A']}];

  "app.application.integration.receive_whatsapp_message" -> "app.domain.models.message" [color={colors['use_color_A']}];
  "app.application.integration.receive_whatsapp_message" -> "app.domain.interfaces.message_repository" [color={colors['use_color_A']}];

  // ===== GPT Whatsapp Module =====
  "app.main" -> "app.presentation.controllers.gpt_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.gpt_routes" -> "app.application.integration.process_ai_reply" [color={colors['cont_color_A']}];
  "app.presentation.controllers.gpt_routes" -> "app.presentation.dtos.gpt_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.gpt_routes" -> "app.presentation.dependencies.di_ai" [color={colors['cont_color_A']}];

  "app.application.integration.process_ai_reply" -> "app.application.integration.generate_ai_reply" [color={colors['use_color_A']}];
  "app.application.integration.process_ai_reply" -> "app.application.message.save_outbound_message" [color={colors['use_color_A']}];

  "app.application.integration.generate_ai_reply" -> "app.domain.interfaces.ai_responder_gateway" [color={colors['use_color_A']}];

  //"app.presentation.dependencies.di_ai" -> "app.domain.interfaces.ai_responder_gateway" [color={colors['dep_color_A']}];
  //"app.presentation.dependencies.di_ai" -> "app.domain.interfaces.message_repository" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.application.integration.generate_ai_reply" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.application.message.save_outbound_message" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.application.integration.process_ai_reply" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.infrastructure.gateways.ai_responder_gateway_openai" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.infrastructure.gateways.openai_client" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_ai" -> "app.infrastructure.repositories.message_repository_postgres" [color={colors['dep_color_A']}];

  "app.application.message.save_outbound_message" -> "app.domain.models.message" [color={colors['use_color_A']}];
  "app.application.message.save_outbound_message" -> "app.domain.interfaces.message_repository" [color={colors['use_color_A']}];

  "app.infrastructure.gateways.ai_responder_gateway_openai" -> "app.domain.interfaces.ai_responder_gateway" [color={colors['gate_color_A']}];

  "app.infrastructure.gateways.openai_client" -> "app.core.config" [color={colors['gate_color_A']}];

  

}}
"""
with open("dependency_graph.dot", "w") as f:
    f.write(dot)