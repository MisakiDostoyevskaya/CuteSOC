// CuteSOC dashboard interactions (no dependencies).
(function () {
    "use strict";

    var toast = document.getElementById("toast");
    var toastTimer;

    function showToast(message) {
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add("show");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () {
            toast.classList.remove("show");
        }, 1600);
    }

    // Severity filter: apply as soon as it changes.
    var select = document.querySelector('.filters select[name="severity"]');
    if (select) {
        select.addEventListener("change", function () {
            select.form.submit();
        });
    }

    // Press "/" to jump to the IP search box.
    var ipInput = document.querySelector('.filters input[name="ip"]');
    document.addEventListener("keydown", function (event) {
        var tag = (event.target.tagName || "").toLowerCase();
        if (event.key === "/" && ipInput && tag !== "input" && tag !== "select") {
            event.preventDefault();
            ipInput.focus();
        }
    });

    // Click an IP to copy it.
    document.querySelectorAll(".copy-ip").forEach(function (el) {
        el.addEventListener("click", function () {
            var ip = el.textContent.trim();
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(ip).then(
                    function () { showToast("Copied " + ip + " ♡"); },
                    function () { showToast("Could not copy"); }
                );
            } else {
                showToast("Clipboard not available");
            }
        });
    });

    // Sortable table columns.
    var table = document.getElementById("alerts-table");
    if (!table) return;
    var tbody = table.tBodies[0];

    function cellValue(row, index, type) {
        var cell = row.cells[index];
        if (!cell) return "";
        if (type === "sev") {
            var badge = cell.querySelector("[data-rank]");
            return badge ? Number(badge.dataset.rank) : 0;
        }
        var text = cell.textContent.trim();
        return type === "num" ? Number(text) || 0 : text.toLowerCase();
    }

    function sortBy(th) {
        var rows = Array.prototype.slice.call(tbody.rows).filter(function (r) {
            return !r.querySelector(".empty-state");
        });
        if (rows.length < 2) return;

        var index = th.cellIndex;
        var type = th.dataset.sort;
        var asc = !th.classList.contains("sorted-asc");

        table.querySelectorAll("th").forEach(function (h) {
            h.classList.remove("sorted-asc", "sorted-desc");
        });
        th.classList.add(asc ? "sorted-asc" : "sorted-desc");

        rows.sort(function (a, b) {
            var x = cellValue(a, index, type);
            var y = cellValue(b, index, type);
            if (x < y) return asc ? -1 : 1;
            if (x > y) return asc ? 1 : -1;
            return 0;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
    }

    table.querySelectorAll("th[data-sort]").forEach(function (th) {
        th.addEventListener("click", function () { sortBy(th); });
        th.addEventListener("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                sortBy(th);
            }
        });
    });
})();
