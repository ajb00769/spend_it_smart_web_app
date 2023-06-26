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
    type: "bar",
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
         <option value="resto">I Ate Outside</option>
         <option value="clothing">Clothing</option>
         <option value="shoes">Shoes</option>
         <option value="bags">Bags</option>
         <option value="luxury">Luxury Item ($1000+)</option>
         <option value="electronics">TV / PC / Sound System / Etc</option>
         <option value="utilities">I paid my utility bills (electricity, water, internet, etc)</option>
         <option value="transpo">I bought gasoline / spent on transportation</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else if (selectedValue === "sell") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="oldelectronics">Owned Electronics</option>
         <option value="oldfurniture">Owned Furniture</option>
         <option value="oldclothes">Old Clothes</option>
         <option value="oldshoes">Old Shoes</option>
         <option value="oldbags">Old Bags</option>
         <option value="oldluxury">Old Luxury Item</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else if (selectedValue === "income") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="salary">I earned my regular wage</option>
         <option value="businesssvc">I earned money from my service business</option>
         <option value="businesssku">I sold products from my business</option>
         <option value="allowance">I got some allowance</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else if (selectedValue === "invest") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="stocks">Stocks</option>
         <option value="bonds">Bonds</option>
         <option value="mfund">Mutual Funds</option>
         <option value="insurance">Investment Type Insurace</option>
         <option value="crypto">Crypto</option>
         <option value="preciousmetals">Precious Metals (i.e. Gold / Silver Bars or Forex, not jewelry)</option>
       `;
            secondSelect.innerHTML = DOMPurify.sanitize(optionsHTML);
            secondSelectContainer.style.display = "block";
        } else if (selectedValue === "debt") {
            let optionsHTML = `
         <option value="" hidden></option>
         <option value="studentloan">Student Loan</option>
         <option value="salaryloan">Salary Loan</option>
         <option value="carloan">Car Loan</option>
         <option value="mortgage">I took our a Mortgage</option>
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

document
    .getElementById("entry-form")
    .addEventListener("submit", function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData,
        })
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                if (data.success) {
                    document.getElementById("save-success").style.display =
                        "block";
                    document.getElementById("save-error").style.display =
                        "none";
                    setTimeout(function () {
                        $("#entry-form")[0].reset();
                        document.getElementById("save-success").style.display =
                            "none";
                        $("#log-entry-modal").modal("hide");
                    }, 1500);
                    setTimeout(function () {
                        location.reload();
                    }, 2000);
                } else {
                    document.getElementById("save-error").style.display =
                        "block";
                    document.getElementById("save-success").style.display =
                        "none";
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    });
