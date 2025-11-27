from logging import exception
import itertools 
from datasets import load_dataset
from qdrant_client import QdrantClient ,models
from itertools import dropwhile, takewhile
from fastembed import TextEmbedding 
import os


#--------------------------- values ------------------------------------------

QDRANT_URL = os.getenv("QDRANT_URL")  # from HF Secrets
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# ------------------- Function to get paragraphs---------------------------

def get_paragraphs(book_name_sup: str):
    print(f"[DEBUG] get_paragraphs called with book_name_sup={book_name_sup}", flush=True)

    # 1. Try loading the dataset ----------
    try:
        print("[DEBUG] Loading dataset…", flush=True)
        dataset = load_dataset(
            "Navanjana/Gutenberg_books", 
            split="train", 
            streaming=True
        )
        print("[DEBUG] Dataset loaded successfully (streaming mode).", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}", flush=True)
        return []
    
    # 2. Start scanning dataset until we find the target book ----------
    print("[DEBUG] Starting dropwhile (scanning until first matching book)…", flush=True)
    start_stream = dropwhile(lambda x: x.get("book_name") != book_name_sup, dataset)

    # 3. Prepare takewhile ----------
    print("[DEBUG] Starting takewhile (reading only matching book rows)…", flush=True)
    book_stream = takewhile(lambda x: x.get("book_name") == book_name_sup, start_stream)

    selected_paragraphs = []
    row_count = 0
    match_count = 0
    
    # 4. Iterate through streaming rows ----------
    print("[DEBUG] Iterating through book_stream…", flush=True)
    for row in book_stream:
        row_count += 1
        
        if row_count <= 3:  # First few rows, to confirm structure
            print(f"[DEBUG] Sample row #{row_count}: {row}", flush=True)

        text = row.get("paragraph")
        if text:
            match_count += 1

        if text and len(text) > 20:
            selected_paragraphs.append(text)

        # Safety break: prevent infinite loops or huge scanning
        if row_count % 500 == 0:
            print(f"[DEBUG] Processed {row_count} rows so far, paragraphs collected: {len(selected_paragraphs)}", flush=True)

    # 5. Summary ----------
    print(f"[DEBUG] Finished streaming. Total matching rows: {match_count}", flush=True)
    print(f"[DEBUG] Total selected paragraphs (len > 20): {len(selected_paragraphs)}", flush=True)

    if len(selected_paragraphs) == 0:
        print(f"[WARNING] No paragraphs found for book '{book_name_sup}'.", flush=True)
    
    return selected_paragraphs


#------------------------------ Function to check of collection already exists in qdrant -------------------------
def does_collection_exist(collection_name , client):
  collections = client.get_collections()
  existing_collection_names = {
    collection_info.name.lower()
    for collection_info in collections.collections
  }
  if collection_name not in existing_collection_names:
    return False
  else:
    return True

 #--------------------------------Create a collection function ---------------------------------------
def create_collection(collection_name,client , model , embedding_model):
     client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=model.get_embedding_size(model_name=embedding_model), 
            distance=models.Distance.COSINE
        )
    )
#---------------------- calculate embeddings and upload paragraphs to collection ---------------------------

def upload_embeddings(docs,client,model,collection_name):
  batch_size = 100
  for i in range(0, len(docs), batch_size):
    batch = docs[i:i + batch_size]
    embeddings = list(model.embed(batch))
    points = [
        models.PointStruct(
            id=i + idx,  # unique ID for each vector
            vector=embedding.tolist(),
            payload={"text": text}
        )
        for idx, (embedding, text) in enumerate(zip(embeddings, batch))
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )   
#--------------------------  if book collection exists  move to search if not create collection and populate it with paragraph embeddings ------------------------------------

def create_populate_collection_if_not_exist(book_name_sup):
    print(f"[DEBUG] create_populate_collection_if_not_exist called with: {book_name_sup}")
    client = get_client()
    print("[DEBUG] got Qdrant client")
    model = get_model()
    print("[DEBUG] got embedding model")

    collection_name = book_name_sup.lower().replace(" ", "_")
    print(f"[DEBUG] computed collection_name = {collection_name}")

    collection_exists = does_collection_exist(collection_name, client)
    print(f"[DEBUG] does_collection_exist -> {collection_exists}")

    if collection_exists:
        print("[DEBUG] collection exists, returning 'exists'")
        return "exists"

    create_collection(collection_name, client, model, EMBEDDING_MODEL_NAME)
    print("[DEBUG] collection created")

    selected_paragraphs = get_paragraphs(book_name_sup)
    print(f"[DEBUG] fetched {len(selected_paragraphs)} paragraphs")

    upload_embeddings(selected_paragraphs, client, model, collection_name)
    print("[DEBUG] upload_embeddings finished")

    return "populated"
 

#-------------------------------search------------------------------------------
def search_book(
    bookname: str,
    query_text: str,
    top_k: int = 10,
    score_threshold: float | None = None,
):

    client = get_client()
    model = get_model()
    # 1) Embed the query text
    print("[DEBUG] Calculating Query Vector ........")
    query_vector = list(model.embed([query_text]))[0]
    print(f"Query Vecot : {query_vector}")
    collection_name = collection_name_for_book(bookname)
    # 2) Query Qdrant with cosine similarity (collection is configured as COSINE)
    result = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        score_threshold=score_threshold,  # e.g. 0.3 to filter very weak matches
    )

    # 3) Extract useful info
    hits = []
    for point in result.points:
        hits.append(
            {
                "id": point.id,
                "score": point.score,        # cosine similarity (higher = more similar)
                "text": point.payload["text"]
            }
        )
    print(f"We got some paragraphs Hits:{hits[0]}")   
    return hits


def collection_name_for_book(book_name: str) -> str:
    return book_name.lower().replace(" ", "_")


def get_client() -> QdrantClient:
    print(f"[DEBUG] QDRANT_URL={QDRANT_URL}, QDRANT_API_KEY is set={QDRANT_API_KEY is not None}")
    if QDRANT_URL is None or QDRANT_API_KEY is None:
        raise RuntimeError("QDRANT_URL or QDRANT_API_KEY is not set in environment.")
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )

def get_model() -> TextEmbedding:
    return TextEmbedding(model_name=EMBEDDING_MODEL_NAME)

