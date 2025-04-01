# -*- coding: utf-8 -*-
"""geneiahub.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KC7R6DUmzFP4if7JlTFTiMAezSoUUVEU
"""

import os
os.environ['AICORE_AUTH_URL'] = "" # TODO
os.environ['AICORE_CLIENT_ID'] = "" #TODO
os.environ['AICORE_RESOURCE_GROUP'] = "" #TODO
os.environ['AICORE_CLIENT_SECRET'] = "" #TODO
os.environ['AICORE_BASE_URL'] = ""#TODO
os.environ['HANA_VECTOR_USER'] = ""#TODO
os.environ['HANA_VECTOR_PASS'] = ""#TODO
os.environ['HANA_HOST_VECTOR'] = ""#TODO

from gen_ai_hub.proxy.langchain.amazon import init_chat_model as amazon_init_chat_model
from gen_ai_hub.proxy.langchain.init_models import init_llm
model_name = 'anthropic--claude-3.5-sonnet'
model_id = 'anthropic.claude-newer-version-202401220-v1:0'
init_func = amazon_init_chat_model
llm = init_llm(model_name, model_id=model_id, init_func=init_func)

from langchain_core.prompts import PromptTemplate
from typing_extensions import TypedDict, Annotated
from hdbcli import dbapi


#give example in template and try different LLMs
template = '''Given an input question, your task is to create a syntactically correct SPARQL query to retrieve information from an RDF graph.
The graph may contain variations in spacing, underscores, dashes, capitalization, reversed relationships, and word order.
You must account for these variations using the `REGEX()` function in SPARQL.
In the RDF graph, subjects are represented as "s", objects are represented as "o", and predicates are represented as "p". Account for underscores.

Example Question: "What are SAP HANA Hotspots"
Example SPARQL Query: SELECT ?s ?p ?o
WHERE {{
    ?s ?p ?o .
    FILTER(
        REGEX(str(?s), "SAP_HANA_Hotspots", "i") ||
        REGEX(str(?o), "SAP_HANA_Hotspots", "i")
    )
}}

Retrieve only triples beginning with "http://test_mission_faqhanahotspots.org/"
Use the following format:
Question: f{input}
S: Subject to look for in the RDF graph
P: Predicate to look for in the RDF graph
O: Object to look for in the RDF graph
SPARQL Query: SPARQL Query to run, including s-p-o structure

The output should only include the SPARQL query, nothing else at all. JUST THE QUERY! Do not yap! Do not repeat the question or the definition. Do not even say here is the query.....
'''

query_prompt_template = PromptTemplate.from_template(template)

class State(TypedDict):
    question: str
    s: str
    p: str
    o: str
    query: str

#return dictionary where key is query and value is SPARQL query string
class QueryOutput(TypedDict):
    """Generated SPARQL query."""
    query: Annotated[str, ..., "Syntactically valid SPARQL query."]

def write_query(state: State):
    """Generate SPARQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "input": state["question"],
        }
    )
 
    result = llm.invoke(prompt)
    print(result.content)
    return {"query": result.content}


def execute_sparql(query_response):
    print()
    cursor = conn.cursor() #TODO connection to the HANA database
    try:
        # Execute
        resp = cursor.callproc('SPARQL_EXECUTE', (query_response["query"], 'Metadata headers describing Input and/or Output', '?', None))

        # Check if the response contains expected OUT parameters
        if resp:
            # Extract metadata and query results from the OUT parameters
            metadata_headers = resp[3]  # OUT: RQX Response Metadata/Headers
            query_response = resp[2]    # OUT: RQX Response

            # Handle response
            print("Query Response:", query_response)
            print("Response Metadata:", metadata_headers)
            return query_response
        else:
            print("No response received from stored procedure.")

    except Exception as e:
        print("Error executing stored procedure:", e)
    finally:
        cursor.close()

def summarize_info(question, query_response):
    prompt = """Answer the user question below given the following relational information in XML format. Use as much as the query response as possible to give a full, detailed explanation. Interpret the URI and predicate information using context. Don't use phrases like 'the entity identified by the URI,' just say what the entity is.
    Also make sure the output is readable in a format that can be display through an HTML file, add appropriate formatting.
    Please remove unnecessary information. Do not add information about the triples. Do not add the source of the data.
    Do not include details about what they are identified as or what kind of entity they are unless asked. Do not add any suggestions unless explicitly asked. Simply give a crisp and direct answer to what has been asked!
    If you do not have an answer, please say so. DO NOT HALLUCINATE!. Just give me an explanation, no need to create a graph
    User Question: {question}
    Information: {information}
    """
    summarize = PromptTemplate.from_template(prompt)
    prompt_input = summarize.invoke(
            {
                "question": question,
                "information": query_response,
            }
        )

    class QuestionAnswer(TypedDict):
        """Generated SPARQL query."""
        final_answer: Annotated[str, ..., "Answer to user's question."]

    final_answer = llm.invoke(prompt_input)
    print(final_answer.content)

#==========SAMPLE QUESTIONS==============#
#Question 1
question1 = "What is SAP HANA HotSpots Cloud?" 
sparql1 = write_query({"question": question1})
response1 = execute_sparql(sparql1)
summarize_info(question1, response1)

# Question 2
question2 = "What is hscmd?"
sparql2 = write_query({"question": question2})
response2 = execute_sparql(sparql2)
summarize_info(question2, response2)

# Question 3
question3 = "What is the SAP HANA KPI collector?"
sparql3 = write_query({"question": question3})
response3 = execute_sparql(sparql3)
summarize_info(question3, response3)