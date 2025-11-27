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
        margin: 0 !important;
        background: white !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }
    
    /* Supprimer TOUS les gaps et marges */
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
    
    /* Header Section - EXACTEMENT COMME L'IMAGE */
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 0 40px 0 !important;
        margin: 0 !important;
        text-align: center;
    }
    
    .header-content {
        max-width: 600px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .header-text h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .header-text p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0;
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* Features Section - STYLE EXACT DE L'IMAGE */
    .features-section {
        background: white;
        padding: 40px 0 30px 0 !important;
        margin: 0 !important;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 20px;
        max-width: 500px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .feature-item {
        text-align: center;
        padding: 0;
    }
    
    .feature-item h3 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 8px 0;
        line-height: 1.3;
    }
    
    .feature-item p {
        font-size: 1rem;
        color: #718096;
        line-height: 1.4;
        margin: 0;
    }
    
    /* Search Section - STYLE EXACT */
    .search-section {
        background: white;
        padding: 30px 0 40px 0 !important;
        margin: 0 !important;
        text-align: center;
    }
    
    .search-content {
        max-width: 500px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .search-title {
        margin-bottom: 20px;
    }
    
    .search-title h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 12px 0;
        line-height: 1.2;
    }
    
    .search-subtitle {
        font-size: 1rem;
        color: #718096;
        line-height: 1.4;
        margin: 0;
    }
    
    /* Search Input - STYLE EXACT */
    .search-inputs {
        max-width: 500px;
        margin: 0 auto !important;
        padding: 0 20px !important;
    }
    
    .search-box-container {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
        align-items: center;
    }
    
    .search-box-container input {
        flex: 1;
        padding: 12px 16px !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        background: white !important;
        color: #2d3748 !important;
    }
    
    .search-box-container input:focus {
        border-color: #667eea !important;
        outline: none !important;
    }
    
    .search-box-container input::placeholder {
        color: #9ca3af !important;
    }
    
    .search-button {
        padding: 12px 24px !important;
        background: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        min-width: 80px !important;
    }
    
    .search-button:hover {
        background: #5a6fd8 !important;
    }
    
    .status-message {
        max-width: 500px;
        margin: 0 auto !important;
        text-align: center;
        font-size: 0.9rem;
    }
    
    /* Chat Section - STYLE EXACT COMME L'IMAGE */
    .chat-section-wrapper {
        background: #f8fafc;
        padding: 40px 0 60px 0 !important;
        margin: 0 !important;
        border-top: 1px solid #e5e7eb;
    }
    
    .chat-section {
        max-width: 500px !important;
        margin: 0 auto !important;
        padding: 0 20px !important;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .chat-header h3 {
        font-size: 1.2rem;
        font-weight: 500;
        color: #6b7280;
        margin: 0 0 20px 0;
        font-style: italic;
    }
    
    /* Chat Interface Styling - TRÈS SIMPLE */
    .chat-interface {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Chatbot Styling */
    .gradio-chatbot {
        border: none !important;
        background: white !important;
        min-height: 200px !important;
        max-height: 300px !important;
        box-shadow: none !important;
    }
    
    /* Textbox Styling - BOUTON "Send" */
    .gradio-textbox {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        background: white !important;
    }
    
    /* Button Styling */
    .gradio-button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        margin-left: 8px !important;
    }
    
    .gradio-button:hover {
        background: #5a6fd8 !important;
    }
    
    /* Container for chat input */
    .gradio-row {
        gap: 8px !important;
    }
    
    /* Force remove all gaps */
    div[data-testid] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide the submit button label if it exists */
    .submit-button {
        display: none !important;
    }
    """
) as demo:
    
    # Header Section - EXACTEMENT COMME L'IMAGE
    gr.HTML("""
    <div class="header-section">
        <div class="header-content">
            <div class="header-text">
                <h1>Welcome to ChatBook</h1>
                <p>Your intelligent reading companion</p>
            </div>
        </div>
    </div>
    """)
    
    # Features Section - EXACTEMENT COMME L'IMAGE
    gr.HTML("""
    <div class="features-section">
        <div class="features-grid">
            <div class="feature-item">
                <h3>Deep Discussions</h3>
                <p>Ask complex questions about plot, themes, and characters</p>
            </div>
            <div class="feature-item">
                <h3>Instant Answers</h3>
                <p>Get immediate AI-powered responses about any book</p>
            </div>
        </div>
    </div>
    """)
    
    # Search Section - EXACTEMENT COMME L'IMAGE
    gr.HTML("""
    <div class="search-section">
        <div class="search-content">
            <div class="search-title">
                <h2>Find Your Book</h2>
                <p class="search-subtitle">Enter a book title and start an intelligent conversation about it</p>
            </div>
        </div>
    </div>
    """)
    
    # Search Inputs
    with gr.Group(elem_classes="search-inputs"):
        with gr.Row(elem_classes="search-box-container"):
            book_box = gr.Textbox(
                placeholder="Enter book title...",
                show_label=False,
                container=False,
                scale=7
            )
            search_btn = gr.Button("Search", elem_classes="search-button", scale=3)
        
        status_text = gr.HTML("", visible=False)
    
    # Chat Section (hidden initially) - EXACTEMENT COMME L'IMAGE
    with gr.Group(visible=False) as chat_section:
        gr.HTML("""
        <div class="chat-section-wrapper">
            <div class="chat-section">
                <div class="chat-header">
                    <h3>Ask me a question about any book...</h3>
                </div>
        """)
        
        # Chat Interface - SIMPLE COMME L'IMAGE
        chat = gr.ChatInterface(
            fn=echo,
            type="messages",
            chatbot=gr.Chatbot(
                height=200, 
                type="messages",
                show_label=False,
                container=False,
                show_copy_button=False
            ),
            textbox=gr.Textbox(
                placeholder="Type your question here...",
                container=False,
                scale=8
            ),
            submit_btn="Send",
            title=""
        )
        
        gr.HTML("""
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