const urlParams = new URLSearchParams(window.location.search);
const problemId = urlParams.get('id');
const token = localStorage.getItem('accessToken');
const userId = 1; // add dinamic user solution

fetch(`http://localhost:8000/api/main/problem/${problemId}/`, {
   headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json'
   }
})
.then(response => response.json())
.then(data => {
   document.getElementById('problem-title').innerText = `${data.id}. ${data.title}`;
   document.getElementById('problem-subtitle').innerText = data.subtitle;
   document.getElementById('problem-description').innerText = data.description;
   document.getElementById('problem-difficulty').innerText = data.difficulty;
   document.getElementById('likes').innerText = data.rates.likes;
   document.getElementById('dislikes').innerText = data.rates.dislikes;
   document.getElementById('count-solutions').innerText = data.count_solutions;
})
.catch(error => console.error('Error fetching problem details:', error));

fetch(`http://localhost:8000/api/main/problem/${problemId}/testcases?not_full=true`, {
   headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json'
   }
})
.then(response => response.json())
.then(data => {
   const tbody = document.getElementById('testcase-table-body');
   tbody.innerHTML = '';
   data.forEach(testcase => {
         const tr = document.createElement('tr');
         tr.innerHTML = `
            <td>${testcase.input_data}</td>
            <td>${testcase.expected_output}</td>
         `;
         tbody.appendChild(tr);
   });
})
.catch(error => console.error('Error fetching test cases:', error));

const editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");

function formatJSON(obj) {
   const jsonStr = JSON.stringify(obj, null, 2);
   return jsonStr.replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/(\{|\}|\[|\])/g, match => `<span class="json-bracket">${match}</span>`)
         .replace(/("[^"]*")(\s*:\s*)/g, (match, p1, p2) => `<span class="json-key">${p1}</span>${p2}`)
         .replace(/:\s*(-?\d+\.?\d*e?[+-]?\d*|-?\d+\.?\d*|true|false|null)/g, match => `: <span class="json-value">${match.slice(2)}</span>`)
         .replace(/(\[)([^[]*?)(\])/g, (match, p1, p2, p3) => `${p1}<span class="json-array">${p2}</span>${p3}`);
}

function fetchTaskStatus(taskId, intervalId, saveResult) {
   fetch(`http://localhost:8000/api/interpreter/task-status/${taskId}/`, {
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         }
   })
   .then(response => response.json())
   .then(resultData => {
         console.log('Result Data:', resultData);
         if (resultData.state === 'SUCCESS') {
            clearInterval(intervalId);
            const formattedResult = formatJSON(resultData.result);
            document.getElementById('test-output').innerHTML = `<pre class="formatted-json">${formattedResult}</pre>`;
            if (saveResult && resultData.result.passed) { 
               saveSolution(resultData.result);
            }
         } else if (resultData.state === 'FAILURE' || resultData.state === 'REVOKED') {
            clearInterval(intervalId);
            document.getElementById('test-output').innerText = 'Error: ' + resultData.result;
         }
   })
   .catch(error => {
         clearInterval(intervalId);
         document.getElementById('test-output').innerText = 'Error fetching task status: ' + error.message;
         console.error('Error fetching task status:', error);
   });
}

