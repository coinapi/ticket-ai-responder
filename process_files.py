import openai
import os
import json
import sys
import pandas as pd
import numpy as np
from ast import literal_eval
from embeddings_script.embeddings_utils import *

# Function to load the OpenAI API key
def load_api_key(api_key_file):
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()
    return api_key

def load_local_embeddings():
    df=pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(literal_eval).apply(np.array)
    return df

def create_context(
    question, df, api_key, max_len=1800, size="ada"
):    
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    openai.api_key = api_key
    q_embeddings = openai.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
        
        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)

# Function to get embeddings for a given text
def get_embeddings(text, api_key, model_name):

    df = load_local_embeddings()
    context = create_context(text, df, api_key)

    response = openai.completions.create(
        # prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
        prompt=f"Context: {context}\n\n---\n\nQuestion: {text}\nAnswer:",
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        model=model_name,
    )
    # print(response)
    return response.choices[0].text.strip()

    # response = openai.Embedding.create(
    #     model=model_name,
    #     input=text
    # )
    # return response

# Function to process input files and write responses to an output file
def process_files(input_files, output_file, api_key, model_name):
    responses = {}
    for file_path in input_files:
        with open(file_path, 'r') as file:
            text = file.read()
        response = get_embeddings(text, api_key, model_name)
        responses[file_path] = response
    
    with open(output_file, 'w') as outfile:
        json.dump(responses, outfile, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <api_key_file> <output_file> <model_name> <input_file1> <input_file2> ...")
        sys.exit(1)
    
    api_key_file = sys.argv[1]
    output_file = sys.argv[2]
    model_name = sys.argv[3]
    input_files = sys.argv[4:]
    
    api_key = load_api_key(api_key_file)
    
    # Process the input files and save the responses
    process_files(input_files, output_file, api_key, model_name)
    print(f"Responses have been saved to {output_file}")