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
        font-family: 'Segoe UI', system-ui, sans-serif !important;
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
    
    /* Header Section - Style image */
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 80px 0 60px 0 !important;
        margin: 0 !important;
        text-align: center;
    }
    
    .header-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .header-text h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0 0 16px 0;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .header-text p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        margin: 0;
        font-weight: 400;
        line-height: 1.4;
    }
    
    /* Features Section - Style image */
    .features-section {
        background: white;
        padding: 60px 0 !important;
        margin: 0 !important;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 30px;
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .feature-item {
        text-align: center;
        padding: 0 20px;
    }
    
    .feature-item h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 12px 0;
        line-height: 1.3;
    }
    
    .feature-item p {
        font-size: 1.1rem;
        color: #718096;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Divider Line */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 50%, transparent 100%);
        margin: 40px auto;
        max-width: 1000px;
    }
    
    /* Search Section - Style image */
    .search-section {
        background: white;
        padding: 40px 0 80px 0 !important;
        margin: 0 !important;
        text-align: center;
    }
    
    .search-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .search-title {
        margin-bottom: 30px;
    }
    
    .search-title h2 {
        font-size: 2.2rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 16px 0;
        line-height: 1.2;
    }
    
    .search-subtitle {
        font-size: 1.2rem;
        color: #718096;
        line-height: 1.5;
        margin: 0;
    }
    
    /* Search Input - Style image */
    .search-inputs {
        max-width: 600px;
        margin: 0 auto !important;
        padding: 0 20px !important;
    }
    
    .search-box-container {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: center;
    }
    
    .search-box-container input {
        flex: 1;
        padding: 16px 20px !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        background: white !important;
        color: #2d3748 !important;
        transition: all 0.3s ease !important;
    }
    
    .search-box-container input:focus {
        border-color: #667eea !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .search-box-container input::placeholder {
        color: #a0aec0 !important;
    }
    
    .search-button {
        padding: 16px 32px !important;
        background: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        min-width: 120px !important;
    }
    
    .search-button:hover {
        background: #5a6fd8 !important;
        transform: translateY(-1px);
    }
    
    .status-message {
        max-width: 600px;
        margin: 0 auto !important;
        text-align: center;
    }
    
    /* Chat Section - Style image */
    .chat-section-wrapper {
        background: #f7fafc;
        padding: 60px 0 80px 0 !important;
        margin: 0 !important;
        border-top: 1px solid #e2e8f0;
    }
    
    .chat-section {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 0 20px !important;
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .chat-header h3 {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin: 0 0 12px 0;
    }
    
    .chat-header p {
        font-size: 1.1rem;
        color: #718096;
        margin: 0;
    }
    
    /* Chat Interface Styling */
    .chat-interface {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Chatbot Styling */
    .gradio-chatbot {
        border: none !important;
        background: white !important;
        min-height: 400px !important;
        max-height: 500px !important;
    }
    
    .gradio-chatbot .message {
        border: none !important;
        padding: 16px 20px !important;
        margin: 8px 16px !important;
        border-radius: 12px !important;
    }
    
    .gradio-chatbot .user-message {
        background: #667eea !important;
        color: white !important;
        margin-left: 60px !important;
    }
    
    .gradio-chatbot .bot-message {
        background: #f7fafc !important;
        color: #2d3748 !important;
        margin-right: 60px !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Textbox Styling */
    .gradio-textbox {
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        font-size: 1rem !important;
        background: white !important;
    }
    
    .gradio-textbox:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button Styling */
    .gradio-button {
        background: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
    }
    
    .gradio-button:hover {
        background: #5a6fd8 !important;
    }
    
    /* Hide elements until book is selected */
    .hidden-section {
        display: none !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-text h1 {
            font-size: 2.5rem;
        }
        
        .header-text p {
            font-size: 1.2rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
            gap: 40px;
        }
        
        .search-box-container {
            flex-direction: column;
        }
        
        .search-button {
            width: 100%;
        }
    }
    
    /* Force remove all gaps */
    div[data-testid] {
        margin: 0 !important;
        padding: 0 !important;
    }
    """
) as demo:
    
    # Header Section
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
    
    # Features Section
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
            <div class="feature-item">
                <h3>Save Time</h3>
                <p>No need to re-read - get quick summaries and insights</p>
            </div>
            <div class="feature-item">
                <h3>Learn More</h3>
                <p>Discover hidden meanings and literary analysis</p>
            </div>
        </div>
        <div class="divider"></div>
    </div>
    """)
    
    # Search Section
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
                placeholder="Enter book title (e.g., The Great Gatsby)...",
                show_label=False,
                container=False,
                scale=6
            )
            search_btn = gr.Button("Search", elem_classes="search-button", scale=2)
        
        status_text = gr.HTML("", visible=False)
    
    # Chat Section (hidden initially)
    with gr.Group(visible=False) as chat_section:
        gr.HTML("""
        <div class="chat-section-wrapper">
            <div class="chat-section">
                <div class="chat-header">
                    <h3>Ask me a question about any book...</h3>
                </div>
        """)
        
        # Chat Interface with custom styling
        chat = gr.ChatInterface(
            fn=echo,
            type="messages",
            chatbot=gr.Chatbot(
                height=400, 
                type="messages",
                show_label=False,
                container=False
            ),
            textbox=gr.Textbox(
                placeholder="Type your question here...",
                container=False,
                scale=7
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