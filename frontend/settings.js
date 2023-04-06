import { base_url, check_creds, creds } from '/utils.js';

async function init_checkbox() {
    let response = await fetch(base_url + "/enable", {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    });

    let enabled = (await response.text()) === "true";
    document.getElementById("enable").checked = enabled;
}

async function update_threschold(dir) {
    let response = await fetch(base_url + "/threshold/" + dir, {
        method: "POST",
        headers: {
            "Authorization": creds,
	},
        body: JSON.stringify({
            temperature: document.getElementById(dir + "-threshold").value
        })
    });
}

async function update_enable() {
    let response = await fetch(base_url + "/enable", {
        method: "POST",
        headers: {
            "Authorization": creds,
	},
        body: JSON.stringify({
            enable: document.getElementById("enable").checked
        })
    });
}

async function init_threshold(dir) {
    let response = await fetch(base_url + "/threshold/" + dir, {
        method: "GET",
        headers: {
            "Authorization": creds,
	}
    });

    let threshold = await response.json();
    document.getElementById(dir + "-threshold").value = threshold;
}

async function init() {
    await check_creds();
    init_checkbox();
    init_threshold("inner");
    init_threshold("outer");
}

document.getElementById("update-values").addEventListener("click", (e) => {
    e.preventDefault();
    update_enable();
    update_threschold("inner");
    update_threschold("outer");
    return false;
});

init();
