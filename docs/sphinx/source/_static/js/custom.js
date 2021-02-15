function addGithubButton() {
    const button = `
        <iframe src="https://ghbtns.com/github-btn.html?user=dmlls&repo=jizt&type=star&count=true" 
        frameborder="0" scrolling="0" width="150" height="20" title="GitHub" style="width: 30%; margin: 0 auto 5px auto;"></iframe>
    `;
    document.querySelector("#rtd-search-form").insertAdjacentHTML('beforebegin', button);
}

function addTocEntry(caption, link) {
    const entry = `
        <p class="caption" style="padding:0;">
            <span class="caption-text">
            <a href="${link}" style="padding:0; color:#55a5d9; line-height: 32px; padding: 0 1.618em;">${caption}</a>
            </span>
        </p>
    `;
    document.querySelector(".wy-menu, .wy-menu-vertical").insertAdjacentHTML('beforeend', entry);
}

function onLoad() {
    addGithubButton();
    addTocEntry("Docs API REST", "https://docs.api.jizt.it");
}

window.addEventListener("load", onLoad);
