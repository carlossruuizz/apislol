const img = document.getElementById("cat-img");
const skeleton = document.getElementById("skeleton");
const meta = document.getElementById("meta");
const btn = document.getElementById("btn");

async function fetchCat() {
    btn.disabled = true;
    img.classList.remove("loaded");
    skeleton.classList.remove("hidden");
    meta.textContent = "";

    try {
        const res = await fetch("/cat");
        if (!res.ok) throw new Error("Server error " + res.status);
        const data = await res.json();

        const fresh = new Image();
        fresh.onload = () => {
            img.src = fresh.src;
            img.classList.add("loaded");
            skeleton.classList.add("hidden");
            const tags = data.tags && data.tags.length ? data.tags.join(", ") : "no tags";
            meta.textContent = "id: " + data.id + "  ·  " + tags;
            btn.disabled = false;
        };
        fresh.onerror = () => showError("Image failed to load.");
        fresh.src = data.url;
    } catch (err) {
        showError(err.message);
    }
}

function showError(msg) {
    skeleton.classList.add("hidden");
    meta.textContent = "Error: " + msg;
    btn.disabled = false;
}

fetchCat();
