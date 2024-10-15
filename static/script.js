async function sendMessage() {
  const userMessage = document.getElementById("userMessage").value;
  if (userMessage.trim() === '') return;

  // Add user message to chat
  const chatBox = document.getElementById("chatBox");
  const userMessageElem = document.createElement('p');
  userMessageElem