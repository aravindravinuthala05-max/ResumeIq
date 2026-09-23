const SCORE_LIMITS = {
    skills_score: 40,
    projects_score: 15,
    experience_score: 15,
    education_score: 10,
    sections_score: 10,
    formatting_score: 10,
};

const asArray = value => Array.isArray(value) ? value : [];
const escapeHtml = value => String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
}

function setHtml(id, value) {
    const element = document.getElementById(id);
    if (element) element.innerHTML = value;
}

function formatLabel(key) {
    return key.replace(/_/g, ' ').replace(/\b\w/g, letter => letter.toUpperCase());
}

function displayValue(value) {
    if (Array.isArray(value)) return value.map(displayValue).join(', ');
    if (value && typeof value === 'object') {
        return Object.entries(value)
            .filter(([, item]) => notEmpty(item))
            .map(([key, item]) => `${formatLabel(key)}: ${displayValue(item)}`)
            .join('; ');
    }
    return String(value ?? '');
}

function infoItem(label, value) {
    return `<div class="info-item"><strong>${escapeHtml(label)}</strong><span>${escapeHtml(displayValue(value))}</span></div>`;
}

function notEmpty(value) {
    return value !== undefined && value !== null && value !== '' && value !== false;
}

function displayTags(id, values, emptyMessage, missing = false) {
    const items = asArray(values);
    const style = missing ? ' style="background: linear-gradient(135deg, #ef4444, #f97316);"' : '';
    setHtml(id, items.length
        ? items.map(value => `<span class="skill-tag"${style}>${escapeHtml(value)}</span>`).join('')
        : `<p>${escapeHtml(emptyMessage)}</p>`);
}

function uniqueSkillValues(values) {
    const seen = new Set();
    return asArray(values).map(value => String(value ?? '').trim()).filter(value => {
        const key = value.toLowerCase();
        if (!value || seen.has(key)) return false;
        seen.add(key);
        return true;
    });
}

function displayHealth(data) {
    const score = Number(data.overall_ats_score);
    setText('healthAtsScore', Number.isFinite(score) ? `${score.toFixed(1)}%` : 'Unknown');
    const hasJd = data.job_description_present !== false;
    setText('healthJdMatch', hasJd
        ? `${asArray(data.matched_skills).length} matched / ${asArray(data.missing_skills).length} missing`
        : 'No job description');
    const priorities = asArray(data.recommendation_details).filter(item => item && item.priority === 'HIGH');
    setText('healthPriorityCount', String(priorities.length));
    setText('healthInterviewCount', String(asArray(data.interview_questions).length));
}

function displayScore(score) {
    const canvas = document.getElementById('scoreCanvas');
    if (!canvas) return;
    const context = canvas.getContext('2d');
    const center = canvas.width / 2;
    const radius = 88;
    const percentage = Math.max(0, Math.min(1, score / 100));

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.lineWidth = 10;
    context.strokeStyle = '#dbeafe';
    context.beginPath();
    context.arc(center, center, radius, 0, Math.PI * 2);
    context.stroke();
    context.strokeStyle = '#6366f1';
    context.beginPath();
    context.arc(center, center, radius, -Math.PI / 2, -Math.PI / 2 + percentage * Math.PI * 2);
    context.stroke();
}

function displayOverview(data) {
    const details = asArray(data.recommendation_details).filter(item => item && typeof item === 'object');
    const strengths = details.filter(item => item.jd_relevance && item.source === 'resume_evidence').slice(0, 2);
    const highPriority = details.find(item => item.priority === 'HIGH');
    const matched = asArray(data.matched_skills);
    const missing = asArray(data.missing_skills);
    const hasJd = data.job_description_present !== false;

    setText('overviewJdStatus', hasJd ? 'JD-aware analysis' : 'No job description provided');
    setHtml('overviewStrengths', strengths.length
        ? strengths.map(item => `<span class="overview-chip">${escapeHtml(item.evidence?.[0] || item.title)}</span>`).join('')
        : '<span class="overview-muted">No evidence-backed strengths yet.</span>');
    setHtml('overviewPriority', highPriority
        ? `<strong>${escapeHtml(highPriority.title)}</strong><span>${escapeHtml(highPriority.section || 'Resume')}</span>`
        : '<span class="overview-muted">No priority improvements detected.</span>');
    setHtml('overviewMatch', hasJd
        ? `<strong>${matched.length} matched</strong><span>${missing.length ? `${missing.length} not currently supported` : 'No unsupported JD skills detected'}</span>`
        : '<span class="overview-muted">Add a job description to compare alignment.</span>');
}

