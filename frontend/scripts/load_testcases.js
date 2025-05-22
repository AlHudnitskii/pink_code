document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const problemId = document.getElementById('problemId').value;
    const fileInput = document.getElementById('fileInput').files[0];
    const formData = new FormData();
    formData.append('file', fileInput);
    formData.append('problem_id', problemId);

    const token = localStorage.getItem('accessToken');
    if (!token) {
        document.getElementById('uploadResult').innerHTML = `<div class="alert alert-danger">Error: Missing access token. Please log in.</div>`;
        return;
    }

    fetch(`http://localhost:8000/api/main/problem/${problemId}/load-testcases/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            const resultDiv = document.getElementById('uploadResult');
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else if (data.message === "Test cases uploaded successfully") {
            alert("Test case created successfully."); 
            window.location.href = `problem_details.html?id=${problemId}`; 
        } else {
            const resultDiv = document.getElementById('uploadResult');
            resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
        }
    })
    .catch(error => {
        document.getElementById('uploadResult').innerHTML = `<div class="alert alert-danger">Error uploading test cases: ${error.message}</div>`;
    });
});