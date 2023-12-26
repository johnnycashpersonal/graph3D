# embed_in_database.py

import re
import torch
from transformers import AutoTokenizer, AutoModel
import pinecone
import classify  # Import the classify module

# Initialize BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Initialize Pinecone
pinecone.init(api_key='90e6e2e9-31f1-4ff2-9629-0f4bcf990a8e', environment='us-west4-gcp-free') 
index = pinecone.Index('chart3d') 

def generate_bert_embedding(text):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors='pt')

    # Generate the BERT embeddings
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

    return embeddings

def extract_title(text):
    # Extract the title using regex
    match = re.search(r'Title:(.*?)\n', text)
    if match:
        title = match.group(1).strip()
    else:
        title = None
    
    print(title)
    return title
    

def main():
    # Get the GPT-3 response from the classify script
    gpt3_response = classify.main()

    if gpt3_response:
        # Extract the title from the GPT-3 response
        title = extract_title(gpt3_response)
        print(title)

        if title:
            # Generate BERT embeddings for the GPT-3 response
            embeddings = generate_bert_embedding(gpt3_response)

            # Flatten the embeddings array and convert it to a list
            embeddings_list = embeddings.flatten().tolist()

            # Upload the embeddings to Pinecone
            upsert_response = index.upsert(
                vectors=[
                    {
                        'id': title, 
                        'values': embeddings_list, 
                        'metadata': {'classifiers': 'test'},
                    }
                ],
                namespace='test'
            )

            # Store the id in a file
            with open('ids.txt', 'a') as f:
                f.write(title + '\n')

            print(upsert_response)
        else:
            print("No title found in GPT-3 response. Exiting.")
    else:
        print("No GPT-3.5-turbo response received. Exiting.")

if __name__ == "__main__":
    main()