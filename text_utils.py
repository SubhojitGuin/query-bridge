from operator import itemgetter
import os
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import requests
import json

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# os.environ["X_API_KEY"] = os.getenv("X_API_KEY")

embeddings = OpenAIEmbeddings()


def get_search_response(question):
    url = "https://google.serper.dev/news"

    payload = json.dumps({
        "q": question,
        "num": 1
    })
    headers = {
        'X-API-KEY': os.getenv("X_API_KEY"),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


    
# db = FAISS.load_local("jalshakti_faiss_index", embeddings,allow_dangerous_deserialization=True)
prompt_template1 = """
    Answer the question as detailed as possible from the chat history and the context (if the question requires it). Make sure to include all the details. If the answer is not provided in the chat history and the context,if you do not have specific or exact information, just return "NA" only.\n\n.
    Answer the user question to the best of your ability in proper {language}.
    Answer only from the provided chat history and the context and not from anywhere else.
    Question: \n{question}\n
    Context: \n{context}\n


    Answer:
    """

# prompt_template2 = """
#     Answer the question as detailed as possible from the , make sure to provide all the details. Even if you dont have specific or exact information, provide the best possible response.
#     Answer the user question to the best of your ability in proper {language}.
#     Answer only from the provided context and not from anywhere else.
#     Question: \n{question}\n
    
#     Answer:
#     """
model1 = os.getenv("model")
llm = ChatOpenAI(model=model1, temperature=0)
# prompt = PromptTemplate(template = prompt_template , input_variables={"context","question"})

prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", prompt_template1),
        MessagesPlaceholder(variable_name="messages"),
    ]    
 )

# prompt2 = ChatPromptTemplate.from_messages(
#     [
#         ("system", prompt_template2)
#     ]    
#  )

# retriever = db.as_retriever()

text_chain1 = (
    {
        "context": lambda x: get_search_response(str(itemgetter("question")(x))),
        "question": itemgetter("question"),
        "language": itemgetter("language"),
        "messages":itemgetter("messages")
    }
    | prompt1
    | llm
    | StrOutputParser()
)

# text_chain2 = (
#     {
#         "context": itemgetter("question") | retriever,
#         "question": itemgetter("question"),
#         "language": itemgetter("language")
#     }
#     | prompt2
#     | llm
#     | StrOutputParser()
# )

# while True:
#     question = input("Query: ")
#     language = input("Language: ")
#     SessionId = input("SessionId: ")
#     response = text_chain.invoke(
#         {"question" : question , "language" : language ,"messages": [HumanMessage(content=question)]}
#         ,config={"configurable": {"session_id": SessionId}}
#         )
#     print(response)

