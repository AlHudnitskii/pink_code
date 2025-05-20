const token = localStorage.getItem('accessToken');
if (!token) {
   alert("You are not logged in. Please log in first.");
   window.location.href = "login.html";
}

document.getElementById('createProblemForm').addEventListener('submit', function(event) {
   event.preventDefault();

   const type = document.getElementById('type').value;
   const title = document.getElementById('title').value;
   const subtitle = document.getElementById('subtitle').value;
   const description = document.getElementById('description').value;
   const firstLine = document.getElementById('firstLine').value;
   const difficulty = document.getElementById('difficulty').value;

   const problemData = {
         type: type,
         title: title,
         subtitle: subtitle,
         description: description,
         fst_line: firstLine,
         difficulty: difficulty
   };

   fetch('http://localhost:8000/api/main/problem/', {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
         },
         body: JSON.stringify(problemData)
   })
   .then(response => response.json())
   .then(data => {
         if (data.id) {
            alert("Problem created successfully.");
            window.location.href = `problem_details.html?id=${data.id}`;
         } else {
            alert("Error creating problem: " + JSON.stringify(data));
         }
   })
   .catch(error => {
         console.error('Error creating problem:', error);
         alert('Error creating problem. Check console for details.');
   });
});