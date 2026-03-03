// ===============================
// FORM SUBMISSION (AJAX)
// ===============================
document.getElementById("analyzeForm").addEventListener("submit", function(e) {
    e.preventDefault();

    let skillsInput = this.skills.value.trim();
    let resumeUploaded = this.resume.files.length;

    // Require at least one input (skills OR resume)
    if (!skillsInput && resumeUploaded === 0) {
        alert("Please enter skills OR upload a resume.");
        return;
    }

    let formData = new FormData(this);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
});


// ===============================
// DISPLAY RESULTS
// ===============================
function displayResults(data) {
    let container = document.getElementById("results");
    container.innerHTML = "";

    let labels = [];
    let scores = [];

    data.forEach(r => {
        labels.push(r.career);
        scores.push(r.confidence);

        container.innerHTML += `
            <div class="card">
                <h2>${r.career} — ${r.confidence}%</h2>
                <p><strong>Missing Skills:</strong> ${r.missing.length ? r.missing.join(", ") : "None 🎉"}</p>
                <p><strong>Roadmap:</strong></p>
                <ul>
                    ${r.roadmap.map(step => `<li>${step}</li>`).join("")}
                </ul>
            </div>
        `;
    });

    // Add Chart Canvas
    container.innerHTML += `<canvas id="chart" style="max-width:600px; margin:40px auto;"></canvas>`;

    renderChart(labels, scores);
}


// ===============================
// RENDER CHART
// ===============================
function renderChart(labels, scores) {
    const ctx = document.getElementById("chart").getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Confidence %",
                data: scores,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}


// ===============================
// DARK / LIGHT MODE TOGGLE
// ===============================
function toggleTheme() {
    document.body.classList.toggle("light-mode");

    // Save preference in browser
    if (document.body.classList.contains("light-mode")) {
        localStorage.setItem("theme", "light");
    } else {
        localStorage.setItem("theme", "dark");
    }
}


// ===============================
// LOAD SAVED THEME
// ===============================
window.onload = function() {
    let savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
    }
};
