# AI Agent Analysis of a CRM System

Refs:
- https://www.dataside.com.br/dataside-community/big-data/afinal-o-que-e-a-arquitetura-medalhao
- https://www.pymc-marketing.io/en/stable/notebooks/clv/bg_nbd.html
-


Fluxo de ETL feito para o pre-processamento, FEature Engineering e previsão de modelos no dataset completo do CRM:

```mermaid
graph TD
    A[Inicio: full_dataset_preparation] --> B[Carregar dados de contas]
    A --> C[Carregar dados de produtos]
    A --> D[Carregar dados do pipeline de vendas]
    A --> E[Carregar dados das equipes de vendas]

    B --> F[Filtrar e limpar dados]
    C --> F
    D --> F
    E --> F

    F --> G[Mesclar DataFrames]
    G --> H[Pré-processamento de dados]
    H --> I{Etapa do negócio é 'Won'?}
    I -->|Sim| J[Feature Engineering para 'Won']
    I -->|Nao| K[Erro: Apenas 'Won' implementado]

    J --> L[Filtrar por deal_stage]
    L --> M[Calcular RFM]
    M --> N[Expandir recursos de RFM]

    N --> O[Modelar BG/NBD]
    N --> P[Modelar Gamma-Gamma]
    P --> Q[Prever CLTV]
    O --> Q[Prever CLTV]

    Q --> R[Remover duplicatas]
    R --> S[Mesclar CLTV e RFM com dados principais]
    S --> T[Fim: Retornar DataFrame Final]

    style K fill:#f96,stroke:#333,stroke-width:4px
    style T fill:#9f6,stroke:#333,stroke-width:4px
```