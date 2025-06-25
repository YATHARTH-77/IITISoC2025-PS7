let uplDiv = document.getElementById("uplDiv");
let uplBtn = document.getElementById('uplBtn');
let submitBtn = document.getElementById('submitBtn');
let uplLogo = document.getElementById('upllogo');
let finalFile;
let bool=false;

const filefunction = (file) => {
    if (file && (file.type === "image/jpeg" || file.type === "image/png")) {
        const reader = new FileReader();
        reader.onload = function(event) {
            uplLogo.src = event.target.result;
            uplLogo.style.display = 'inline-block';
            const remInPx = parseFloat(getComputedStyle(document.documentElement).fontSize);
            const maxWidth = uplDiv.offsetWidth - (3 * remInPx);
            if ((uplLogo.style.naturalWidth)*250/(uplLogo.style.naturalHeight) > maxWidth) {
                uplLogo.style.width = maxWidth + 'px';
                uplLogo.style.height = 'auto';
            } else {
                uplLogo.style.width = 'auto';
                uplLogo.style.height = '15rem';
            }
            finalFile = file;
            bool=true;
            console.log("Accepted file:", file);
        };
        reader.readAsDataURL(file);
    } else {
        console.error("Unsupported file type:", file.type);
        alert("Please upload a valid image file (JPEG or PNG).");
    }
};

uplBtn.onclick = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/jpeg, image/png';
    fileInput.onchange = (event) => {
        const files = event.target.files;
        if (files.length > 0) {
            const file = files[0];
            filefunction(file);
        }
    };
    fileInput.click();
};

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uplDiv.addEventListener(eventName, e => e.preventDefault());
    uplDiv.addEventListener(eventName, e => e.stopPropagation());
});

uplDiv.addEventListener('dragover', () => {
    uplDiv.classList.add('dragover');
});
uplDiv.addEventListener('dragleave', () => {
    uplDiv.classList.remove('dragover');
});
uplDiv.addEventListener('drop', () => {
    uplDiv.classList.remove('dragover');
});


uplDiv.addEventListener('drop', (f) => {
    const files = f.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        filefunction(file);
    }
});

submitBtn.onclick = () => {
    let lang = document.getElementsByName('lang');
    let selectedLang;
    lang.forEach((radio) => {
        if (radio.checked) {
            selectedLang = radio.value;
        }
    });
    if ((bool)&&(selectedLang)) {
        // Proceed with form submission
    } else {
        alert("Please upload a valid image file and select a language before submitting.");
    }
}