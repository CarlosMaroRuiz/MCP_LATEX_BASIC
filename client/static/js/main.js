document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('latexForm');
    const loading = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    const latexCode = document.getElementById('latexCode');
    const downloadBtn = document.getElementById('downloadBtn');
    const copyBtn = document.getElementById('copyBtn');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        loading.style.display = 'block';
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';

        const prompt = document.getElementById('prompt').value;

        fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        })
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.success) {
                latexCode.textContent = data.output;
                resultDiv.style.display = 'block';

                // Descargar archivo
                downloadBtn.onclick = function () {
                    const blob = new Blob([data.output], { type: 'text/x-tex' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'documento_latex.tex';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                };

                // Copiar al portapapeles
                copyBtn.onclick = function () {
                    navigator.clipboard.writeText(data.output);
                };
            } else {
                errorMessage.textContent = data.error || 'Error desconocido';
                errorDiv.style.display = 'block';
            }
        })
        .catch(err => {
            loading.style.display = 'none';
            errorMessage.textContent = 'Error en la petición: ' + err;
            errorDiv.style.display = 'block';
        });
    });
});