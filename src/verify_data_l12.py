from pymilvus import connections, utility, Collection

# --- Configuração ---
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "diario_uniao_l12" # Coleção para o modelo L12

def verify_data_in_milvus():
    """Conecta ao Milvus e recupera algumas entidades para verificação."""
    try:
        print("Conectando ao Milvus...")
        connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
        
        if not utility.has_collection(COLLECTION_NAME):
            print(f"A coleção '{COLLECTION_NAME}' não foi encontrada.")
            return

        collection = Collection(COLLECTION_NAME)
        collection.load()
        
        print(f"Total de entidades na coleção '{COLLECTION_NAME}': {collection.num_entities}")

        results = collection.query(
            expr="id > 0", 
            output_fields=["id", "orgao", "tipo_ato", "resumo_texto"], 
            limit=3
        )
        
        print("\nAmostra de dados recuperados:")
        for result in results:
            print(result)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if connections.has_connection("default"):
            connections.disconnect("default")
            print("\nDesconectado do Milvus.")

if __name__ == "__main__":
    verify_data_in_milvus()
