import requests
import time

url = 'https://script.google.com/macros/s/AKfycbxmTpCJTOIYjO_F8JVyuTlj0ULDrNLxlx-VRwBzSCrHwWFu17fIjoM0o5Asv5zN9z6Pxg/exec'  # Replace with your actual Web App URL

def get_doc_content():
    response = requests.get(url)
    if 'text/plain' in response.headers.get('Content-Type', ''):
        return response.text.strip()
    else:
        print("Failed to fetch document content.")
        return None

def write_to_doc(update_text):
    response = requests.post(url, data={'text': update_text})
    if response.status_code == 200:
        print("Write response: ", response.text)
    else:
        print("Failed to write document. Status code: ", response.status_code, response.text)

while True:
    doc_content = get_doc_content()
    if doc_content:
        print(f"Document content at {time.strftime('%Y-%m-%d %H:%M:%S')}: {doc_content}")
        # Define your specific condition here
        if "specific condition" in doc_content:
            new_text = "New text to append based on condition"
            write_to_doc(new_text)
        else:
            print("Specific condition not met.")
    time.sleep(2)  # Modify as necessary for rate limits
