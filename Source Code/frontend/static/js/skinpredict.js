const imageInput = document.getElementById("imageInput");
const predictBtn = document.getElementById("predictBtn");
const resultsGrid = document.getElementById("results");

let files = [];
let previews = [];
let loading = false;

/* ===============================
   HANDLE IMAGE SELECTION
=============================== */
imageInput.addEventListener("change", function (e) {
    files = Array.from(e.target.files);
    previews = files.map(file => URL.createObjectURL(file));
    resultsGrid.innerHTML = "";
});

/* ===============================
   HANDLE PREDICT
=============================== */
predictBtn.addEventListener("click", async function () {
    if (!files.length || loading) {
        alert("Please select image(s) first.");
        return;
    }

    const formData = new FormData();
    files.forEach(file => formData.append("images", file));

    loading = true;
    predictBtn.innerText = "Analyzing...";
    predictBtn.disabled = true;

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const enriched = (data.results || []).map(r => ({
            ...r,
            preview: previews[r.index]
        }));

        displayResults(enriched);

    } catch (error) {
        alert("Prediction failed. Check backend.");
        console.error(error);
    }

    loading = false;
    predictBtn.innerText = "Predict";
    predictBtn.disabled = false;
});

/* ===============================
   DISPLAY RESULTS
=============================== */
function displayResults(results) {
    resultsGrid.innerHTML = "";

    results.forEach(r => {
        const card = document.createElement("div");
        card.className = "result-card";

        let html = "";

        if (r.preview) {
            html += `<img src="${r.preview}" class="result-image">`;
        }

        html += `<h3>${r.filename}</h3>`;

        if (r.rejected) {
            html += `<p class="error">❌ Rejected: ${r.reason}</p>`;
        } else {
            html += `<h4>CNN Results</h4>`;

            for (const model in r.cnn_results) {
                const d = r.cnn_results[model];

                html += `
                    <div class="result-row">
                        <span><b>${model}</b>: ${d.class_code}</span>
                        <span class="score">${d.confidence}%</span>
                    </div>
                `;
            }
        }

        card.innerHTML = html;
        resultsGrid.appendChild(card);
    });
}
