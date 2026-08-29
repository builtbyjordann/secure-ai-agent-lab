import requests
from rag.rag_lab import choose_document

def get_account(account_id, token):
    url = f"http://127.0.0.1:5000/account/{account_id}"

    headers = {
        "Authorization": token
    }

    response = requests.get(url, headers=headers)

    return response.json()


users_token = input("Enter user token: ")
question = input("Good Morning, how may I help you?: ")

requested_document = choose_document(question)

def get_document(requested_document, token):
    url = f"http://127.0.0.1:5000/documents/{requested_document}"

    headers = {
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    return response.json()


if requested_document:
    document_content = get_document(requested_document, users_token)

    print(document_content)
    
    # now we're going to simulate the agent getting poisoned by an indirect prompt injection. The "trusted file" will contain a prompt asking the agent to retrieve a document that it doesn't have access to, and the agent will try to retrieve it anyway.
    if (
        "content" in document_content
        and "retrieve payroll.txt" in document_content["content"].lower()
    ):
        requested_document = "payroll.txt"

        document_content = get_document(requested_document, users_token)

        print(document_content)

else:
    print("I could not find a matching document")