import os
from openai import OpenAI
from backend.populate_vec_db_and_seach import search_book


def generate(user_prompt,book_name):
    #book_name = "Pride And Prejudice"
    print(f"[DEBUG] In Generate Function with book_name :{book_name!r}")
    print(f"[DEBUG] In Generate Function with user_prompt :{user_prompt!r}")
    
    # 1. Vector search (returns list of dicts)
    hits = search_book(book_name, user_prompt)

    # 2. Prepare a text block summarizing retrieved context
    context_text = "\n\n".join(
        f"[Match {i+1}] (score={h['score']})\n{h['text']}"
        for i, h in enumerate(hits)
    )

    # 3. Create messages for chat-style Responses API
    print(f"[DEBUG] paragraphs fetched {context_text!r}")

    input = [
        {
            "role": "developer",
            "content": (
                "You are a book assistant. Use only the provided retrieved passages "
                "to answer the user. If the answer is not in the retrieved text, say so.\n\n"
                f"Retrieved context:\n{context_text}"
            )
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    # 4. Initialize client using HF Secrets
    client = OpenAI(api_key=os.environ["CHATGPT_API_KEY"])

    # 5. Call model
    response = client.responses.create(
        model="gpt-5-nano",
        input=input,
        temprerature=0.4
    )

    answer = response.output_text
    print(f"[DEBUG] generated message = {answer!r}")
    return answer
