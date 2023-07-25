# API import Section
from fastapi import FastAPI, Request
# LLM section import
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# IMPORTS FOR TEXT GENERATION PIPELINE CHAIN
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
import copy

app = FastAPI(
    title="Inference API for Lamini-77M",
    description="A simple API that use MBZUAI/LaMini-Flan-T5-77M as a chatbot",
    version="1.0",
)


### INITIALIZING LAMINI MODEL
checkpoint = "./model/"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,
                                                    device_map='auto',
                                                    torch_dtype=torch.float32)

### INITIALIZING PIPELINE WITH LANGCHAIN
llm = HuggingFacePipeline.from_model_id(model_id=checkpoint,
                                        task = 'text2text-generation',
                                        model_kwargs={"temperature":0.45,"min_length":30, "max_length":350, "repetition_penalty": 5.0})

template = """{text}"""

prompt = PromptTemplate(template=template, input_variables=["text"])
chat = LLMChain(prompt=prompt, llm=llm)


@app.get('/')
async def hello():
    return {"hello" : "Medium enthusiast"}


@app.get('/model')
async def model():
    res = chat.run("Who is Ada Lovelace?")
    result = copy.deepcopy(res)
    return {"result" : result}

@app.get('/lamini')
async def lamini(question : str):
    res = chat.run(question)
    result = copy.deepcopy(res)
    return result

