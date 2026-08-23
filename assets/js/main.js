// ── Theme (Dark Mode) ─────────────────────────
(function initTheme() {
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = stored || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
})();

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}

// ── Year ──────────────────────────────────────
document.getElementById('year').textContent = new Date().getFullYear();

// ── Mobile Menu ───────────────────────────────
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuClose = document.getElementById('mobile-menu-close');
const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

function toggleMenu(show) {
    mobileMenuBtn.setAttribute('aria-expanded', String(show));
    if (show) {
        mobileMenu.classList.remove('hidden');
        mobileMenuOverlay.classList.remove('hidden');
        mobileMenu.offsetHeight; // force reflow
        mobileMenu.classList.remove('hidden-drawer');
        mobileMenuOverlay.classList.replace('opacity-0', 'opacity-100');
        document.body.style.overflow = 'hidden';
    } else {
        mobileMenu.classList.add('hidden-drawer');
        mobileMenuOverlay.classList.replace('opacity-100', 'opacity-0');
        document.body.style.overflow = '';
        setTimeout(() => {
            mobileMenu.classList.add('hidden');
            mobileMenuOverlay.classList.add('hidden');
        }, 300);
    }
}

mobileMenuBtn.addEventListener('click', () => toggleMenu(true));
mobileMenuClose.addEventListener('click', () => toggleMenu(false));
mobileMenuOverlay.addEventListener('click', () => toggleMenu(false));
mobileNavLinks.forEach(link => link.addEventListener('click', () => toggleMenu(false)));

// ── Smooth Scroll ─────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        e.preventDefault();
        const target = document.querySelector(targetId);
        if (target) window.scrollTo({ top: target.offsetTop - 64, behavior: 'smooth' });
    });
});

// ── Chatbot Logic ─────────────────────────────
const CHATBOT_API_URL = 'https://rudra-g-23-rudra-portfolio-rag-chatbot-api.hf.space/chat';
const CHATBOT_TIMEOUT_MS = 45000;

const chatModal = document.getElementById('chatbot-modal');
const chatBubble = document.getElementById('chatbot-bubble');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatStartupNotice = document.getElementById('chatbot-startup-notice');
let isFirstMessage = true;

// Bounce the attraction bubble a few times, then hide it automatically.
if (chatBubble) {
    chatBubble.addEventListener('animationend', () => {
        chatBubble.classList.add('hidden');
    });
}

