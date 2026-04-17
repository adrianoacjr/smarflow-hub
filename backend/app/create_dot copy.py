colors = {
    'main_color_A': '"#000000"',
    'main_color_B': '"#000000"',
    # === DOMAIN LAYER ===
    # Tons terrosos/laranja representam a base conceitual sólida do sistema
    'dom_color_A': '"#000000"',   # Vermelho escuro (fundamento)
    'dom_color_B': '"#fffbc2"',   # Vermelho claro

    # Models – base de entidades, estável e confiável
    'model_color_A': '"#d65600"', # Marrom escuro (terra/base)
    'model_color_B': '"#ff802b"', # Marrom claro

    # Interfaces – conectam, são pontes (amarelo esverdeado)
    'inter_color_A': '"#d9d95f"', # Amarelo oliva escuro
    'inter_color_B': '"#ffff87"', # Amarelo claro

    # === INFRASTRUCTURE LAYER ===
    # Representa a sustentação técnica (tons de cinza/vermelho metálico)
    'infra_color_A': '"#000000"', # Bordô escuro (profundidade)
    'infra_color_B': '"#c2ffc4"', # Lilás metálico suave

    # Repositories – parte técnica, armazenamento (verde, “persistência”)
    'repo_color_A': '"#00a30b"',  # Verde escuro
    'repo_color_B': '"#14ff24"',  # Verde claro

    # Gateways – interfaces externas, conexão com o mundo (azul petróleo)
    'gate_color_A': '"#00bf79"',  # Verde-azulado escuro
    'gate_color_B': '"#2effb2"',  # Verde-água claro

    # === APPLICATION LAYER ===
    # Camada lógica e de orquestração (roxo — inteligência e abstração)
    'app_color_A': '"#000000"',   # Roxo escuro
    'app_color_B': '"#ffc2c2"',   # Roxo claro

    # Use cases – a “mente” do sistema (violeta vibrante)
    'use_color_A': '"#bf4e4e"',   # Roxo médio (já ótimo)
    'use_color_B': '"#ff7d7d"',   # Roxo lavanda

    # user
    'user_color_A': '"#c44545"',
    'user_color_B': '"#ff6b6b"',
    # message
    'mess_color_A': '"#cc3b3b"',
    'mess_color_B': '"#ff5959"',
    # customer
    'cust_color_A': '"#cf2d2d"',
    'cust_color_B': '"#ff4a4a"',
    # integration
    'inte_color_A': '"#d11f1f"',
    'inte_color_B': '"#ff3838"',

    # === PRESENTATION LAYER ===
    # Comunicação com o usuário (vermelho/rosa – energia, interface)
    'pres_color_A': '"#000000"',  # Vermelho forte
    'pres_color_B': '"#c2e4ff"',  # Rosa claro

    # Controllers – controle e entrada (cinza-azulado, neutro e sólido)
    'cont_color_A': '"#263238"',  # Azul petróleo escuro
    'cont_color_B': '"#90A4AE"',  # Cinza-azulado claro

    # DTOs – transporte de dados (laranja, clareza e estrutura)
    'dto_color_A': '"#E65100"',   # Laranja escuro
    'dto_color_B': '"#FFCC80"',   # Laranja claro

    # Dependencies – injeção e ligação (ciano, remete à conexão)
    'dep_color_A': '"#1120a8"',   # Azul petróleo escuro
    'dep_color_B': '"#7d8aff"',   # Azul claro

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

    // ===== Entities =====
    subgraph cluster_entities {{
      label="Entities & Value Objects\n(User, etc.)";
      color={colors['model_color_A']};
      style="filled,rounded";
      fillcolor={colors['model_color_B']};

      "app.domain.entities.user";
      "app.domain.entities.message";
      "app.domain.entities.customer";
    }}
    // ==== Interfaces =====
    subgraph cluster_domain_interfaces {{
      label="Interfaces\n(IUserRepository, etc.)";
      color={colors['inter_color_A']};
      style="filled,rounded";
      fillcolor={colors['inter_color_B']};

      "app.domain.interfaces.user_repository";
      "app.domain.interfaces.message_repository";
      "app.domain.interfaces.customer_repository";
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

      "app.adapters.dtos.user_dto";
      "app.adapters.dtos.message_dto";
      "app.adapters.dtos.customer_dto";
      "app.adapters.dtos.auth_dto";
      "app.adapters.dtos.gpt_dto";
      "app.adapters.dtos.whatsapp_webhook_dto";
    }}

    // ===== Use Cases =====
    subgraph cluster_use_cases {{
      label="User Cases Layer";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};
      // ===== User =====
      subgraph cluster_user_application {{
        label="User Application";
        color={colors['user_color_A']};
        style="filled,rounded";
        fillcolor={colors['user_color_B']};

        "app.application.use_cases.user.authenticate_user";
        "app.application.use_cases.user.create_user";
        "app.application.use_cases.user.delete_user";
        "app.application.use_cases.user.get_all_users";
        "app.application.use_cases.user.get_user";
        "app.application.use_cases.user.update_user";
      }}
      // ===== Message =====
      subgraph cluster_message_application {{
        label="Message Application";
        color={colors['mess_color_A']};
        style="filled,rounded";
        fillcolor={colors['mess_color_B']};

        "app.application.use_cases.message.create_message";
        "app.application.use_cases.message.get_message_by_id";
        "app.application.use_cases.message.list_message_by_user";
        "app.application.use_cases.message.list_message_by_customer";
        "app.application.use_cases.message.delete_message";
        "app.application.use_cases.message.analyze_message";
        "app.application.use_cases.message.get_all_messages";
        "app.application.use_cases.message.receive_message";
        "app.application.use_cases.message.send_message";
        "app.application.use_cases.message.save_outbound_message";
      }}
      // ===== Customer =====
      subgraph cluster_customer_application {{
        label="Customer Application";
        color={colors['cust_color_A']};
        style="filled,rounded";
        fillcolor={colors['cust_color_B']};

        "app.application.use_cases.customer.create_customer";
        "app.application.use_cases.customer.delete_customer";
        "app.application.use_cases.customer.get_all_customers";
        "app.application.use_cases.customer.get_customer";
        "app.application.use_cases.customer.update_customer";
      }}
      // ===== Integration =====
      subgraph cluster_integration_application {{
        label="Integration Application";
        color={colors['inte_color_A']};
        style="filled,rounded";
        fillcolor={colors['inte_color_B']};

        "app.application.use_cases.integration.generate_ai_reply";
        "app.application.use_cases.integration.process_ai_reply";
        "app.application.use_cases.integration.receive_whatsapp_message";
      }}
    }}

    // ==== Interfaces =====
    subgraph cluster_application_interfaces {{
      label="Interfaces\n(IUserRepository, etc.)";
      color={colors['inter_color_A']};
      style="filled,rounded";
      fillcolor={colors['inter_color_B']};

      "app.application.interfaces.ai_responder_gateway";
      "app.application.interfaces.message_gateway";
      "app.application.interfaces.token_service";
    }}
  }}

  // ===== Adapters Layer =====
  subgraph cluster_adapters_layer {{
    label="Adapters Layer";
    color={colors['infra_color_A']};
    style="filled,rounded";
    fillcolor={colors['infra_color_B']};

    // ===== Controllers =====
    subgraph cluster_controllers {{
      label="Routers\n(user_router, whatsapp_router, etc.)";
      color={colors['cont_color_A']};
      style="filled,rounded";
      fillcolor={colors['cont_color_B']};

      "app.adapters.controllers.user_routes";
      "app.adapters.controllers.message_routes";
      "app.adapters.controllers.customer_routes";
      "app.adapters.controllers.auth_routes";
      "app.adapters.controllers.gpt_routes";
      "app.adapters.controllers.webhook_whatsapp_routes";
    }}

    // ===== Security =====
    subgraph cluster_secutiry {{
      label="Security";
      color={colors['sec_color_A']};
      style="filled,rounded";
      fillcolor={colors['sec_color_B']}

      "app.adapters.security.jwt_config";
      "app.adapters.security.token_service_jwt";
    }}
  }}

  // ===== Infrastructure Layer =====
  subgraph cluster_infrastructure_layer {{
    label="Infrastructure Layer";
    color={colors['pres_color_A']};
    style="filled,rounded";
    fillcolor={colors['pres_color_B']};

    // ===== Mappers =====
    subgraph cluster_mappers {{
      label="Mappers";
      color={colors['orm_color_A']}
      style="filled,rounded";
      fillcolor={colors['orm_color_B']};

      "app.infrastructure.mappers.user_mapper";
      "app.infrastructure.mappers.message_mapper";
      "app.infrastructure.mappers.customer_mapper";
    }}

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

    // ===== Dependencies =====
    subgraph cluster_dependencies {{
      label="Dependencies";
      color={colors['dep_color_A']};
      style="filled,rounded";
      fillcolor={colors['dep_color_B']};

      "app.infrastructure.dependencies.di_user";
      "app.infrastructure.dependencies.di_message";
      "app.infrastructure.dependencies.di_customer";
      "app.infrastructure.dependencies.di_auth";
      "app.infrastructure.dependencies.di_ai";
    }}

    // ===== Orm =====
    subgraph cluster_orm {{
      label="Orm";
      color={colors['orm_color_A']}
      style="filled,rounded";
      fillcolor={colors['orm_color_B']};

      "app.infrastructure.orm.base";
      "app.infrastructure.orm.user_orm";
      "app.infrastructure.orm.message_orm";
      "app.infrastructure.orm.customer_orm";
    }}
  }}

  // ===== Core Layer =====
  subgraph cluster_core_layer {{
    label="Core Layer";
    color={colors['core_color_A']};
    style="filled,rounded";
    fillcolor={colors['core_color_B']};

    "app.infrastructure.config";
    "app.infrastructure.database";

  }}

  // ===== Edges =====
  "app.main" -> "app.infrastructure.database" [color={colors['main_color_A']}];

  // ===== User Module =====
  "app.main" -> "app.adapters.controllers.user_routes" [color={colors['main_color_A']}];
  "app.main" -> "app.infrastructure.dependencies.di_user" [color={colors['main_color_A']}];
  
  //"app.adapters.controllers.user_routes" -> "app.infrastructure.dependencies.di_user" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.adapters.dtos.user_dto" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.application.use_cases.user.create_user" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.application.use_cases.user.delete_user" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.application.use_cases.user.get_all_users" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.application.use_cases.user.get_user" [color={colors['cont_color_A']}];
  "app.adapters.controllers.user_routes" -> "app.application.use_cases.user.update_user" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.user_routes" -> "app.infrastructure.database" [color={colors['cont_color_A']}];

  //"app.infrastructure.dependencies.di_user" -> "app.domain.interfaces.user_repository" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.application.use_cases.user.create_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.application.use_cases.user.get_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.application.use_cases.user.get_all_users" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.application.use_cases.user.delete_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.application.use_cases.user.update_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_user" -> "app.infrastructure.repositories.user_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.user_repository" -> "app.domain.entities.user" [color={colors['inter_color_A']}];

  "app.application.use_cases.user.create_user" -> "app.domain.entities.user" [color={colors['user_color_A']}];
  "app.application.use_cases.user.create_user" -> "app.domain.interfaces.user_repository" [color={colors['user_color_A']}];

  "app.application.use_cases.user.get_user" -> "app.domain.entities.user" [color={colors['user_color_A']}];
  "app.application.use_cases.user.get_user" -> "app.domain.interfaces.user_repository" [color={colors['user_color_A']}];

  "app.application.use_cases.user.get_all_users" -> "app.domain.entities.user" [color={colors['user_color_A']}];
  "app.application.use_cases.user.get_all_users" -> "app.domain.interfaces.user_repository" [color={colors['user_color_A']}];

  "app.application.use_cases.user.delete_user" -> "app.domain.interfaces.user_repository" [color={colors['user_color_A']}];

  "app.infrastructure.repositories.user_repository_postgres" -> "app.domain.entities.user" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.domain.interfaces.user_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.infrastructure.orm.user_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_postgres" -> "app.infrastructure.mappers.user_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.user_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];
  
  "app.infrastructure.mappers.user_mapper" -> "app.domain.entities.user" [color={colors['orm_color_A']}];
  "app.infrastructure.mappers.user_mapper" -> "app.infrastructure.orm.user_orm" [color={colors['orm_color_A']}];

  "app.adapters.dtos.user_dto" -> "app.domain.entities.user" [color={colors['dto_color_A']}];

  "app.infrastructure.database" -> "app.infrastructure.config" [color={colors['core_color_A']}];

  // ===== Message Module =====
  "app.main" -> "app.adapters.controllers.message_routes" [color={colors['main_color_A']}];
  "app.main" -> "app.infrastructure.dependencies.di_message" [color={colors['main_color_A']}];

  //"app.adapters.controllers.message_routes" -> "app.infrastructure.dependencies.di_message" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.adapters.dtos.message_dto" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.application.use_cases.message.create_message" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.application.use_cases.message.get_message_by_id" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.application.use_cases.message.list_message_by_user" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.application.use_cases.message.list_message_by_customer" [color={colors['cont_color_A']}];
  "app.adapters.controllers.message_routes" -> "app.application.use_cases.message.delete_message" [color={colors['cont_color_A']}];

  //"app.presentation.dependencies.di_message" -> "app.domain.interfaces.message_repository" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.integration.receive_whatsapp_message" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.message.create_message" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.message.get_message_by_id" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.message.list_message_by_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.message.list_message_by_customer" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.application.use_cases.message.delete_message" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_message" -> "app.infrastructure.repositories.message_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.message_repository" -> "app.domain.entities.message" [color={colors['inter_color_A']}];

  "app.application.use_cases.integration.receive_whatsapp_message" -> "app.domain.entities.message" [color={colors['inte_color_A']}];
  "app.application.use_cases.integration.receive_whatsapp_message" -> "app.domain.interfaces.message_repository" [color={colors['inte_color_A']}];

  "app.infrastructure.repositories.message_repository_postgres" -> "app.domain.entities.message" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.domain.interfaces.message_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.infrastructure.orm.message_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.message_repository_postgres" -> "app.infrastructure.mappers.message_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.message_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];

  "app.infrastructure.mappers.message_mapper" -> "app.domain.entities.message" [color={colors['orm_color_A']}];
  "app.infrastructure.mappers.message_mapper" -> "app.infrastructure.orm.message_orm" [color={colors['orm_color_A']}];

  "app.adapters.dtos.message_dto" -> "app.domain.entities.message" [color={colors['dto_color_A']}];

  // ===== Customer Module =====
  "app.main" -> "app.adapters.controllers.customer_routes" [color={colors['main_color_A']}];
  "app.main" -> "app.infrastructure.dependencies.di_customer" [color={colors['main_color_A']}];

  //"app.adapters.controllers.customer_routes" -> "app.infrastructure.dependencies.di_customer" [color={colors['cont_color_A']}];
  "app.adapters.controllers.customer_routes" -> "app.adapters.dtos.customer_dto" [color={colors['cont_color_A']}];
  "app.adapters.controllers.customer_routes" -> "app.application.use_cases.customer.create_customer" [color={colors['cont_color_A']}];
  "app.adapters.controllers.customer_routes" -> "app.application.use_cases.customer.delete_customer" [color={colors['cont_color_A']}];
  "app.adapters.controllers.customer_routes" -> "app.application.use_cases.customer.get_all_customers" [color={colors['cont_color_A']}];
  "app.adapters.controllers.customer_routes" -> "app.application.use_cases.customer.get_customer" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.customer_routes" -> "app.infrastructure.database" [color={colors['cont_color_A']}];

  //"app.presentation.dependencies.di_customer" -> "app.domain.interfaces.customer_repository" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_customer" -> "app.application.use_cases.customer.create_customer" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_customer" -> "app.infrastructure.repositories.customer_repository_postgres" [color={colors['dep_color_A']}];

  "app.domain.interfaces.customer_repository" -> "app.domain.entities.customer" [color={colors['inter_color_A']}];

  "app.application.use_cases.customer.create_customer" -> "app.domain.entities.customer" [color={colors['cust_color_A']}];
  "app.application.use_cases.customer.create_customer" -> "app.domain.interfaces.customer_repository" [color={colors['cust_color_A']}];

  "app.infrastructure.repositories.customer_repository_postgres" -> "app.domain.entities.customer" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.domain.interfaces.customer_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.infrastructure.orm.customer_orm" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.customer_repository_postgres" -> "app.infrastructure.mappers.customer_mapper" [color={colors['repo_color_A']}];

  "app.infrastructure.orm.customer_orm" -> "app.infrastructure.orm.base" [color={colors['orm_color_A']}];

  "app.infrastructure.mappers.customer_mapper" -> "app.domain.entities.customer" [color={colors['orm_color_A']}];
  "app.infrastructure.mappers.customer_mapper" -> "app.infrastructure.orm.customer_orm" [color={colors['orm_color_A']}];

  "app.adapters.dtos.customer_dto" -> "app.domain.entities.customer" [color={colors['dto_color_A']}];

  // ===== Auth Module =====
  "app.main" -> "app.adapters.controllers.auth_routes" [color={colors['main_color_A']}];
  "app.main" -> "app.infrastructure.dependencies.di_auth" [color={colors['main_color_A']}];

  "app.adapters.controllers.auth_routes" -> "app.application.use_cases.user.authenticate_user" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.auth_routes" -> "app.infrastructure.dependencies.di_auth" [color={colors['cont_color_A']}];
  "app.adapters.controllers.auth_routes" -> "app.adapters.dtos.auth_dto" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.auth_routes" -> "app.infrastructure.database" [color={colors['cont_color_A']}];

  "app.application.use_cases.user.authenticate_user" -> "app.domain.interfaces.user_repository" [color={colors['user_color_A']}];
  "app.application.use_cases.user.authenticate_user" -> "app.application.interfaces.token_service" [color={colors['user_color_A']}];

  //"app.presentation.dependencies.di_auth" -> "app.domain.interfaces.user_repository" [color={colors['dep_color_A']}];
  //"app.presentation.dependencies.di_auth" -> "app.application.interfaces.token_service" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_auth" -> "app.application.use_cases.user.authenticate_user" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_auth" -> "app.infrastructure.repositories.user_repository_postgres" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_auth" -> "app.adapters.security.token_service_jwt" [color={colors['dep_color_A']}];

  "app.adapters.security.token_service_jwt" -> "app.adapters.security.jwt_config" [color={colors['sec_color_A']}];

  // ===== Webhook Whatsapp Module =====
  "app.main" -> "app.adapters.controllers.webhook_whatsapp_routes" [color={colors['main_color_A']}];

  "app.adapters.controllers.webhook_whatsapp_routes" -> "app.application.use_cases.integration.receive_whatsapp_message" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.webhook_whatsapp_routes" -> "app.infrastructure.dependencies.di_message" [color={colors['cont_color_A']}];
  "app.adapters.controllers.webhook_whatsapp_routes" -> "app.adapters.dtos.whatsapp_webhook_dto" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.webhook_whatsapp_routes" -> "app.infrastructure.database" [color={colors['cont_color_A']}];

  "app.application.use_cases.integration.receive_whatsapp_message" -> "app.domain.entities.message" [color={colors['inte_color_A']}];
  "app.application.use_cases.integration.receive_whatsapp_message" -> "app.domain.interfaces.message_repository" [color={colors['inte_color_A']}];

  // ===== GPT Whatsapp Module =====
  "app.main" -> "app.adapters.controllers.gpt_routes" [color={colors['main_color_A']}];
  "app.main" -> "app.infrastructure.dependencies.di_ai" [color={colors['main_color_A']}];

  "app.adapters.controllers.gpt_routes" -> "app.application.use_cases.integration.process_ai_reply" [color={colors['cont_color_A']}];
  "app.adapters.controllers.gpt_routes" -> "app.adapters.dtos.gpt_dto" [color={colors['cont_color_A']}];
  //"app.adapters.controllers.gpt_routes" -> "app.infrastructure.dependencies.di_ai" [color={colors['cont_color_A']}];

  "app.application.use_cases.integration.process_ai_reply" -> "app.application.use_cases.integration.generate_ai_reply" [color={colors['inte_color_A']}];
  "app.application.use_cases.integration.process_ai_reply" -> "app.application.use_cases.message.save_outbound_message" [color={colors['inte_color_A']}];

  "app.application.use_cases.integration.generate_ai_reply" -> "app.application.interfaces.ai_responder_gateway" [color={colors['inte_color_A']}];

  //"app.infrastructure.dependencies.di_ai" -> "app.application.interfaces.ai_responder_gateway" [color={colors['dep_color_A']}];
  //"app.infrastructure.dependencies.di_ai" -> "app.domain.interfaces.message_repository" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.application.use_cases.integration.generate_ai_reply" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.application.use_cases.message.save_outbound_message" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.application.use_cases.integration.process_ai_reply" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.infrastructure.gateways.ai_responder_gateway_openai" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.infrastructure.gateways.openai_client" [color={colors['dep_color_A']}];
  "app.infrastructure.dependencies.di_ai" -> "app.infrastructure.repositories.message_repository_postgres" [color={colors['dep_color_A']}];

  "app.application.use_cases.message.save_outbound_message" -> "app.domain.entities.message" [color={colors['mess_color_A']}];
  "app.application.use_cases.message.save_outbound_message" -> "app.domain.interfaces.message_repository" [color={colors['mess_color_A']}];

  "app.infrastructure.gateways.ai_responder_gateway_openai" -> "app.application.interfaces.ai_responder_gateway" [color={colors['gate_color_A']}];

  "app.infrastructure.gateways.openai_client" -> "app.infrastructure.config" [color={colors['gate_color_A']}];

  

}}
"""
with open("dependency_graph.dot", "w") as f:
    f.write(dot)