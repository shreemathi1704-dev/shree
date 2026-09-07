const camera =
    document.getElementById("camera");

const canvas =
    document.getElementById("canvas");

const startButton =
    document.getElementById("start-camera");

const stopButton =
    document.getElementById("stop-camera");

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

let scanTimer = null;

let processing = false;


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

        if (stream) {

            stopCamera();

        }


        stream =
            await navigator.mediaDevices
                .getUserMedia({

                    video: {

                        facingMode: {
                            ideal: "environment"
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


        cameraStatus.textContent =
            "Camera ready — place the leaf inside the frame";


        scanning = true;


        autoDot.classList.add(
            "active"
        );


        autoText.textContent =
            "Automatic AI scanning is ON";


        /*
        Wait for camera
        */

        setTimeout(
            startAutomaticScanning,
            1500
        );


    } catch (error) {

        console.error(error);


        cameraStatus.textContent =
            "Camera permission denied";


        alert(
            "Please allow camera permission and try again."
        );

    }

}


/*
========================================
STOP CAMERA
========================================
*/

stopButton.addEventListener(
    "click",
    stopCamera
);


function stopCamera() {

    scanning = false;


    if (scanTimer) {

        clearTimeout(
            scanTimer
        );

        scanTimer = null;

    }


    if (stream) {

        stream.getTracks().forEach(
            track => track.stop()
        );

        stream = null;

    }


    camera.srcObject = null;


    autoDot.classList.remove(
        "active"
    );


    autoText.textContent =
        "Automatic scanning is off";


    cameraStatus.textContent =
        "Camera stopped";

}


/*
========================================
AUTOMATIC SCANNING
========================================
*/

function startAutomaticScanning() {

    if (!scanning) {

        return;

    }


    captureAndAnalyze();


    /*
    Capture again after 4 seconds.
    */

    scanTimer = setTimeout(
        startAutomaticScanning,
        4000
    );

}


/*
========================================
CAPTURE FRAME
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
        "🔍 AI is analyzing the leaf...";


    try {

        /*
        Set canvas size
        */

        canvas.width =
            camera.videoWidth;

        canvas.height =
            camera.videoHeight;


        const context =
            canvas.getContext("2d");


        context.drawImage(
            camera,
            0,
            0,
            canvas.width,
            canvas.height
        );


        /*
        Convert camera frame
        into JPEG blob
        */

        const blob =
            await new Promise(
                resolve =>
                    canvas.toBlob(
                        resolve,
                        "image/jpeg",
                        0.85
                    )
            );


        if (!blob) {

            processing = false;

            return;

        }


        /*
        Send image to Flask
        */

        const formData =
            new FormData();


        formData.append(
            "image",
            blob,
            "live_leaf.jpg"
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


        if (
            data.status ===
            "success"
        ) {

            displayResult(
                data
            );


            cameraStatus.textContent =
                "✓ Analysis complete — scanning again automatically";


        } else {

            cameraStatus.textContent =
                "Move the camera closer to the leaf";

        }


    } catch (error) {

        console.error(
            "AI error:",
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


    /*
    Disease
    */

    document.getElementById(
        "disease"
    ).textContent =
        data.disease;


    /*
    Crop
    */

    document.getElementById(
        "crop"
    ).textContent =
        data.crop;


    /*
    Confidence
    */

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


    /*
    Severity
    */

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
        function (item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

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
        function (item) {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                item;

            preventionList.appendChild(
                li
            );

        }
    );


    /*
    Scroll result into view
    */

    result.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });


    loadHistory();

}


/*
========================================
LOAD HISTORY
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
            record => {

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


/*
========================================
INITIALIZE
========================================
*/

loadHistory();