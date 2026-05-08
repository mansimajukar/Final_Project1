async function checkURL() {
    const url = document.getElementById("urlInput").value;

    const response = await fetch(
        "http://127.0.0.1:5000/predict",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        }
    );

    const data = await response.json();

    document.getElementById("result").innerHTML =
        `
        Prediction: ${data.prediction}<br>
        Risk Score: ${data.risk_score}%<br>
        URL: ${data.url}
        `;
}