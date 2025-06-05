const token = localStorage.getItem('accessToken');
if (!token) {
   alert("You are not logged in. Please log in first.");
   window.location.href = "login.html";
}

fetch('http://localhost:8000/api/users/profile/', {
   method: 'GET',
   headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json',
         'Accept': 'application/json'
   }
})
.then(response => response.json())
.then(data => {
   document.getElementById('username').innerText = data.username;
   document.getElementById('rank').innerText = `Rank: ${data.rank}`;
   document.getElementById('was_complited_problems').innerText = data.was_complited_problems;

   const solvedProblemsTable = document.getElementById('solved_problems_table');
   solvedProblemsTable.innerHTML = '';
   data.solved_problems.forEach(problem => {
         const row = document.createElement('tr');
         row.innerHTML = `
            <td><a href="solution.html?id=${problem.id}" class="text-white">${problem.problem.id}. ${problem.problem.title}</a></td>
            <td>Python</td>
            <td>${problem.passed ? 'Yes' : 'No'}</td>
            <td>${new Date(problem.executed_at).toLocaleDateString()}</td>
         `;
         solvedProblemsTable.appendChild(row);
   });
})
.catch(error => {
   console.error('Error fetching user profile:', error);
});

document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
       logoutButton.addEventListener('click', function() {
            console.log('Logout button clicked'); 
            logout();
        });
    }
});

async function logout() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.error('No refresh token available');
        return;
    }

    const response = await fetch('http://127.0.0.1:8000/api/auth/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        },
        body: JSON.stringify({ refresh: refreshToken })
    });

    if (response.ok) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        console.log('Logged out successfully');
        window.location.href = 'login.html'; 
    } else {
        console.error('Logout failed');
    }
}