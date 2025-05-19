async function logout() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        console.error('No refresh token available');
        return;
    }

    const response = await fetch('http://127.0.0.1:8000/api/user/logout/', {
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
    } else {
        console.error('Logout failed');
    }
}