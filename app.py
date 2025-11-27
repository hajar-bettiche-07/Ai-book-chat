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
    /* Global Styles */
    .gradio-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    /* Header Section */
    .header-section {
        background: linear-gradient(135deg, #d97706 0%, #dc2626 100%);
        padding: 60px 80px;
        margin: 0 0 40px 0;
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: repeating-linear-gradient(
            90deg,
            rgba(255, 255, 255, 0.03) 0px,
            rgba(255, 255, 255, 0.03) 2px,
            transparent 2px,
            transparent 20px
        );
        pointer-events: none;
    }
    
    .header-content {
        display: flex;
        align-items: center;
        gap: 24px;
        position: relative;
        z-index: 1;
    }
    
    .header-icon {
        width: 80px;
        height: 80px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        backdrop-filter: blur(10px);
    }
    
    .header-text h1 {
        color: white;
        font-size: 48px;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    
    .header-text p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 20px;
        margin: 0;
        font-weight: 400;
    }
    
    /* Feature Cards */
    .features-section {
        padding: 0 80px 60px 80px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        margin-bottom: 40px;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 32px 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .feature-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 20px auto;
        font-size: 28px;
    }
    
    .feature-card h3 {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin: 0 0 12px 0;
    }
    
    .feature-card p {
        font-size: 14px;
        color: #6b7280;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Search Section */
    .search-section {
        padding: 0 80px;
        margin-bottom: 60px;
    }
    
    .search-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 48px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        display: flex;
        gap: 40px;
        align-items: center;
    }
    
    .search-image {
        flex-shrink: 0;
        width: 300px;
        height: 200px;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .search-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .search-content {
        flex: 1;
    }
    
    .search-title {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .search-title h2 {
        font-size: 32px;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .search-subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 24px;
    }
    
    .search-box-container {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .search-box-container input {
        flex: 1;
        padding: 14px 20px !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        font-size: 15px !important;
    }
    
    .search-box-container input:focus {
        border-color: #f97316 !important;
        outline: none !important;
    }
    
    .search-button {
        padding: 14px 32px !important;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    .search-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4) !important;
    }
    
    .status-message {
        padding: 12px 20px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Chat Section */
    .chat-section {
        padding: 0 80px 80px 80px;
    }
    
    .chat-container {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .chat-header {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 24px;
    }
    """
) as demo:
    
    # Header
    gr.HTML("""
    <div class="header-section">
        <div class="header-content">
            <div class="header-icon">📖</div>
            <div class="header-text">
                <h1>Book Chat AI</h1>
                <p>Your intelligent reading companion</p>
            </div>
        </div>
    </div>
    """)
    
    # Feature Cards
    gr.HTML("""
    <div class="features-section">
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
    with gr.Group(elem_classes="search-section"):
        gr.HTML("""
        <div class="search-card">
            <div class="search-image">
                <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop" alt="Person reading">
            </div>
            <div class="search-content">
                <div class="search-title">
                    <span style="font-size: 32px;">✨</span>
                    <h2>Find Your Book</h2>
                </div>
                <p class="search-subtitle">Enter a book title and start an intelligent conversation about it</p>
            </div>
        </div>
        """)
        
        with gr.Row(elem_classes="search-box-container"):
            book_box = gr.Textbox(
                placeholder="Enter book title (e.g, The Great Gatsby)...",
                show_label=False,
                container=False,
                scale=5
            )
            search_btn = gr.Button("🔍 Search", elem_classes="search-button", scale=1)
        
        status_text = gr.HTML("", visible=False)
    
    # Chat Section
    with gr.Group(visible=False, elem_classes="chat-section") as chat_section:
        gr.HTML('<div class="chat-header">💬 Chat with Your Book</div>')
        with gr.Group(elem_classes="chat-container"):
            chat = gr.ChatInterface(
                fn=echo,
                type="messages",
                chatbot=gr.Chatbot(height=500, type="messages"),
                textbox=gr.Textbox(
                    placeholder="Ask anything about the book...",
                    container=False,
                    scale=7
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