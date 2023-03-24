const base_url = "https://cooler.amos.wtf/api"

var creds

async function check_creds() {
    creds = localStorage.getItem("credentials");

    const response = await fetch(base_url, {
        method: "GET",
        headers: {
            "Authorization": creds,
        }
    })
    return response.status === 200
}

export { check_creds, base_url, creds };
