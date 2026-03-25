/*
=====================================
 Signup Script (Frontend only)
 Stores credentials in localStorage
 No backend required
=====================================
*/

const form = document.getElementById("signupForm");
const errorMsg = document.getElementById("errorMsg");

form.addEventListener("submit", function (e) {

    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    errorMsg.innerText = "";

    /* ===== Validation ===== */

    if (!name || !email || !password || !confirmPassword) {
        errorMsg.innerText = "All fields are required";
        return;
    }

    if (password.length < 6) {
        errorMsg.innerText = "Password must be at least 6 characters";
        return;
    }

    if (password !== confirmPassword) {
        errorMsg.innerText = "Passwords do not match";
        return;
    }

    /* ===== Prevent duplicate account ===== */
    const storedEmail = localStorage.getItem("userEmail");

    if (storedEmail && storedEmail === email) {
        errorMsg.innerText = "Account already exists. Please login.";
        return;
    }

    /* ===== Store credentials ===== */
    localStorage.setItem("userName", name);
    localStorage.setItem("userEmail", email);
    localStorage.setItem("userPassword", password);

    alert("Signup successful! Please login.");

    /* redirect to login */
    window.location.href = "/login";
});
