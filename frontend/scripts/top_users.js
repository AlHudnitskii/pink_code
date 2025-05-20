const apiUrl = 'http://localhost:8000/api/u/top-users/';
let currentPage = 1;
let pageSize = 10;
const token = localStorage.getItem('accessToken');

document.addEventListener('DOMContentLoaded', function () {
      loadUsers(currentPage);

      document.getElementById('pagination').addEventListener('click', function (e) {
         if (e.target.tagName === 'A') {
            e.preventDefault();
            const page = parseInt(e.target.getAttribute('data-page'));
            if (!isNaN(page)) {
                  currentPage = page;
                  loadUsers(currentPage);
            }
         }
      });
});

function loadUsers(page) {
      fetch(`${apiUrl}?page=${page}&page_size=${pageSize}`, {
         headers: {
            'Authorization': `Bearer ${token}`
         }
      })
         .then(response => response.json())
         .then(data => {
            const tbody = document.getElementById('user-table-body');
            tbody.innerHTML = '';
            data.results.forEach(user => {
                  const tr = document.createElement('tr');
                  tr.innerHTML = `
                     <td>${user.position}</td>
                     <td>${user.username}</td>
                     <td>${user.solved_problems}</td>
                  `;
                  tbody.appendChild(tr);
            });
            updatePagination(data);
         })
         .catch(error => console.error('Error fetching users:', error));
}

function updatePagination(data) {
      const pagination = document.getElementById('pagination');
      pagination.innerHTML = '';

      if (data.previous) {
         const prevPage = document.createElement('li');
         prevPage.className = 'page-item';
         prevPage.innerHTML = `<a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>`;
         pagination.appendChild(prevPage);
      }

      for (let i = 1; i <= data.total_pages; i++) {
         const pageItem = document.createElement('li');
         pageItem.className = 'page-item' + (i === currentPage ? ' active' : '');
         pageItem.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
         pagination.appendChild(pageItem);
      }

      if (data.next) {
         const nextPage = document.createElement('li');
         nextPage.className = 'page-item';
         nextPage.innerHTML = `<a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>`;
         pagination.appendChild(nextPage);
      }
}