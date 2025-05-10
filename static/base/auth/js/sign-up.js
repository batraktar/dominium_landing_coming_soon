// === Генералізоване оновлення лейблу ===
function updateLabel(inputId, labelId) {
    const input = document.getElementById(inputId)
    const label = document.getElementById(labelId)
    const hasText = input.value.trim() !== ''
    const isFocused = document.activeElement === input

    if (hasText || isFocused) {
        label.classList.add('active')
    } else {
        label.classList.remove('active')
    }
}

// === Email-форма ===
function validateEmail() {
    const emailInput = document.getElementById('email')
    const email = emailInput.value.trim()
    const errorMsg = document.getElementById('email-error')
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    emailInput.classList.remove('border-red-500', 'focus:border-red-500', 'border-green-500', 'focus:border-green-500')

    if (email === '') {
        errorMsg.classList.add('hidden')
        emailInput.classList.add('border-gray-300')
        return
    }

    if (emailRegex.test(email)) {
        errorMsg.classList.add('hidden')
        emailInput.classList.add('border-green-500', 'focus:border-green-500')
    } else {
        errorMsg.classList.remove('hidden')
        emailInput.classList.add('border-red-500', 'focus:border-red-500')
    }
}

function checkEmailPasswordsMatch() {
    const password = document.getElementById('password').value
    const confirmInput = document.getElementById('confirm')
    const confirm = confirmInput.value
    const errorMsg = document.getElementById('confirm-error')

    confirmInput.classList.remove('border-green-500', 'border-red-500', 'focus:border-green-500', 'focus:border-red-500')

    if (confirm === '') {
        errorMsg.classList.add('hidden')
        confirmInput.classList.add('border-gray-300')
        return
    }

    if (password === confirm) {
        errorMsg.classList.add('hidden')
        confirmInput.classList.remove('border-gray-300')
        confirmInput.classList.add('border-green-500', 'focus:border-green-500')
    } else {
        errorMsg.classList.remove('hidden')
        confirmInput.classList.remove('border-gray-300')
        confirmInput.classList.add('border-red-500', 'focus:border-red-500')
    }
}

// === Telegram-форма ===
function checkTelegramPasswordsMatch() {
    const password = document.getElementById('tg-password').value
    const confirmInput = document.getElementById('tg-confirm')
    const confirm = confirmInput.value
    const errorMsg = document.getElementById('tg-confirm-error')

    confirmInput.classList.remove('border-green-500', 'border-red-500', 'focus:border-green-500', 'focus:border-red-500')

    if (confirm === '') {
        errorMsg.classList.add('hidden')
        confirmInput.classList.add('border-gray-300')
        return
    }

    if (password === confirm) {
        errorMsg.classList.add('hidden')
        confirmInput.classList.remove('border-gray-300')
        confirmInput.classList.add('border-green-500', 'focus:border-green-500')
    } else {
        errorMsg.classList.remove('hidden')
        confirmInput.classList.remove('border-gray-300')
        confirmInput.classList.add('border-red-500', 'focus:border-red-500')
    }
}

// === Toggle visibility ===
function togglePassword() {
    const input = document.getElementById('password')
    input.type = input.type === 'password' ? 'text' : 'password'
    updateLabel('password', 'password-label')
}

function toggleConfirmPassword() {
    const input = document.getElementById('confirm')
    input.type = input.type === 'password' ? 'text' : 'password'
    updateLabel('confirm', 'confirm-label')
}

function toggleTelegramPassword() {
    const input = document.getElementById('tg-password')
    input.type = input.type === 'password' ? 'text' : 'password'
    updateLabel('tg-password', 'tg-password-label')
}

function toggleTelegramConfirmPassword() {
    const input = document.getElementById('tg-confirm')
    input.type = input.type === 'password' ? 'text' : 'password'
    updateLabel('tg-confirm', 'tg-confirm-label')
}

function goBackToChoice() {
    document.getElementById('email-signup')?.classList.add('hidden');
    document.getElementById('telegram-signup')?.classList.add('hidden');
    document.getElementById('method-select')?.classList.remove('hidden');

    const wrapper = document.getElementById('signup-wrapper');
    wrapper?.classList.remove('min-h-[500px]');
    wrapper?.classList.remove('min-h-[580px]');
    wrapper?.classList.add('min-h-auto');
}