function runCode(saveResult) {
   const code = editor.getValue();
   fetch(`http://localhost:8000/api/interpreter/run-code/${problemId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({ code: code })
   })
   .then(response => response.json())
   .then(data => {
         const taskId = data.task_id;
         console.log('Task ID:', taskId);
         const intervalId = setInterval(() => {
            fetchTaskStatus(taskId, intervalId, saveResult);
         }, 2000);
   })
   .catch(error => {
         document.getElementById('test-output').innerText = 'Error running code: ' + error.message;
         console.error('Error running code:', error);
   });
}
/*function submitCode(is_submit) {
   const userCode = editor.getValue();
   const problemId = parseInt(document.getElementById('problem-title').innerText.split('.')[0]);
   const token = localStorage.getItem('token'); 

   fetch(`http://localhost:8000/api/interpreter/submit-code/${problemId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({ code: userCode })
   })
   .then(response => {
         if (!response.ok) {
            throw new Error('Network response was not ok'); 
         }
         return response.json();
   })
   .then(data => {
         if (is_submit) {
            saveSolution(problemId, data);
         }
   })
   .catch(error => {
         console.error('Error submitting code:', error);
         alert('Error submitting code.');
   });
} */
function submitCode(saveResult) {
   const code = editor.getValue();
   fetch(`http://localhost:8000/api/interpreter/submit-code/${problemId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({ code: code })
   })
   .then(response => response.json())
   .then(data => {
         const taskId = data.task_id;
         console.log('Task ID:', taskId);
         const intervalId = setInterval(() => {
            fetchTaskStatus(taskId, intervalId, saveResult);
         }, 2000);
   })
   .catch(error => {
         document.getElementById('test-output').innerText = 'Error running code: ' + error.message;
         console.error('Error running code:', error);
   });
} 

/*function saveSolution(result) {
   const userId = localStorage.getItem('user_id'); 
   fetch('http://localhost:8000/api/interpreter/save-solution/', {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            problem: problemId,
            user: parseInt(userId),
            lead_time: parseInt(result.lead_time_total_milliseconds),
            memory_used: "20.04",
            user_code: editor.getValue(),
            passed: result.passed
         })
   })
   .then(response => {
         if (!response.ok) {
            throw new Error('Network response was not ok');
         }
         var alertElement = document.querySelector('.alert-popup');
         alertElement.style.display = 'block';

         setTimeout(function() {
            $(alertElement).alert('close');
         }, 5000);
         return response.text();
   })
   .then(saveData => {
         if (saveData) {
            console.log('Save Data:', JSON.parse(saveData));
         } else {
            console.log('Save Data: No content');
         }
   })
   .catch(error => console.error('Error saving solution:', error));
} */

function saveSolution(result) {
   const problemId = parseInt(document.getElementById('problem-title').innerText.split('.')[0]);
   //const token = localStorage.getItem('token');
   fetch(`http://localhost:8000/api/interpreter/save-solution//${problemId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         },
         body: JSON.stringify({
            problem: problemId,
            lead_time: parseInt(result.lead_time_total_milliseconds),
            memory_used: "20.04",
            user_code: editor.getValue(),
            passed: result.passed
         })
   })
   .then(response => {
         if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
         }
         var alertElement = document.querySelector('.alert-popup');
         alertElement.style.display = 'block';

         setTimeout(function() {
            $(alertElement).alert('close');
         }, 5000);
         return response.text();
   })
   .then(saveData => {
         if (saveData) {
            console.log('Save Data:', JSON.parse(saveData));
         } else {
            console.log('Save Data: No content');
         }
   })
   .catch(error => console.error('Error saving solution:', error));
}

function showAlert(message) {
   const alertDiv = document.querySelector('.alert-popup');
   if (alertDiv) {
         alertDiv.querySelector('strong').textContent = message;
         alertDiv.style.display = 'block';
         setTimeout(() => {
            alertDiv.style.display = 'none';
         }, 3000); 
   }
}

function disableButtons() {
   const likeBtn = document.getElementById('like-btn');
   const dislikeBtn = document.getElementById('dislike-btn');
   likeBtn.classList.add('disabled');
   dislikeBtn.classList.add('disabled');
   likeBtn.style.pointerEvents = 'none';
   dislikeBtn.style.pointerEvents = 'none';
}

function likeProblem() {
   fetch(`http://localhost:8000/api/main/problem/${problemId}/like/${userId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         }
   })
   .then(response => {
         if (response.ok) {
            document.getElementById('likes').innerText = parseInt(document.getElementById('likes').innerText) + 1;
            disableButtons();
         } else {
            alert('Error liking the problem.');
         }
   })
   .catch(error => console.error('Error liking problem:', error));
}

function dislikeProblem() {
   fetch(`http://localhost:8000/api/main/problem/${problemId}/dislike/${userId}/`, {
         method: 'POST',
         headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
         }
   })
   .then(response => {
         if (response.ok) {
            document.getElementById('dislikes').innerText = parseInt(document.getElementById('dislikes').innerText) + 1;
            disableButtons();
         } else {
            alert('Error disliking the problem.');
         }
   })
   .catch(error => console.error('Error disliking problem:', error));
}

document.getElementById('run-code').addEventListener('click', () => runCode(false));
document.getElementById('submit-code').addEventListener('click', () => submitCode(true));
document.getElementById('like-btn').addEventListener('click', likeProblem);
document.getElementById('dislike-btn').addEventListener('click', dislikeProblem);
