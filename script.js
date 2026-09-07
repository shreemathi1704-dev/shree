const imageUpload = document.getElementById("image-upload");
const uploadButton = document.getElementById("upload-button");
const uploadPreview = document.getElementById("upload-preview");
const uploadPreviewContainer =
    document.getElementById("upload-preview-container");
const uploadStatus = document.getElementById("upload-status");


// Preview selected image
imageUpload.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        uploadPreviewContainer.style.display = "none";
        return;
    }

    if (!file.type.startsWith("image/")) {
        uploadStatus.textContent = "Please select a valid image.";
        return;
    }

    const reader = new FileReader();

    reader.onload = function (event) {
        uploadPreview.src = event.target.result;
        uploadPreviewContainer.style.display = "block";
        uploadStatus.textContent = "Image selected. Click Analyze Image.";
    };

    reader.readAsDataURL(file);
});


// Upload and analyze image
uploadButton.addEventListener("click", async function () {

    const file = imageUpload.files[0];

    if (!file) {
        uploadStatus.textContent = "Please select an image first.";
        return;
    }

    uploadStatus.textContent = "🤖 AI is analyzing the image...";
    uploadButton.disabled = true;

    try {

        const formData = new FormData();

        formData.append("image", file);

        const response = await fetch("/api/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Prediction failed.");
        }

        // Display the result using your existing function
        displayResult(data);

        uploadStatus.textContent =
            "✅ Analysis completed successfully.";

        // Scroll to result
        document.getElementById("result-section")
            ?.scrollIntoView({
                behavior: "smooth"
            });

        // Refresh history
        if (typeof loadHistory === "function") {
            loadHistory();
        }

    } catch (error) {

        console.error(error);

        uploadStatus.textContent =
            "❌ " + error.message;

    } finally {

        uploadButton.disabled = false;
    }
});