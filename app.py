import gradio as gr

def yes_man(message, history):
    if message.endswith("?"):
        return "Yes"
    else:
        return "Ask me anything!"

def search_book(book_name):
    return f"Searching for: {book_name}"
   

with gr.Blocks() as demo:
    gr.Markdown("## Book Search")

    book_box = gr.Textbox(
        label="Enter book name",
        placeholder="e.g. Pride and Prejudice"
    )

    search_btn = gr.Button("Search")

    output = gr.Textbox(label="Result")

    # When the button is clicked, the function is called with the textbox content
    search_btn.click(
        fn=search_book,          # function to execute
        inputs=book_box,         # value from the textbox
        outputs=output           # put result here
    )

demo.launch()

gr.ChatInterface(
    yes_man,
    type="messages",
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Chat With Book", container=False, scale=7),
    title="Book Chat",
    description="Ask specific questions about books you're reading",
    theme="ocean",
).launch()

