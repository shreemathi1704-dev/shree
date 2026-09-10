/*
==================================================
 AGRIGUARD AI
 FRONTEND JAVASCRIPT
==================================================
*/

/*
 IMPORTANT:

 FOR LOCAL TESTING:
 http://127.0.0.1:5000

 AFTER DEPLOYING BACKEND:
 change this to your Render backend URL.

 Example:

 const BACKEND_URL =
 "https://agriguard-ai-api.onrender.com";
*/

const BACKEND_URL =
    "http://127.0.0.1:5000";


let stream = null;

let facingMode = "environment";

let selectedFile = null;

let coordinates = {
    latitude: null,
    longitude: null
};


/* SHORTCUT */

function $(id) {

    return document.getElementById(id);

}


/*
==================================================
 PAGE LOAD
==================================================
*/

window.addEventListener(
    "load",
    function () {

        checkBackend();

        getGPS();

    }
);


/*
==================================================
 CHECK BACKEND
==================================================
*/

async function checkBackend() {

    try {

        const response =
            await fetch(
                `${BACKEND_URL}/health`,
                {
                    cache: "no-store"
                }
            );


        const data =
            await response.json();


        if (response.ok) {

            $("backendStatus").innerHTML =
                `
                <span
                    style="
                    background:#22a447;
                    ">
                </span>

                AI Service Online
                `;

        } else {

            showBackendOffline();

        }

    }

    catch (error) {

        console.log(
            "Backend not connected:",
            error
        );

        showBackendOffline();

    }

}


/*
==================================================
 BACKEND OFFLINE MESSAGE
==================================================
*/

function showBackendOffline() {

    $("backendStatus").innerHTML =
        `
        <span
            style="
            background:#e39b00;
            ">
        </span>

        Start Backend
        `;

}


/*
==================================================
 START CAMERA
==================================================
*/

async function startCamera() {

    if (
        !navigator.mediaDevices ||
        !navigator.mediaDevices.getUserMedia
    ) {

        $("cameraMessage").innerHTML =
            `
            <strong>
                ⚠️ Camera unavailable
            </strong>

            <span>
                Use Chrome or Edge with HTTPS.
            </span>
            `;

        return;

    }


    try {

        stopCamera();


        stream =
            await navigator.mediaDevices.getUserMedia({

                video: {

                    facingMode: {
                        ideal: facingMode
                    },

                    width: {
                        ideal: 1280
                    },

                    height: {
                        ideal: 720
                    }

                },

                audio: false

            });


        $("video").srcObject =
            stream;


        $("video").style.display =
            "block";


        $("captured").style.display =
            "none";


        $("cameraMessage").style.display =
            "none";


        $("startBtn").textContent =
            "✓ Camera Running";

    }

    catch (error) {

        console.error(error);


        $("cameraMessage").innerHTML =
            `
            <strong>
                📷 Camera permission required
            </strong>

            <span>
                Click Allow when the browser asks.
            </span>
            `;


        $("cameraMessage").style.display =
            "flex";


        $("startBtn").textContent =
            "▶ Start Camera";

    }

}


/*
==================================================
 STOP CAMERA
==================================================
*/

function stopCamera() {

    if (stream) {

        stream
            .getTracks()
            .forEach(
                track =>
                    track.stop()
            );

        stream = null;

    }


    if ($("startBtn")) {

        $("startBtn").textContent =
            "▶ Start Camera";

    }

}


/*
==================================================
 SWITCH CAMERA
==================================================
*/

async function switchCamera() {

    if (
        facingMode ===
        "environment"
    ) {

        facingMode =
            "user";

    }

    else {

        facingMode =
            "environment";

    }


    await startCamera();

}


/*
==================================================
 CAPTURE PHOTO
==================================================
*/

function capturePhoto() {

    const video =
        $("video");


    if (!video.videoWidth) {

        alert(
            "Please start the camera first."
        );

        return;

    }


    const canvas =
        document.createElement(
            "canvas"
        );


    canvas.width =
        video.videoWidth;


    canvas.height =
        video.videoHeight;


    const context =
        canvas.getContext(
            "2d"
        );


    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );


    canvas.toBlob(

        function (blob) {

            selectedFile =
                new File(
                    [blob],
                    "crop-camera.jpg",
                    {
                        type:
                            "image/jpeg"
                    }
                );


            showPreview(
                selectedFile
            );

        },

        "image/jpeg",

        0.92

    );

}


/*
==================================================
 UPLOAD IMAGE
==================================================
*/

$("upload").addEventListener(
    "change",
    function (event) {

        const file =
            event.target.files[0];


        if (!file) {

            return;

        }


        if (
            !file.type.startsWith(
                "image/"
            )
        ) {

            alert(
                "Please select an image."
            );

            return;

        }


        selectedFile =
            file;


        showPreview(
            file
        );

    }
);


