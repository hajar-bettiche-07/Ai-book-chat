import gradio as gr
from backend.populate_vec_db_and_seach import create_populate_collection_if_not_exist
from backend.chatgpt import generate

BOOK_NAME = ""

# ---------------- Backend functions ----------------

def echo(message, history):
    chat_response = generate(message, BOOK_NAME)
    return chat_response

def show_loading_message():
    return gr.update(value="Searching for your book...", visible=True)

def clickTrigger(book_name):
    global BOOK_NAME
    # Validation if empty
    if not book_name or book_name.strip() == "":
        return gr.update(value="Please enter a book name!", visible=True), gr.update(visible=False)

    print(f"[DEBUG] Button clicked with book_name={book_name!r}")
    BOOK_NAME = book_name
    try:
        create_populate_collection_if_not_exist(book_name)
    except Exception as exc:
        error_msg = f"Unable to prepare book data: {exc}"
        print(f"[ERROR] {error_msg}")
        return gr.update(value=error_msg, visible=True), gr.update(visible=False)

    success_msg = f"Book '{BOOK_NAME}' is ready! You can start chatting below."
    return gr.update(value=success_msg, visible=True), gr.update(visible=True)

# ---------------- Frontend ----------------

with gr.Blocks() as demo:
    gr.Markdown("# Book Chat")

    # ---------- Book Search UI ------------------
    with gr.Group():
        book_box = gr.Textbox(
            label="Book Name",
            placeholder="Enter the exact or partial name of a book…"
        )
        search_btn = gr.Button("Search")
        status_text = gr.Markdown("", visible=False)

    # ---------- Chat Interface ----------
    with gr.Group(visible=False) as chat_section:
        chat = gr.ChatInterface(
            fn=echo,
            type="messages",
            chatbot=gr.Chatbot(height=300, type="messages"),
            textbox=gr.Textbox(
                placeholder="Ask a question about the book...",
                container=False,
                scale=7
            )
        )

    # ---------- Button click behavior ----------
    search_btn.click(
        fn=show_loading_message,
        outputs=status_text,
        queue=False
    ).then(
        fn=clickTrigger,
        inputs=book_box,
        outputs=[status_text, chat_section]
    )

demo.launch()
