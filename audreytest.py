# import requests
# import time
# import os
# import google.generativeai as genai

# api_key = os.getenv('GOOGLE_API_KEY')
# # Configure API key and model
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('gemini-1.5-pro-latest')


# url = 'https://script.google.com/macros/s/AKfycbxACdxAAv-Zqcf0n1WQHAv-oFczv_wJ2wgK0r3GqIsVW-dbKhpJOO-ZyO5pAUtv5K2SKQ/exec'

# def get_doc_content():
#    response = requests.get(url)
#    if 'text/plain' in response.headers.get('Content-Type', ''):
#        return response.text.strip()
#    else:
#        print("Failed to fetch document content.")
#        return None


# def write_to_doc(update_text, full_replace=False):
#    global internal_update
#    data = {'text': update_text, 'fullReplace': str(full_replace).lower()}
#    response = requests.post(url, data=data)
#    if response.status_code == 200:
#        print("Write response: ", response.text)
#        if full_replace:
#            internal_update = True  # Mark this update as internal
#        time.sleep(6)
#    else:
#        print(f"Failed to write document. Status code: {response.status_code}, {response.text}")


# def detect_changes(old_content, new_content):
#    if internal_update:
#        print("Skipping detection for internal update.")
#        return  # Skip detection if the last update was internal
#    update_text = new_content[len(old_content):].strip()
#    if update_text:
#        print("Update Detected:")
#        print("----")
#        print(update_text)  # Display new text only
#        print("----")
#        classify_update(update_text, new_content)


# def classify_update(text, full_text):
#    try:
#        response = model.generate_content(f"Classify the following sentence as either 'transcription' or 'command': {text}")
#        classification = response.text.strip().lower()
#        print("Classification:", classification)
#        if classification == 'transcription':
#            if text not in full_text:
#                write_to_doc(text, full_replace=False)  # Append the transcription text to the document only if not present
#            else:
#                print("Transcription text already present in document.")
#        else:
#            # Process command and replace entire document text
#            command_response = model.generate_content(f"Process the following command in context: {text} Context: {full_text}. Output should be as if the final output.")
#            output_text = command_response.text.strip()
#            write_to_doc(output_text, full_replace=True)  # Replace the entire document content with the command response
#    except Exception as e:
#        print("Failed to classify or process text:", str(e))


# internal_update = False  # Flag to track whether the last update was done internally
# previous_content = None
# while True:
#    current_content = get_doc_content()
#    if current_content:
#        if internal_update:
#            # Reset the internal update flag and skip this cycle
#            internal_update = False
#            previous_content = current_content
#            continue


#        if previous_content is None:
#            previous_content = current_content  # Initialize previous_content
#        print(f"Document content at {time.strftime('%Y-%m-%d %H:%M:%S')}: {current_content}")


#        if previous_content != current_content:
#            detect_changes(previous_content, current_content)
#            previous_content = current_content  # Update previous_content to the new current content


#    time.sleep(5)  # Modify as necessary for rate limits

import requests
import time
import os
import google.generativeai as genai


# Configure API key and model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro-latest')


url = 'https://script.google.com/macros/s/AKfycbyUcIM0_wxrp7EABBJGij9jJ81tbGaR-i3UKrGvxPQwKDLknVAdbD03MyN6CDNhGVPYXA/exec'


def get_doc_content():
   response = requests.get(url)
   if 'text/plain' in response.headers.get('Content-Type', ''):
       return response.text.strip()
   else:
       print("Failed to fetch document content.")
       return None


def write_to_doc(update_text, full_replace=False):
   global internal_update
   data = {'text': update_text, 'fullReplace': str(full_replace).lower()}
   response = requests.post(url, data=data)
   if response.status_code == 200:
       print("Write response: ", response.text)
       if full_replace:
           internal_update = True  # Mark this update as internal
   else:
       print(f"Failed to write document. Status code: {response.status_code}, {response.text}")


def detect_changes(old_content, new_content):
   if internal_update:
       print("Skipping detection for internal update.")
       return
   update_text = new_content[len(old_content):].strip()
   if update_text:
       print("Update Detected:")
       print("----")
       print(update_text)  # Display new text only
       print("----")
       classify_update(update_text, new_content)


def classify_update(text, full_text):
   try:
       response = model.generate_content(f"Classify the following sentence as either 'transcription' or 'command': {text}")
       if response.parts:
           classification = response.parts[0].text.strip().lower()
           print("Classification:", classification)
           handle_classification(classification, text, full_text)
       else:
           print("No valid part returned in response:", response.candidate.safety_ratings if response.candidate.safety_ratings else "No details")
   except Exception as e:
       print("Failed to classify or process text:", str(e))


def handle_classification(classification, text, full_text):
   if classification == 'transcription':
       if text not in full_text:
           write_to_doc(text, full_replace=False)
       else:
           print("Transcription text already present in document.")
   else:
       command_response = model.generate_content(f"Process the following command in context: {text} Context: {full_text}. Your output must be final and polished.")
       if command_response.parts:
           output_text = command_response.parts[0].text.strip()
           write_to_doc(output_text, full_replace=True)
       else:
           print("Command processing failed or blocked:", command_response.candidate.safety_ratings if command_response.candidate.safety_ratings else "No details")


internal_update = False
previous_content = None
while True:
   current_content = get_doc_content()
   if current_content:
       if internal_update:
           internal_update = False
           previous_content = current_content
           continue


       if previous_content is None:
           previous_content = current_content
       print(f"Document content at {time.strftime('%Y-%m-%d %H:%M:%S')}: {current_content}")


       if previous_content != current_content:
           detect_changes(previous_content, current_content)
           previous_content = current_content


   time.sleep(5)



