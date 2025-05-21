document.addEventListener('DOMContentLoaded', function () {
      fetchProblems();

      document.getElementById('searchButton').addEventListener('click', filterAndRenderProblems);
      document.getElementById('searchInput').addEventListener('input', filterAndRenderProblems);
      document.getElementById('typeFilter').addEventListener('change', filterAndRenderProblems);
      document.getElementById('difficultySort').addEventListener('change', filterAndRenderProblems);
});

let allProblems = [];

function fetchProblems() {
fetch('http://localhost:8000/api/main/problems/')
      .then(response => response.json())
      .then(data => {
            allProblems = data.results;
            renderProblems(allProblems);
      })
      .catch(error => console.error('Error fetching problems:', error));
}

function renderProblems(problems) {
      const tbody = document.getElementById('problem-table-body');
      tbody.innerHTML = '';
      if (!problems || problems.length === 0) {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td colspan="3" class="text-center">No problems found</td>`;
            tbody.appendChild(tr);
            return;
      }
      problems.forEach(problem => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                  <td class="clickable" onclick="redirectToProblem(${problem.id})">${problem.id}. ${problem.title}</td>
                  <td class="clickable">${problem.type}</td>
                  <td class="clickable">${problem.difficulty}</td>
            `;
            tbody.appendChild(tr);
      });
}

function filterAndRenderProblems() {
      const searchTerm = document.getElementById('searchInput').value.toLowerCase();
      const typeFilter = document.getElementById('typeFilter').value;
      const difficultySort = document.getElementById('difficultySort').value;

      let filteredProblems = [...allProblems]; 

      if (searchTerm) {
            filteredProblems = filteredProblems.filter(problem =>
                  problem.title.toLowerCase().includes(searchTerm)
            );
      }

      if (typeFilter !== 'all') {
            filteredProblems = filteredProblems.filter(problem =>
                  problem.type.toLowerCase() === typeFilter.toLowerCase()
            );
      }

      if (difficultySort === 'easy') {
            filteredProblems.sort((a, b) => {
                  const order = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
                  return order[a.difficulty] - order[b.difficulty];
            });
      } else if (difficultySort === 'hard') {
            filteredProblems.sort((a, b) => {
                  const order = { 'Easy': 1, 'Medium': 2, 'Hard': 3 };
                  return order[b.difficulty] - order[a.difficulty];
            });
      }

      renderProblems(filteredProblems);
}

function redirectToProblem(id) {
      window.location.href = `problem_details.html?id=${id}`;
}