function displayBreakdown(breakdown) {
    Object.entries(SCORE_LIMITS).forEach(([key, maximum]) => {
        const prefix = key.replace('_score', '');
        const score = Number(breakdown[key]) || 0;
        const progress = document.getElementById(`${prefix}Progress`);
        if (progress) progress.style.width = `${Math.max(0, Math.min(100, score / maximum * 100))}%`;
        setText(`${prefix}Score`, `${score.toFixed(1)}/${maximum}`);
    });
}

function renderItems(id, items, emptyMessage) {
    setHtml(id, items.length
        ? items.join('')
        : `<p>${escapeHtml(emptyMessage)}</p>`);
}

function displaySemanticMatches(result) {
    const target = document.getElementById('semanticMatches');
    if (!target) return;
    if (!result || result.available === false) {
        setHtml('semanticMatches', `<p>${escapeHtml(result?.reason || 'Local semantic analysis is unavailable. Your deterministic analysis remains available.')}</p>`);
        return;
    }
    const matches = asArray(result.matches);
    if (!matches.length) {
        setHtml('semanticMatches', '<p>No semantic requirement comparisons are available for this job description.</p>');
        return;
    }
    setHtml('semanticMatches', matches.map(item => {
        const evidence = item.evidence
            ? `<p><strong>Resume evidence:</strong> ${escapeHtml(item.evidence)}</p><p class="semantic-meta">${escapeHtml(item.section || 'resume')} · ${escapeHtml(item.type || 'evidence')} · ${(Number(item.similarity || 0) * 100).toFixed(0)}% relevance</p>`
            : '<p class="semantic-meta">No meaningful evidence relationship detected.</p>';
        return `<article class="semantic-match"><span class="semantic-label">${escapeHtml(item.label || 'No Meaningful Match')}</span><h3>${escapeHtml(item.requirement || 'Job requirement')}</h3>${evidence}</article>`;
    }).join(''));
}

function displayCareerEligibility(payload) {
    const requirements = asArray(payload?.requirements);
    if (!requirements.length) { setHtml('careerEligibilitySummary', ''); setHtml('careerEligibility', '<p>No explicit career or academic eligibility requirements were detected.</p>'); return; }
    setHtml('careerEligibilitySummary', `<span>Supported: ${Number(payload?.supported_count || 0)}</span><span>Conflicts: ${Number(payload?.conflict_count || 0)}</span><span>Not evidenced: ${Number(payload?.not_evidenced_count || 0)}</span>`);
    setHtml('careerEligibility', requirements.map(item => `<article class="eligibility-item eligibility-${escapeHtml(String(item.status || '').toLowerCase())}"><strong>${escapeHtml(item.requirement || 'Requirement')}</strong><span>${escapeHtml(item.status === 'NOT_EVIDENCED' ? 'Not evidenced in resume' : item.status || 'Unknown')}</span><p><strong>Resume evidence:</strong> ${escapeHtml(item.resume_evidence || 'Not evidenced in resume')}</p><p>${escapeHtml(item.reason || '')}</p></article>`).join(''));
}

function displayContact(contact) {
    if (!contact || Object.keys(contact).length === 0) {
        setHtml('contactInfo', '<p>No contact information found.</p>');
        return;
    }

    const items = [];
    if (notEmpty(contact.email)) items.push(infoItem('Email', contact.email));
    if (notEmpty(contact.phone)) items.push(infoItem('Phone', contact.phone));
    if (notEmpty(contact.location)) items.push(infoItem('Location', contact.location));
    if (notEmpty(contact.linkedin)) items.push(infoItem('LinkedIn', contact.linkedin));
    if (notEmpty(contact.website)) items.push(infoItem('Website', contact.website));
    if (notEmpty(contact.summary)) items.push(infoItem('Summary', contact.summary));

    Object.entries(contact).forEach(([key, value]) => {
        if (['email', 'phone', 'location', 'linkedin', 'website', 'summary'].includes(key)) return;
        if (!notEmpty(value)) return;
        items.push(infoItem(key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), Array.isArray(value) ? value.join(', ') : value));
    });

    renderItems('contactInfo', items, 'No contact information found.');
}

