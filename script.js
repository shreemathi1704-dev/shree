const camera =
    document.getElementById("camera");

const canvas =
    document.getElementById("canvas");

const startButton =
    document.getElementById("start-camera");

const stopButton =
    document.getElementById("stop-camera");

const switchButton =
    document.getElementById("switch-camera");

const cameraStatus =
    document.getElementById("camera-status");

const autoDot =
    document.getElementById("auto-dot");

const autoText =
    document.getElementById("auto-text");

const result =
    document.getElementById("result");


let stream = null;

let scanning = false;

let processing = false;

let scanTimer = null;


/*
========================================
CAMERA MODE
========================================

environment = BACK CAMERA

user = FRONT CAMERA
*/

let cameraMode = "environment";


/*
========================================
START CAMERA
========================================
*/

startButton.addEventListener(
    "click",
    startCamera
);


async function startCamera() {

    try {

        stopCurrentCamera();


        stream =
            await navigator.mediaDevices
                .getUserMedia({

                    video: {

                        facingMode: {
                            ideal: cameraMode
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


        camera.srcObject =
            stream;


        await camera.play();


        scanning = true;


        autoDot.classList.add(
            "active"
        );


        autoText.textContent =
            cameraMode === "environment"
                ? "Back camera • Automatic scanning ON"
                : "Front camera • Automatic scanning ON";


        cameraStatus.textContent =
            cameraMode === "environment"
                ? "📷 Back camera ready — place leaf inside frame"
                : "🤳 Front camera ready";


        /*
        Start automatic AI scanning
        */

        setTimeout(
            automaticScanning,
            1500
        );


    } catch (error) {

        console.error(
            "Camera error:",
            error
        );


        cameraStatus.textContent =
            "Unable to access camera";


        alert(
            "Camera permission is required."
        );

    }

}


/*
========================================
SWITCH CAMERA
========================================
*/

switchButton.addEventListener(
    "click",
    async function () {

        /*
        Change camera
        */

        if (
            cameraMode ===
            "environment"
        ) {

            cameraMode = "user";

        } else {

            cameraMode = "environment";

        }


        /*
        Restart camera
        */

        if (stream) {

            await startCamera();

        } else {

            cameraStatus.textContent =
                cameraMode === "environment"
                    ? "Back camera selected"
                    : "Front camera selected";

        }

    }
);


/*
========================================
STOP CURRENT CAMERA
========================================
*/

function stopCurrentCamera() {

    scanning = false;


    if (scanTimer) {

        clearTimeout(
            scanTimer
        );

        scanTimer = null;

    }


    if (stream) {

        stream.getTracks().forEach(
            function (track) {

                track.stop();

            }
        );

        stream = null;

    }


    camera.srcObject = null;

}


/*
========================================
STOP CAMERA BUTTON
========================================
*/

stopButton.addEventListener(
    "click",
    function () {

        stopCurrentCamera();


        autoDot.classList.remove(
            "active"
        );


        autoText.textContent =
            "Automatic scanning is off";


        cameraStatus.textContent =
            "Camera stopped";

    }
);


/*
========================================
AUTOMATIC SCANNING
========================================
*/

function automaticScanning() {

    if (!scanning) {
        return;
    }


    captureAndAnalyze();


    /*
    Analyze every 4 seconds
    */

    scanTimer = setTimeout(
        automaticScanning,
        4000
    );

}


/*
========================================
CAPTURE CAMERA FRAME
========================================
*/

async function captureAndAnalyze() {

    if (!scanning) {
        return;
    }


    if (processing) {
        return;
    }


    if (
        camera.readyState <
        HTMLMediaElement.HAVE_CURRENT_DATA
    ) {

        return;

    }


    processing = true;


    cameraStatus.textContent =
        "🔍 Scanning leaf with AI...";


    try {

        /*
        Canvas dimensions
        */

        canvas.width =
            camera.videoWidth;

        canvas.height =
            camera.videoHeight;


        const context =
            canvas.getContext("2d");


        /*
        Capture current frame
        */

        context.drawImage(

            camera,

            0,

            0,

            canvas.width,

            canvas.height

        );


        /*
        Convert to image
        */

        const blob =
            await new Promise(
                function (resolve) {

                    canvas.toBlob(

                        resolve,

                        "image/jpeg",

                        0.85

                    );

                }
            );


        if (!blob) {

            processing = false;

            return;

        }


        /*
        Send to backend
        */

        const formData =
            new FormData();


        formData.append(
            "image",
            blob,
            "camera_leaf.jpg"
        );


        const response =
            await fetch(
                "/api/predict",
                {

                    method: "POST",

                    body: formData

                }
            );


        const data =
            await response.json();


        /*
        Prediction successful
        */

        if (
            data.status ===
            "success"
        ) {

            displayResult(
                data
            );


            cameraStatus.textContent =
                "✓ Disease analysis complete";

        }


        else {

            cameraStatus.textContent =
                "Move camera closer to the leaf";

        }


    } catch (error) {

        console.error(
            error
        );


        cameraStatus.textContent =
            "Waiting for a clear leaf image...";

    }


    processing = false;

}


/*
========================================
DISPLAY RESULT
========================================
*/

function displayResult(data) {

    result.classList.remove(
        "hidden"
    );


    document.getElementById(
        "disease"
    ).textContent =
        data.disease;


    document.getElementById(
        "crop"
    ).textContent =
        data.crop;


    const confidence =
        Number(
            data.confidence
        );


    document.getElementById(
        "confidence"
    ).textContent =
        confidence.toFixed(1)
        + "%";


    document.getElementById(
        "progress-bar"
    ).style.width =
        Math.min(
            confidence,
            100
        ) + "%";


    document.getElementById(
        "severity"
    ).textContent =
        data.severity;


    /*
    Solution
    */

    const solutionList =
        document.getElementById(
            "solution-list"
        );


    solutionList.innerHTML = "";


    data.solution.forEach(
        function (solution) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                solution;

            solutionList.appendChild(
                li
            );

        }
    );


    /*
    Prevention
    */

    const preventionList =
        document.getElementById(
            "prevention-list"
        );


    preventionList.innerHTML = "";


    data.prevention.forEach(
        function (prevention) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                prevention;

            preventionList.appendChild(
                li
            );

        }
    );


    /*
    Show result
    */

    result.scrollIntoView({

        behavior: "smooth",

        block: "start"

    });


    loadHistory();

}


/*
========================================
HISTORY
========================================
*/

async function loadHistory() {

    try {

        const response =
            await fetch(
                "/api/history"
            );


        const data =
            await response.json();


        if (
            data.status !==
            "success"
        ) {

            return;

        }


        if (
            data.data.length === 0
        ) {

            document.getElementById(
                "history"
            ).innerHTML =
                "<p>No scans yet.</p>";

            return;

        }


        let html = `

            <table class="history-table">

                <thead>

                    <tr>

                        <th>Date</th>
                        <th>Crop</th>
                        <th>Disease</th>
                        <th>Confidence</th>
                        <th>Severity</th>

                    </tr>

                </thead>

                <tbody>

        `;


        data.data.forEach(
            function (record) {

                html += `

                    <tr>

                        <td>
                            ${record.created_at}
                        </td>

                        <td>
                            ${record.crop}
                        </td>

                        <td>
                            ${record.disease}
                        </td>

                        <td>
                            ${record.confidence}%
                        </td>

                        <td>
                            ${record.severity}
                        </td>

                    </tr>

                `;

            }
        );


        html += `

                </tbody>

            </table>

        `;


        document.getElementById(
            "history"
        ).innerHTML =
            html;


    } catch (error) {

        console.error(
            error
        );

    }

}


loadHistory();