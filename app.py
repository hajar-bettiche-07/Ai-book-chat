import gradio as gr
from backend.populate_vec_db_and_seach import search_book , create_populate_collection_if_not_exist
def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

def clickTrigger(book_name: str):
    if not book_name or not book_name.strip():
        # Don’t crash if user clicks with empty input
        return "Please enter a book name.", gr.update(visible=False)
    
    # Do the heavy work
    result = create_populate_collection_if_not_exist(book_name)

    print(f"[DEBUG] create_populate_collection_if_not_exist result: {result}", flush=True)

    if result == "exists":
        final_msg = f"Collection for '{book_name}' already exists. You can start chatting now."
    else:
        final_msg = f"Finished indexing '{book_name}'. You can start chatting now."

    # First output: status text
    # Second output: make the chat block visible
    return final_msg, gr.update(visible=True)

with gr.Blocks() as demo:
    gr.Markdown("Book chat")

    # ---------- Book Search UI ------------------
    with gr.Group():
        book_box = gr.Textbox(
            label="Enter book name",
            placeholder="e.g. Pride and Prejudice"
        )
        search_btn = gr.Button("Search")
        output = gr.Textbox(label="Result")

        search_btn.click(
            fn=clickTrigger,
            inputs=book_box)

    # ---------- Chat Interface ----------


    chat = gr.ChatInterface(
        fn=yes_man,
        type="messages",
        chatbot=gr.Chatbot(height=300),
        textbox=gr.Textbox(
            placeholder="Chat With Book",
            container=False,
            scale=7
        )
       
    )

demo.launch()