function displayEducation(education) {
    if (!education || Object.keys(education).length === 0) {
        setHtml('educationInfo', '<p>No education information found.</p>');
        return;
    }

    const items = [];
    Object.entries(education).forEach(([key, value]) => {
        if (key === 'education_found' || value === 'Not Found' || !notEmpty(value)) return;
        items.push(infoItem(formatLabel(key), value));
    });
    if (education.education_found === false) items.length = 0;

    renderItems('educationInfo', items, 'No education information found.');
}

function displayExperience(experience) {
    if (!experience || Object.keys(experience).length === 0 || experience.experience_found === false) {
        setHtml('experienceInfo', '<p>No experience information found.</p>');
        return;
    }

    const items = Object.entries(experience)
        .filter(([key, value]) => key !== 'experience_found' && notEmpty(value))
        .map(([key, value]) => infoItem(formatLabel(key), value));

    renderItems('experienceInfo', items, 'No experience information found.');
}

function displayProjects(projects) {
    if (!projects || Object.keys(projects).length === 0) {
        setHtml('projectsInfo', '<p>No projects information found.</p>');
        return;
    }

    const items = Object.entries(projects)
        .filter(([key, value]) => key !== 'project_found' && notEmpty(value))
        .map(([key, value]) => infoItem(formatLabel(key), value));

    renderItems('projectsInfo', items, 'No projects information found.');
}

function displayCertifications(certifications) {
    if (!certifications || Object.keys(certifications).length === 0) {
        setHtml('certificationsInfo', '<p>No certifications found.</p>');
        return;
    }

    const items = [];
    if (certifications.total_certifications !== undefined) items.push(infoItem('Total Certifications', certifications.total_certifications));
    if (Array.isArray(certifications.aws_certifications) && certifications.aws_certifications.length) items.push(infoItem('AWS Certifications', certifications.aws_certifications.join(', ')));
    if (Array.isArray(certifications.azure_certifications) && certifications.azure_certifications.length) items.push(infoItem('Azure Certifications', certifications.azure_certifications.join(', ')));
    if (Array.isArray(certifications.gcp_certifications) && certifications.gcp_certifications.length) items.push(infoItem('GCP Certifications', certifications.gcp_certifications.join(', ')));
    if (Array.isArray(certifications.other_certifications) && certifications.other_certifications.length) items.push(infoItem('Other Certifications', certifications.other_certifications.join(', ')));

    renderItems('certificationsInfo', items, 'No certifications found.');
}

function displayAchievements(achievements) {
    if (!achievements) {
        setHtml('achievementsInfo', '<p>No achievements found.</p>');
        return;
    }

    if (Array.isArray(achievements) && achievements.length) {
        setHtml('achievementsInfo', achievements.map(item => `<div class="info-item">${escapeHtml(item)}</div>`).join(''));
        return;
    }

    const items = Object.entries(achievements || {})
        .filter(([, value]) => notEmpty(value))
        .map(([key, value]) => infoItem(key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), Array.isArray(value) ? value.join(', ') : value));

    renderItems('achievementsInfo', items, 'No achievements found.');
}

function displayLanguages(languages) {
    if (!languages) {
        setHtml('languagesInfo', '<p>No languages found.</p>');
        return;
    }

    const items = [];
    if (Array.isArray(languages.programming_languages) && languages.programming_languages.length) items.push(infoItem('Programming Languages', languages.programming_languages.join(', ')));
    if (Array.isArray(languages.scripting_languages) && languages.scripting_languages.length) items.push(infoItem('Scripting Languages', languages.scripting_languages.join(', ')));
    if (Array.isArray(languages.natural_languages) && languages.natural_languages.length) items.push(infoItem('Languages', languages.natural_languages.join(', ')));

    if (items.length === 0) {
        Object.entries(languages).forEach(([key, value]) => {
            if (!notEmpty(value)) return;
            items.push(infoItem(key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()), Array.isArray(value) ? value.join(', ') : value));
        });
    }

    renderItems('languagesInfo', items, 'No languages found.');
}

