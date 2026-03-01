document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const tabText = document.getElementById('tab-text');
    const tabImage = document.getElementById('tab-image');
    const textInputArea = document.getElementById('text-input-area');
    const imageInputArea = document.getElementById('image-input-area');

    const prescriptionText = document.getElementById('prescription-text');
    const fileUpload = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image');

    const btnExplain = document.getElementById('btn-explain');
    const btnReset = document.getElementById('btn-reset');
    const loadingIndicator = document.getElementById('loading-indicator');

    const outputSection = document.getElementById('output-section');
    const simpleExplanationText = document.getElementById('simple-explanation-text');
    const dataMedicine = document.getElementById('data-medicine');
    const dataDosage = document.getElementById('data-dosage');
    const dataFrequency = document.getElementById('data-frequency');
    const dataTiming = document.getElementById('data-timing');
    const dataDuration = document.getElementById('data-duration');
    const dataInstructions = document.getElementById('data-instructions');

    const ocrContextContainer = document.getElementById('ocr-context-container');
    const ocrRawText = document.getElementById('ocr-raw-text');

    const errorToast = document.getElementById('error-toast');
    const errorMessage = document.getElementById('error-message');

    // State
    let currentMode = 'text'; // 'text' or 'image'
    let currentFile = null;

    const API_URL = 'http://127.0.0.1:8000/explain'; // Default local FastAPI url

    // Tab Switching
    function switchTab(mode) {
        currentMode = mode;
        if (mode === 'text') {
            tabText.classList.add('text-medical-600', 'border-medical-500');
            tabText.classList.remove('text-gray-500', 'border-transparent');
            tabImage.classList.add('text-gray-500', 'border-transparent');
            tabImage.classList.remove('text-medical-600', 'border-medical-500');

            textInputArea.classList.remove('hidden');
            imageInputArea.classList.add('hidden');
        } else {
            tabImage.classList.add('text-medical-600', 'border-medical-500');
            tabImage.classList.remove('text-gray-500', 'border-transparent');
            tabText.classList.add('text-gray-500', 'border-transparent');
            tabText.classList.remove('text-medical-600', 'border-medical-500');

            imageInputArea.classList.remove('hidden');
            textInputArea.classList.add('hidden');
        }
    }

    tabText.addEventListener('click', () => switchTab('text'));
    tabImage.addEventListener('click', () => switchTab('image'));

    // Image Upload Handling
    function handleFile(file) {
        if (file && file.type.startsWith('image/')) {
            currentFile = file;
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                dropZone.classList.add('hidden');
                imagePreviewContainer.classList.remove('hidden');
            };
            reader.readAsDataURL(file);
        } else {
            showError("Please upload a valid image file.");
        }
    }

    fileUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFile(e.target.files[0]);
    });

    removeImageBtn.addEventListener('click', () => {
        currentFile = null;
        fileUpload.value = '';
        imagePreview.src = '';
        imagePreviewContainer.classList.add('hidden');
        dropZone.classList.remove('hidden');
    });

    // Drag and Drop implementation
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('border-medical-500', 'bg-medical-50');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('border-medical-500', 'bg-medical-50');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) handleFile(files[0]);
    }, false);

    // API Call & Processing
    btnExplain.addEventListener('click', async () => {
        // Validate input
        if (currentMode === 'text' && !prescriptionText.value.trim()) {
            showError("Please enter prescription text.");
            prescriptionText.focus();
            return;
        }
        if (currentMode === 'image' && !currentFile) {
            showError("Please upload an image first.");
            return;
        }

        // Prepare request
        const formData = new FormData();
        if (currentMode === 'text') {
            formData.append('prescription_text', prescriptionText.value.trim());
        } else {
            formData.append('file', currentFile);
        }

        // Setup UI for Loading
        btnExplain.disabled = true;
        btnExplain.classList.add('opacity-70', 'cursor-not-allowed');
        loadingIndicator.classList.remove('hidden');
        outputSection.classList.add('hidden');
        hideError();

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                // Determine if it's an OCR error
                let errorMsg = result.detail || "Failed to parse prescription.";
                throw new Error(errorMsg);
            }

            // Success - Populate Output
            displayResults(result);

        } catch (error) {
            console.error('API Error:', error);
            // Check if connection failed
            if (error.message.includes('Failed to fetch')) {
                showError("Failed to connect to the server. Is the FastAPI backend running?");
            } else {
                showError(error.message);
            }

        } finally {
            // Restore UI
            btnExplain.disabled = false;
            btnExplain.classList.remove('opacity-70', 'cursor-not-allowed');
            loadingIndicator.classList.add('hidden');
        }
    });

    function displayResults(data) {
        const structured = data.structured_data;

        // Output explanation
        simpleExplanationText.textContent = data.simple_explanation;

        // Output grid data
        dataMedicine.textContent = structured.medicine || "Not found";
        dataDosage.textContent = structured.dosage || "Not specified";
        dataFrequency.textContent = structured.frequency || "Not specified";
        dataTiming.textContent = structured.timing || "Not specified";
        dataDuration.textContent = structured.duration || "Not specified";
        dataInstructions.textContent = structured.instructions || "None";

        // Show OCR raw text if available
        if (structured.extracted_text_from_ocr) {
            ocrRawText.textContent = structured.extracted_text_from_ocr;
            ocrContextContainer.classList.remove('hidden');
        } else {
            ocrContextContainer.classList.add('hidden');
        }

        // Reveal section
        outputSection.classList.remove('hidden');

        // Scroll to results smoothly
        setTimeout(() => {
            outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
    }

    // Reset Flow
    btnReset.addEventListener('click', () => {
        outputSection.classList.add('hidden');
        prescriptionText.value = '';
        if (currentMode === 'image') {
            removeImageBtn.click();
        } else {
            prescriptionText.focus();
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Error Toast handling
    let errorTimeout;
    function showError(message) {
        errorMessage.textContent = message;
        errorToast.classList.remove('translate-y-24', 'opacity-0');

        clearTimeout(errorTimeout);
        errorTimeout = setTimeout(hideError, 5000);
    }

    function hideError() {
        errorToast.classList.add('translate-y-24', 'opacity-0');
    }
});
