document.getElementById('analyze').addEventListener('click', async () => {
    const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            urls: ["https://www.bbc.com/news", "https://www.bbc.com/sport"]
        })
    });

    if (response.ok) {
        const result = await response.json();
        document.getElementById('result').textContent = JSON.stringify(result);
    } else {
        document.getElementById('result').textContent = "Error: Unable to analyze content.";
    }
}); 