const token = localStorage.getItem('accessToken');
if (!token) {
   alert("You are not logged in. Please log in first.");
   window.location.href = "login.html";
}

document.getElementById('createTestCaseForm').addEventListener('submit', function(event) {
   event.preventDefault();

   const problemId = document.getElementById('problemId').value;
   const inputData = document.getElementById('inputData').value;
   const expectedOutput = document.getElementById('expectedOutput').value;
   const testCaseData = {
         problem: problemId,
         input_data: inputData,
         expected_output: expectedOutput
   };

   fetch(`http://localhost:8000/api/main/problem/${problemId}/testcase/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
         },
         body: JSON.stringify(testCaseData)
   })
   .then(response => {
         if (!response.ok) {
            return response.json().then(errorData => {
               throw new Error(JSON.stringify(errorData));
            });
         }
         return response.json();
   })
   .then(data => {
         alert("Test case created successfully.");
         window.location.href = `problem_details.html?id=${data.problem}`;
   })
   .catch(error => {
         console.error('Error creating test case:', error);
         alert('Error creating test case: ' + error.message);
   });
});