function onOpen() {
  var ui = DocumentApp.getUi();
  ui.createMenu('Custom Tools')
    .addItem('big ball with gemini', 'editDocWithGemini')
    .addToUi();
}

function editDocWithGemini() {
  var doc = DocumentApp.getActiveDocument();
  var body = doc.getBody();
  var text = body.getText();

  var apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  var apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent";
  var url = apiUrl + "?key=" + apiKey;

  var requestBody = {
    "contents": [
      {
        "parts": [
          {
            "text": "Summarize and enhance the following content: " + text
          }
        ]
      }
    ]
  };

  var options = {
    "method": "POST",
    "contentType": "application/json",
    "payload": JSON.stringify(requestBody)
  };

  var response = UrlFetchApp.fetch(url, options);
  var data = JSON.parse(response.getContentText());
  var editedText = data.candidates[0].content.parts[0].text;

  // Clear the existing text and insert the edited text
  body.clear();
  body.appendParagraph(editedText);
}
