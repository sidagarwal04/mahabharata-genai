# Import necessary libraries
import google.generativeai as genai
import base64
import json
import re
import gradio as gr
from neo4j import GraphDatabase
import os

# Update with your Gemini API key in Hugging Face(required for using the generative AI model)
api_key = os.getenv("GEMINI_API_KEY")

# Update with your Neo4j connection details in Hugging Face(required for connecting to the Neo4j database)
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Configure the generative AI model with your API key
genai.configure(api_key = api_key)



#This function generates the Cypher query based on the user's natural language question by leveraging the Gemini generative AI model.
def get_answer(input):

  # Define the generation configuration for the model, controlling factors like temperature and output length
  generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
  }

  # Define safety settings to filter out harmful content
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

  # Load the Gemini model (update with the appropriate model name)
  model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

  # Define prompts for the model, including examples to guide it towards generating the desired Cypher query
  prompt_parts = [
    "You are an expert in converting English questions to Neo4j Cypher Graph code! The Graph has just 1 Node Label - Person! the Movie Node has the following properties: name, gender, type, dynasty, count, health, marital_status, nickname, number_of_children and title. The Neo4j Graph has the following Relationship types DAUGHTER_OF, FATHER_OF, HUSBAND_OF, KILLED, MOTHER_OF, SON_OF and WIFE_OF.In this graph, if FATHER_OF or MOTHER_OF relationship exists between two nodes that mean that starting node are parents of the destination node. So if I am asking, who are the parents of a node named \"Karna\", the graph should search for FATHER_OF and/or MOTHER_OF relationship ending to Karna and generate a cypher query and hence a response accordingly. Similarly if HUSBAND_OF or WIFE_OF relationship exists between two nodes that mean that both starting nodes and the destination node are married to each other. So if I am asking, who is Kunti married to, the graph should search for WIFE_OF relationship starting from Kunti or HUSBAND_OF relationship ending to Kunto and generate a cypher query and hence a response accordingly.\n\nDo not include ```, \\n and other verbose in the output. Also, do not include single quotes with the output. Just give the final cypher statement in the output.",
    "input: Who is the husband of Kunti?",
    "output: MATCH (n:Person)-[HUSBAND_OF]->(m:Person) where m.name = \"Kunti\" RETURN n.name;",
    "input: Who are the parents of Karna?",
    "output: MATCH (karna:Person {name: \"Karna\"}), (p:Person)-[:FATHER_OF|MOTHER_OF]->(karna) RETURN p.name",
    "input: Who is Kunti married to?",
    "output: MATCH (n:Person),(m:Person {name:\"Kunti\"})WHERE (n)-[:HUSBAND_OF]->(m) OR (m)-[:WIFE_OF]->(n)RETURN n.name",
    f"input:{input}",
  ]

  # Generate the response (Cypher query) using the model
  response = model.generate_content(prompt_parts)

  return response.text

# Establish a Neo4j driver connection using the provided credentials (update these with your details)
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))



#This function extracts the Cypher query and the return key from the response generated by the `get_answer` function.
def extract_query_and_return_key(input_query_result):
    slash_n_pattern = r'[ \n]+'
    ret_pattern = r'RETURN\s+(.*)'
    replacement = ' '

    cleaned_query = re.sub(slash_n_pattern, replacement, input_query_result)
    if cleaned_query:
        match = re.search(ret_pattern, cleaned_query)
        if match:
            extracted_string = match.group(1)
        else:
            extracted_string = ""
    return cleaned_query, extracted_string



#This function takes a list of names and formats it into a human-readable string.
def format_names_with_ampersand(names):
    if len(names) == 0:
        return ""
    elif len(names) == 1:
        return names[0]
    else:
        formatted_names = ", ".join(names[:-1]) + " & " + names[-1]
        return formatted_names


#This function executes the provided Cypher query on the Neo4j database and retrieves the results based on the return key.
def run_cypher_on_neo4j(inp_query, inp_key):
  out_list = []

  # Establish a temporary session with the Neo4j database using the global driver object
  with driver.session() as session:
      result = session.run(inp_query)
      for record in result:
          out_list.append(record[inp_key])
  driver.close()
  if len(out_list) > 1:
      return format_names_with_ampersand(out_list)
  elif len(out_list) == 1:
      return out_list[0]
  else:
      return ""

#  This function serves as the core logic for processing user input and retrieving results from the Neo4j database.
def generate_and_exec_cypher(input_query):
    # Get the Cypher query and return key by parsing the response from `get_answer`
    gen_query, gen_key = extract_query_and_return_key(get_answer(input_query))
    return run_cypher_on_neo4j(gen_query, gen_key)


#This function acts as the chatbot interface, handling user interactions and responses.
def chatbot(input, history=[]):
    
    # Generate and execute the Cypher query to retrieve results based on the user's input
    output = str(generate_and_exec_cypher(input))

    # Append the current question and answer to the conversation history
    history.append((input, output))
    
    # Gradio expects the same data for both outputs, so return the updated history twice
    return history, history


# Launch the Gradio interface for the chatbot
gr.Interface(fn = chatbot,
             inputs = ["text",'state'],
             outputs = ["chatbot",'state']).launch(debug = True, share=True)
