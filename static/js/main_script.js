const chartData = {
    labels: ["Food", "Utilities", "Luxury", "Savings"],
    data: [10, 20, 30, 40],
};

const myChart = document.querySelector(".my-chart");

new Chart(myChart, {
    type: "doughnut",
    data: {
        labels: chartData.labels,
        datasets: [
            {
                label: "Category Spend / Save",
                data: chartData.data,
            },
        ],
    },
    options: {
        borderWidth: 5,
        hoverBorderWidth: 0,
        plugins: {
            legend: {
                FontFaceSet: "Questrial",
            },
        },
    },
});

const graphIncomeData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    data: [30000, 40000, 37000, 22000, 32000, 27000],
};

const graphExpenseData = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    data: [15000, 20000, 18000, 16000, 24000, 19000],
};

const myGraphChart = document.querySelector(".my-graph-chart");

new Chart(myGraphChart, {
    type: "line",
    data: {
        labels: graphIncomeData.labels,
        graphExpenseData,
        datasets: [
            {
                label: "Income",
                data: graphIncomeData.data,
            },
            {
                label: "Expenses",
                data: graphExpenseData.data,
            },
        ],
    },
    options: {
        plugins: {
            legend: {
                FontFaceSet: "Questrial",
            },
        },
    },
});

document
    .getElementById("category-select")
    .addEventListener("change", function () {
        let selectedValue = this.value;
        let secondSelectContainer = document.getElementById(
            "second-select-container"
        );
        let secondSelect = document.getElementById("second-select");

        if (selectedValue === "purchase") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="snacks">Snacks</option>
         <option value="groceries">Groceries</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else if (selectedValue === "sell") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="electronics">Electronics</option>
         <option value="furniture">Furniture</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else {
            secondSelect.innerHTML = '<option value=""></option>';
            secondSelectContainer.style.display = "none";
        }
    });

document
    .getElementById("second-select")
    .addEventListener("change", function () {
        let secondValue = this.value;
        let transactAmountContainer = document.getElementById(
            "transact-amount-container"
        );
        let transactAmount = document.getElementById("transact-amount");

        if (secondValue !== "") {
            transactAmountContainer.style.display = "block";
        } else {
            transactAmountContainer.style.display = "none";
        }
    });
