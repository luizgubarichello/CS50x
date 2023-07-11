document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault();
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var message = document.getElementById("message").value;
    
    // Perform validation and send the form data to the server
    // You can customize this part according to your needs
    if (name && email && message) {
      alert("Message sent successfully!");
      document.getElementById("contact-form").reset();
    } else {
      alert("Please fill in all fields.");
    }
  });
  