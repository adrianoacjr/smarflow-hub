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
      "app.domain.models.integration_config";
    }}
    // ==== Interfaces =====
    subgraph cluster_interfaces {{
      label="Interfaces\n(IUserRepository, etc.)";
      color={colors['inter_color_A']};
      style="filled,rounded";
      fillcolor={colors['inter_color_B']};

      "app.domain.interfaces.user_repository";
      "app.domain.interfaces.message_repository";
    }}
  }}

  // ===== Infrastructure Layer =====
  subgraph cluster_infrastructure {{
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

      "app.infrastructure.repositories.user_repository_fake";
      "app.infrastructure.repositories.message_repository_fake";
    }}

    // ===== Gateways =====
    subgraph cluster_gateways {{
      label="Gateways Impl\n(WhatsAppGatewayImpl, etc.)";
      color={colors['gate_color_A']};
      style="filled,rounded";
      fillcolor={colors['gate_color_B']};
    }}
  }}

  // ===== Application Layer =====
  subgraph cluster_application_layer {{
    label="Application Layer";
    color={colors['app_color_A']};
    style="filled,rounded";
    fillcolor={colors['app_color_B']};

    // ===== User =====
    subgraph cluster_user_application {{
      label="User Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

      "app.application.user.create_user";
      "app.application.user.get_user";
      "app.application.user.get_all_users";
      "app.application.user.delete_user";
    }}
    // ===== Message =====
    subgraph cluster_message_application {{
      label="Message Application";
      color={colors['use_color_A']};
      style="filled,rounded";
      fillcolor={colors['use_color_B']};

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
    }}
    // ===== dtos =====
    subgraph cluster_dtos {{
      label="DTOs";
      color={colors['dto_color_A']};
      style="filled,rounded";
      fillcolor={colors['dto_color_B']};

      "app.presentation.dtos.user_dto";
      "app.presentation.dtos.message_dto";
    }}
    // ===== Dependencies =====
    subgraph cluster_dependencies {{
      label="Dependencies";
      color={colors['dep_color_A']};
      style="filled,rounded";
      fillcolor={colors['dep_color_B']};

      "app.presentation.dependencies.di_user";
      "app.presentation.dependencies.di_message";
    }}
    "app.main";
  }}

  // ===== Edges =====
  // ==== User Module ====
  "app.main" -> "app.presentation.controllers.user_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.user_routes" -> "app.presentation.dtos.user_dto" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.presentation.dependencies.di_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.create_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.get_user" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.get_all_users" [color={colors['cont_color_A']}];
  "app.presentation.controllers.user_routes" -> "app.application.user.delete_user" [color={colors['cont_color_A']}];

  "app.presentation.dtos.user_dto" -> "app.domain.models.user" [color={colors['dto_color_A']}];

  "app.presentation.dependencies.di_user" -> "app.infrastructure.repositories.user_repository_fake" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.create_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.get_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.get_all_users" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.application.user.delete_user" [color={colors['dep_color_A']}];
  "app.presentation.dependencies.di_user" -> "app.domain.interfaces.user_repository" [color={colors['dep_color_A']}];
  "app.application.user.create_user" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.create_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.application.user.get_user" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.get_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];
  "app.application.user.get_all_users" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.get_all_users" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.application.user.delete_user" -> "app.domain.models.user" [color={colors['use_color_A']}];
  "app.application.user.delete_user" -> "app.domain.interfaces.user_repository" [color={colors['use_color_A']}];

  "app.infrastructure.repositories.user_repository_fake" -> "app.domain.interfaces.user_repository" [color={colors['repo_color_A']}];
  "app.infrastructure.repositories.user_repository_fake" -> "app.domain.models.user" [color={colors['repo_color_A']}];

  "app.domain.interfaces.user_repository" -> "app.domain.models.user" [color={colors['inter_color_A']}];

  // ===== Message Module =====
  "app.main" -> "app.presentation.controllers.message_routes" [color={colors['pres_color_A']}];

  "app.presentation.controllers.message_routes" -> "app.presentation.dtos.message_dto" [color={colors['cont_color_A']}];

}}
"""
with open("dependency_graph.dot", "w") as f:
    f.write(dot)