from qdrant_client import QdrantClient ,models



qdrant_api = os.getenv("Qdrant_Api")
client = QdrantClient(
    url="https://15ec16ad-cec7-4df1-b0dd-340919c72ae4.eu-central-1-0.aws.cloud.qdrant.io",
    api_key=qdrant_api,
)

def search_book(
    collection_name: str,
    query_text: str,
    top_k: int = 5,
    score_threshold: float | None = None,
):
    

    # 1) Embed the query text
    query_vector = list(model.embed([query_text]))[0] 

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
    return hits
collection_name="dracula"
results = search_book(
    collection_name,
    "is there a soft side to dracula", ## change - here- this is the query
    top_k=5,
    score_threshold=0.3,
)
for r in results:
    print(f"Score: {r['score']:.4f}")
    print(r["text"])
    print("-" * 80)