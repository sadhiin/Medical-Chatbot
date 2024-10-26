import os
from xml.dom.minidom import Document
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class DataHandler():
    def __init__(self, data_path:str):
        self.data_path = data_path

    def __load_pdfs(self):
        loader = DirectoryLoader(self.data_path,
                                 glob="*.pdf",
                                 loader_cls=PyPDFLoader)
        return loader.load()
    def __split_documents(self):
        documents = self.__load_pdfs()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)

    def get_documents(self):
        return self.__split_documents()

if __name__ == "__main__":
    dh = DataHandler(data_path="data/")
    docs = dh.get_documents()
    print('Number of documents: ', len(docs))