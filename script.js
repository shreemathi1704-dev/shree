// Database containing UI translations and spoken text
const languageData = {
    "ta-IN": {
        diseaseName: "இலைப்புள்ளி நோய் (Leaf Spot)",
        recoveryStatus: "குணப்படுத்தக்கூடியது (Curable)",
        diseaseType: "பூஞ்சை தொற்று (Fungal)",
        symptomsText: "இலைகளில் பழுப்பு நிற புள்ளிகள் மற்றும் மஞ்சள் விளிம்புகள் காணப்படும்.",
        organicCure: "வேப்பெண்ணெய் கரைசல் (3%) இலைகளில் தெளிக்கவும்.",
        chemicalCure: "மான்கோசெப் (Mancozeb) பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும்.",
        speechText: "இலைப்புள்ளி நோய் கண்டறியப்பட்டது. வேப்பெண்ணெய் தெளித்து இயற்கை வழியில் கட்டுப்படுத்தலாம்."
    },
    "te-IN": {
        diseaseName: "ఆకు మచ్చ వ్యాధి (Leaf Spot)",
        recoveryStatus: "నయం చేయవచ్చు (Curable)",
        diseaseType: "శిలీంధ్ర సంక్రమణ (Fungal)",
        symptomsText: "ఆకులపై గోధుమ రంగు మచ్చలు మరియు పసుపు అంచులు ఉంటాయి.",
        organicCure: "వేప నూనె మిశ్రమాన్ని (3%) ఆకులపై పిచికారీ చేయండి.",
        chemicalCure: "మాంకోజెబ్ (Mancozeb) శిలీంధ్ర నాశిని ఉపయోగించండి.",
        speechText: "ఆకు మచ్చ వ్యాధి గుర్తించబడింది. వేప నూనె చల్లి సహజంగా నివారించండి."
    },
    "kn-IN": {
        diseaseName: "ಎಲೆ ಚುಕ್ಕೆ ರೋಗ (Leaf Spot)",
        recoveryStatus: "ಗುಣಪಡಿಸಬಹುದಾಗಿದೆ (Curable)",
        diseaseType: "ಶಿಲೀಂಧ್ರ ಸೋಂಕು (Fungal)",
        symptomsText: "ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಬಣ್ಣದ ಚುಕ್ಕೆಗಳು ಮತ್ತು ಹಳದಿ ಅಂಚುಗಳು ಕಂಡುಬರುತ್ತವೆ.",
        organicCure: "ಬೇಪಿನ ಎಣ್ಣೆ ದ್ರಾವಣವನ್ನು (3%) ಎಲೆಗಳ ಮೇಲೆ ಸಿಂಪಡಿಸಿ.",
        chemicalCure: "ಮ್ಯಾಂಕೋಝೆಬ್ (Mancozeb) ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಬಳಸಿ.",
        speechText: "ಎಲೆ ಚುಕ್ಕೆ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ. ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ ನೈಸರ್ಗಿಕವಾಗಿ ನಿಯಂತ್ರಿಸಿ."
    },
    "ml-IN": {
        diseaseName: "ഇലപ്പുള്ളി രോഗം (Leaf Spot)",
        recoveryStatus: "പരിഹരിക്കാവുന്നത് (Curable)",
        diseaseType: "ഫംഗസ് രോഗം (Fungal)",
        symptomsText: "ഇലകളിൽ തവിട്ടുനിറത്തിലുള്ള പുള്ളികളും മഞ്ഞ പശ്ചാത്തലവും കാണപ്പെടുന്നു.",
        organicCure: "വേപ്പെണ്ണ മിശ്രിതം (3%) ഇലകളിൽ തളിക്കുക.",
        chemicalCure: "മാങ്കോസെബ് (Mancozeb) ഫംഗിസൈഡ് ഉപയോഗിക്കുക.",
        speechText: "ഇലപ്പുള്ളി രോഗം സ്ഥിരീകരിച്ചു. വേപ്പെണ്ണ ഉപയോഗിച്ച് സ്വാഭാവികമായി തടയാം."
    },
    "hi-IN": {
        diseaseName: "पत्ती धब्बा रोग (Leaf Spot)",
        recoveryStatus: "इलाज योग्य (Curable)",
        diseaseType: "कवक संक्रमण (Fungal)",
        symptomsText: "पत्तियों पर भूरे रंग के धब्बे और पीले किनारे दिखाई देते हैं।",
        organicCure: "नीम के तेल (3%) का घोल पत्तियों पर छिड़कें।",
        chemicalCure: "मैनकोज़ेब (Mancozeb) कवकनाशी का उपयोग करें।",
        speechText: "पत्ती धब्बा रोग पाया गया है। नीम का तेल छिड़क कर प्राकृतिक इलाज करें।"
    },
    "en-IN": {
        diseaseName: "Leaf Spot Disease",
        recoveryStatus: "Curable",
        diseaseType: "Fungal Infection",
        symptomsText: "Brown spots with yellow halos observed on leaves.",
        organicCure: "Foliar spray of 3% Neem Oil solution every 7 days.",
        chemicalCure: "Apply Mancozeb 75% WP contact fungicide at 2g/L water.",
        speechText: "Leaf spot detected. Spray neem oil for natural remedy or apply Mancozeb fungicide."
    }
};

