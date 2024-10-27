import os
from xml.dom.minidom import Document
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataHandler():
    def __init__(self, data_path:str, chunk_size=1000, overlap_size=200):
        self.data_path = data_path
        self.chunks_size = chunk_size
        self.overlap_size=overlap_size

    def __load_pdfs(self):
        loader = DirectoryLoader(self.data_path,
                                 glob="*.pdf",
                                 loader_cls=PyPDFLoader)
        return loader.load()
    def __split_documents(self):
        documents = self.__load_pdfs()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunks_size, chunk_overlap=self.overlap_size)
        return text_splitter.split_documents(documents)

    def get_documents(self):
        return self.__split_documents()

if __name__ == "__main__":
    dh = DataHandler(data_path="data/")
    docs = dh.get_documents()
    print('Number of documents with chunk : ', len(docs))