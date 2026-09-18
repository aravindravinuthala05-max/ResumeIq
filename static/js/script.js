// Global interface controls

document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    const aboutToggle = document.getElementById('aboutToggle');
    const aboutModal = document.getElementById('aboutModal');
    const storedTheme = localStorage.getItem('resumeiq-theme');

    function applyTheme(theme) {
        const isDark = theme === 'dark';
        document.body.classList.toggle('dark-mode', isDark);
        document.body.classList.toggle('light-mode', !isDark);
        if (themeToggle) {
            themeToggle.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
            themeToggle.setAttribute('aria-pressed', String(isDark));
            themeToggle.innerHTML = `<i class="fas fa-${isDark ? 'sun' : 'moon'}" aria-hidden="true"></i>`;
        }
    }

    applyTheme(storedTheme === 'light' ? 'light' : 'dark');

    themeToggle?.addEventListener('click', () => {
        const nextTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
        localStorage.setItem('resumeiq-theme', nextTheme);
        applyTheme(nextTheme);
    });

    function closeAboutModal() {
        if (!aboutModal) return;
        aboutModal.hidden = true;
        document.body.classList.remove('modal-open');
        aboutToggle?.focus();
    }

    aboutToggle?.addEventListener('click', () => {
        if (!aboutModal) return;
        aboutModal.hidden = false;
        document.body.classList.add('modal-open');
        aboutModal.querySelector('.about-close')?.focus();
    });

    aboutModal?.querySelectorAll('[data-close-about]').forEach(element => element.addEventListener('click', closeAboutModal));
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && aboutModal && !aboutModal.hidden) closeAboutModal();
    });
});

// Upload workflow and session handling

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (!uploadForm) return;

    const navigation = performance.getEntriesByType('navigation')[0];
    if (navigation?.type === 'reload') {
        sessionStorage.removeItem('analysisData');
        sessionStorage.removeItem('resumeDraft');
    }

    const resumeInput = document.getElementById('resume');
    const resumeDropZone = document.getElementById('resumeDropZone');
    const resumeFileName = document.getElementById('resumeFileName');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const jobDescriptionInput = document.getElementById('jobDescription');
    const formMessage = document.getElementById('formMessage');
    const analysisProgress = document.querySelectorAll('.analysis-progress li');
    const analyzeButton = uploadForm.querySelector('button[type="submit"]');
    let analysisReady = Boolean(sessionStorage.getItem('analysisData'));

    restoreResumeDraft();

    if (resumeInput) {
        resumeInput.addEventListener('change', handleFileSelect);
    }

    if (resumeDropZone && resumeInput) {
        resumeDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            resumeDropZone.style.borderColor = 'var(--secondary-color)';
        });

        resumeDropZone.addEventListener('dragleave', () => {
            resumeDropZone.style.borderColor = 'var(--primary-color)';
        });

        resumeDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            resumeDropZone.style.borderColor = 'var(--primary-color)';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const dataTransfer = new DataTransfer();
                Array.from(files).forEach(file => dataTransfer.items.add(file));
                resumeInput.files = dataTransfer.files;
                handleFileSelect();
            }
        });

        resumeDropZone.addEventListener('click', () => {
            resumeInput.click();
        });
    }

    function handleFileSelect() {
        if (!resumeInput) return;

        if (resumeInput.files.length > 0) {
            analysisReady = false;
            sessionStorage.removeItem('analysisData');
            sessionStorage.removeItem('resumeDraft');
            resumeFileName.textContent = `✅ ${resumeInput.files[0].name}`;
            resumeFileName.style.color = 'var(--success-color)';
        } else {
            resumeFileName.textContent = 'No file selected';
            resumeFileName.style.color = 'var(--text-secondary)';
        }
    }

    function restoreResumeDraft() {
        const savedDraft = sessionStorage.getItem('resumeDraft');
        if (!savedDraft) return;

        try {
            const draft = JSON.parse(savedDraft);
            if (jobDescriptionInput && draft.jobDescription) jobDescriptionInput.value = draft.jobDescription;
            if (draft.resumeName) {
                resumeFileName.textContent = `Uploaded: ${draft.resumeName}`;
                resumeFileName.style.color = 'var(--success-color)';
            }
        } catch {
            sessionStorage.removeItem('resumeDraft');
        }
    }

    function showFormMessage(message) {
        if (!formMessage) return;
        formMessage.textContent = message;
        formMessage.classList.add('is-visible');
    }

    function setProcessing(isProcessing) {
        if (!analyzeButton) return;
        analyzeButton.disabled = isProcessing;
        analyzeButton.setAttribute('aria-busy', String(isProcessing));
    }

    function resetAnalysisProgress() {
        analysisProgress.forEach((step, index) => {
            step.classList.remove('is-complete', 'is-active');
            if (index === 0) step.classList.add('is-active');
            const icon = step.querySelector('i');
            if (icon) icon.className = index === 0 ? 'fas fa-spinner' : 'fas fa-clock';
        });
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!resumeInput || !jobDescriptionInput) return;

        if (!resumeInput.files.length) {
            showFormMessage('Please upload a resume before analyzing.');
            return;
        }

        if (!jobDescriptionInput.value.trim()) {
            showFormMessage('Please paste a job description before analyzing.');
            return;
        }

        const selectedFile = resumeInput.files[0];
        if (!/\.(pdf|docx)$/i.test(selectedFile.name)) {
            showFormMessage('Please upload a PDF or DOCX resume.');
            return;
        }

        resetAnalysisProgress();
        setProcessing(true);
        if (loadingSpinner) loadingSpinner.style.display = 'flex';
        uploadForm.style.display = 'none';

        try {
            const formData = new FormData();
            formData.append('resume', selectedFile);
            formData.append('job_description', jobDescriptionInput.value);

            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json().catch(() => ({}));

            if (response.ok && data.success) {
                sessionStorage.setItem('analysisData', JSON.stringify(data));
                sessionStorage.setItem('resumeDraft', JSON.stringify({
                    resumeName: selectedFile.name,
                    jobDescription: jobDescriptionInput.value
                }));
                analysisReady = true;
                resetAnalysisProgress();
                window.location.href = '/result';
                return;
            }

            showFormMessage(data.error || 'We could not analyze your resume. Please try again.');
        } catch (error) {
            showFormMessage('Upload failed. Please check your connection and try again.');
        } finally {
            if (loadingSpinner) loadingSpinner.style.display = 'none';
            uploadForm.style.display = 'flex';
            setProcessing(false);
        }
    });
});

