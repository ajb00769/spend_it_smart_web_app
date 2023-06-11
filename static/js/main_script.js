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
