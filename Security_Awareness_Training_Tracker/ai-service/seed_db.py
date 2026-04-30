from chromadb import Client
from chromadb.config import Settings
import os

# Create DB WITHOUT embedding model (important fix)
client = Client(Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection(
    name="security_knowledge",
    embedding_function=None   # 🔥 THIS LINE FIXES YOUR ERROR
)

folder = "knowledge_base"

for file in os.listdir(folder):
    with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
        content = f.read()

        collection.add(
            documents=[content],
            ids=[file]
        )

print("✅ ChromaDB seeded successfully (NO model download)")