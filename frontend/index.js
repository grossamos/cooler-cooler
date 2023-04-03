import { base_url, check_creds, creds } from '/utils.js';

var plug_is_on = false;
var chart_drawn = false;

async function testCredentials() {
    if (!await check_creds()) {
        window.location.replace("/login.html");
    }
}

async function init() {
    await testCredentials();
    init_temperature();
    update_status();
    show_inner_temp();
}

async function update_status() {
    let response = await fetch(base_url + "/device", {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    });

    let plug_status = await response.json();
    plug_is_on = plug_status.is_on;
    update_toggle_text();

    document.getElementById("power-status").innerHTML = plug_status.current_power;

    if (!chart_drawn) {
        draw_power_chart(plug_status);
    }
}

function format_date(date, show_time) {
    let min = date.getMinutes();
    if (min == 0) {
        min = "00";
    } else if (min < 10) {
        min = "0" + min;
    }
    return date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear() + (show_time? " " + date.getHours() + ":" + min : "");
}

function draw_power_chart(plug_status) {

    let labels = [];

    for (let i = 1; i <= plug_status.daily_power.length; i++) {
        let date = new Date(new Date() - plug_status.daily_power.length + i);
        labels.push(format_date(date));
    }

    const ctx = document.getElementById('consumption-chart');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Power Consumption in kV',
                data: plug_status.daily_power,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    chart_drawn = true;
}

async function init_temperature() {
    let inner_respose = await fetch(base_url + "/temperature/inner", {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    })
    inner_respose = await inner_respose.json()
    let outer_respose = await fetch(base_url + "/temperature/outer", {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    })
    outer_respose = await outer_respose.json()

    const ctx_in = document.getElementById('temp-inside-chart');
    new Chart(ctx_in, {
        type: 'line',
        data: {
            labels: inner_respose.history.map(row => format_date(new Date(row.time * 1000), true)),
            datasets: [{
                label: 'Inside Temperature (in C)',
                data: inner_respose.history.map(row => row.temperature),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    document.getElementById("temp-in-status").innerHTML = inner_respose.current_temp

    const ctx_out = document.getElementById('temp-outside-chart');
    new Chart(ctx_out, {
        type: 'line',
        data: {
            labels: outer_respose.history.map(row => format_date(new Date(row.time * 1000), true)),
            datasets: [{
                label: 'Outside Temperature (in C)',
                data: outer_respose.history.map(row => row.temperature),
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    document.getElementById("temp-out-status").innerHTML = outer_respose.current_temp
}

async function show_inner_temp() {
    let enable_inner_response = await fetch(base_url + "/enable", {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    })
    let enable = await enable_inner_response.json();

    if (!enable) {
        document.getElementById("inside-temperature").style["display"] = "none";
    }
}

async function toggle_power() {
    await fetch(base_url + "/device", {
        method: "POST",
        headers: {
            "Authorization": creds,
        },
        body: JSON.stringify({
            is_on: !plug_is_on
        })
    });
    plug_is_on = !plug_is_on;
    update_toggle_text();
    document.getElementById("power-status").innerHTML = "Loading...";
    await update_status();
}

function update_toggle_text() {
    if (plug_is_on) {
        document.getElementById("power-toggle").innerHTML = "Turn Off";
    } else {
        document.getElementById("power-toggle").innerHTML = "Turn On";
    }
}

document.getElementById("power-toggle").addEventListener("click", (e) => {
    e.preventDefault();
    toggle_power();
    return false;
});

init()

