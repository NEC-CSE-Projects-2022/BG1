/*
=====================================
 Login Script (Frontend only)
 Uses localStorage credentials
 No backend required
=====================================
*/

const form = document.getElementById("loginForm");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const errorBox = document.getElementById("errorBox");

form.addEventListener("submit", function (e) {

    e.preventDefault();

    const email = emailInput.value.trim().toLowerCase();
    const password = passwordInput.value;

    errorBox.innerText = "";

    /* ===== Validation ===== */
    if (!email || !password) {
        errorBox.innerText = "Please enter email and password";
        return;
    }

    /* ===== Get stored credentials from signup ===== */
    const storedEmail = localStorage.getItem("userEmail");
    const storedPassword = localStorage.getItem("userPassword");

    /* ===== If user never registered ===== */
    if (!storedEmail || !storedPassword) {
        errorBox.innerText = "No account found. Please register first.";
        return;
    }

    /* ===== Button UX ===== */
    const btn = form.querySelector(".login-btn");
    btn.disabled = true;
    btn.innerText = "Logging in...";

    setTimeout(() => {

        /* ===== Check credentials ===== */
        if (email === storedEmail && password === storedPassword) {

            // Save login session
            localStorage.setItem("isLoggedIn", "true");

            alert("Login successful!");

            /* ✅ FIXED REDIRECT */
            window.location.href = "/";   // ← changed from /home

        } else {
            errorBox.innerText = "Invalid email or password";
        }

        btn.disabled = false;
        btn.innerText = "Login";

    }, 400);
});
