import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

def search_book(book_name):
    return f"Searching for: {book_name}"

with gr.Blocks() as demo:
    gr.Markdown("Book chat")

    # ---------- Book Search UI ----------
    with gr.Group():
        gr.Markdown("### Search for a Book")
        book_box = gr.Textbox(
            label="Enter book name",
            placeholder="e.g. Pride and Prejudice"
        )
        search_btn = gr.Button("Search")
        output = gr.Textbox(label="Result")

        search_btn.click(
            fn=search_book,
            inputs=book_box)

    # ---------- Chat Interface ----------
    gr.Markdown("### Book Chatbot")

    chat = gr.ChatInterface(
        fn=yes_man,
        type="messages",
        chatbot=gr.Chatbot(height=300),
        textbox=gr.Textbox(
            placeholder="Chat With Book",
            container=False,
            scale=7
        )
       
    )

demo.launch()