function recommendationMarkup(item) {
    const priority = String(item.priority || 'LOW').toUpperCase();
    const action = item.next_action || item.action;
    return `<article class="recommendation-item recommendation-${escapeHtml(priority.toLowerCase())}">
        <div class="recommendation-meta">
            <span class="recommendation-priority">${escapeHtml(priority)}</span>
            <span class="recommendation-section">${escapeHtml(item.section || 'Resume')}</span>
            ${item.jd_relevance ? '<span class="recommendation-jd">JD relevant</span>' : ''}
        </div>
        <h3>${escapeHtml(item.title || 'Resume recommendation')}</h3>
        <p>${escapeHtml(item.description || '')}</p>
        ${asArray(item.evidence).length ? `<div class="recommendation-evidence"><strong>Evidence:</strong> ${escapeHtml(item.evidence.join(', '))}</div>` : ''}
        ${action ? `<div class="recommendation-action"><strong>Next action:</strong> ${escapeHtml(action)}</div>` : ''}
        ${item.action_target ? `<button type="button" class="overview-action recommendation-link" data-action-target="${escapeHtml(item.action_target)}">${escapeHtml(item.action_label || 'Review next step')}</button>` : ''}
    </article>`;
}

function displayStrengths(details = []) {
    const strengths = asArray(details).filter(item => (
        item && typeof item === 'object'
        && item.source === 'resume_evidence'
        && item.jd_relevance
        && asArray(item.evidence).length
    ));
    renderItems(
        'strengths',
        strengths.map(item => recommendationMarkup({ ...item, priority: 'STRENGTH' })),
        'No specific strengths identified from the available resume/JD data.',
    );
}

function displayPriorityRecommendations(details = []) {
    const priorities = asArray(details)
        .filter(item => item && typeof item === 'object' && ['HIGH', 'MEDIUM'].includes(String(item.priority || '').toUpperCase()))
        .sort((left, right) => {
            const rank = { HIGH: 0, MEDIUM: 1 };
            return rank[String(left.priority).toUpperCase()] - rank[String(right.priority).toUpperCase()];
        });
    renderItems('priorityRecommendations', priorities.map(recommendationMarkup), 'No recommendations available.');
}

function displayRecommendations(suggestions, details = []) {
    const structured = asArray(details).filter(item => item && typeof item === 'object');
    const remaining = structured.filter(item => !['HIGH', 'MEDIUM'].includes(String(item.priority || '').toUpperCase()));
    const items = structured.length
        ? remaining.map(recommendationMarkup)
        : asArray(suggestions).map(item => `<div class="recommendation-item">${escapeHtml(item)}</div>`);
    renderItems('recommendations', items, 'No recommendations available.');
}

function displayInterviewQuestions(questions) {
    const items = asArray(questions).map((item, index) => {
        const question = item && typeof item === 'object' ? item.question : item;
        const category = item && typeof item === 'object' ? item.category : '';
        const source = item && typeof item === 'object' ? item.source : '';
        const labels = [category, source === 'resume' ? 'Resume evidence' : '', source === 'job_description' ? 'Resume gap' : '', item && item.jd_match ? 'JD match' : '']
            .filter(Boolean)
            .map(label => `<span class="question-label">${escapeHtml(label)}</span>`)
            .join('');
        return `<div class="question-item"><span class="question-number">${index + 1}</span><div><div>${escapeHtml(question)}</div>${labels ? `<div class="question-labels">${labels}</div>` : ''}</div></div>`;
    });
    renderItems('interviewQuestions', items, 'No interview questions available.');
}

