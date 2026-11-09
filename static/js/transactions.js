
document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("transactionSearch");
    const filterSelect = document.getElementById("transactionFilter");
    const tableBody = document.getElementById("transactionTableBody");

    if (!searchInput || !filterSelect || !tableBody) {
        return;
    }

    function filterTransactions() {

        const searchValue = searchInput.value.toLowerCase().trim();
        const selectedType = filterSelect.value;

        const rows = tableBody.querySelectorAll(".transaction-row");

        rows.forEach(function (row) {

            const rowText = row.textContent.toLowerCase();
            const transactionType = row.dataset.type;

            const matchesSearch = rowText.includes(searchValue);

            const matchesType =
                selectedType === "ALL" ||
                transactionType === selectedType;

            row.style.display =
                matchesSearch && matchesType ? "" : "none";

        });

    }

    searchInput.addEventListener("input", filterTransactions);

    filterSelect.addEventListener("change", filterTransactions);

});
