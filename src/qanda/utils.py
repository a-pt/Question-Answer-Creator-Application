import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from transformers import AutoTokenizer
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from . import prompts

# Groq Authentication
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

def file_processing(file_path):
    """
    Process the file and return the chunks
    """
    loader = PyPDFLoader(file_path)
    data = loader.load()
    content = ""
    for page in data:
        content += page.page_content

    # Load a specific Hugging Face tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Create the splitter using the loaded tokenizer's encode method
    text_splitter = TokenTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=200,
        chunk_overlap=50
    )

    # Split your content
    chunks = text_splitter.split_text(content)

    # Document object for the entire content
    document = Document(page_content=content)

    # convert string chunks to Document format
    document_chunks = [Document(page_content=chunk) for chunk in chunks]
    
    return document, document_chunks


def create_vector_store(document_chunks):
    """
    Create a vector store from the document chunks
    """
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = FAISS.from_documents(document_chunks, embedding_model)
    return vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def llm_pipeline(file_path):
    """
    Create a pipeline for generating questions and answers
    """
    document, document_chunks = file_processing(file_path)

    openaiChatModel =  ChatGroq(model="openai/gpt-oss-120b",temperature = 0.3)

    question_prompt = PromptTemplate(
        template = prompts.question_prompt_template, 
        input_variables = ["text"]
    )

    refine_question_prompt = PromptTemplate(
        input_variables = ["existing_answer","text"],
        template = prompts.refine_question_template
    )

    # Define the chains using LCEL
    initial_chain = question_prompt | openaiChatModel | StrOutputParser()

    refine_chain = refine_question_prompt | openaiChatModel | StrOutputParser()

    # Start with the first chunk
    current_questions = initial_chain.invoke({"text": document_chunks[0].page_content})

    # Iteratively refine with the rest of the chunks
    for i, doc in enumerate(document_chunks[1:], start=2):
        current_questions = refine_chain.invoke({
            "existing_answer": current_questions,
            "text": doc.page_content
        })

    questions = current_questions.split("\n\n")

    vector_store = create_vector_store(document_chunks)

    retriever = vector_store.as_retriever()

    retrieval_prompt = PromptTemplate(
        template = prompts.retrieval_promt,
        input_variables = ["context", "question"]
    )

    answer_chain = (
        RunnableParallel(
            context=retriever | format_docs,
            question=RunnablePassthrough()
        )
        | retrieval_prompt
        | openaiChatModel
        | StrOutputParser()
    )
    
    return questions, answer_chain
