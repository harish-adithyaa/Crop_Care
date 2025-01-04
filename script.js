document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');

    // Handle drag over event
    dropZone.addEventListener('dragover', function(event) {
        event.preventDefault();
        dropZone.classList.add('drag-over');
    });

    // Handle drag leave event
    dropZone.addEventListener('dragleave', function(event) {
        event.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    // Handle drop event
    dropZone.addEventListener('drop', async function(event) {
        event.preventDefault();
        dropZone.classList.remove('drag-over');

        const file = event.dataTransfer.files[0];
        handleFileUpload(file);
    });

    // Handle file input change event
    document.getElementById('file-input').addEventListener('change', function(event) {
        const file = event.target.files[0];
        handleFileUpload(file);
    });

    // Function to handle file upload
    async function handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                if (result.error) {
                    document.getElementById('result').innerText = `Error: ${result.error}`;
                } else {
                    document.getElementById('result').innerText = `Disease: ${result.disease}`;
                }
            } else {
                const errorText = await response.text();
                document.getElementById('result').innerText = `Error: ${errorText}`;
            }
        } catch (error) {
            document.getElementById('result').innerText = `Error: ${error.message}`;
        }
    }
});
