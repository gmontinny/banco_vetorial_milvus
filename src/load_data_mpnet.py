
import csv
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer

# --- Configuração ---
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "diario_uniao_mpnet" # Nova coleção para este modelo
CSV_FILE_PATH = "C:/projetos-ia/milvus/data/diario_uniao.csv"

# --- Modelo de Embedding ---
# Modelo: all-mpnet-base-v2. Um modelo maior que produz vetores de 768 dimensões.
MODEL_NAME = 'all-mpnet-base-v2'
embedding_model = SentenceTransformer(MODEL_NAME)
VECTOR_DIMENSION = embedding_model.get_sentence_embedding_dimension()

def connect_to_milvus():
    """Estabelece a conexão com o servidor Milvus."""
    print("Conectando ao Milvus...")
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
    print("Conexão com o Milvus estabelecida com sucesso.")

def create_collection_if_not_exists():
    """Cria uma coleção no Milvus se ela ainda não existir."""
    if utility.has_collection(COLLECTION_NAME):
        print(f"A coleção '{COLLECTION_NAME}' já existe. Criação ignorada.")
        return Collection(COLLECTION_NAME)

    print(f"A coleção '{COLLECTION_NAME}' não existe. Criando...")
    
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="orgao", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="tipo_ato", dtype=DataType.VARCHAR, max_length=200),
        FieldSchema(name="data_publicacao", dtype=DataType.VARCHAR, max_length=20),
        FieldSchema(name="secao", dtype=DataType.VARCHAR, max_length=10),
        FieldSchema(name="resumo_texto", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSION)
    ]
    schema = CollectionSchema(fields, description="Coleção para o modelo all-mpnet-base-v2")
    
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    print(f"Coleção '{COLLECTION_NAME}' criada com sucesso.")
    
    print("Criando índice para a coleção...")
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    print("Índice criado com sucesso.")
    
    return collection

def load_csv_and_prepare_data():
    """Lê o arquivo CSV e prepara os dados para inserção."""
    print(f"Lendo dados de '{CSV_FILE_PATH}'...")
    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    
    resumos = [row['resumo_texto'] for row in data]

    print(f"Gerando embeddings com o modelo {MODEL_NAME}...")
    embeddings = embedding_model.encode(resumos)
    print("Embeddings gerados.")

    entities = [
        [int(row['id']) for row in data],
        [row['orgao'] for row in data],
        [row['tipo_ato'] for row in data],
        [row['data_publicacao'] for row in data],
        [row['secao'] for row in data],
        resumos,
        embeddings
    ]
    
    return entities

def main():
    """Função principal para executar o processo de carregamento de dados."""
    try:
        connect_to_milvus()
        collection = create_collection_if_not_exists()
        
        if collection.num_entities == 0:
            entities_to_insert = load_csv_and_prepare_data()
            print("Inserindo dados no Milvus...")
            collection.insert(entities_to_insert)
            collection.flush()
            print(f"{len(entities_to_insert[0])} entidades inseridas com sucesso em '{COLLECTION_NAME}'.")
        else:
            print("A coleção não está vazia. Inserção de dados ignorada.")

        collection.load()
        print(f"Coleção '{COLLECTION_NAME}' carregada em memória.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if connections.has_connection("default"):
            connections.disconnect("default")
            print("Desconectado do Milvus.")

if __name__ == "__main__":
    main()
