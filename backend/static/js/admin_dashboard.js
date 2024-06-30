document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData();
        const fileInput = document.getElementById('file-input');
        formData.append('file', fileInput.files[0]);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                messageDiv.textContent = data.message || data.error;
                if (data.message) {
                    messageDiv.style.color = 'green';
                } else {
                    messageDiv.style.color = 'red';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageDiv.textContent = 'An error occurred during upload.';
                messageDiv.style.color = 'red';
            });
    });
});