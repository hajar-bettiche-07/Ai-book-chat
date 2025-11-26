import gradio as gr

# ====== Fonction principale du chatbot ======
def book_chat(message, history):
    """
    Logique simple pour Book-Chat.
    Remplace cette partie par ton vrai modèle ou traitement.
    """
    if message.strip() == "":
        return "Écris quelque chose, s'il te plaît !"

    if message.endswith("?"):
        return "Bonne question ! Laisse-moi t'expliquer..."
    elif "résumé" in message.lower():
        return "Voici un résumé simple du passage demandé..."
    elif "personnage" in message.lower():
        return "Les personnages principaux sont : … (à compléter selon le texte)"
    else:
        return "D'accord ! Voici ma réponse : " + message

# ====== Interface Gradio ======
gr.ChatInterface(
    book_chat,
    type="messages",
    chatbot=gr.Chatbot(height=350),
    textbox=gr.Textbox(
        placeholder="Pose ta question sur un livre...",
        container=False,
        scale=7
    ),
    title="📘 Book-Chat",
    description="Discute avec ton assistant sur les livres, résumés et analyses.",
    theme="ocean",
    examples=[
        "Peux-tu résumer ce chapitre ?",
        "Que signifie cette phrase ?",
        "Parle-moi des personnages principaux."
    ],
    cache_examples=True,
).launch()
