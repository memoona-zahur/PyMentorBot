document
  .getElementById("user-input")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      handleUserInput();
    }
  });

async function handleUserInput() {
  let userInput = document.getElementById("user-input").value.trim();
  if (!userInput) return;

  displayMessage(userInput, "user-message");
  document.getElementById("user-input").value = "";

  let botMessageElement = displayMessage("", "bot-message");

  try {
    let response = await fetch("http://127.0.0.1:8000/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userInput }),
    });

    let data = await response.json();
    let botResponse = formatResponse(data.response);

    streamResponse(botResponse, botMessageElement);
  } catch (error) {
    console.error("Error fetching response:", error);
    botMessageElement.textContent =
      "Error: Unable to get a response from the server.";
  }
}

function displayMessage(message, messageType) {
  const chatOutput = document.getElementById("chat-output");
  const messageElement = document.createElement("div");
  messageElement.className = "message " + messageType;
  messageElement.innerHTML = message;
  chatOutput.appendChild(messageElement);
  chatOutput.scrollTop = chatOutput.scrollHeight;
  return messageElement;
}

function streamResponse(text, element) {
  let words = text.split(" ");
  let index = 0;

  function addNextWord() {
    if (index < words.length) {
      element.innerHTML += words[index] + " ";
      index++;
      setTimeout(addNextWord, 50);
      element.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  }

  addNextWord();
}

function formatResponse(response) {
  response = response.replace(/\n/g, "<br>"); // Preserve new lines
  response = response.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>"); // Bold text

  // Format Python code blocks
  response = response.replace(
    /```python/g,
    '<pre><code class="language-python">'
  );
  response = response.replace(/```/g, "</code></pre>");

  return response;
}

function showLessons() {
  document.getElementById("quiz-section").style.display = "none";
  document.getElementById("lesson-section").style.display = "block";
}

function showQuiz() {
  document.getElementById("lesson-section").style.display = "none";
  document.getElementById("quiz-section").style.display = "block";
}
