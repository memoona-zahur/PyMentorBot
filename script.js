const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent form from submitting the default way
  
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        email: email, 
        password: password 
    }),
  })

    const result = await response.json();

    if (response.ok) {
      //alert("Login successful! Redirecting to PyMentorBot...");
      window.location.href = "file:///C:/Users/User/Downloads/login/static/lesson/index1.html"; // Redirect to PyMentorBot interface
     
    } else {
      alert(`Error: ${result.detail}`);
    }
  } catch (error) {
    console.error("Error logging in:", error);
    alert("An error occurred. Please try again later.");
  }
});

//<a href="http://127.0.0.1:8000/pymentorbot" target="_blank">Go to PyMentorBot</a>