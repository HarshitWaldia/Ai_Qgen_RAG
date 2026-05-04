let currentDocId = null;
let sectionCounter = 0;

// Helper function to create a new section row dynamically
function addSectionRow() {
    sectionCounter++;
    const charName = String.fromCharCode(64 + sectionCounter); // Converts 1->A, 2->B, etc.

    const row = document.createElement('div');
    row.className = 'row section-row';
    row.style.display = 'flex';
    row.style.alignItems = 'center';
    row.style.gap = '10px';
    row.style.marginBottom = '15px';

    row.innerHTML = `
        <input type="text" class="secName" value="Section ${charName}" placeholder="Section Name" style="flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
        <select class="qType" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
            <option value="MCQ">MCQ</option>
            <option value="Short Answer">Short Answer</option>
            <option value="Long Answer">Long Answer</option>
            <option value="Case-Based">Case-Based</option>
        </select>
        <input type="number" class="qCount" value="5" min="1" max="50" title="Number of Questions" style="width: 60px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
        <select class="qDiff" style="padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
            <option value="Medium">Medium</option>
            <option value="Easy">Easy</option>
            <option value="Hard">Hard</option>
        </select>
        <input type="number" class="qMarks" value="1" min="1" title="Marks per Question" style="width: 60px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
        <button type="button" class="remove-sec-btn" style="background-color: #dc3545; padding: 8px 12px; border: none; border-radius: 4px; color: white; cursor: pointer;" title="Remove Section">❌</button>
    `;

    // Add event listener to delete this specific section
    row.querySelector('.remove-sec-btn').addEventListener('click', () => {
        row.remove();
    });

    document.getElementById('sectionsContainer').appendChild(row);
}

// Attach event listener for the "+ Add Another Section" button
document.getElementById('addSectionBtn').addEventListener('click', addSectionRow);

// --- 1. UPLOAD LOGIC ---
document.getElementById('uploadBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('pdfUpload').files[0];
    if (!fileInput) return alert("Please select a PDF first.");

    const formData = new FormData();
    formData.append('file', fileInput);

    document.getElementById('uploadStatus').innerText = "Uploading & chunking... ⏳";

    try {
        const res = await fetch('/api/upload', { method: 'POST', body: formData });
        const data = await res.json();

        if (res.ok) {
            currentDocId = data.document_id;
            document.getElementById('uploadStatus').innerText = `✅ Processed ${data.chunks_processed} chunks.`;
            document.getElementById('configCard').style.display = 'block';

            // Clear previous sections and add the first default section automatically
            document.getElementById('sectionsContainer').innerHTML = '';
            sectionCounter = 0;
            addSectionRow();

        } else {
            alert("Upload Error: " + data.detail);
        }
    } catch (e) {
        alert("Server error during upload.");
        console.error(e);
    }
});

// --- 2. GENERATE LOGIC ---
document.getElementById('generateBtn').addEventListener('click', async () => {

    // Gather all sections from the UI
    const sectionElements = document.querySelectorAll('.section-row');

    if (sectionElements.length === 0) {
        return alert("Please add at least one section before generating.");
    }

    // Build the sections array to send to the backend
    const sectionsArray = Array.from(sectionElements).map(row => {
        return {
            name: row.querySelector('.secName').value,
            q_type: row.querySelector('.qType').value,
            count: parseInt(row.querySelector('.qCount').value),
            difficulty: row.querySelector('.qDiff').value,
            marks_per_question: parseInt(row.querySelector('.qMarks').value)
        };
    });

    // Show the loader
    document.getElementById('loader').style.display = 'block';
    document.getElementById('resultCard').style.display = 'none';

    // Construct the request payload
    const reqBody = {
        document_id: currentDocId,
        language: document.getElementById('language').value,
        sections: sectionsArray
    };

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reqBody)
        });

        const data = await res.json();

        if (res.ok) {
            // Show the result card and populate download links
            document.getElementById('resultCard').style.display = 'block';
            document.getElementById('btnDocx').href = data.download_urls.qp_docx;
            document.getElementById('btnPdf').href = data.download_urls.qp_pdf;
            document.getElementById('btnKey').href = data.download_urls.ak_docx;

            // Scroll down to the results
            document.getElementById('resultCard').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert("Generation Error: " + data.detail);
        }
    } catch (e) {
        alert("Failed to generate paper. Check console for details.");
        console.error(e);
    }

    // Hide the loader
    document.getElementById('loader').style.display = 'none';
});