const levelInput = document.getElementById("level");
const levelLabel = document.getElementById("level-label");
const tagList = document.getElementById("tag-list");
const results = document.getElementById("results");

const LEVEL_NAMES = ["Beginner", "Beginner", "Intermediate", "Intermediate", "Advanced", "Advanced"];

let activeTag = "";
let debounceTimer = null;

async function loadTags() {
    try {
        const res = await fetch("/recommend/levels");
        const data = await res.json();
        data.tags.forEach(tag => {
            const btn = document.createElement("button");
            btn.className = "tag";
            btn.textContent = tag;
            btn.onclick = () => toggleTag(btn, tag);
            tagList.appendChild(btn);
        });
    } catch (_) { }
}

function toggleTag(btn, tag) {
    if (activeTag === tag) {
        activeTag = "";
        btn.classList.remove("active");
    } else {
        document.querySelectorAll(".tag").forEach(b => b.classList.remove("active"));
        activeTag = tag;
        btn.classList.add("active");
    }
    fetchRecommendations();
}

async function fetchRecommendations() {
    const level = levelInput.value;
    const params = new URLSearchParams({ level });
    if (activeTag) params.set("tag", activeTag);

    results.innerHTML = skeletons(3);

    try {
        const res = await fetch("/recommend?" + params);
        if (!res.ok) throw new Error("Server error " + res.status);
        const data = await res.json();
        renderBoards(data.boards);
    } catch (err) {
        results.innerHTML = '<p class="empty">Error: ' + err.message + "</p>";
    }
}

function renderBoards(boards) {
    if (!boards.length) {
        results.innerHTML = '<p class="empty">No boards match this filter. Try removing the tag.</p>';
        return;
    }
    results.innerHTML = boards.map(card).join("");
}

function card(b) {
    const price = "$" + b.price_usd;
    return (
        '<div class="card">' +
        '<img src="' + b.image + '" alt="' + b.name + '" loading="lazy" />' +
        '<div class="card-body">' +
        '<div class="card-name">' + b.name + "</div>" +
        '<div class="card-desc">' + b.description + "</div>" +
        '<div class="card-specs">' +
        '<span class="spec">' + b.specs.flash_kb + "KB flash</span>" +
        '<span class="spec">' + b.specs.ram_kb + "KB RAM</span>" +
        '<span class="spec">' + b.specs.clock_mhz + "MHz</span>" +
        '<span class="spec">' + b.specs.pins + " pins</span>" +
        "</div>" +
        "</div>" +
        '<div class="card-footer">' +
        '<span class="price">' + price + "</span>" +
        '<a href="' + b.store + '" target="_blank">Buy →</a>' +
        "</div>" +
        "</div>"
    );
}

function skeletons(n) {
    const s = '<div class="card skeleton-card"><div class="sk-img"></div><div class="sk-body"><div class="sk-line w60"></div><div class="sk-line w90"></div><div class="sk-line w40"></div></div></div>';
    return Array(n).fill(s).join("");
}

levelInput.addEventListener("input", () => {
    levelLabel.textContent = LEVEL_NAMES[levelInput.value];
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(fetchRecommendations, 180);
});

loadTags();
fetchRecommendations();
