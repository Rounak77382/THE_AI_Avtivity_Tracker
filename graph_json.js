document.getElementById("datePicker").style.display = "none";

document.addEventListener("DOMContentLoaded", function () {
  const datePicker = document.getElementById("datePicker");
  const mainDataButton = document.getElementById("mainData");
  const shortDataButton = document.getElementById("shortData");
  const aiEvaluatedDataButton = document.getElementById("aiEvaluatedData");
  let chartInstance; // Keep a reference to the Chart.js instance
  let pieChartInstance;

  datePicker.addEventListener("change", updateChart);

  datePicker.addEventListener("change", function () {
    document.querySelector(".Box2").innerHTML = "";
    document.querySelector(".screen-time").innerHTML = "";
    document.querySelector(".Title").textContent = "";
  });

  mainDataButton.addEventListener("click", function () {
    updateChart("");
  });

  shortDataButton.addEventListener("click", function () {
    updateChart("_short");
  });

  aiEvaluatedDataButton.addEventListener("click", function () {
    updateChart("_AI_Evaluated");
  });

  async function updateChart(option) {
    const selectedDate = datePicker.value;

    // Clear the previous chart if it exists
    if (chartInstance) {
      chartInstance.destroy();
    }

    if (option instanceof Event) {
      option = "";
    }

    const chartData = `new_datas/${selectedDate}${option}.json`;

    const filePath = chartData.substring(
      chartData.lastIndexOf("/") + 1,
      chartData.lastIndexOf(".json")
    );
    document.querySelector(".Title").textContent = filePath;

    try {
      const response = await fetch(chartData);
      const datapoints = await response.json();
      var name = [];
      var time = [];

      for (let i = 0; i < datapoints.length; i++) {
        let decodedName;
        try {
          decodedName = decodeURIComponent(escape(datapoints[i].name));
        } catch (e) {
          console.error(`Error decoding name: ${datapoints[i].name}`, e);
          decodedName = datapoints[i].name;
        }
        name.push(decodedName);
        time.push(datapoints[i].time / 60);
      }

      total_time = time.reduce((a, b) => a + b, 0);

      const screenTimeElement = document.querySelector(".screen-time");

      const hours = Math.floor(total_time / 60);
      const minutes = Math.floor(total_time % 60);
      screenTimeElement.textContent = `${hours} hrs ${minutes} mins`;

      const ctx = document.getElementById("myChart");

      if (name.length > 40) {
        const sortedIndices = time
          .map((value, index) => ({ value, index }))
          .sort((a, b) => b.value - a.value)
          .slice(0, 40)
          .map(({ index }) => index);

        const topNames = sortedIndices.map((index) => name[index]);
        const topTimes = sortedIndices.map((index) => time[index]);

        const originalOrder = sortedIndices
          .map((index, i) => ({
            index,
            name: topNames[i],
            time: topTimes[i],
          }))
          .sort((a, b) => a.index - b.index);

        name = originalOrder.map((item) => item.name);
        time = originalOrder.map((item) => item.time);
      }

      chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: name,
          datasets: [
            {
              label: "Process Name",
              data: time,
              borderWidth: 1,
              backgroundColor: "#3CD8FF", // Change the color here
            },
          ],
        },
        options: {
          indexAxis: "x",
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Time(min)  --->",
              },
              ticks: {
                font: { size: 15 },
              },
              grid: {
                display: false, // Disable grid lines
              },
            },
            x: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Process Name  --->",
              },
              ticks: {
                display: false,
              },
              grid: {
                display: false, // Disable grid lines
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              enabled: true,
            },
          },
        },
        responsive: true,
      });

      const aidata_path = `new_datas/${selectedDate}_AI_Evaluated.json`;
      const date_path = `new_datas/${selectedDate}.json`;

      let aidata123 = [];
      let date123 = [];

      const aidataResponse = await fetch(aidata_path);
      if (aidataResponse.ok) {
        aidata123 = await aidataResponse.json();

        const dateResponse = await fetch(date_path);
        if (!dateResponse.ok) {
          throw new Error(
            `HTTP error! status: ${dateResponse.status} - ${dateResponse.statusText}`
          );
        }
        date123 = await dateResponse.json();

        let new_datas = [];

        for (let i = 0; i < aidata123.length; i++) {
          new_datas.push({
            name: aidata123[i].output,
            time: date123[i].time,
          });
        }

        let productivity_time = 0;
        let unproductivity_time = 0;

        for (let i = 0; i < new_datas.length; i++) {
          const timeValue = parseInt(new_datas[i].time, 10);
          if (isNaN(timeValue)) {
            console.warn(
              `Invalid time value for entry ${i}: ${new_datas[i].time}`
            );
            continue;
          }
          if (new_datas[i].name === "true") {
            productivity_time += timeValue;
          } else {
            unproductivity_time += timeValue;
          }
        }

        const productivity_data = {
          "Productive Percentage":
            (productivity_time / (productivity_time + unproductivity_time)) *
            100,
          "Unproductive Percentage":
            (unproductivity_time / (productivity_time + unproductivity_time)) *
            100,
        };

        if (pieChartInstance) {
          pieChartInstance.destroy();
        }

        const pieCtx = document.getElementById("pieChart").getContext("2d");
        const labels = ["Productive", "Unproductive"];
        const backgroundColors = ["#40FF3C ", "#FF3C3C "]; // Colors for each activity

        const pieData = {
          labels: labels,
          datasets: [
            {
              data: Object.values(productivity_data).map(Number),
              backgroundColor: backgroundColors,
            },
          ],
        };

        pieChartInstance = new Chart(pieCtx, {
          type: "doughnut",
          data: pieData,
          options: {
            plugins: {
              legend: {
                display: true,
                position: "bottom",
              },
            },
          },
        });
      } else {
        console.warn(`AI data not available for ${selectedDate}`);
        if (pieChartInstance) {
          pieChartInstance.destroy();
          pieChartInstance = null;
        }
      }

      const productivityResponse = await fetch(chartData);
      const data = await productivityResponse.json();

      // Sort data by time in descending order
      data.sort((a, b) => b.time - a.time);

      // Get the top 5 processes
      let topProcesses = data.slice(0, 5);

      // Get the Box 2 div
      let box2 = document.querySelector(".Box2");

      // Clear any existing content
      box2.innerHTML = "";

      let title = document.createElement("p");
      title.textContent = "TOP 5 PROCESSES:";
      box2.appendChild(title);

      // Create and append new elements for each process
      topProcesses.forEach((process) => {
        let processElement = document.createElement("div");
        processElement.className = "process-item"; // Add class
        let list = document.createElement("ul");
        let listItem = document.createElement("li");
        listItem.className = "process-list-item"; // Add class

        let displayName = decodeURIComponent(escape(process.name));
        if (displayName.length > 20) {
          displayName = displayName.substring(0, 30) + "...";
        }
        let time = parseFloat(process.time / 60).toFixed(2);
        listItem.innerHTML = `<span class="process-name">${displayName}</span> : <span class="process-time">${time}min</span>`;

        list.appendChild(listItem);
        processElement.appendChild(list);
        box2.appendChild(processElement);
      });
    } catch (error) {
      console.error("Error fetching data:", error);
      if (pieChartInstance) {
        pieChartInstance.destroy();
        pieChartInstance = null;
      }
    }

    // Add picker-selected class to the clicked button in Box1
    const box1Buttons = document.querySelectorAll(".Box1 button");
    box1Buttons.forEach((button) => {
      button.addEventListener("click", function () {
        box1Buttons.forEach((btn) => btn.classList.remove("picker-selected"));
        this.classList.add("picker-selected");
      });
    });
  }
});