function displayInterviewCoach(coach, legacyQuestions) {
    const questions = asArray(coach?.questions);
    const roadmap = asArray(coach?.roadmap);
    setHtml('interviewRoadmap', roadmap.length ? `<h3>Preparation Roadmap</h3>${roadmap.map(item => `<div class="coach-roadmap"><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(asArray(item.topics).join(', ') || 'Review your factual resume evidence.')}</span></div>`).join('')}` : '');
    const source = questions.length ? questions : legacyQuestions;
    const items = asArray(source).map((item, index) => {
        const evidence = asArray(item.evidence);
        return `<details class="question-item" ${index < 3 ? 'open' : ''}><summary><span class="question-number">${index + 1}</span>${escapeHtml(item.question)} <span class="question-label">${escapeHtml(item.category || 'Interview')}</span><span class="question-label">${escapeHtml(item.difficulty || '')}</span><span class="question-label">${escapeHtml(item.priority || '')}</span></summary><p><strong>Why this question:</strong> ${escapeHtml(item.reason || 'Grounded in available interview preparation data.')}</p>${evidence.length ? `<p><strong>Evidence:</strong> ${escapeHtml(evidence.join(', '))}</p>` : ''}<p><strong>What to prepare:</strong> ${escapeHtml(asArray(item.what_to_prepare).join(', '))}</p>${asArray(item.what_to_learn_first).length ? `<p><strong>What to learn first:</strong> ${escapeHtml(item.what_to_learn_first.join(' '))}</p>` : ''}${asArray(item.how_to_practise).length ? `<p><strong>How to practise:</strong> ${escapeHtml(item.how_to_practise.join(' '))}</p>` : ''}${asArray(item.interview_preparation).length ? `<p><strong>How to prepare for the interview:</strong> ${escapeHtml(item.interview_preparation.join(' '))}</p>` : ''}<p><strong>Answer structure:</strong> ${escapeHtml(asArray(item.answer_structure).join(' '))}</p>${asArray(item.follow_ups).length ? `<p><strong>Follow-ups:</strong> ${escapeHtml(item.follow_ups.join(' '))}</p>` : ''}</details>`;
    });
    renderItems('interviewQuestions', items, 'No interview questions available.');
}

function displayFormatting(formatting) {
    if (!formatting || Object.keys(formatting).length === 0) {
        setHtml('formattingInfo', '<p>No formatting analysis available.</p>');
        return;
    }

    const items = [];
    if (formatting.formatting_score !== undefined) items.push(infoItem('Formatting Score', `${formatting.formatting_score}/100`));
    if (formatting.ats_compatible !== undefined) items.push(infoItem('ATS Compatible', formatting.ats_compatible ? 'Yes' : 'No'));
    if (Array.isArray(formatting.strengths) && formatting.strengths.length) {
        items.push(`<div class="formatting-strength">${escapeHtml('Strengths')}</div>`);
        items.push(...formatting.strengths.map(item => `<div class="formatting-strength">${escapeHtml(item)}</div>`));
    }
    if (Array.isArray(formatting.issues) && formatting.issues.length) {
        items.push(`<div class="formatting-issue">${escapeHtml('Issues')}</div>`);
        items.push(...formatting.issues.map(item => `<div class="formatting-issue">${escapeHtml(item)}</div>`));
    }

    renderItems('formattingInfo', items, 'No formatting analysis available.');
}

let rewriteItems = [];

const REWRITE_SECTION_LABELS = {
    summary: 'Professional Summary',
    experience: 'Experience',
    project: 'Projects',
    skills: 'Technical Skills',
    education: 'Education',
};

function rewriteSectionLabel(section) {
    return REWRITE_SECTION_LABELS[section] || formatLabel(section || 'Resume content');
}