function displayProjects(projects) {
    const div = document.getElementById('projectsInfo');
    const items = [
        `<strong>Total Projects:</strong> ${projects.total_projects}`,
        `<strong>AI Projects:</strong> ${projects.ai_projects}`,
        `<strong>Web Projects:</strong> ${projects.web_projects}`,
        `<strong>Mobile Projects:</strong> ${projects.mobile_projects}`,
        `<strong>IoT Projects:</strong> ${projects.iot_projects}`
    ];
    
    div.innerHTML = items.map(item => `<div class="info-item">${item}</div>`).join('');
}

function displayCertifications(certifications) {
    const div = document.getElementById('certificationsInfo');
    const items = [];
    
    items.push(`<strong>Total Certifications:</strong> ${certifications.total_certifications}`);
    if (certifications.aws_certifications.length > 0) {
        items.push(`<strong>AWS:</strong> ${certifications.aws_certifications.join(', ')}`);
    }
    if (certifications.gcp_certifications.length > 0) {
        items.push(`<strong>GCP:</strong> ${certifications.gcp_certifications.join(', ')}`);
    }
    if (certifications.azure_certifications.length > 0) {
        items.push(`<strong>Azure:</strong> ${certifications.azure_certifications.join(', ')}`);
    }
    if (certifications.other_certifications.length > 0) {
        items.push(`<strong>Other:</strong> ${certifications.other_certifications.join(', ')}`);
    }
    
    div.innerHTML = items.map(item => `<div class="info-item">${item}</div>`).join('');
}

function displayLanguages(languages) {
    const div = document.getElementById('languagesInfo');
    const items = [];
    
    if (languages.programming_languages.length > 0) {
        items.push(`<strong>Programming:</strong> ${languages.programming_languages.join(', ')}`);
    }
    if (languages.scripting_languages.length > 0) {
        items.push(`<strong>Scripting:</strong> ${languages.scripting_languages.join(', ')}`);
    }
    if (languages.natural_languages.length > 0) {
        items.push(`<strong>Languages:</strong> ${languages.natural_languages.join(', ')}`);
    }
    
    div.innerHTML = items.length > 0 ?
        items.map(item => `<div class="info-item">${item}</div>`).join('') :
        '<p>No language information found</p>';
}

function displayRecommendations(suggestions) {
    const div = document.getElementById('recommendations');
    div.innerHTML = suggestions.map(suggestion => 
        `<div class="recommendation-item">${suggestion}</div>`
    ).join('');
}

function displayInterviewQuestions(questions) {
    const div = document.getElementById('interviewQuestions');
    div.innerHTML = questions.map((question, index) => `
        <div class="question-item">
            <span class="question-number">${index + 1}</span>
            ${question}
        </div>
    `).join('');
}

function displayFormatting(formatting) {
    const div = document.getElementById('formattingInfo');
    let html = `<p><strong>Formatting Score:</strong> ${formatting.formatting_score}/100</p>`;
    html += `<p><strong>ATS Compatible:</strong> ${formatting.ats_compatible ? '✅ Yes' : '❌ No'}</p>`;
    
    if (formatting.strengths.length > 0) {
        html += '<h3 style="margin-top: 1rem;">Strengths:</h3>';
        html += formatting.strengths.map(item => 
            `<div class="formatting-strength">${item}</div>`
        ).join('');
    }
    
    if (formatting.issues.length > 0) {
        html += '<h3 style="margin-top: 1rem;">Issues to Fix:</h3>';
        html += formatting.issues.map(item => 
            `<div class="formatting-issue">${item}</div>`
        ).join('');
    }
    
    div.innerHTML = html;
}

