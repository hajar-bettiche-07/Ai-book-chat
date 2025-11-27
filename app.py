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
    if not book_name or book_name.strip() == "":
        return gr.update(value="Please enter a book title!", visible=True), gr.update(visible=False)
    
    print(f"[DEBUG] Button clicked with book_name={book_name!r}")
    BOOK_NAME = book_name
    try:
        create_populate_collection_if_not_exist(book_name)
    except Exception as exc:
        error_msg = f"Unable to prepare book data: {exc}"
        print(f"[ERROR] {error_msg}")
        return gr.update(value=error_msg, visible=True), gr.update(visible=False)

    success_msg = f"Book '{BOOK_NAME}' is ready! Start chatting below."
    return gr.update(value=success_msg, visible=True), gr.update(visible=True)

with gr.Blocks(
    css="""
    .gradio-container {
        max-width: 100% !important;
    }
    
    /* Header */
    .header-bar {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        padding: 40px;
        text-align: center;
        margin: -16px -16px 32px -16px;
    }
    
    .header-bar h1 {
        color: white;
        font-size: 36px;
        font-weight: 700;
        margin: 0 0 8px 0;
    }
    
    .header-bar p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 16px;
        margin: 0;
    }
    
    /* Feature Cards Container */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 40px;
        padding: 0 40px;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    
    .feature-icon {
        width: 48px;
        height: 48px;
        background: #ff8c00;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        font-size: 24px;
    }
    
    .feature-card h3 {
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 8px 0;
    }
    
    .feature-card p {
        font-size: 13px;
        color: #6b7280;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Search Section */
    .search-wrapper {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 32px;
        margin: 0 40px 40px 40px;
    }
    
    .search-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    
    .search-header h2 {
        font-size: 24px;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }
    
    .search-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 24px;
    }
    
    /* Make input and button inline */
    .search-row {
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    
    .search-row > div:first-child {
        flex: 1;
    }
    
    /* Status message */
    .status-msg {
        margin-top: 16px;
        padding: 12px;
        border-radius: 8px;
        font-size: 14px;
    }
    
    /* Chat section */
    .chat-wrapper {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 32px;
        margin: 0 40px;
    }
    
    .chat-wrapper h2 {
        font-size: 24px;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 24px 0;
    }
    """
) as demo:
    
    # Header
    gr.HTML("""
    <div class="header-bar">
        <h1>📚 AI Book Chat</h1>
        <p>Your intelligent reading companion</p>
    </div>
    """)
    
    # Feature Cards
    gr.HTML("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Deep Discussions</h3>
            <p>Ask complex questions about plot, themes, and characters</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Instant Answers</h3>
            <p>Get immediate AI-powered responses about any book</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <h3>Save Time</h3>
            <p>No need to re-read - get quick summaries and insights</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Learn More</h3>
            <p>Discover hidden meanings and literary analysis</p>
        </div>
    </div>
    """)
    
    # Search Section
    with gr.Group(elem_classes="search-wrapper"):
        gr.HTML("""
        <div class="search-header">
            <span style="font-size: 24px;">✨</span>
            <h2>Find Your Book</h2>
        </div>
        <p class="search-subtitle">Enter a book title and start an intelligent conversation about it</p>
        """)
        
        with gr.Row(elem_classes="search-row"):
            book_box = gr.Textbox(
                label="Book Name",
                placeholder="Enter the exact or partial name of a book...",
                scale=4
            )
            search_btn = gr.Button("Search", variant="primary", scale=1)
        
        status_text = gr.HTML("", visible=False, elem_classes="status-msg")
    
    # Chat Section (hidden initially)
    with gr.Group(visible=False, elem_classes="chat-wrapper") as chat_section:
        gr.HTML('<h2>💬 Chat with the Book</h2>')
        chat = gr.ChatInterface(
            fn=echo,
            type="messages",
            chatbot=gr.Chatbot(height=400, type="messages"),
            textbox=gr.Textbox(
                placeholder="Ask a question about the book...",
                container=False
            )
        )
    
    # Event Handlers
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