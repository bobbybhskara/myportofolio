if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
}

const navigationEntry = performance.getEntriesByType("navigation")[0];
const shouldResetScroll = !window.location.hash || navigationEntry?.type === "reload";

if (window.location.hash && shouldResetScroll) {
    history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
}

const resetScrollPosition = () => {
    document.documentElement.style.scrollBehavior = "auto";
    window.scrollTo(0, 0);

    requestAnimationFrame(() => {
        document.documentElement.style.removeProperty("scroll-behavior");
    });
};

if (shouldResetScroll) {
    window.addEventListener("DOMContentLoaded", resetScrollPosition);
}

window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
        resetScrollPosition();
    }
});