function showEmailForm() {
    hideAllForms();
    document.getElementById('signup-wrapper').classList.remove('min-h-[300px]');
    document.getElementById('signup-wrapper').classList.add('min-h-[500px]');
    document.getElementById('email-signup').classList.remove('hidden');
}


function showTelegramForm() {
    hideAllForms();
    document.getElementById('signup-wrapper').classList.remove('min-h-[300px]');
    document.getElementById('signup-wrapper').classList.add('min-h-[500px]');
    document.getElementById('telegram-signup').classList.remove('hidden');
}


function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}


function setupTelegramUsernameCheck() {
    const tgInput = document.getElementById("telegram_username");
    const tgError = document.getElementById("telegram-error");

    tgInput?.addEventListener("blur", async () => {
        const username = tgInput.value.trim().replace(/^@/, "");
        if (!username) return;

        try {
            const response = await fetch(`/ajax/check-telegram/?username=${encodeURIComponent(username)}`);
            const data = await response.json();

            if (!data.available) {
                tgError.textContent = "Цей Telegram-username вже зайнятий.";
                tgError.classList.remove("hidden");
                tgInput.classList.add("border-red-500");
            } else {
                tgError.classList.add("hidden");
                tgInput.classList.remove("border-red-500");
            }
        } catch (err) {
            tgError.textContent = "Помилка перевірки. Спробуйте пізніше.";
            tgError.classList.remove("hidden");
        }
    });
}


// === DOM READY ===
document.addEventListener('DOMContentLoaded', () => {
    setupTelegramUsernameCheck();

    // Email форма
    const emailFields = [
        { inputId: 'email', labelId: 'email-label' },
        { inputId: 'password', labelId: 'password-label' },
        { inputId: 'confirm', labelId: 'confirm-label' },
        { inputId: 'email_code', labelId: 'email-code-label' }
    ]

    emailFields.forEach(({ inputId, labelId }) => {
        const input = document.getElementById(inputId)
        if (input) {
            input.addEventListener('input', () => updateLabel(inputId, labelId))
            input.addEventListener('focus', () => updateLabel(inputId, labelId))
            input.addEventListener('blur', () => updateLabel(inputId, labelId))
            updateLabel(inputId, labelId)
        }
    })


    document.getElementById('email')?.addEventListener('blur', validateEmail)
    document.getElementById('confirm')?.addEventListener('input', checkEmailPasswordsMatch)

    document.querySelectorAll('form[action*="register_email"]').forEach(form => {
        form.addEventListener('submit', (e) => {
            const password = document.getElementById('password')?.value
            const confirm = document.getElementById('confirm')?.value
            const errorMsg = document.getElementById('confirm-error')

            if (password !== confirm) {
                e.preventDefault()
                errorMsg?.classList.remove('hidden')
            } else {
                errorMsg?.classList.add('hidden')
            }
        })
    })


    document.querySelectorAll('form[action*="register_via_telegram"]').forEach(form => {
        form.addEventListener('submit', (e) => {
            const password = document.getElementById('tg-password')?.value
            const confirm = document.getElementById('tg-confirm')?.value
            const errorMsg = document.getElementById('tg-confirm-error')

            if (password !== confirm) {
                e.preventDefault()
                errorMsg?.classList.remove('hidden')
            } else {
                errorMsg?.classList.add('hidden')
            }
        })
    })


    // Telegram форма
    const tgFields = [
        { inputId: 'telegram_username', labelId: 'telegram-label' },
        { inputId: 'tg-password', labelId: 'tg-password-label' },
        { inputId: 'tg-confirm', labelId: 'tg-confirm-label' }
    ]

    tgFields.forEach(({ inputId, labelId }) => {
        const input = document.getElementById(inputId)
        if (input) {
            input.addEventListener('input', () => updateLabel(inputId, labelId))
            input.addEventListener('focus', () => updateLabel(inputId, labelId))
            input.addEventListener('blur', () => updateLabel(inputId, labelId))
            updateLabel(inputId, labelId)
        }
    })

    document.getElementById('tg-confirm')?.addEventListener('input', checkTelegramPasswordsMatch)
})
