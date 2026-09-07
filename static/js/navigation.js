if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
}

if (window.location.hash) {
    history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
}

const resetScrollPosition = () => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);

    requestAnimationFrame(() => {
        document.documentElement.style.removeProperty("scroll-behavior");
    });
};

window.addEventListener("DOMContentLoaded", resetScrollPosition);
window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
        resetScrollPosition();
    }
});