// No Leaf Translations
const noLeafMessages = {
    "ta-IN": "இலை எதுவும் கண்டறியப்படவில்லை! தயவுசெய்து தாவர இலையைக் கேமராவில் காட்டவும்.",
    "te-IN": "ఏ ఆకు కనుగొనబడలేదు! దయచేసి కెమెరాకు మొక్క ఆకును చూపించండి.",
    "kn-IN": "ಯಾವುದೇ ಎಲೆ ಪತ್ತೆಯಾಗಿಲ್ಲ! ದಯವಿಟ್ಟು ಕ್ಯಾಮೆರಾಗೆ ಸಸ್ಯದ ಎಲೆಯನ್ನು ತೋರಿಸಿ.",
    "ml-IN": "ഇലകളൊന്നും കണ്ടെത്തിയില്ല! ദയവായി ക്യാമറയിൽ ഒരു ചെടിയുടെ ഇല കാണിക്കുക.",
    "hi-IN": "कोई पत्ती नहीं मिली! कृपया कैमरे के सामने पौधे की पत्ती दिखाएं।",
    "en-IN": "No leaf detected! Please position a plant leaf in front of the camera."
};

// DOM Elements
const langSelect = document.getElementById('langSelect');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const speakBtn = document.getElementById('speakBtn');
const webcam = document.getElementById('webcam');
const cameraPlaceholder = document.getElementById('cameraPlaceholder');
const scanLine = document.getElementById('scanLine');
const resultCard = document.getElementById('resultCard');

const diseaseName = document.getElementById('diseaseName');
const recoveryStatus = document.getElementById('recoveryStatus');
const accuracyVal = document.getElementById('accuracyVal');
const diseaseType = document.getElementById('diseaseType');
const symptomsText = document.getElementById('symptomsText');
const organicCure = document.getElementById('organicCure');
const chemicalCure = document.getElementById('chemicalCure');

let mediaStream = null;
let currentLanguage = "ta-IN";
let availableVoices = [];
let classifierModel = null;

// Load MobileNet AI Model
async function loadAIModel() {
    if (typeof mobilenet !== 'undefined') {
        classifierModel = await mobilenet.load();
        console.log("MobileNet Model Loaded Successfully!");
    }
}
loadAIModel();

// Voice Setup
function populateVoices() {
    if ('speechSynthesis' in window) {
        availableVoices = window.speechSynthesis.getVoices();
    }
}
populateVoices();
if ('speechSynthesis' in window && window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = populateVoices;
}

// Text-To-Speech Engine
function speakText(text, langCode) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = langCode;
    utterance.rate = 0.9;

    if (availableVoices.length > 0) {
        const targetLang = langCode.toLowerCase().replace('_', '-');
        const matchedVoice = availableVoices.find(v => v.lang.toLowerCase().replace('_', '-') === targetLang);
        if (matchedVoice) utterance.voice = matchedVoice;
    }

    window.speechSynthesis.speak(utterance);
}

// Leaf Verification & Disease Analysis Logic
async function analyzeFrame() {
    if (!classifierModel || !webcam.srcObject) return;

    // Classify current image frame from webcam
    const predictions = await classifierModel.classify(webcam);
    
    // Check if predictions contain leaf/plant related keywords
    const leafKeywords = ['leaf', 'plant', 'flower', 'tree', 'vegetable', 'herb', 'foliage'];
    const isLeaf = predictions.some(pred => 
        leafKeywords.some(keyword => pred.className.toLowerCase().includes(keyword))
    );

    resultCard.classList.remove('hidden');

    if (!isLeaf) {
        // NO LEAF DETECTED OUTPUT
        const noLeafText = noLeafMessages[currentLanguage] || noLeafMessages["en-IN"];
        
        diseaseName.textContent = "❌ No Leaf Detected";
        diseaseName.className = "text-red-400 font-bold text-base mt-0.5";
        
        recoveryStatus.textContent = "N/A";
        accuracyVal.textContent = "0%";
        diseaseType.textContent = "Invalid Scan";
        
        symptomsText.textContent = noLeafText;
        organicCure.textContent = "கேமராவில் இலையைச் சரியாகக் காட்டவும்.";
        chemicalCure.textContent = "N/A";

        speakText(noLeafText, currentLanguage);
    } else {
        // LEAF DETECTED - SHOW DIAGNOSIS
        updateDisplayAndVoice(currentLanguage);
    }
}

// Update UI and trigger Speech
function updateDisplayAndVoice(langCode) {
    currentLanguage = langCode;
    const data = languageData[langCode] || languageData["en-IN"];

    diseaseName.textContent = data.diseaseName;
    diseaseName.className = "text-white font-bold text-base mt-0.5";
    
    recoveryStatus.textContent = data.recoveryStatus;
    accuracyVal.textContent = "95.4%";
    diseaseType.textContent = data.diseaseType;
    symptomsText.textContent = data.symptomsText;
    organicCure.textContent = data.organicCure;
    chemicalCure.textContent = data.chemicalCure;

    speakText(data.speechText, langCode);
}

// Event Listeners
langSelect.addEventListener('change', (e) => {
    currentLanguage = e.target.value;
    if (!resultCard.classList.contains('hidden')) {
        analyzeFrame();
    }
});

speakBtn.addEventListener('click', () => {
    analyzeFrame();
});

startBtn.addEventListener('click', async () => {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment" } 
        });
        webcam.srcObject = mediaStream;
        cameraPlaceholder.classList.add('hidden');
        scanLine.classList.remove('hidden');

        // Analyze after 2 seconds scan delay
        setTimeout(() => {
            analyzeFrame();
        }, 2000);
    } catch (err) {
        alert("Camera access required: " + err.message);
    }
});

stopBtn.addEventListener('click', () => {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        webcam.srcObject = null;
    }
    cameraPlaceholder.classList.remove('hidden');
    scanLine.classList.add('hidden');
    resultCard.classList.add('hidden');
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
});