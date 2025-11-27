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
    /* Global Styles - ELIMINER LES ESPACES */
    .gradio-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Supprimer TOUS les gaps et marges entre les sections */
    .gradio-container > .contain {
        gap: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .contain > div {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Header Section - PLUS DE MARGES */
    .header-section {
        background: linear-gradient(135deg, #d97706 0%, #dc2626 100%);
        padding: 100px 0 80px 0 !important;
        margin: 0 !important;
        position: relative;
        overflow: hidden;
        border-radius: 0 !important;
        min-height: 300px;
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
        gap: 30px;
        position: relative;
        z-index: 1;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 80px;
    }
    
    .header-icon {
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        backdrop-filter: blur(10px);
    }
    
    .header-text h1 {
        color: white;
        font-size: 56px;
        font-weight: 700;
        margin: 0 0 12px 0;
        letter-spacing: -0.5px;
    }
    
    .header-text p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 24px;
        margin: 0;
        font-weight: 400;
    }
    
    /* Feature Cards Section - COLLÉ À L'HEADER */
    .features-section {
        background: linear-gradient(135deg, #f5e6d3 0%, #e8d4b8 100%);
        padding: 60px 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 24px;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 80px;
    }
    
    .feature-card {
        background: white;
        border: 2px solid #d2b48c;
        border-radius: 20px;
        padding: 32px 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.1);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(139, 69, 19, 0.2);
        border-color: #d2691e;
    }
    
    .feature-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #d2691e 0%, #a0522d 100%);
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
    
    /* Search Section - COLLÉ AUX FEATURES */
    .search-section-wrapper {
        background: white;
        padding: 80px 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
    
    .search-section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 80px;
    }
    
    .search-card {
        background: linear-gradient(135deg, #ffe4cc 0%, #ffd4a3 100%);
        border: 2px solid #ffb366;
        border-radius: 25px;
        padding: 60px;
        box-shadow: 0 6px 16px rgba(255, 140, 0, 0.2);
        display: flex;
        gap: 50px;
        align-items: center;
        min-height: 280px;
    }
    
    .search-image {
        flex-shrink: 0;
        width: 350px;
        height: 240px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
        margin-bottom: 20px;
    }
    
    .search-title h2 {
        font-size: 38px;
        font-weight: 700;
        color: #8b4513;
        margin: 0;
    }
    
    .search-subtitle {
        color: #654321;
        font-size: 18px;
        margin-bottom: 0;
    }
    
    /* Search Inputs - COLLÉ À LA SEARCH SECTION */
    .search-inputs {
        max-width: 1400px;
        margin: 30px auto 0 auto !important;
        padding: 0 80px !important;
    }
    
    .search-box-container {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .search-box-container input {
        flex: 1;
        padding: 16px 24px !important;
        border: 2px solid #d2691e !important;
        border-radius: 15px !important;
        font-size: 16px !important;
        background: white !important;
    }
    
    .search-box-container input:focus {
        border-color: #8b4513 !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(139, 69, 19, 0.1) !important;
    }
    
    .search-button {
        padding: 16px 40px !important;
        background: linear-gradient(135deg, #8b4513 0%, #a0522d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(139, 69, 19, 0.3) !important;
    }
    
    .search-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(139, 69, 19, 0.4) !important;
        background: linear-gradient(135deg, #a0522d 0%, #8b4513 100%) !important;
    }
    
    .status-message {
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Chat Section - COLLÉ AUX SEARCH INPUTS */
    .chat-section-wrapper {
        background: white;
        padding: 60px 0 80px 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
    
    .chat-section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 80px;
    }
    
    .chat-container {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 25px;
        padding: 32px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    .chat-header {
        font-size: 24px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 24px;
    }
    
    /* FORCER la suppression de tous les espaces entre les blocs Gradio */
    div[data-testid]:has(.header-section) {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    div[data-testid]:has(.features-section) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    div[data-testid]:has(.search-section-wrapper) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    div[data-testid]:has(.search-inputs) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    div[data-testid]:has(.chat-section-wrapper) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    """
) as demo:
    
    # Header
    gr.HTML("""
    <div class="header-section">
        <div class="header-content">
            <div class="header-icon">📖</div>
            <div class="header-text">
                <h1>Welcome to ChatBook</h1>
                <p>Your intelligent reading companion</p>
            </div>
        </div>
    </div>
    """)
    
    # Feature Cards
    gr.HTML("""
    <div class="features-section">
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
    </div>
    """)
    
    # Search Section
    gr.HTML("""
    <div class="search-section-wrapper">
        <div class="search-section">
            <div class="search-card">
                <div class="search-image">
                    <img src="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=600&h=400&fit=crop" alt="Person reading">
                </div>
                <div class="search-content">
                    <div class="search-title">
                        <span style="font-size: 38px;"></span>
                        <h2>Find Your Book</h2>
                    </div>
                    <p class="search-subtitle">Enter a book title and start an intelligent conversation about it</p>
                </div>
            </div>
        </div>
    </div>
    """)
    
    with gr.Group(elem_classes="search-inputs"):
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
    with gr.Group(visible=False) as chat_section:
        gr.HTML("""
        <div class="chat-section-wrapper">
            <div class="chat-section">
                <div class="chat-header">💬 Chat with Your Book</div>
                <div class="chat-container">
        """)
        
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
        
        gr.HTML("""
                </div>
            </div>
        </div>
        """)
    
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