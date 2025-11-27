import gradio as gr
from backend.populate_vec_db_and_seach import create_populate_collection_if_not_exist
from backend.chatgpt import generate

BOOK_NAME = ""

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

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate"
    ),
    css="""
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
    }
    .header-section h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
        font-weight: 600;
    }
    .header-section p {
        color: rgba(255, 255, 255, 0.9);
        margin: 8px 0 0 0;
        font-size: 1.1em;
    }
    .search-section {
        background: white;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .chat-section {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .status-message {
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        font-weight: 500;
    }
    .status-success {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    .status-error {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        color: #7f1d1d;
    }
    """
) as demo:
    with gr.Group(elem_classes="header-section"):
        gr.HTML("""
            <h1>📚 AI Book Chat</h1>
            <p>Explore your favorite books with intelligent Q&A</p>
        """)

    with gr.Group(elem_classes="search-section"):
        gr.Markdown("### Find Your Book")
        with gr.Row():
            book_box = gr.Textbox(
                label="Book Name",
                placeholder="Enter the exact or partial name of a book...",
                scale=6,
                lines=1
            )
            search_btn = gr.Button(
                "Search",
                variant="primary",
                scale=1,
                min_width=120
            )
        
        status_text = gr.HTML("", visible=False)

    with gr.Group(visible=False, elem_classes="chat-section") as chat_section:
        gr.Markdown("### Chat with the Book")
        chat = gr.ChatInterface(
            fn=echo,
            type="messages",
            chatbot=gr.Chatbot(
                height=400,
                type="messages",
                label="Conversation"
            ),
            textbox=gr.Textbox(
                placeholder="Ask a question about the book...",
                container=False,
                scale=7
            )
        )

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