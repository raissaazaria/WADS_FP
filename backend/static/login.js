document.getElementById('login-form').addEventListener('submit', function (event) {
  event.preventDefault();

  var email = document.getElementById('email').value;
  var password = document.getElementById('password').value;

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/login');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function () {
    var response = JSON.parse(xhr.responseText);
    if (xhr.status === 200) {
      // Login successful
      window.location.href = '/static/dashboard.html';
    } else {
      // Login failed
      document.getElementById('response-message').textContent = 'Login failed. ' + response.detail;
    }
  };
  xhr.send(JSON.stringify({ email: email, password: password }));
});
