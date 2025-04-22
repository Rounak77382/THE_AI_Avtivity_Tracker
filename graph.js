document.getElementById('datePicker').style.display = 'none';

document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('datePicker');
    const mainDataButton = document.getElementById('mainData');
    const shortDataButton = document.getElementById('shortData');
    const aiEvaluatedDataButton = document.getElementById('aiEvaluatedData');
    let chartInstance; // Keep a reference to the Chart.js instance
    let pieChartInstance;

    datePicker.addEventListener('change', updateChart);

    datePicker.addEventListener('change', function() {
        document.querySelector('.Box2').innerHTML = '';
        document.querySelector('.screen-time').innerHTML = '';
    });

    mainDataButton.addEventListener('click', function() {
        updateChart('');
    });

    shortDataButton.addEventListener('click', function() {
        updateChart('_short');
    });

    aiEvaluatedDataButton.addEventListener('click', function() {
        updateChart('_AI_Evaluated');
    });

    function updateChart(option) {
        const selectedDate = datePicker.value;

        // Clear the previous chart if it exists
        if (chartInstance) {
            chartInstance.destroy();
        }

        

        if (option instanceof Event) {
            option = '';
        }

        // In a real application, you would fetch data related to the selected date
        // For this example, we'll simulate fetching data based on the selected date
        const chartData = `datas/${selectedDate}${option}.csv`;

        const filePath = chartData.substring(chartData.lastIndexOf('/') + 1, chartData.lastIndexOf('.csv'));
        document.querySelector('.Title').textContent = filePath;

        d3.csv(chartData).then(function(datapoints) {
            var name = [];
            var time = [];

            for (let i = 0; i < datapoints.length; i++) {
                name.push(datapoints[i].name);
                time.push(datapoints[i].time / 60);
            }

            total_time = time.reduce((a, b) => a + b, 0);

            const screenTimeElement = document.querySelector('.screen-time');
            console.log(screenTimeElement);
            const hours = Math.floor(total_time / 60);
            const minutes = Math.floor(total_time % 60);
            screenTimeElement.textContent = `${hours} hrs ${minutes} mins`;

            const ctx = document.getElementById('myChart');

            if (name.length > 40) {
                const sortedIndices = time
                    .map((value, index) => ({ value, index }))
                    .sort((a, b) => b.value - a.value)
                    .slice(0, 40)
                    .map(({ index }) => index);
            
                const topNames = sortedIndices.map(index => name[index]);
                const topTimes = sortedIndices.map(index => time[index]);
            
                const originalOrder = sortedIndices
                    .map((index, i) => ({ index, name: topNames[i], time: topTimes[i] }))
                    .sort((a, b) => a.index - b.index);
            
                name = originalOrder.map(item => item.name);
                time = originalOrder.map(item => item.time);
            }
            
            console.log(name);
            console.log(time);

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: name,
                    datasets: [{
                        label: 'Time(min)',
                        data: time,
                        borderWidth: 1,
                        backgroundColor: '#3CD8FF' // Change the color here
                    }]
                },
                options: {
                    indexAxis: 'x',
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Name --->'
                            },
                            ticks: {
                                font: { size: 15 }
                            },
                            grid: {
                                display: false // Disable grid lines
                            }
                        },
                        x: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Time(min) --->'
                            },
                            ticks: {
                                display: false
                            },
                            grid: {
                                display: false // Disable grid lines
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: true
                        }
                    }
                },
                responsive: true,
            });
        });

        if (pieChartInstance) {
            pieChartInstance.destroy();
        }
    

        const pieData123 = `datas/${selectedDate}_prod_percent.json`;
        const date123 = `datas/${selectedDate}.csv`;

        d3.csv(date123).then(data => {
            // Sort data by time in descending order
            data.sort((a, b) => b.time - a.time);
        
            // Get the top 5 processes
            let topProcesses = data.slice(0, 5);
        
            // Get the Box 2 div
            let box2 = document.querySelector('.Box2');
        
            // Clear any existing content
            box2.innerHTML = '';
            
            let title = document.createElement('p');
            title.textContent = 'TOP 5 PROCESSES:';
            box2.appendChild(title);

            // Create and append new elements for each process
            topProcesses.forEach(process => {
                let processElement = document.createElement('div');
                processElement.className = 'process-item'; // Add class
                let list = document.createElement('ul');
                let listItem = document.createElement('li');
                listItem.className = 'process-list-item'; // Add class
            
                let displayName = process.name;
                if (displayName.length > 20) {
                    displayName = displayName.substring(0, 30) + '...';
                }
                let time = parseFloat(process.time/60).toFixed(2);
                listItem.innerHTML = `<span class="process-name">${displayName}</span> : <span class="process-time">${time}min</span>`;
                
                list.appendChild(listItem);
                processElement.appendChild(list);
                box2.appendChild(processElement);
            });


        }).catch(error => {
            console.log(error);
        });
        console.log(pieData123);
        // Fetch the JSON file
        let data = [];

        fetch(pieData123)
            .then(response => response.json())
            .then(jsonData => {
                // Extract only the numeric values
                data = Object.values(jsonData).map(Number);
        
                const pieCtx = document.getElementById('pieChart').getContext('2d');
                const labels = ['Productive', 'Unproductive'];
                const backgroundColors = ['#40FF3C ','#FF3C3C ']; // Colors for each activity
        
                const pieData = {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: backgroundColors,
                    }]
                };
        
                pieChartInstance = new Chart(pieCtx, {
                    type: 'doughnut',
                    data: pieData,
                    options: {
                        plugins: {
                            legend: {
                                display: true,
                                position: 'bottom',
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error:', error));

            // Add picker-selected class to the clicked button in Box1
            const box1Buttons = document.querySelectorAll('.Box1 button');
            box1Buttons.forEach(button => {
                button.addEventListener('click', function() {
                box1Buttons.forEach(btn => btn.classList.remove('picker-selected'));
                this.classList.add('picker-selected');
                });
            });
    }
});


function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours} : ${minutes} : ${seconds}`;
    document.getElementById('clock').textContent = timeString;
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
    fetch('/detect_afk')
        .then(response => response.json())
        .then(data => {
            const box3 = document.querySelector('.Box3'); 

            box3.innerHTML = data.result;
            box3.style.color = '#3498db';
            box3.style.fontSize = '17px'; 
            box3.style.padding = '15px'; 
            box3.style.fontFamily = 'Arial, Helvetica, sans-serif';
            box3.style.fontWeight = '500';
            box3.style.display = 'flex';
            box3.style.justifyContent = 'center';
            box3.style.alignItems = 'center';

            // Change the image in Box3
            const image = document.createElement('img');
            image.src = `./animations/${data.result}.gif`; // Update with the correct image path
            image.alt = 'Description of image';
            image.style.width = '70px'; // Adjust the size as needed
            image.style.height = '70px'; // Adjust the size as needed

            // Append the image to Box3
            box3.appendChild(image);
        });
}