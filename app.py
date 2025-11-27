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

def start_chat_with_popular_book(book_name):
    """Function to handle popular book selection"""
    global BOOK_NAME
    BOOK_NAME = book_name
    try:
        create_populate_collection_if_not_exist(book_name)
        return gr.update(value=f"Book '{BOOK_NAME}' is ready! You can start chatting below.", visible=True), gr.update(visible=True)
    except Exception as exc:
        error_msg = f"Unable to prepare book data: {exc}"
        return gr.update(value=error_msg, visible=True), gr.update(visible=False)

# ---------------- Frontend ----------------

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate"
    ),
    css="""
    .header-section {
        background: linear-gradient(135deg, #1f3d7a 0%, #2e4a7e 100%);
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
    .feature-box {
        background-color: #f0f5ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #4a6fc7;
    }
    .book-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .rating {
        color: #ffc107;
        font-weight: bold;
        margin: 8px 0;
    }
    .sidebar {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        height: fit-content;
    }
    .popular-books-section {
        margin-top: 30px;
    }
    """
) as demo:
    
    with gr.Row():
        # Sidebar (Left Column)
        with gr.Column(scale=1, min_width=250):
            with gr.Group(elem_classes="sidebar"):
                gr.Markdown("# Book Chat AI")
                gr.Markdown("Your intelligent reading companion")
                gr.Markdown("---")
                gr.Markdown("**My Library**")
                gr.Markdown("**Settings**")
                gr.Markdown("**Help**")
                gr.Markdown("---")
                
                # Features Section
                gr.Markdown("## Features")
                with gr.Group(elem_classes="feature-box"):
                    gr.Markdown("**Deep Discussions**")
                    gr.Markdown("Ask complex questions about plot, themes, and characters")
                
                with gr.Group(elem_classes="feature-box"):
                    gr.Markdown("**Instant Answers**")
                    gr.Markdown("Get immediate AI-powered responses about any book")
                
                with gr.Group(elem_classes="feature-box"):
                    gr.Markdown("**Save Time**")
                    gr.Markdown("No need to re-read - get quick summaries and insights")
                
                with gr.Group(elem_classes="feature-box"):
                    gr.Markdown("**Learn More**")
                    gr.Markdown("Discover hidden meanings and literary analysis")

        # Main Content (Right Column)
        with gr.Column(scale=3):
            with gr.Group(elem_classes="header-section"):
                gr.HTML("""
                    <h1>Book Chat AI</h1>
                    <p>Your intelligent reading companion</p>
                """)

            # Search Section
            with gr.Group(elem_classes="search-section"):
                gr.Markdown("## Find Your Book")
                gr.Markdown("Enter a book title and start an intelligent conversation about it")
                
                with gr.Row():
                    book_box = gr.Textbox(
                        label="Book Name",
                        placeholder="Enter book title (e.g., The Great Gatsby)",
                        scale=4,
                        lines=1,
                        container=False
                    )
                    search_btn = gr.Button(
                        "Search",
                        variant="primary",
                        scale=1,
                        min_width=120
                    )
                
                status_text = gr.HTML("", visible=False)

            # Popular Books Section
            with gr.Group(elem_classes="popular-books-section"):
                gr.Markdown("## Popular Books")
                
                # Book Cards in a grid
                with gr.Row():
                    with gr.Column():
                        with gr.Group(elem_classes="book-card"):
                            gr.Markdown("**The Great Gatsby**")
                            gr.Markdown("F. Scott Fitzgerald")
                            gr.Markdown('<div class="rating">⭐ 4.5</div>')
                            gatsby_btn = gr.Button("Start Chat", size="sm", variant="secondary")
                    
                    with gr.Column():
                        with gr.Group(elem_classes="book-card"):
                            gr.Markdown("**1984**")
                            gr.Markdown("George Orwell")
                            gr.Markdown('<div class="rating">⭐ 4.7</div>')
                            orwell_btn = gr.Button("Start Chat", size="sm", variant="secondary")
                
                with gr.Row():
                    with gr.Column():
                        with gr.Group(elem_classes="book-card"):
                            gr.Markdown("**Pride and Prejudice**")
                            gr.Markdown("Jane Austen")
                            gr.Markdown('<div class="rating">⭐ 4.6</div>')
                            austen_btn = gr.Button("Start Chat", size="sm", variant="secondary")
                    
                    with gr.Column():
                        with gr.Group(elem_classes="book-card"):
                            gr.Markdown("**To Kill a Mockingbird**")
                            gr.Markdown("Harper Lee")
                            gr.Markdown('<div class="rating">⭐ 4.8</div>')
                            lee_btn = gr.Button("Start Chat", size="sm", variant="secondary")
                
                # View All button
                view_all_btn = gr.Button("View All", variant="secondary")

            # Chat Section (initially hidden)
            with gr.Group(visible=False, elem_classes="chat-section") as chat_section:
                gr.Markdown("## Chat with the Book")
                chat = gr.ChatInterface(
                    fn=echo,
                    type="messages",
                    chatbot=gr.Chatbot(
                        height=400,
                        type="messages",
                        label="Conversation",
                        scale=1,
                        show_copy_button=True
                    ),
                    textbox=gr.Textbox(
                        placeholder="Ask a question about the book...",
                        container=False,
                        scale=7,
                        lines=2
                    ),
                    submit_btn="Send",
                    retry_btn="Retry",
                    undo_btn="Remove Last",
                    clear_btn="Clear Chat"
                )

    # ---------- Event handlers ----------
    
    # Main search button
    search_btn.click(
        fn=show_loading_message,
        outputs=status_text,
        queue=False
    ).then(
        fn=clickTrigger,
        inputs=book_box,
        outputs=[status_text, chat_section]
    )
    
    # Popular books buttons
    gatsby_btn.click(
        fn=lambda: start_chat_with_popular_book("The Great Gatsby"),
        outputs=[status_text, chat_section]
    )
    
    orwell_btn.click(
        fn=lambda: start_chat_with_popular_book("1984"),
        outputs=[status_text, chat_section]
    )
    
    austen_btn.click(
        fn=lambda: start_chat_with_popular_book("Pride and Prejudice"),
        outputs=[status_text, chat_section]
    )
    
    lee_btn.click(
        fn=lambda: start_chat_with_popular_book("To Kill a Mockingbird"),
        outputs=[status_text, chat_section]
    )
    
    # View All button (placeholder)
    view_all_btn.click(
        fn=lambda: gr.update(value="More books coming soon!", visible=True),
        outputs=status_text
    )

demo.launch()