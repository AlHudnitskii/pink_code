document.addEventListener('DOMContentLoaded', function () {
fetch('http://localhost:8000/api/main/problems/')
      .then(response => response.json())
      .then(data => {
         const tbody = document.getElementById('problem-table-body');
         tbody.innerHTML = '';
         data.results.forEach(problem => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                  <td class="clickable" onclick="redirectToProblem(${problem.id})">${problem.id}. ${problem.title}</td>
                  <td class="clickable" onclick="redirectToProblem(${problem.id})">${problem.type}</td>
                  <td class="clickable" onclick="redirectToProblem(${problem.id})">${problem.difficulty}</td>
            `;
            tbody.appendChild(tr);
         });
      })
      .catch(error => console.error('Error fetching problems:', error));
});

function redirectToProblem(id) {
window.location.href = `problem_details.html?id=${id}`;
}