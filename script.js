let stream = null;

let currentCamera = "environment";

let capturedBlob = null;

let currentLatitude = null;

let currentLongitude = null;


/* -------------------------------------------
   START CAMERA
------------------------------------------- */

async function startCamera() {

    const video =
        document.getElementById("camera");

    const message =
        document.getElementById("cameraMessage");


    try {

        // Stop previous camera
        if (stream) {

            stream.getTracks().forEach(
                track => track.stop()
            );

        }


        stream =
            await navigator.mediaDevices.getUserMedia({

                video: {

                    facingMode: {
                        ideal: currentCamera
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


        video.srcObject =
            stream;


        message.style.display =
            "none";


    } catch (error) {

        console.error(
            "Camera error:",
            error
        );


        message.innerHTML =
            "❌ Camera access denied.<br>Allow camera permission.";


        message.style.display =
            "block";

    }

}


/* -------------------------------------------
   SWITCH CAMERA
------------------------------------------- */

async function switchCamera() {

    if (
        currentCamera ===
        "environment"
    ) {

        currentCamera =
            "user";

    } else {

        currentCamera =
            "environment";

    }


    await startCamera();

}


/* -------------------------------------------
   CAPTURE IMAGE
------------------------------------------- */

function captureImage() {

    const video =
        document.getElementById("camera");


    if (
        !video.videoWidth ||
        !video.videoHeight
    ) {

        alert(
            "Camera is not ready."
        );

        return;

    }


    const canvas =
        document.createElement("canvas");


    canvas.width =
        video.videoWidth;

    canvas.height =
        video.videoHeight;


    const context =
        canvas.getContext("2d");


    context.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );


    canvas.toBlob(
        function(blob) {

            capturedBlob =
                blob;


            const imageURL =
                URL.createObjectURL(
                    blob
                );


            document.getElementById(
                "preview"
            ).src = imageURL;


            document.getElementById(
                "previewSection"
            ).classList.remove(
                "hidden"
            );


            document.getElementById(
                "status"
            ).innerText =
                "📸 Image captured. Ready for AI analysis.";


            getGPS();

        },
        "image/jpeg",
        0.90
    );

}


/* -------------------------------------------
   IMAGE UPLOAD
------------------------------------------- */

document.getElementById(
    "imageUpload"
).addEventListener(
    "change",
    function(event) {

        const file =
            event.target.files[0];


        if (!file) {

            return;

        }


        capturedBlob =
            file;


        const imageURL =
            URL.createObjectURL(
                file
            );


        document.getElementById(
            "preview"
        ).src = imageURL;


        document.getElementById(
            "previewSection"
        ).classList.remove(
            "hidden"
        );


        document.getElementById(
            "status"
        ).innerText =
            "🖼️ Image selected. Ready for analysis.";


        getGPS();

    }
);


/* -------------------------------------------
   GPS
------------------------------------------- */

function getGPS() {

    if (!navigator.geolocation) {

        console.log(
            "GPS not supported."
        );

        return;

    }


    navigator.geolocation.getCurrentPosition(

        function(position) {

            currentLatitude =
                position.coords.latitude;

            currentLongitude =
                position.coords.longitude;


            console.log(
                "GPS:",
                currentLatitude,
                currentLongitude
            );

        },

        function(error) {

            console.log(
                "GPS error:",
                error
            );

        },

        {

            enableHighAccuracy:
                true,

            timeout:
                10000,

            maximumAge:
                0

        }

    );

}


/* -------------------------------------------
   ANALYZE
------------------------------------------- */

async function analyzeImage() {

    if (!capturedBlob) {

        alert(
            "Please capture or upload an image."
        );

        return;

    }


    const status =
        document.getElementById(
            "status"
        );


    status.innerText =
        "🤖 AI is analyzing the crop...";


    document.getElementById(
        "scanLine"
    ).style.display =
        "none";


    const formData =
        new FormData();


    formData.append(
        "image",
        capturedBlob,
        "crop.jpg"
    );


    if (
        currentLatitude !== null
    ) {

        formData.append(
            "latitude",
            currentLatitude
        );

    }


    if (
        currentLongitude !== null
    ) {

        formData.append(
            "longitude",
            currentLongitude
        );

    }


    try {

        const response =
            await fetch(
                "/predict",
                {

                    method:
                        "POST",

                    body:
                        formData

                }
            );


        const data =
            await response.json();


        if (!data.success) {

            status.innerText =
                "❌ " + data.message;

            return;

        }


        showResult(
            data
        );


        status.innerText =
            "✅ Analysis completed.";


    } catch (error) {

        console.error(
            error
        );


        status.innerText =
            "❌ Server connection error.";

    }

}


/* -------------------------------------------
   SHOW RESULT
------------------------------------------- */

function showResult(data) {

    const result =
        document.getElementById(
            "result"
        );


    result.classList.remove(
        "hidden"
    );


    const disease =
        data.crop_disease;


    document.getElementById(
        "disease"
    ).innerText =
        disease.disease;


    document.getElementById(
        "confidence"
    ).innerText =
        disease.confidence +
        "%";


    document.getElementById(
        "severity"
    ).innerText =
        disease.severity;


    document.getElementById(
        "description"
    ).innerText =
        disease.description;


    document.getElementById(
        "recommendation"
    ).innerText =
        disease.recommendation;


    /* GPS */

    if (data.gps) {

        document.getElementById(
            "latitude"
        ).innerText =
            data.gps.latitude || "-";


        document.getElementById(
            "longitude"
        ).innerText =
            data.gps.longitude || "-";

    }


    /* SATELLITE */

    if (
        data.satellite &&
        data.satellite.success
    ) {

        const satellite =
            data.satellite;


        document.getElementById(
            "ndvi"
        ).innerText =
            satellite.ndvi;


        document.getElementById(
            "vegetation"
        ).innerText =
            satellite.field_status;


        document.getElementById(
            "fieldCondition"
        ).innerText =
            satellite.field_condition;


        document.getElementById(
            "imagesFound"
        ).innerText =
            satellite.images_found;


    } else {

        document.getElementById(
            "ndvi"
        ).innerText =
            "Unavailable";


        document.getElementById(
            "vegetation"
        ).innerText =
            "Unavailable";


        document.getElementById(
            "fieldCondition"
        ).innerText =
            "Unavailable";


        document.getElementById(
            "imagesFound"
        ).innerText =
            "-";

    }


    // Scroll to result

    result.scrollIntoView({

        behavior:
            "smooth"

    });

}


/* -------------------------------------------
   START
------------------------------------------- */

window.addEventListener(
    "load",
    function() {

        startCamera();

        getGPS();

    }
);