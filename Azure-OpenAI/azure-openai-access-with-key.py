# pip install openai

from openai import AzureOpenAI

# Azure OpenAI Service details
AZURE_OPENAI_ENDPOINT = "https://retroburn-oai-west.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
DEPLOYMENT_NAME = "gpt-4o"  # Replace with your model deployment name
SAS_KEY = "your_sas_key_here"  # Replace with your actual SAS key

# Authenticate using SAS key
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01",
    api_key=SAS_KEY
)

chat_prompt = [ 
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "How do I decide which ontology framework to use?"
            }
        ]
    }
]

# Sample request to OpenAI
completion = client.chat.completions.create(  
    model=DEPLOYMENT_NAME,  
    messages=chat_prompt,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False  
) 

# Print the assistant's response
print(completion.choices[0].message.content)
