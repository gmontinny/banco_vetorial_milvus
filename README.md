# Projeto de Exemplo com Milvus: Vetorização de Dados do Diário Oficial

## Visão Geral

Este projeto demonstra um fluxo completo de como utilizar o banco de dados vetorial Milvus para indexar e armazenar documentos de texto. O exemplo abrange modelos de *embedding* locais (open-source) e modelos via API (pagos), como o da OpenAI.

## Arquitetura

1.  **Infraestrutura (Docker Compose):**
    -   **Milvus, Etcd, MinIO:** A pilha completa para o banco de dados vetorial.
    -   **Attu:** Interface de usuário web para gerenciar e visualizar os dados no Milvus.

2.  **Scripts Python:
    -   **Scripts de Carga (`src/`):** Oito scripts de ETL, cada um dedicado a um modelo de embedding.
    -   **Scripts de Verificação:** Oito scripts para consultar e verificar os dados inseridos em cada coleção.

3.  **Dados de Exemplo (`data/`):
    -   `diario_uniao.csv`: Arquivo com dados de amostra.

## Modelos de Embedding Utilizados

### Modelos Locais (Open-Source)

Estes modelos são baixados e executados na sua máquina local.

1.  **`all-MiniLM-L6-v2`:** Dimensões: 384. Leve e rápido. (Coleção: `diario_uniao`)
2.  **`all-MiniLM-L12-v2`:** Dimensões: 384. Qualidade superior ao L6. (Coleção: `diario_uniao_l12`)
3.  **`all-mpnet-base-v2`:** Dimensões: 768. Ótimo desempenho geral. (Coleção: `diario_uniao_mpnet`)
4.  **`all-roberta-large-v1`:** Dimensões: 1024. Modelo grande e de alta precisão. (Coleção: `diario_uniao_roberta`)
5.  **`gtr-t5-large`:** Dimensões: 768. Modelo do Google para busca semântica. (Coleção: `diario_uniao_t5`)
6.  **`neuralmind/bert-base-portuguese-cased`:** Dimensões: 768. BERT treinado para português do Brasil. (Coleção: `diario_uniao_bert_pt`)
7.  **`xlm-roberta-base`:** Dimensões: 768. Modelo multilíngue (100 idiomas). (Coleção: `diario_uniao_xlm_roberta`)

### Modelo via API (Serviço Pago)

8.  **OpenAI `text-embedding-ada-002`:**
    -   **Dimensões:** 1536
    -   **Descrição:** Modelo de ponta da OpenAI, acessado via API.
    -   **Coleção:** `diario_uniao_openai`
    -   **Atenção:** Este é um **serviço pago**. O uso da API da OpenAI incorrerá em custos na sua conta OpenAI, cobrados por quantidade de dados processados.

## Como Executar o Projeto

### 1. Iniciar a Infraestrutura

```sh
docker-compose up -d --force-recreate
```

### 2. Instalar as Dependências Python

```sh
pip install -r requirements.txt
```

### 3. Configurar a Chave de API (Para OpenAI)

Para usar o exemplo da OpenAI, você precisa configurar sua chave de API como uma variável de ambiente. **Nunca coloque sua chave diretamente no código.**

Primeiro, obtenha sua chave no [site da OpenAI](https://platform.openai.com/api-keys).

Depois, defina a variável de ambiente `OPENAI_API_KEY`. A forma de fazer isso depende do seu sistema operacional:

-   **Windows (CMD):**
    ```sh
    set OPENAI_API_KEY="sua-chave-aqui"
    ```
-   **Windows (PowerShell):**
    ```sh
    $env:OPENAI_API_KEY="sua-chave-aqui"
    ```
-   **Linux / macOS:**
    ```sh
    export OPENAI_API_KEY="sua-chave-aqui"
    ```

### 4. Executar os Scripts de Carga e Verificação

**Modelos Locais (Gratuitos):**
```sh
python src/load_data_bert_pt.py && python verify_data_bert_pt.py
# (e outros scripts de modelos locais)
```

**Modelo OpenAI (Pago):**
```sh
# Certifique-se de que a variável de ambiente OPENAI_API_KEY está configurada!
python src/load_data_openai.py && python verify_data_openai.py
```

### 5. Acessando a Interface Gráfica (Attu)

-   **URL:** **http://localhost:8000**

Na interface do Attu, você poderá explorar todas as oito coleções criadas.

## Estrutura de Arquivos

```
milvus/
├── data/
│   └── diario_uniao.csv
├── src/
│   ├── load_data.py                    # MiniLM-L6-v2
│   ├── load_data_l12.py               # MiniLM-L12-v2
│   ├── load_data_mpnet.py             # MPNet-base-v2
│   ├── load_data_roberta.py           # RoBERTa-large
│   ├── load_data_t5.py                # GTR-T5-large
│   ├── load_data_bert_pt.py           # BERT-PT
│   ├── load_data_xlm_roberta.py       # XLM-RoBERTa
│   ├── load_data_openai.py            # OpenAI Ada-002
│   ├── verify_data.py                 # Verificação MiniLM-L6-v2
│   ├── verify_data_l12.py             # Verificação MiniLM-L12-v2
│   ├── verify_data_mpnet.py           # Verificação MPNet-base-v2
│   ├── verify_data_roberta.py         # Verificação RoBERTa-large
│   ├── verify_data_t5.py              # Verificação GTR-T5-large
│   ├── verify_data_bert_pt.py         # Verificação BERT-PT
│   ├── verify_data_xlm_roberta.py     # Verificação XLM-RoBERTa
│   └── verify_data_openai.py          # Verificação OpenAI Ada-002
├── volumes/                           # Dados persistentes do Docker
│   ├── etcd/                         # Dados do Etcd
│   ├── milvus/                       # Dados do Milvus
│   └── minio/                        # Dados do MinIO
├── .env                              # Variáveis de ambiente
├── artigo_projeto_milvus.md          # Artigo técnico detalhado
├── docker-compose.yml                # Configuração da infraestrutura
├── milvus.png                        # Imagem da arquitetura
├── requirements.txt                  # Dependências Python
└── README.md                         # Documentação do projeto
```
