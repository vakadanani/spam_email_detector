function checkSpam() {
    const emailText = document.getElementById("emailText").value;
    const resultBox = document.getElementById("result");

    // Helper function to show a custom message box instead of alert()
    function showCustomMessage(message, isError = false) {
        resultBox.style.display = "block";
        if (isError) {
            resultBox.style.background = "#ffcccc";
            resultBox.style.color = "#cc0000";
            resultBox.innerText = message;
        } else {
            // Revert to hidden, as this is just a quick check for empty input
            resultBox.style.display = "none";
            // For a production app, you might use a dedicated modal/toast system
            console.warn(message);
        }
    }

    if (emailText.trim() === "") {
        // Use a console warning or a subtle display message instead of alert
        showCustomMessage("Please enter some text.", true);
        return;
    }

    // Show a temporary loading state
    resultBox.style.display = "block";
    resultBox.style.background = "#ffffcc";
    resultBox.style.color = "#333";
    resultBox.innerText = "⏳ Checking...";


    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: emailText })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        if (data.prediction === "spam") {
            resultBox.style.background = "#ffcccc";
            resultBox.style.color = "#cc0000";
            resultBox.innerText = "🚨 SPAM EMAIL!";
        } else {
            resultBox.style.background = "#ccffcc";
            resultBox.style.color = "#006600";
            resultBox.innerText = "✅ NOT SPAM";
        }
    })
    .catch(error => {
        console.error("Error connecting to server:", error);
        showCustomMessage("❌ Failed to connect to the backend server. Make sure 'server.py' is running.", true);
    });
}