function updateClock() {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");
  const timeString = `${hours} : ${minutes} : ${seconds}`;
  document.getElementById("clock").textContent = timeString;
}

// Update the clock every second
setInterval(updateClock, 1000);

// Initial call to display the time
updateClock();

flatpickr("#datePicker", {
  inline: true, // display the calendar inline
  static: true, // prevent the calendar from auto-closing
});

// Call the function immediately when the page loads
fetchDataAndUpdateBox3();

// Then call the function every 5 seconds
setInterval(fetchDataAndUpdateBox3, 5000);

function fetchDataAndUpdateBox3() {
  fetch("/detect_afk")
    .then((response) => response.json())
    .then((data) => {
      const box3 = document.querySelector(".Box3");

      box3.innerHTML = data.result;
      box3.style.color = "#3498db";
      box3.style.fontSize = "17px";
      box3.style.padding = "15px";
      box3.style.fontFamily = "Arial, Helvetica, sans-serif";
      box3.style.fontWeight = "500";
      box3.style.display = "flex";
      box3.style.justifyContent = "center";
      box3.style.alignItems = "center";

      // Change the image in Box3
      const image = document.createElement("img");
      image.src = `./animations/${data.result}.gif`; // Update with the correct image path
      image.alt = "Description of image";
      image.style.width = "70px"; // Adjust the size as needed
      image.style.height = "70px"; // Adjust the size as needed

      // Append the image to Box3
      box3.appendChild(image);
    });
}
