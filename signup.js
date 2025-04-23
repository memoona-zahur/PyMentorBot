document.getElementById("signupForm").addEventListener("submit", async (event) => {
  event.preventDefault(); // Prevent the default form submission

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/auth/signup/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        email,
        password,
      }),
    });

    if (response.ok) {
      const data = await response.json();
      alert("Sign up successful! You can now log in.");
      window.location.href = "file:///C:/Users/User/Downloads/login/static/index.html"; // Redirect to login page
    } else {
      const error = await response.json();
      alert(`Sign up failed: ${error.detail}`);
    }
  } catch (error) {
    console.error("Error during sign up:", error);
    alert("An error occurred. Please try again later.");
  }
});
