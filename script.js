let cameraStream = null;
let selectedImage = null;

const camera = document.getElementById("camera");
const preview = document.getElementById("preview");
const imageInput = document.getElementById("imageInput");


// START CAMERA
async function startCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: { ideal: "environment" }
            },
            audio: false
        });

        if (camera) {
            camera.srcObject = cameraStream;
            camera.style.display = "block";
        }

        if (preview) {
            preview.style.display = "none";
        }

        const status = document.getElementById("status");
        if (status) {
            status.innerText = "Camera started. Place the crop leaf inside the frame.";
        }

    } catch (error) {
        alert("Camera permission denied or camera is unavailable.");
        console.log(error);
    }
}


// STOP CAMERA
function stopCamera() {

    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    if (camera) {
        camera.style.display = "none";
    }

    const status = document.getElementById("status");

    if (status) {
        status.innerText = "Camera stopped.";
    }
}


// IMAGE UPLOAD
if (imageInput) {

    imageInput.addEventListener("change", function(event) {

        const file = event.target.files[0];

        if (!file) return;

        selectedImage = file;

        const url = URL.createObjectURL(file);

        if (preview) {
            preview.src = url;
            preview.style.display = "block";
        }

        if (camera) {
            camera.style.display = "none";
        }

        const status = document.getElementById("status");

        if (status) {
            status.innerText = "Image selected. Click Analyze.";
        }
    });
}


// CAPTURE CAMERA IMAGE
function captureImage() {

    if (!cameraStream) {
        alert("Please start the camera first.");
        return;
    }

    const canvas = document.createElement("canvas");

    canvas.width = camera.videoWidth;
    canvas.height = camera.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(
        camera,
        0,
        0,
        canvas.width,
        canvas.height
    );

    canvas.toBlob(function(blob) {

        selectedImage = new File(
            [blob],
            "crop.jpg",
            {
                type: "image/jpeg"
            }
        );

        if (preview) {
            preview.src = URL.createObjectURL(blob);
            preview.style.display = "block";
        }

        if (camera) {
            camera.style.display = "none";
        }

        const status = document.getElementById("status");

        if (status) {
            status.innerText = "Crop image captured successfully.";
        }

    }, "image/jpeg");
}


// ANALYZE CROP
function analyzeCrop() {

    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const status = document.getElementById("status");

    if (loading) {
        loading.style.display = "block";
    }

    if (result) {
        result.style.display = "none";
    }

    if (status) {
        status.innerText = "Analyzing crop...";
    }


    // DEMO AI PROCESSING
    setTimeout(function() {

        if (loading) {
            loading.style.display = "none";
        }

        if (result) {
            result.style.display = "block";

            result.innerHTML = `

                <div class="result-card">

                    <h2>🌿 AI Crop Analysis Result</h2>

                    <div class="result-row">
                        <span>🌱 Crop</span>
                        <strong>Tomato</strong>
                    </div>

                    <div class="result-row">
                        <span>🦠 Disease</span>
                        <strong>Tomato Early Blight</strong>
                    </div>

                    <div class="result-row">
                        <span>🎯 Confidence</span>
                        <strong>94.5%</strong>
                    </div>

                    <div class="result-row">
                        <span>⚠️ Severity</span>
                        <strong>Moderate</strong>
                    </div>

                    <h3>🔍 Description</h3>

                    <p>
                        Possible Tomato Early Blight
                        symptoms detected in the crop leaf.
                    </p>

                    <h3>💊 Recommended Action</h3>

                    <div class="recommendation">

                        Remove severely affected leaves.
                        Maintain good field sanitation.
                        Avoid unnecessary overhead watering.
                        Monitor the crop regularly.

                    </div>

                    <h2 style="margin-top:30px;">
                        🛰️ Sentinel-2 Satellite Analysis
                    </h2>

                    <div class="ndvi">
                        0.65
                    </div>

                    <p style="text-align:center;">
                        NDVI Value
                    </p>

                    <div class="result-row">
                        <span>🛰️ Satellite</span>
                        <strong>Sentinel-2</strong>
                    </div>

                    <div class="result-row">
                        <span>🌾 Field Condition</span>
                        <strong>Healthy</strong>
                    </div>

                    <div class="result-row">
                        <span>📍 Location</span>
                        <strong>GPS Ready</strong>
                    </div>

                    <div class="recommendation">

                        ✅ Crop analysis completed<br>
                        ✅ Disease identified<br>
                        ✅ Field condition checked<br>
                        ✅ Recommended action generated

                    </div>

                </div>
            `;
        }

        if (status) {
            status.innerText =
                "Analysis completed successfully!";
        }

    }, 2000);
}