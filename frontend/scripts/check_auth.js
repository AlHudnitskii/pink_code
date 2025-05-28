if (localStorage.getItem('access') === null || localStorage.getItem('access') === NaN) {
    var authPages = document.getElementById("authPages")
    authPages.className = "hidden"
}

document.addEventListener('DOMContentLoaded', function() {
  const profileLink = document.querySelector('#authPages a[href="profile.html"]'); // Или другой селектор
  if (profileLink) {
    if (window.location.pathname === '/profile.html') {
      profileLink.style.display = 'none'; // Скрыть элемент
    } else {
      profileLink.style.display = ''; // Показать элемент (или 'block', 'inline-block' в зависимости от стиля)
    }
  }
});

// Вам также может понадобиться обновлять это при изменении URL (например, при навигации без перезагрузки страницы)
window.addEventListener('popstate', function() {
  // Повторно проверьте и измените видимость элемента
  const profileLink = document.querySelector('#authPages a[href="profile.html"]');
  if (profileLink) {
    profileLink.style.display = (window.location.pathname === '/profile.html') ? 'none' : '';
  }
});