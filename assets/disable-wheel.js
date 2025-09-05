// assets/disable-wheel.js
document.addEventListener("wheel", function(e) {
    var el = document.activeElement;
    if (el && el.tagName === "INPUT" && el.type === "number") {
        e.preventDefault();
    }
}, { passive: false });
