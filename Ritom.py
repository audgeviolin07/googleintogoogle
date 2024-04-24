import requests
import time
import os
import google.generativeai as genai
import webcolors

url = 'https://script.google.com/macros/s/AKfycbwFizilh0CvwnKsv_oXbMG_Zcs9zFu0YI8gb2OkdeqpNM2AOSnxIiWVWvlLLWT8fBzT/exec'

# Configure API key and model
genai.configure(api_key='AIzaSyBcjpZukdkRzkToebblttw3fPjdPadwWFw')
def change_font_size(text:str, size:str):
    """ changes the font size of the text to the given size

    Args:
        text: String, The text that is to be displayed on the google doc
        size: String, The font size that the text is to be set to
    """
    data = {'text': text, "font_size": size }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Success: Font Size")
        
    else:
        print(f"Failed to change Font Size. Status code: {response.status_code}, {response.text}")


def change_font_style(text:str, style:str):
    """ changes the font style of the text to the given types (underline, italic, Bold)

    Args:
        text: String, The text that is to be displayed on the google doc
        style: String, The font style that the text is to be set to (underlined, italicized, Bold)
    """
    data = {'text': text, "font_style": style }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Success: Font Style")
        
    else:
        print(f"Failed to change Font. Status code: {response.status_code}, {response.text}")

def change_font_color(text:str, color:str):
    """ changes the font color of the text to the color given

    Args:
        text: String, The text that is to be displayed on the google doc
        color: String, The font color that the text is to be set to, should be a string like 'red', 'blue', or 'green'
    """
    hex_color = webcolors.name_to_hex(color)
    data = {'text': text, "font_color": hex_color }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Success: Font Color")
        
    else:
        print(f"Failed to change Font Color. Status code: {response.status_code}, {response.text}")

def change_font_family(text:str, font:str):
    """ changes the font family of the text to the family given

    Args:
        text: String, The text that is to be displayed on the google doc
        font: String, The font family that the text is to be set to, should be a string like 'Times New Roman', 'Comic Sans'
    """
    data = {'text': text, "font_family": font }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Success: Font Family")
        
    else:
        print(f"Failed to change Font Color. Status code: {response.status_code}, {response.text}")

functions = {"change_font_color": change_font_color, "change_font_size": change_font_size, "change_font_style": change_font_style, "change_font_family": change_font_family}
model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction="I want you to act as a text editor for me. Where when I tell you to do something with my text, you edit the text the way I ask you to and return the edited text back to me. Keep relativley consistent spacing with the text.", tools=functions.values())
model2 = genai.GenerativeModel('gemini-pro')


def call_function(function_call, functions):
    function_name = function_call.name
    function_args = function_call.args
    functions[function_name](**function_args)

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

    #    time.sleep(6)
   else:
       print(f"Failed to write document. Status code: {response.status_code}, {response.text}")


def detect_changes(old_content, new_content):
   if internal_update:
       print("Skipping detection for internal update.")
       return  # Skip detection if the last update was internal
   update_text = ""
   if len(new_content)> len(old_content):
       update_text = new_content.replace(old_content, "").strip()
   else:
       update_text = new_content.replace(old_content, "").strip()       
   if update_text and '.' in update_text:
       print("Update Detected:")
       print("----")
       print(update_text)  # Display new text only
       print("----")
       classify_update(update_text, new_content)


def classify_update(text, full_text):
    try:
        response = model2.generate_content(f"Classify the following text as either 'transcription' (part of the piece of writing I am writing) or 'command' (I am telling you to do something with the text or search something up for me): {text}")
        classification = response.candidates[0].content.parts[0].text.strip().lower()
        print("Classification:", classification)
        if classification == 'transcription':
            print("Transcription")
            print("----")
            command_response = model2.generate_content(f"Can you fix the typos in the following text if there are any {full_text}. Output only the returned text without anything else. For example, If I say today is a good dayday. Only output today is a good day. But keep the spacing the same as before.")
            output_text = command_response.candidates[0].content.parts[0].text
            write_to_doc(output_text, full_replace=True)
        #    if text not in full_text:
        #        write_to_doc(text, full_replace=False)  # Append the transcription text to the document only if not present
        #    else:
        #        print("Transcription text already present in document.")
        else:
           # Process command and replace entire document text
            command_response = model.generate_content(f"Can you run the following command - {text} - on the following content - {full_text}. Output only the returned text without the command. For example, If I say Turn this into a list, I want you to turn the text into a list and only return the bulleted form, not the command. Or if I tell you to expand on what I wrote in a beautiful manner, I want you to return the full expansion including what I wrote before, but do not return the command text. ")
            print(command_response)
            part = command_response.candidates[0].content.parts[0]
            print(part)
           
            if part.function_call:
                call_function(part.function_call, functions)
            if part.text:
                output_text = part.text.strip()
                write_to_doc(output_text, full_replace=True)  # Replace the entire document content with the command response
    except Exception as e:
       print("Failed to classify or process text:", str(e))


internal_update = False  # Flag to track whether the last update was done internally
previous_content = None
while True:
    current_content = get_doc_content()
    if current_content:
        if internal_update:
            # Reset the internal update flag and skip this cycle
            internal_update = False
            previous_content = current_content
            continue


        if previous_content is None:
            previous_content = current_content  # Initialize previous_content
        #    print(f"Document content at {time.strftime('%Y-%m-%d %H:%M:%S')}: {current_content}")


        if previous_content != current_content:
            detect_changes(previous_content, current_content)
            previous_content = current_content  # Update previous_content to the new current content

        if "End Gemini".lower() in current_content.lower():
            break
            
    time.sleep(7)
   
     # Modify as necessary for rate limits


