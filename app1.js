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

  // Clear input box
  document.getElementById("user-input").value = "";

  const chatOutput = document.getElementById("chat-output");

  // ✅ Create a wrapper for one full message (user + bot)
  const wrapper = document.createElement("div");
  wrapper.className = "chat-pair";

  // ✅ Add user message
  const userMessage = document.createElement("div");
  userMessage.className = "message user-message";
  userMessage.textContent = userInput;
  wrapper.appendChild(userMessage);

  // ✅ Add placeholder for bot response
  const botMessage = document.createElement("div");
  botMessage.className = "message bot-message";
  botMessage.innerHTML = "Thinking...";
  wrapper.appendChild(botMessage);

  // ✅ Append the pair to chat output
  chatOutput.appendChild(wrapper);
  chatOutput.scrollTop = chatOutput.scrollHeight;

  try {
    let response = await fetch("http://127.0.0.1:8000/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: userInput }),
    });

    let data = await response.json();

    // Remove the placeholder
    wrapper.removeChild(botMessage);

    // Add full bot response with explanation and code
    displayCode(data.code, data.explanation, wrapper);
  } catch (error) {
    console.error("Error fetching response:", error);
    botMessage.textContent = "Error: Unable to get a response from the server.";
  }
}

function displayCode(code, explanation) {
  const chatOutput = document.getElementById("chat-output");

  // Format explanation
  const formattedExplanation = explanation
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n{2,}/g, "</p><p>")
    .replace(/\n/g, "<br>");

  // Only show code block if code is not empty
  let codeBlock = "";
  if (code.trim()) {
    codeBlock = `
      <div class="code-block">
        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
        <pre><code class="language-python">${code
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")}</code></pre>
      </div>
    `;
  }

  const html = `
    <div class="message bot-message">
      ${codeBlock}
      <div class="explanation">
        // <h3>Explanation:</h3>
        <p>${formattedExplanation}</p>
      </div>
    </div>
  `;

  chatOutput.innerHTML += html;
  hljs.highlightAll(); // re-highlight after injecting new code
}

function copyCode(button) {
  const codeBlock = button.nextElementSibling?.querySelector("code");
  const code = codeBlock?.innerText || "";
  navigator.clipboard.writeText(code).then(() => {
    button.textContent = "Copied!";
    setTimeout(() => {
      button.textContent = "Copy";
    }, 2000);
  });
}

function displayMessage(message, messageType) {
  const chatOutput = document.getElementById("chat-output");
  const messageElement = document.createElement("div");
  messageElement.className = "message " + messageType;
  messageElement.innerHTML = message;
  chatOutput.appendChild(messageElement);
  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function showLessons() {
  document.getElementById("quiz-section").style.display = "none";
  document.getElementById("lesson-section").style.display = "block";
}

function showQuiz() {
  document.getElementById("lesson-section").style.display = "none";
  document.getElementById("quiz-section").style.display = "block";
}

//
//
//
async function handleBotResponse(endpoint, questionText) {
  console.log(`${endpoint} called`);

  const chatOutput = document.getElementById("chat-output");
  const wrapper = document.createElement("div");
  wrapper.className = "chat-pair";

  const userMessage = document.createElement("div");
  userMessage.className = "message user-message";
  userMessage.textContent = questionText;
  wrapper.appendChild(userMessage);

  const botMessage = document.createElement("div");
  botMessage.className = "message bot-message";
  botMessage.textContent = "Loading...";
  wrapper.appendChild(botMessage);

  chatOutput.appendChild(wrapper);
  chatOutput.scrollTop = chatOutput.scrollHeight;

  try {
    const response = await fetch(`http://127.0.0.1:8000/${endpoint}`);
    if (!response.ok) throw new Error(`Server returned ${response.status}`);

    const data = await response.json();

    wrapper.removeChild(botMessage);
    displayCode(data.code, data.explanation, wrapper);
  } catch (error) {
    console.error(`Error fetching ${endpoint} response:`, error);
    botMessage.textContent = "Error: Unable to get a response from the server.";
  }
}

//
//
//
//
// For Variables and Data Types button
function getVariableDataTypes() {
  handleBotResponse(
    "getVariableDataTypes",
    "Tell me about Variables and Data Types in Python."
  );
}

// For Introducing List button
function Introducing_list() {
  handleBotResponse(
    "Introducing_list",
    "Tell me about introducing lists in Python."
  );
}

// for Working_with_Lists
async function Working_with_Lists() {
  handleBotResponse(
    "Working_with_Lists",
    "Tell me about working with list in Python."
  );
}

async function if_statements() {
  handleBotResponse("if_statements", "Tell me about if statements in Python.");
}

async function Dictionaries() {
  handleBotResponse("Dictionaries", "Tell me about Dictionaries in Python.");
}

async function User_Input_and_while_loops() {
  handleBotResponse(
    "User_Input_and_while_loops",
    "Tell me about User Input and while loops in python"
  );
}

async function Function1() {
  handleBotResponse("Function1", "Tell me about Function in python");
}

async function Classes() {
  handleBotResponse("Classes", "Tell me about Classes in Python");
}

async function File_and_Exception() {
  handleBotResponse(
    "File_and_Exception",
    "Tell me about File and Exception in Python"
  );
}
