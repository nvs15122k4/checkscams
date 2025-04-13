document.addEventListener("DOMContentLoaded", function () {
    console.log("CheckScam - Giao diện đã sẵn sàng!");
    document.querySelectorAll(".nav-link").forEach((item) => {
        item.addEventListener("mouseenter", function () {
            this.classList.add("fw-bold");
        });
        item.addEventListener("mouseleave", function () {
            this.classList.remove("fw-bold");
        });
    });
});
