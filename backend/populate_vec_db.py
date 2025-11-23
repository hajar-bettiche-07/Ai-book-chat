from logging import exception
import itertools 
from datasets import load_dataset
from qdrant_client import QdrantClient ,models
from itertools import dropwhile, takewhile
from fastembed import TextEmbedding 
import os




# ------------------- Function to get paragraphs---------------------------

def get_paragraphs(book_name_sup:str):
  dataset = load_dataset("Navanjana/Gutenberg_books", split="train", streaming=True)
  start_stream = dropwhile(lambda x: x.get('book_name') != book_name_sup, dataset)
  book_stream = takewhile(lambda x: x.get('book_name') == book_name_sup, start_stream)
  selected_paragraphs = []
  for row in book_stream:
    text = row.get('paragraph')
    if text and len(text) > 20:
        selected_paragraphs.append(text)
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
def create_collection(collection_name,client , model , model_name):
     client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=model.get_embedding_size(model_name=embedding_model), 
            distance=models.Distance.COSINE
        )
    )
#---------------------- calculate embeddings and upload paragraphs to collection ---------------------------

def upload_embeddings(docs,model,collection_name):
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
#--------------------------  if book exists collection move to search of not create collection and populate it with paragraph embeddings ------------------------------------
book_name_sup = "Dracula" 
qdrant_api = os.getenv("Qdrant_Api")
client = QdrantClient(
    url="https://15ec16ad-cec7-4df1-b0dd-340919c72ae4.eu-central-1-0.aws.cloud.qdrant.io",
    api_key=qdrant_api,
)
embedding_model = "BAAI/bge-small-en-v1.5"
model = TextEmbedding(model_name=embedding_model)
collection_name = book_name_sup.lower().replace(" ", "_") 

collection_exists = does_collection_exist(collection_name,client)
print(f"does collection exis : {collection_exists}")

if collection_exists : 
      collection_info = client.get_collection(collection_name=collection_name)
      print(f"Collection '{collection_name}' information:")
      print(collection_info)
else : 
      create_collection(collection_name,client,model,embedding_model)
      selected_paragraphs = get_paragraphs(book_name_sup)
      upload_embeddings(selected_paragraphs,model,collection_name)

