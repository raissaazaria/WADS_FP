document.getElementById('signup-form').addEventListener('submit', function (event) {
    event.preventDefault();
  
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var address = document.getElementById('address').value;
  
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/users');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
      var response = JSON.parse(xhr.responseText);
      if (xhr.status === 200) {
        // Signup successful
        window.location.href = '/static/login.html';
      } else {
        // Signup failed
        document.getElementById('response-message').textContent = 'Signup failed. ' + response.detail;
      }
    };
    xhr.send(JSON.stringify({ email: email, password: password, address: address }));
  });
  