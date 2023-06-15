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

function modalHandler() {
  $("#log-entry-modal").modal("show");
}

$("#entry-form").submit(function (e) {
  e.preventDefault();
  const form = $(e.target);
  const content = $("#entry-form").serialize();
  $.ajax({
    url: "/submit",
    data: {
      content: $("#entry-form").serialize(),
    },
    success: function () {
      $("#log-entry-modal").modal("hide");
    },
  });
});
