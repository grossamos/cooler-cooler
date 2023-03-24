import { base_url, check_creds } from '/utils.js';

async function login() {
    let access_key = document.getElementById("accesskey").value;
    localStorage.setItem("credentials", access_key);
    if (await check_creds()) {
        window.location.replace("/")
    } else {
        document.getElementById("error").style["display"] = "inline";
    }
}

document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();
    login();
    return false;
});

export default login;
