/**
 * Welcome Portal - Interactive Frontend Application
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const welcomeForm = document.getElementById('welcome-form');
    const nameInput = document.getElementById('visitor-name');
    const roleInput = document.getElementById('visitor-role');
    const submitBtn = document.getElementById('welcome-submit-btn');
    
    // Result elements
    const resultBox = document.getElementById('welcome-result-box');
    const resultHeadline = document.getElementById('result-headline');
    const resultNote = document.getElementById('result-note');
    const resultAvatar = document.getElementById('result-avatar');
    const resultTimestamp = document.getElementById('result-timestamp');
    const copyGreetingBtn = document.getElementById('copy-greeting-btn');

    // Telemetry & Visitor feed elements
    const visitorsList = document.getElementById('visitors-list');
    const refreshVisitorsBtn = document.getElementById('refresh-visitors-btn');
    const metricTotalVisitors = document.getElementById('metric-total-visitors');
    const metricServerUptime = document.getElementById('metric-server-uptime');
    const systemStatusText = document.getElementById('system-status-text');
    const systemStatusPill = document.getElementById('system-status-pill');

    let currentGreetingText = '';

    // ==========================================
    // 1. Initial Data Fetch & Health Telemetry
    // ==========================================
    async function checkHealth() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const data = await res.json();
                systemStatusText.textContent = `Online • ${data.environment.toUpperCase()}`;
                metricServerUptime.textContent = Math.round(data.uptime_seconds);
                metricTotalVisitors.textContent = data.total_visitors_served;
            } else {
                systemStatusText.textContent = 'API Degraded';
            }
        } catch (err) {
            systemStatusText.textContent = 'Backend Offline';
        }
    }

    async function loadVisitors() {
        try {
            const res = await fetch('/api/visitors');
            if (!res.ok) throw new Error('Failed to fetch visitors');
            const visitors = await res.json();

            metricTotalVisitors.textContent = visitors.length;

            if (visitors.length === 0) {
                visitorsList.innerHTML = '<div class="empty-state">No visitors registered yet. Be the first!</div>';
                return;
            }

            visitorsList.innerHTML = visitors.map(v => {
                const initials = v.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'V';
                const formattedTime = new Date(v.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                return `
                    <div class="visitor-item">
                        <div class="visitor-avatar-mini" style="background-color: ${v.avatar_color || '#6366f1'}">
                            ${initials}
                        </div>
                        <div class="visitor-details">
                            <div class="visitor-details-name">${escapeHtml(v.name)}</div>
                            <div class="visitor-details-role">${escapeHtml(v.role || 'Visitor')} • ${formattedTime}</div>
                        </div>
                        <span class="visitor-style-badge">${escapeHtml(v.style)}</span>
                    </div>
                `;
            }).join('');
        } catch (error) {
            visitorsList.innerHTML = '<div class="empty-state">Unable to load visitor feed</div>';
        }
    }

    // ==========================================
    // 2. Handle Form Submission
    // ==========================================
    welcomeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = nameInput.value.trim();
        const role = roleInput.value.trim() || 'Explorer';
        const styleInput = document.querySelector('input[name="style"]:checked');
        const style = styleInput ? styleInput.value : 'warm';

        if (!name) {
            nameInput.focus();
            return;
        }

        // Loading state
        submitBtn.disabled = true;
        const originalBtnText = submitBtn.querySelector('.btn-text').textContent;
        submitBtn.querySelector('.btn-text').textContent = 'Creating Welcome...';

        try {
            const response = await fetch('/api/welcome', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, role, style })
            });

            if (!response.ok) {
                throw new Error('Server returned an error');
            }

            const data = await response.json();

            // Display customized welcome
            resultHeadline.textContent = data.message;
            resultNote.textContent = data.personalized_note;
            currentGreetingText = `${data.message}\n${data.personalized_note}`;

            // Avatar initials
            const initials = data.visitor.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
            resultAvatar.textContent = initials;
            resultAvatar.style.backgroundColor = data.visitor.avatar_color || '#6366f1';
            resultTimestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

            // Reveal result box
            resultBox.classList.remove('hidden');

            // Trigger celebration confetti
            triggerConfetti();

            // Refresh recent visitors feed and counters
            loadVisitors();
            checkHealth();

            // Smooth scroll to result if on mobile
            if (window.innerWidth < 768) {
                resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        } catch (err) {
            alert('Could not submit welcome: ' + err.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = originalBtnText;
        }
    });

    // ==========================================
    // 3. Copy Greeting to Clipboard
    // ==========================================
    copyGreetingBtn.addEventListener('click', () => {
        if (!currentGreetingText) return;
        navigator.clipboard.writeText(currentGreetingText).then(() => {
            const orig = copyGreetingBtn.textContent;
            copyGreetingBtn.textContent = '✅ Copied!';
            setTimeout(() => {
                copyGreetingBtn.textContent = orig;
            }, 2000);
        });
    });

    refreshVisitorsBtn.addEventListener('click', () => {
        loadVisitors();
        checkHealth();
    });

    // ==========================================
    // 4. Lightweight Confetti Animation Engine
    // ==========================================
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    let confettiParticles = [];
    let animationFrameId = null;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function triggerConfetti() {
        const colors = ['#6366f1', '#a855f7', '#06b6d4', '#ec4899', '#f59e0b', '#10b981'];
        confettiParticles = [];

        for (let i = 0; i < 75; i++) {
            confettiParticles.push({
                x: window.innerWidth / 2,
                y: window.innerHeight / 3,
                vx: (Math.random() - 0.5) * 14,
                vy: (Math.random() - 0.7) * 15,
                size: Math.random() * 8 + 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                rotation: Math.random() * 360,
                rotationSpeed: (Math.random() - 0.5) * 10,
                opacity: 1
            });
        }

        if (!animationFrameId) {
            updateConfetti();
        }
    }

    function updateConfetti() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        let active = false;

        for (let p of confettiParticles) {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.35; // gravity
            p.rotation += p.rotationSpeed;
            p.opacity -= 0.012; // fade out

            if (p.opacity > 0) {
                active = true;
                ctx.save();
                ctx.globalAlpha = Math.max(0, p.opacity);
                ctx.translate(p.x, p.y);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
                ctx.restore();
            }
        }

        if (active) {
            animationFrameId = requestAnimationFrame(updateConfetti);
        } else {
            animationFrameId = null;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    // Helper: Escape HTML to avoid XSS
    function escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Initial load & periodic heartbeat
    checkHealth();
    loadVisitors();
    setInterval(checkHealth, 15000);
});
