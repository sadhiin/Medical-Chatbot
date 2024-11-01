import torch
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

from transformers import pipeline, TextStreamer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from src.utils import setup_logger
from src.prompt import generate_prompt
from src.vectordb import VectorDB
import gc
import os

logger = setup_logger(__name__, 'logs/large_language_model.log')

class LargeLanguageModel():
    def __init__(self, model_name_hf_id="TheBloke/Llama-2-13B-chat-GPTQ", model_basename='model', revision_ckpt='gptq-4bit-128g-actorder_True'):
        # Set PyTorch memory allocation configuration
        torch.cuda.set_per_process_memory_fraction(0.9)  # Use only 90% of available GPU memory
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

        self.DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model_name_or_path = model_name_hf_id
        self.model_basename = model_basename
        self.revision_ckpt = revision_ckpt

        logger.info(f"Using device: {self.DEVICE}")

        # Clear memory before loading model
        gc.collect()
        torch.cuda.empty_cache()

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name_or_path,
                use_fast=True,
                trust_remote_code=True
            )

            gc.collect()
            torch.cuda.empty_cache()

            self.model = AutoGPTQForCausalLM.from_quantized(
                model_name_or_path=self.model_name_or_path,
                revision=self.revision_ckpt,
                model_basename=model_basename,
                use_safetensors=True,
                trust_remote_code=True,
                inject_fused_attention=False,
                device=self.DEVICE,
                quantize_config=None,
                use_cache=True,
                low_cpu_mem_usage=True
            )

            gc.collect()
            torch.cuda.empty_cache()

            # self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)

        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise


    def __get_pipeline(self):
        text_pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=1024,
            temperature=0.2,
            top_p=0.95,
            repetition_penalty=1.15,
            # streamer=self.streamer,
        )
        return HuggingFacePipeline(pipeline=text_pipeline, model_kwargs={"temperature": 0.2})


    def get_llm(self):
        return self.__get_pipeline()



class MedicalChatbot():
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MedicalChatbot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not MedicalChatbot._initialized:
            self.prompt = PromptTemplate(
                template=generate_prompt(
                    prompt="""
                    Question: {question}
                    """),
                input_variables=["question"])
            self.vector_database = VectorDB().get_index()
            self.llm = LargeLanguageModel()
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm.get_llm(),
                chain_type="stuff",
                retriever=self.vector_database.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": self.prompt},
            )
            MedicalChatbot._initialized = True

    def answer_question(self, question) -> str:
        return self.qa_chain.invoke({"query": question})


if __name__ == "__main__":
    medical_chatbot = MedicalChatbot()
    print(medical_chatbot.answer_question("What is the treatment for diabetes?"))
