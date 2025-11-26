import gradio as gr

# ====== Main chatbot function ======
def book_chat(message, history):
    if message.strip() == "":
        return "Please type something!"

    if message.endswith("?"):
        return "Good question! Let me explain..."
    elif "summary" in message.lower():
        return "Here is a concise summary of the requested passage."
    elif "character" in message.lower():
        return "The main characters are: … (to be completed based on the text)"
    else:
        return "Alright! Here’s my response: " + message

# ====== Professional Gradio interface with valid colors ======
custom_theme = gr.themes.Base(
    primary_hue="blue",       # main buttons and accents
    secondary_hue="gray",     # textbox and chat background
    neutral_hue="#f5f5f5"     # general background (light gray)
)

with gr.Blocks(theme=custom_theme, css="""
    #chatbot .chatbot-message {
        border-radius: 10px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }
    #chatbot .chatbot-message.user {
        background-color: #d0e1ff;
    }
    #chatbot .chatbot-message.bot {
        background-color: #f0f4f8;
    }
""") as demo:

    gr.Markdown(
        """
        ## Book-Chat Assistant
        Chat with your assistant about books, summaries, and analyses.
        Ask questions and receive clear, professional answers.
        """
    )

    chatbot = gr.Chatbot(label="Book-Chat", height=400, elem_id="chatbot")

    with gr.Row():
        txt = gr.Textbox(
            placeholder="Type your question here...",
            label="Your Question",
            scale=8
        )
        btn = gr.Button("Send", variant="primary")

    # ====== Interaction logic ======
    def respond(message, history):
        reply = book_chat(message, history)
        history = history or []
        history.append((message, reply))
        return history, history

    btn.click(respond, [txt, chatbot], [chatbot, chatbot])
    txt.submit(respond, [txt, chatbot], [chatbot, chatbot])

demo.launch()
