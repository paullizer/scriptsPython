# Azure OpenAI

This repository provides **two example Python scripts** demonstrating how to connect to and interact with the **Azure OpenAI Service** using the `openai` Python library and the specialized `AzureOpenAI` class. Each script showcases a different authentication method:

1. **Script 1:** Using a **Shared Access Signature (SAS) key**
2. **Script 2:** Using **Azure Active Directory (AAD)** credentials (through either Azure CLI or Interactive Browser Credential)

Both scripts send a sample conversation to an Azure OpenAI model and print the AI’s response in the console.

## Prerequisites

1. **Python 3.7+**
    Make sure you have Python 3.7 or higher installed. You can check your version with:

   ```bash
   python --version
   ```

2. **Azure OpenAI Resource**

   - Have an Azure OpenAI resource set up in the Azure Portal.
   - Obtain the resource’s **endpoint URL** and **deployment name**.
   - For the first script, you will also need the **SAS key** (api key) associated with your OpenAI resource.

3. **Azure Subscription** (for the second script)

   - You should already be authenticated with Azure CLI (`az login`) if you plan to use `AzureCliCredential`, or you should have access to a browser for the `InteractiveBrowserCredential`.

## Overview of the Scripts

### 1. `azure-openai-access-with-key.py` (Using SAS Key Authentication)

This script demonstrates how to authenticate directly with your Azure OpenAI service via SAS key.

```python
# pip install openai

from openai import AzureOpenAI

# Azure OpenAI Service details
AZURE_OPENAI_ENDPOINT = "https://endpoint_name.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-4o"
SAS_KEY = "your_sas_key_here"

# Create a client using the SAS key
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version="2024-02-01",
    api_key=SAS_KEY
)

# Define a chat prompt
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

# Create a completion request
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

# Print the AI's response
print(completion.choices[0].message.content)
```

#### Installation

```bash
pip install openai
```

#### How to Use

1. **Replace** the placeholder values:

   - `AZURE_OPENAI_ENDPOINT` with your endpoint (e.g., `https://myresource.openai.azure.com/`).
   - `DEPLOYMENT_NAME` with your deployment name (e.g., `my-gpt-model-deployment`).
   - `SAS_KEY` with your actual SAS key.

2. **Run** the script:

   ```bash
   python script_sas_key.py
   ```

3. The console output should display the AI’s response to the prompt.

### 2. `azure-openai-access-with-managed-identity.py` (Using Azure AD Credentials)

This script shows how to authenticate with Azure OpenAI using **Azure Active Directory** credentials. You can either:

- **Option 1:** Use `InteractiveBrowserCredential()`, which will open a browser window for you to log in.
- **Option 2:** Use `AzureCliCredential()`, which uses your already logged-in Azure CLI session.

```python
# pip install openai azure-identity

from azure.identity import InteractiveBrowserCredential, AzureCliCredential
from openai import AzureOpenAI

# Choose authentication method:
# Option 1: Use Interactive Browser Login
# credential = InteractiveBrowserCredential()

# Option 2: Use Azure CLI credentials
credential = AzureCliCredential()

# Azure OpenAI Service details
AZURE_OPENAI_ENDPOINT = "https://endpoint_name.openai.azure.com/"
DEPLOYMENT_NAME = "gpt-4o"

# Define the required scope for Azure OpenAI
TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"

# Create a client using Azure AD credentials
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

# Create a completion request
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

# Print the AI's response
print(completion.choices[0].message.content)
```

#### Installation

```bash
pip install openai azure-identity
```

#### How to Use

1. Configure

    the authentication:

   - Uncomment `InteractiveBrowserCredential()` if you prefer browser-based login.
   - Or leave `AzureCliCredential()` if you have performed `az login` in your environment.

2. **Replace** `AZURE_OPENAI_ENDPOINT` and `DEPLOYMENT_NAME` with your own values.

3. Run

    the script:

   ```bash
   python script_aad_auth.py
   ```

4. Follow any browser prompts (if using `InteractiveBrowserCredential`), or ensure you are already logged in via `az login` (if using `AzureCliCredential`).

5. The script prints the completion response in your console.

## Common Parameters and Explanation

- **max_tokens (int)**: Controls the maximum number of tokens (words/fragments) to generate.
- **temperature (float)**: Controls the randomness of the output. A higher value (close to 1.0) produces more creative or random responses, while a lower value (close to 0.0) makes the output more deterministic.
- **top_p (float)**: Controls the nucleus sampling. The model considers tokens whose cumulative probability mass is up to `top_p`.
- **frequency_penalty (float)** and **presence_penalty (float)**: Adjust the likelihood of repeating the same lines or tokens. Typically set to `0` for default behavior.
- **stream (bool)**: If `True`, the response is returned as a stream of tokens. In these examples, it’s set to `False` for simplicity.

## Troubleshooting

1. **Authentication Failures**
   - Double-check your SAS key if using the first script.
   - Ensure you are logged in with `az login` if you’re using `AzureCliCredential`.
   - For `InteractiveBrowserCredential`, ensure your browser window allows pop-ups or is not blocked by corporate firewalls.
2. **Resource or Quota Errors**
   - Verify that your Azure OpenAI resource is properly deployed and you have enough quota.
   - Check your region: Some regions might not support GPT-4 or other models.
3. **API Version or Model Deployment Issues**
   - The scripts specify `api_version="2024-02-01"`. Make sure your resource supports this version and that your `DEPLOYMENT_NAME` matches the model deployment in Azure.

------

**Author’s Note**: These scripts are provided as **basic examples** to help you get started with Azure OpenAI. Always ensure that your **keys, tokens, and other secrets** are stored securely. For production usage, consider using environment variables or a secure key vault service rather than hardcoding credentials in scripts.