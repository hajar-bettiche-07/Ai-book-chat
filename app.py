import gradio as gr
import time

# ====== Main chatbot function ======
# This is a placeholder for your actual model's logic.
def book_chat(message, history):
    """
    Processes the user's message and generates a response.
    This is a mock function. Replace it with your actual model inference.
    """
    if not message.strip():
        return "Please type a question or a statement."

    # Simulate a "thinking" delay for a more realistic interaction
    time.sleep(0.5)

    if message.endswith("?"):
        return "That's an excellent question. Based on my analysis, the key theme revolves around..."
    elif "summary" in message.lower():
        return "Certainly. Here is a concise summary of the main plot points and character arcs..."
    elif "character" in message.lower():
        return "The main characters are: \n- **Protagonist:** A detailed description of their journey.\n- **Antagonist:** Their motivations and role in the story.\n- **Supporting Character:** How they influence the plot."
    elif "theme" in message.lower():
        return "The central themes of this book include the struggle between fate and free will, the nature of justice, and the search for identity."
    else:
        return f"That's an interesting point. Let me elaborate on that idea in the context of the book: '{message}'"

# ====== 1. Custom Theme Definition ======
# Using a more sophisticated and modern color palette.
custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[
        "ui-sans-serif", "system-ui", "sans-serif"
    ],
    font_mono=[
        "ui-monospace", "Consolas", "monospace"
    ]
)

# ====== 2. Custom CSS for Styling ======
# Adding CSS for a polished look with shadows, rounded corners, and better spacing.
custom_css = """
/* Main container styling */
.gradio-container {
    max-width: 800px !important;
    margin: auto !important;
    padding-top: 2rem;
}

/* Chatbot message bubble styling */
#chatbot .message.user {
    background-color: #6366f1; /* Indigo color for user messages */
    color: white;
    border-radius: 18px 18px 4px 18px;
}

#chatbot .message.bot {
    background-color: #f1f5f9; /* Light slate for bot messages */
    color: #1e293b;
    border-radius: 18px 18px 18px 4px;
    border: 1px solid #e2e8f0;
}

/* Footer styling */
.footer {
    text-align: center;
    margin-top: 20px;
    color: #64748b;
    font-size: 0.9em;
}
"""

# ====== 3. Gradio Interface Layout ======
with gr.Blocks(theme=custom_theme, css=custom_css, title="Book-Chat Pro") as demo:
    # Header with Title and Description
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1>Book-Chat Pro</h1>
            <p>Your professional assistant for in-depth book analysis, summaries, and character exploration.</p>
        </div>
        """
    )

    # Main Chatbot Component
    chatbot = gr.Chatbot(
        label="Conversation",
        elem_id="chatbot",
        height=500,
        show_copy_button=True,
        placeholder="Ask me anything about the book you're reading..."
    )

    # Example prompts to guide the user
    with gr.Row():
        gr.Examples(
            examples=[
                "Can you give me a summary of the last chapter?",
                "What is the main character's primary motivation?",
                "How does the setting contribute to the story's mood?",
                "What are the central themes of this book?"
            ],
            inputs=[chatbot],
            label="Click an example to get started:"
        )

    # Input area with Textbox and Send Button
    with gr.Row():
        txt = gr.Textbox(
            placeholder="Type your question here and press Enter...",
            label="Your Question",
            scale=4,
            container=False
        )
        btn = gr.Button("Send", variant="primary", scale=1)

    # "About" section with additional information
    with gr.Accordion("About this Assistant", open=False):
        gr.Markdown(
            """
            - **Capabilities:** Summaries, character analysis, thematic exploration, and answering specific questions about the book's content.
            - **Limitation:** This is a demonstration model. For real-time, complex analysis, please ensure it's connected to a powerful language model.
            - **How to Use:** Simply type your question or click one of the example prompts.
            """
        )

    # Footer
    gr.Markdown(
        """
        <div class="footer">
            <p>Created by Your Team | © 2024</p>
        </div>
        """
    )

    # ====== 4. Event Handling Logic ======
    def respond(message, history):
        """
        Handles user input, generates a bot response, and updates the chat history.
        """
        if not message:
            return history, ""  # Do nothing if the message is empty

        # Generate the bot's response using the main chat function
        bot_message = book_chat(message, history)
        
        # Append the user's message and the bot's response to the history
        history.append((message, bot_message))
        
        # Clear the textbox and return the updated history
        return "", history

    # Link the events to the components
    txt.submit(respond, [txt, chatbot], [txt, chatbot])
    btn.click(respond, [txt, chatbot], [txt, chatbot])

# Launch the application
if __name__ == "__main__":
    demo.launch()