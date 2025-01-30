# pip install openai azure-identity

from azure.identity import InteractiveBrowserCredential, AzureCliCredential
from openai import AzureOpenAI

# Choose authentication method:
# Option 1: Use Interactive Browser Login (For GUI-based environments)
# credential = InteractiveBrowserCredential()

# Option 2: Use Azure CLI credentials (If already logged in via 'az login')
credential = AzureCliCredential()

# Azure OpenAI Service details
AZURE_OPENAI_ENDPOINT = "https://retroburn-oai-west.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
DEPLOYMENT_NAME = "gpt-4o"  # Replace with your model deployment name

# Define the required scope explicitly for Azure OpenAI
TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"

# Authenticate using Azure AD credentials
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01",
    azure_ad_token_provider=lambda: credential.get_token(TOKEN_SCOPE).token
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
                "text": "How do I decided which ontology framework to use?"
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