// ── Mobile Keyboard: pin modal to top to prevent input being hidden ──
chatInput.addEventListener('focus', () => {
    if (window.innerWidth < 640) {
        chatModal.classList.remove('bottom-24');
        chatModal.classList.add('fixed');
        chatModal.classList.remove('absolute');
        chatModal.style.bottom = 'auto';
        chatModal.style.top = '1rem';
        chatModal.style.maxHeight = 'calc(100dvh - 2rem)';

        // Add a slight delay to scroll to bottom after layout shift
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
});

chatInput.addEventListener('blur', () => {
    if (window.innerWidth < 640) {
        // Restore floating bottom position
        chatModal.classList.add('bottom-24');
        chatModal.classList.remove('fixed');
        chatModal.classList.add('absolute');
        chatModal.style.bottom = '';
        chatModal.style.top = '';
        chatModal.style.maxHeight = '';
    }
});

function toggleChat() {
    const opening = chatModal.classList.contains('hidden');
    chatModal.classList.toggle('hidden');
    chatModal.classList.toggle('flex');
    document.getElementById('chatbot-toggle').setAttribute('aria-expanded', String(opening));
    if (chatBubble && !chatBubble.classList.contains('hidden')) {
        chatBubble.classList.add('hidden');
    }
    if (opening) {
        chatInput.focus();
        if (chatStartupNotice) chatStartupNotice.classList.remove('hidden');
    }
}

function closeChatBubble() {
    chatBubble.classList.add('hidden');
}

function askBot(query) {
    if (chatModal.classList.contains('hidden')) {
        chatModal.classList.remove('hidden');
        chatModal.classList.add('flex');
        document.getElementById('chatbot-toggle').setAttribute('aria-expanded', 'true');
        if (chatStartupNotice) chatStartupNotice.classList.remove('hidden');
    }
    if (chatBubble && !chatBubble.classList.contains('hidden')) {
        chatBubble.classList.add('hidden');
    }

    // Populate input but don't auto-send — user reviews before submitting
    chatInput.value = query;
    chatInput.focus();
}

function sendSuggestion(text) {
    chatInput.value = text;
    handleChatSubmit(new Event('submit'));
}

// ── Render Message ────────────────────────────
function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = sender === 'user' ? 'flex items-end gap-2 justify-end' : 'flex items-end gap-2';

    let contentHtml = '';
    if (sender === 'user') {
        contentHtml = `
            <div class="bg-[#5e17eb] text-white rounded-2xl rounded-br-sm px-4 py-3 max-w-[85%] text-sm shadow-sm break-words">
                ${text}
            </div>
        `;
    } else {
        const parsedText = marked.parse(text);
        contentHtml = `
            <div class="w-8 h-8 rounded-full bg-white border border-zinc-200 flex items-center justify-center shrink-0 shadow-sm p-1">
                <img src="assets/artificial-intelligence.png" alt="AI" class="w-full h-full object-contain">
            </div>
            <div class="bg-white border border-zinc-200 text-zinc-800 rounded-2xl rounded-bl-sm px-4 py-3 max-w-[85%] text-sm shadow-sm prose prose-sm prose-p:my-1 prose-ul:my-1 prose-li:my-0 prose-a:text-[#5e17eb] prose-a:no-underline hover:prose-a:underline break-words">
                ${parsedText}
            </div>
        `;
    }

    msgDiv.innerHTML = contentHtml;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ── Chat Submit ───────────────────────────────
async function handleChatSubmit(e) {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = '';

    const suggestions = document.getElementById('chat-suggestions');
    if (suggestions && !suggestions.classList.contains('hidden')) {
        suggestions.classList.add('hidden');
    }

    addMessage(text, 'user');

    let infoPopup = null;
    if (isFirstMessage) {
        isFirstMessage = false;
        infoPopup = document.createElement('div');
        infoPopup.className = 'text-center text-xs text-zinc-600 my-2 bg-yellow-50 border border-yellow-200 rounded-lg p-2 mx-auto w-11/12 shadow-sm transition-opacity duration-300';
        infoPopup.innerHTML = '<i class="fa-solid fa-clock text-yellow-500 mr-1"></i> As this is your first message, the server might take some time to wake up and respond. Please be patient!';
        chatMessages.appendChild(infoPopup);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        setTimeout(() => {
            if (infoPopup && infoPopup.parentNode) {
                infoPopup.style.opacity = '0';
                setTimeout(() => infoPopup.remove(), 300);
            }
        }, 20000);
    }

    // Typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'flex items-end gap-2 w-full';
    typingDiv.innerHTML = `
        <div class="w-8 h-8 rounded-full bg-white border border-zinc-200 flex items-center justify-center shrink-0 shadow-sm p-1 mb-auto mt-2">
            <img src="assets/artificial-intelligence.png" alt="AI" class="w-full h-full object-contain">
        </div>
        <div class="bg-white border border-zinc-200 rounded-2xl rounded-bl-sm px-4 py-3 text-sm shadow-sm min-w-[240px]">
            <div class="flex flex-col relative pl-4 border-l-2 border-zinc-100 ml-2 space-y-4 py-1">

                <div class="relative" id="search-step-1">
                    <div class="absolute -left-[21px] top-0.5 w-2.5 h-2.5 bg-[#5e17eb] rounded-full ring-4 ring-white animate-pulse indicator-dot"></div>
                    <div class="text-xs text-zinc-600 font-medium flex items-center gap-2 step-text"><i class="fa-solid fa-brain text-[#5e17eb]"></i> Understanding the query...</div>
                </div>

                <div class="relative hidden" id="search-step-2">
                    <div class="absolute -left-[21px] top-0.5 w-2.5 h-2.5 bg-[#5e17eb] rounded-full ring-4 ring-white animate-pulse indicator-dot"></div>
                    <div class="text-xs text-zinc-600 font-medium flex items-center gap-2 step-text"><i class="fa-solid fa-database text-[#5e17eb]"></i> Searching from knowledge db...</div>
                </div>

                <div class="relative hidden" id="search-step-3">
                    <div class="absolute -left-[21px] top-0.5 w-2.5 h-2.5 bg-[#5e17eb] rounded-full ring-4 ring-white animate-pulse indicator-dot"></div>
                    <div class="text-xs text-zinc-600 font-medium flex items-center gap-2 step-text"><i class="fa-solid fa-pen-nib text-[#5e17eb]"></i> Generating response...</div>
                </div>

            </div>
        </div>
    `;
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const step1 = document.getElementById('search-step-1');
    const step2 = document.getElementById('search-step-2');
    const step3 = document.getElementById('search-step-3');

    setTimeout(() => {
        if (step1) {
            step1.querySelector('.indicator-dot').classList.remove('animate-pulse', 'bg-[#5e17eb]');
            step1.querySelector('.indicator-dot').classList.add('bg-green-500');
            step1.querySelector('.step-text').innerHTML = '<i class="fa-solid fa-check text-green-500"></i> Understood the query';
        }
        if (step2) step2.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 800);

    setTimeout(() => {
        if (step2) {
            step2.querySelector('.indicator-dot').classList.remove('animate-pulse', 'bg-[#5e17eb]');
            step2.querySelector('.indicator-dot').classList.add('bg-green-500');
            step2.querySelector('.step-text').innerHTML = '<i class="fa-solid fa-check text-green-500"></i> Searched from knowledge db';
        }
        if (step3) step3.classList.remove('hidden');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 2000);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CHATBOT_TIMEOUT_MS);

    try {
        const response = await fetch(CHATBOT_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: text }),
            signal: controller.signal
        });

        const data = await response.json();

        let botText = "No response";
        if (typeof data === 'string') {
            botText = data;
        } else if (data.response) {
            botText = data.response;
        } else if (data.answer) {
            botText = data.answer;
        } else if (data.message) {
            botText = data.message;
        } else if (data.text) {
            botText = data.text;
        } else {
            botText = JSON.stringify(data);
        }

        if (infoPopup && infoPopup.parentNode) {
            infoPopup.remove();
        }
        document.getElementById('typing-indicator').remove();
        addMessage(botText, 'bot');
    } catch (error) {
        if (infoPopup && infoPopup.parentNode) {
            infoPopup.remove();
        }
        document.getElementById('typing-indicator').remove();
        const message = error.name === 'AbortError'
            ? "The assistant is taking longer than expected to respond. Please try again in a moment."
            : "Sorry, I encountered an error connecting to the server.";
        addMessage(message, 'bot');
    } finally {
        clearTimeout(timeoutId);
    }
}

/* ─── Project Info Toggle ─────────────────── */
/**
 * Toggles the detail panel for a project card.
 * Closes any other currently open panel first to keep one open at a time.
 * @param {HTMLElement} btn - The info button that was clicked.
 */
function toggleInfo(btn) {
    const card = btn.closest('.project-card');
    const details = card.querySelector('.project-details');
    const isOpen = details.classList.contains('open');

    // Close all other open panels first
    document.querySelectorAll('.project-details.open').forEach(el => {
        el.classList.remove('open');
        const otherBtn = el.closest('.project-card').querySelector('.project-info-btn');
        if (otherBtn) otherBtn.classList.remove('active');
    });

    // Toggle current
    if (!isOpen) {
        details.classList.add('open');
        btn.classList.add('active');
    }
}
