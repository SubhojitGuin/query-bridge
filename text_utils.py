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



from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("X_API_KEY")
# os.environ["X_API_KEY"] = os.getenv("X_API_KEY")

embeddings = OpenAIEmbeddings()
model1 = os.getenv("model")
llm = ChatOpenAI(model=model1, temperature=0)


# Initialize Google Serper API wrapper
search = GoogleSerperAPIWrapper()

# Define tools for the agent
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to answer questions about current events or the current state of the world. Input should be a search query."
    )
]

react_agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
    early_stopping_method="force"
)



def modify_question_for_search(question, messages):
    """
    Modify the user's question based on chat history to make it more relevant for Google search.
    """
    refinement_prompt = ChatPromptTemplate.from_messages([
        ("system", "Improve the following user query based on the provided chat history to make it more precise for a Google search.The question should be generic and not exactly specific to the chat history and always specify 'Formula 1' in the context of the modified question. In case of any relevant names in the chat history, include them in the modified question. If the Chat History is empty, just return 'NA'."),
        ("user", "Chat History: {messages}\n\nOriginal Query: {question}")
    ])
    refine_chain = refinement_prompt | llm | StrOutputParser()
    return refine_chain.invoke({"question": question, "messages": messages})


def get_context(question, messages):
    modified_question = modify_question_for_search(question, messages)
    return react_agent.run(modified_question)


def get_search_response(question, messages):
    url = "https://google.serper.dev/search"
    modified_question = modify_question_for_search(question, messages)
    print("MODIFIED QUESTION: ", modified_question)
    payload = json.dumps({
        "q": modified_question,
        "num": 5
    })
    headers = {
        'X-API-KEY': os.getenv("X_API_KEY"),
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)
    return response.text



    
# db = FAISS.load_local("jalshakti_faiss_index", embeddings,allow_dangerous_deserialization=True)
prompt_template1 = """
    Only respond to generic and descriptive questions that require explanations, descriptions, or insights.
    Answer the question in a detailed and informative manner using the provided chat history and context, ensuring completeness and clarity.  

    If the question asks for specific numbers, rankings, statistics, or factual data points (e.g., fastest lap times, number of wins, specific race results, or list of entities), return "NA" only.  

    Ensure the response is well-structured and provided in proper {language}.  
    Do not use any external knowledge beyond the given chat history and context.  

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
        "context": lambda x: get_context(str(itemgetter("question")(x)), itemgetter("messages")(x)),
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

