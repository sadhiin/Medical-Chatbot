import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

class VectorDB():
    def __init__(self, index_name:str ="medibot-index", HF_Embedding_model:str='microsoft/unixcoder-base'):
        load_dotenv()
        self.api_key = os.getenv("PINECONE_API_KEY")
        assert self.api_key is not None, "PINECONE_API_KEY is not set"
        self.index_name = index_name
        self.embed_size = 0
        self.pc = Pinecone(api_key=self.api_key)
        self.HF_Embedding_model = HF_Embedding_model
        self.embedding_model = None
        self.__download_embedding_model()

    def __download_embedding_model(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.HF_Embedding_model)
        q = self.embedding_model.embed_query("Hello world")
        self.embed_size = len(q)


    def create_index(self):
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embed_size,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
            while not self.pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)
            print(f"Created index {self.index_name}")
        else:
            print(f"Index {self.index_name} already exists")

        self.index = self.pc.Index(self.index_name)

    def add_documents(self, document_chunks:list):
        """
        Adds a list of document chunks to the vector database
        """
        try:
            db = PineconeVectorStore(index=self.index, embedding=self.embedding_model)
            db.add_documents(documents=document_chunks)
        except Exception as e:
            print(f"Error adding documents: {e}")

    def get_index(self):
        """
        Returns a vector store object
        """
        try:
            self.index = self.pc.Index(self.index_name)
            db = PineconeVectorStore(index=self.index, embedding=self.embedding_model)
            return db
        except Exception as e:
            print(f"Error getting index: {e}")

if __name__ == "__main__":

    vdb = VectorDB()
    db = vdb.get_index()
    print("Failed to get the index" if db is None else "Successfully got the index")

    # from langchain_pinecone import PineconeVectorStore
    # ## https://python.langchain.com/api_reference/pinecone/vectorstores/langchain_pinecone.vectorstores.PineconeVectorStore.html#pineconevectorstore
    # index = pc.Index(index_name)


    # vector_store = PineconeVectorStore(index=index, embedding=embedding_model)