/*
==================================================
 SHOW PREVIEW
==================================================
*/

function showPreview(file) {

    const url =
        URL.createObjectURL(
            file
        );


    $("preview").src =
        url;


    $("previewCard")
        .classList
        .remove(
            "hidden"
        );


    getGPS();


    $("previewCard")
        .scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

}


/*
==================================================
 GET GPS
==================================================
*/

function getGPS() {

    if (
        !navigator.geolocation
    ) {

        $("gpsLine").textContent =
            "📍 GPS not supported.";

        return;

    }


    $("gpsLine").textContent =
        "📍 Getting GPS location...";


    navigator.geolocation.getCurrentPosition(

        function (position) {

            coordinates.latitude =
                position.coords.latitude;


            coordinates.longitude =
                position.coords.longitude;


            $("gpsLine").textContent =
                `📍 GPS Ready:
                ${coordinates.latitude.toFixed(6)},
                ${coordinates.longitude.toFixed(6)}`;

        },


        function (error) {

            console.log(
                "GPS error:",
                error.message
            );


            $("gpsLine").textContent =
                "📍 GPS permission denied. Satellite analysis unavailable.";

        },


        {

            enableHighAccuracy:
                true,

            timeout:
                15000,

            maximumAge:
                0

        }

    );

}


/*
==================================================
 ANALYZE CROP
==================================================
*/

async function analyzeCrop() {

    if (!selectedFile) {

        alert(
            "Please capture or upload a crop image first."
        );

        return;

    }


    $("loading")
        .classList
        .remove(
            "hidden"
        );


    $("result")
        .classList
        .add(
            "hidden"
        );


    $("loadingTitle").textContent =
        "Connecting to AI + Sentinel-2...";


    try {

        const formData =
            new FormData();


        formData.append(
            "image",
            selectedFile
        );


        if (
            coordinates.latitude !== null
        ) {

            formData.append(
                "latitude",
                coordinates.latitude
            );

        }


        if (
            coordinates.longitude !== null
        ) {

            formData.append(
                "longitude",
                coordinates.longitude
            );

        }


        const response =
            await fetch(
                `${BACKEND_URL}/analyze`,
                {

                    method:
                        "POST",

                    body:
                        formData

                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Analysis failed."
            );

        }


        displayResult(
            data
        );

    }

    catch (error) {

        console.error(
            error
        );


        alert(
            "Backend connection failed.\n\n" +
            "Check that Flask is running and " +
            "BACKEND_URL is correct.\n\n" +
            error.message
        );

    }

    finally {

        $("loading")
            .classList
            .add(
                "hidden"
            );

    }

}


/*
==================================================
 DISPLAY RESULT
==================================================
*/

function displayResult(data) {

    const ai =
        data.crop_disease || {};


    const satellite =
        data.satellite || {};


    $("disease").textContent =
        ai.disease ||
        "Model unavailable";


    $("mode").textContent =
        `Prediction mode:
        ${ai.prediction_mode || "AI"}`;


    $("severity").textContent =
        ai.severity ||
        "Unknown";


    $("confidence").textContent =
        ai.confidence !== undefined
            ? `${ai.confidence}%`
            : "—";


    $("ndvi").textContent =
        satellite.ndvi !== undefined
            ? satellite.ndvi
            : "—";


    $("fieldCondition").textContent =
        satellite.field_condition ||
        "—";


    $("description").textContent =
        ai.description ||
        "—";


    $("recommendation").textContent =
        ai.recommendation ||
        "—";


    $("satelliteSource").textContent =
        satellite.message ||
        "Sentinel-2 analysis";


    $("satStatus").textContent =
        satellite.success
            ? "Connected"
            : "Unavailable";


    if (
        satellite.success
    ) {

        $("satStatus").style.background =
            "#e4f5e7";

        $("satStatus").style.color =
            "#237337";

    }

    else {

        $("satStatus").style.background =
            "#fff0df";

        $("satStatus").style.color =
            "#8a5b15";

    }


    $("lat").textContent =
        satellite.latitude !== undefined
            ? Number(
                satellite.latitude
            ).toFixed(6)
            : "—";


    $("lon").textContent =
        satellite.longitude !== undefined
            ? Number(
                satellite.longitude
            ).toFixed(6)
            : "—";


    $("images").textContent =
        satellite.images_found !== undefined
            ? satellite.images_found
            : "—";


    $("vegetation").textContent =
        satellite.field_status ||
        "—";


    $("result")
        .classList
        .remove(
            "hidden"
        );


    $("result")
        .scrollIntoView({
            behavior: "smooth"
        });

}


/*
==================================================
 RESET
==================================================
*/

function resetAll() {

    selectedFile =
        null;


    $("upload").value =
        "";


    $("previewCard")
        .classList
        .add(
            "hidden"
        );


    $("result")
        .classList
        .add(
            "hidden"
        );


    startCamera();


    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}