function displayRewrites(payload) {
    rewriteItems = asArray(payload.rewrites).filter(item => item && typeof item === 'object');
    const unchangedSections = asArray(payload.unchanged_sections).filter(item => item && typeof item === 'object');
    setText('healthRewriteCount', String(rewriteItems.length));
    setText('rewriterProvider', payload.provider === 'rule_based' ? 'Local fallback' : (payload.provider || 'Provider'));
    if (!rewriteItems.length) {
        setHtml('rewrites', unchangedSections.length ? unchangedSections.map(item => `<article class="rewrite-item"><div class="rewrite-meta"><span class="rewrite-section-label">${escapeHtml(rewriteSectionLabel(item.section))}</span><span class="rewrite-safe rewrite-no-change"><i class="fas fa-circle-check"></i> No improvement required</span></div><div class="rewrite-copy rewrite-improved"><h3>Current Text</h3><p>${escapeHtml(String(item.current_text || ''))}</p></div></article>`).join('') : '<p>No improvement required.</p>');
        setText('rewriterStatus', payload.message || 'No improvement required.');
        return;
    }

    setText('rewriterStatus', payload.message || 'Review each factual rewrite before using it.');
    setHtml('rewrites', rewriteItems.map((item, index) => `
        ${(() => {
            const original = String(item.original ?? '');
            const rewritten = String(item.rewritten ?? '');
            const changed = original !== rewritten;
            return `
        <article class="rewrite-item">
            <div class="rewrite-meta">
                <span class="rewrite-section-label">${escapeHtml(rewriteSectionLabel(item.section))}</span>
                <span class="rewrite-safe ${changed ? '' : 'rewrite-no-change'}"><i class="fas ${changed ? 'fa-shield-halved' : 'fa-circle-check'}"></i> ${changed ? (item.fact_safe === false ? 'Original retained for safety' : 'Factual check passed') : 'No improvement required'}</span>
            </div>
            <div class="rewrite-columns">
                <div class="rewrite-copy rewrite-original"><h3>Original</h3><p>${escapeHtml(original)}</p></div>
                <div class="rewrite-copy rewrite-improved"><h3>${changed ? 'Improved' : 'Current text'}</h3><p>${escapeHtml(rewritten)}</p></div>
            </div>
            <p class="rewrite-reason"><strong>Why:</strong> ${escapeHtml(item.reason)}</p>
            ${asArray(item.keywords).length ? `<p class="rewrite-keywords"><strong>Supported keywords:</strong> ${escapeHtml(item.keywords.join(', '))}</p>` : ''}
            ${asArray(item.keyword_evidence).length ? `<p class="rewrite-keywords"><strong>Evidence:</strong> ${escapeHtml(item.keyword_evidence.map(evidence => `${evidence.keyword} (${evidence.source})`).join(', '))}</p>` : ''}
            ${asArray(item.safety_issues).length ? `<p class="rewrite-keywords"><strong>Safety check:</strong> Unsupported factual tokens were removed: ${escapeHtml(item.safety_issues.join(', '))}</p>` : ''}
            ${changed ? `<button type="button" class="copy-rewrite" data-copy-rewrite="${index}"><i class="fas fa-copy"></i> Copy improved text</button>` : ''}
        </article>
            `;
        })()}
    `).join(''));
}

async function loadRewrites() {
    const section = document.querySelector('.rewriter-section');
    const status = document.getElementById('rewriterStatus');
    if (!section || section.dataset.loaded === 'true' || !status) return;

    let analysis;
    try {
        analysis = JSON.parse(sessionStorage.getItem('analysisData') || '{}');
    } catch {
        setText('rewriterStatus', 'The saved analysis data is not available.');
        return;
    }

    if (!analysis.resume_text) {
        setText('rewriterStatus', 'Resume text is not available for rewriting. Please upload the resume again.');
        return;
    }

    setText('rewriterStatus', 'Preparing factual rewrite suggestions...');
    try {
        const draft = JSON.parse(sessionStorage.getItem('resumeDraft') || '{}');
        const response = await fetch('/rewrite', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                resume_text: analysis.resume_text,
                job_description: draft.jobDescription || '',
                analysis,
            }),
        });
        const payload = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(payload.error || 'Rewrite request failed');
        displayRewrites(payload);
        section.dataset.loaded = 'true';
    } catch (error) {
        setText('rewriterStatus', error.message || 'Rewrite suggestions could not be loaded.');
        setHtml('rewrites', '');
    }
}

async function copyRewrite(index, button) {
    const item = rewriteItems[index];
    if (!item) return;
    try {
        await navigator.clipboard.writeText(item.rewritten);
        const original = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied';
        setTimeout(() => { button.innerHTML = original; }, 1400);
    } catch {
        button.textContent = 'Copy unavailable';
    }
}

