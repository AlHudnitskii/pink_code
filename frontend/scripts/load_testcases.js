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
         const resultDiv = document.getElementById('uploadResult');
         if (data.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
         } else {
            resultDiv.innerHTML = `<div class="alert alert-success">Test cases uploaded successfully.</div>`;
         }
   })
   .catch(error => {
         document.getElementById('uploadResult').innerHTML = `<div class="alert alert-danger">Error uploading test cases: ${error.message}</div>`;
   });
});