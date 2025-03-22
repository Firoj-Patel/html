document.addEventListener('DOMContentLoaded', () => {
    const apiList = document.getElementById('apiList');
    const versionData = document.getElementById('versionData');
    const addApiForm = document.getElementById('addApiForm');
    const versionForm = document.getElementById('versionForm');

    function fetchApis() {
        apiList.innerHTML = '<li>Mock API 1</li><li>Mock API 2</li>';
    }

    function fetchVersionData(apiUrl, version) {
        fetch(`/api/version/${encodeURIComponent(apiUrl)}/${version}`)
            .then(response => response.json())
            .then(data => {
                versionData.innerHTML = JSON.stringify(data, null, 2);
            })
            .catch(error => {
                versionData.innerHTML = `Error: ${error}`;
            });
    }

    addApiForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const apiUrl = document.getElementById('apiUrl').value;
        const interval = document.getElementById('interval').value;
        fetch('/api/apis', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_url: apiUrl, interval: parseInt(interval) }),
        }).then(() => fetchApis());
    });

    versionForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const apiUrl = document.getElementById('versionApiUrl').value;
        const version = document.getElementById('version').value;
        fetchVersionData(apiUrl, version);
    });

    fetchApis();
});
