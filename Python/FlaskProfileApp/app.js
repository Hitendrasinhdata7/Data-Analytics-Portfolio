document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // Basic client-side validation
  if (email === "" || password === "") {
    alert("Please fill in both fields.");
    return;
  }

  // Simulate successful login (you can replace this with actual backend validation)
  alert("Sign-in successful for: " + email);
  
  // Redirect to a different page upon successful login
  window.location.href = "home.html"; // Replace with actual redirect
});




