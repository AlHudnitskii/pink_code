const token = localStorage.getItem('accessToken');
if (!token) {
   alert("You are not logged in. Please log in first.");
   window.location.href = "login.html";
}
const urlParams = new URLSearchParams(window.location.search);
const solutionId = urlParams.get('id');

fetch(`http://localhost:8000/api/u/solution/${solutionId}/`, {
   method: 'GET',
   headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json',
         'Accept': 'application/json'
   }
})
.then(response => response.json())
.then(data => {
   document.getElementById('problem-title').innerText = data.problem.title;
   document.getElementById('submission-status').innerText = data.passed ? 'Accepted' : 'Rejected';
   document.getElementById('submission-status').className = data.passed ? 'badge badge-success' : 'badge badge-danger';
   document.getElementById('runtime').innerText = data.lead_time;
   document.getElementById('memory').innerText = data.memory_used;
   document.getElementById('submitted-code').textContent = data.user_code;
})
.catch(error => {
   console.error('Error fetching solution detail:', error);
});