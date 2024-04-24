var DOC_ID = '';  // Replace 'xxx' with your actual Google Doc ID
function doGet() {
  var document = DocumentApp.openById(DOC_ID);
  var text = document.getBody().getText();
  return ContentService.createTextOutput(text).setMimeType(ContentService.MimeType.TEXT);
}
function doPost(e) {
  var lock = LockService.getScriptLock();
  if (lock.tryLock(30000)) {
    try {
      var doc = DocumentApp.openById(DOC_ID);
      var body = doc.getBody();
      body.clear();
      body.appendParagraph(e.parameter.text);

       if (e.parameter.font_size) {
        var fontSize = parseInt(e.parameter.font_size);
        body.setFontSize(fontSize);
      }
      
      // Apply font style if provided
      if (e.parameter.font_style) {
        var fontStyle = e.parameter.font_style.toLowerCase();
        body.setBold(fontStyle.includes('bold'));
        body.setItalic(fontStyle.includes('italic'));
        body.setUnderline(fontStyle.includes('underline'));
      }
      
      // Apply font color if provided
      if (e.parameter.font_color) {
        var fontColor = e.parameter.font_color;
        body.setForegroundColor(fontColor);
      }

      if (e.parameter.font_family){
        var fontFam = e.parameter.font_family;
        body.setFontFamily(fontFamilyName=fontFam);
      }
      doc.saveAndClose();
      return ContentService.createTextOutput("Write successful").setMimeType(ContentService.MimeType.TEXT);
    } finally {
      lock.releaseLock();
    }
  } else {
    return ContentService.createTextOutput("Failed to get lock, try again.").setMimeType(ContentService.MimeType.TEXT);
  }
}


