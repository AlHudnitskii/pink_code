document.getElementById('register-form').addEventListener('submit', function(e) {
   e.preventDefault();
   const username = document.getElementById('username').value;
   const email = document.getElementById('email').value;
   const password = document.getElementById('password').value;

   fetch('http://localhost:8000/api/auth/register/', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify({ username, email, password }),
   })
   .then(response => response.json())
   .then(data => {
         console.log('Success:', data);
   })
   .catch((error) => {
         console.error('Error:', error);
   });
});