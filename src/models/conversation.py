import chromadb

client = chromadb.Client()
collection = client.create_collection(name="chat_history")

# Guardar mensajes
def save_message(question, answer):
    collection.add(documents=[question], metadatas=[{"answer": answer}])

# Obtener contexto desde la memoria
def get_context():
    context = []
    results = collection.get()
    for doc, meta in zip(results["documents"], results["metadatas"]):
        context.append({'role': 'user', 'content': doc})
        context.append({'role': 'assistant', 'content': meta['answer']})
    return context[-5:]  # Retorna solo los últimos 5 mensajes