function displayResults(data) {
    const score = Number(data.overall_ats_score) || 0;
    const timestamp = new Date(data.analysis_timestamp);

    setText('resumeName', `Resume: ${data.resume_name || 'Unknown'}`);
    setText('timestamp', `Analyzed: ${Number.isNaN(timestamp.getTime()) ? 'Unknown' : timestamp.toLocaleString()}`);
    setText('scoreValue', `${score.toFixed(1)}%`);
    setText('scoreStatus', data.status || 'Analysis complete');
    setText('scoreDescription', score >= 75 ? 'Your resume shows strong alignment with this role.' : 'Review the insights below to strengthen your alignment.');

    displayScore(score);
    displayOverview(data);
    displayHealth(data);
    displayBreakdown(data.score_breakdown || {});
    displayStrengths(data.recommendation_details);
    displayPriorityRecommendations(data.recommendation_details);
    const evidence = data.resume_evidence || {};
    const resumeSkills = uniqueSkillValues(asArray(evidence.skills).map(item => item && item.value));
    const evidenceSkills = uniqueSkillValues(asArray(evidence.technologies).map(item => item && item.value));
    displayTags('resumeSkills', resumeSkills, 'No resume skills identified.');
    displayTags('matchedSkills', data.matched_skills, 'No matched skills found.');
    displayTags('missingSkills', data.missing_skills, 'All required skills are present.', true);
    displayTags('evidenceSkills', evidenceSkills, 'No evidence-backed skills available.');
    displaySemanticMatches(data.semantic_matches);
    displayCareerEligibility(data.career_eligibility);
    displayContact(data.contact);
    displayEducation(data.education);
    displayExperience(data.experience);
    displayProjects(data.projects);
    displayCertifications(data.certifications);
    displayAchievements(data.achievements);
    displayLanguages(data.languages);
    displayRecommendations(data.suggestions, data.recommendation_details);
    displayInterviewCoach(data.interview_coach, data.interview_questions);
    displayFormatting(data.formatting);
}

function showSection(section, button) {
    const sectionMap = {
        dashboard: 'resume-overview',
        insights: 'priority-improvements',
        strengths: 'strengths-section',
        interview: 'interview-section',
        rewriter: 'rewriter-section',
        formatting: 'formatting-details',
        education: 'education-details',
        experience: 'experience-details',
        projects: 'projects-details',
        skills: 'skills-section',
    };
    document.getElementById(sectionMap[section] || sectionMap.dashboard)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.querySelectorAll('.dashboard-nav .nav-btn').forEach(element => {
        element.classList.remove('active');
    });

    const navButtons = Array.from(document.querySelectorAll('.dashboard-nav .nav-btn[data-section]'));
    const activeButton = button || navButtons.find(element => element.dataset.section === section);
    activeButton?.classList.add('active');
    if (section === 'rewriter') loadRewrites();
}

async function downloadReport() {
    const button = document.querySelector('[data-download-report]');
    const data = sessionStorage.getItem('analysisData');
    if (!button || !data) return;
    const original = button.innerHTML;
    button.disabled = true;
    button.textContent = 'Generating PDF...';
    try {
        const response = await fetch('/generate_pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: data,
        });
        if (!response.ok) throw new Error('PDF generation failed');
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `resume-analysis-${new Date().toISOString().slice(0, 10)}.pdf`;
        link.click();
        URL.revokeObjectURL(url);
    } catch {
        window.alert('We could not generate the PDF. Please try again.');
    } finally {
        button.disabled = false;
        button.innerHTML = original;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', event => {
        const button = event.target.closest('[data-copy-rewrite]');
        if (button) copyRewrite(Number(button.dataset.copyRewrite), button);
        const action = event.target.closest('[data-action-target]');
        if (action) document.getElementById(action.dataset.actionTarget)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    const storedData = sessionStorage.getItem('analysisData');
    if (!storedData) {
        window.location.replace('/');
        return;
    }

    try {
        displayResults(JSON.parse(storedData));
        const view = new URLSearchParams(window.location.search).get('view');
        const section = view === 'recommendations'
            ? 'insights'
            : view === 'interview'
                ? 'interview'
                : view === 'formatting'
                    ? 'formatting'
                        : view === 'rewriter'
                            ? 'rewriter'
                    : ['education', 'experience', 'projects', 'skills'].includes(view)
                        ? view
                        : 'dashboard';
        showSection(section);
        const rewriterSection = document.getElementById('rewriter-section');
        if (rewriterSection && 'IntersectionObserver' in window) {
            const observer = new IntersectionObserver(entries => {
                if (entries.some(entry => entry.isIntersecting)) {
                    loadRewrites();
                    observer.disconnect();
                }
            }, { rootMargin: '160px' });
            observer.observe(rewriterSection);
        }
    } catch {
        sessionStorage.removeItem('analysisData');
        window.location.replace('/');
    }
});
