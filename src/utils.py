from audioop import rms
import os
import logging
from langchain_core.documents import Document

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# res = {'query': 'What is the treatment for diabetes?', 'result': "[INST] <>\n            You are an assistant for question-answering tasks.\n    Use the following pieces of retrieved context to answer\n    the question. If you don't know the answer, say that you\n    don't know. Use three sentences maximum and keep the\n    answer concise.\n\n    Of all treatments, though, diet is one of the most\n\nrecuperation than anyother treatment option.\n\nTreatment\nThere is currently no cure for A-T, and treatment\n            <>\n\n            \n                Question: What is the treatment for diabetes?\n                 [/INST]  Based on the provided context, there is no mention of diabetes as a condition being treated. The text only discusses A-T (ATaxia-Telangiectasia), and there is no information about diabetes treatment. Therefore, I cannot provide an answer to this question.",
#        'source_documents': [
#            {"id":'9ceb99c5-e2be-4d16-ae11-331b9f2f3c63', "metadata":{"page": 444.0, "source": 'data/Medical_book.pdf'}, "page_content":'Of all treatments, though, diet is one of the most'},
#            {"id":'8219ee21-e664-4bb4-b014-f8145bbe6a25', "metadata":{"page": 371.0, "source": 'data/Medical_book.pdf'}, "page_content":'recuperation than anyother treatment option.'},
#            {"id":'cd10a593-2e56-4cf2-9a86-cdeba95887e0', "metadata":{"page": 401.0, "source": 'data/Medical_book.pdf'}, "page_content":'Treatment\nThere is currently no cure for A-T, and treatment'}]}



def process_response(model_response):
    result = model_response['result']
    result = result.split('[/INST]')[1]
    # source_documents = model_response['source_documents']
    # source_documents = [doc['page_content'] for doc in source_documents]

    # return {'result': result, 'source_documents': source_documents}
    return {'result': result}

if __name__ == "__main__":
    process_response(rms)