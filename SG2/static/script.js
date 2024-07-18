// scripts.js

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerHTML = 'Optimal Route: ' + data.route.join(', ');
        })
        .catch(error => {
            document.getElementById('result').innerHTML = 'Error: ' + error;
        });
    } else {
        document.getElementById('result').innerHTML = 'Please upload a file.';
    }
});
