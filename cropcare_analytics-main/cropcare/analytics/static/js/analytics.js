document.addEventListener("DOMContentLoaded", function() {
    // Notification toggle
    const notificationIcon = document.querySelector(".notification");
    const notificationContent = document.querySelector(".notification-content");
    if (notificationIcon && notificationContent) {
        notificationIcon.addEventListener("click", function() {
            notificationContent.classList.toggle("show");
        });
    }

    // Initialize charts
    initCharts();
    
    // Start polling for sensor data
    startSensorPolling();
});

// Global variables
const globalConditions = {
    temperature: null,
    moisture: null,
    ph: null,
    humidity: null
};

const colorPriority = {
    '#8E1616': 4, // Dark Red (Highest)
    '#EA7300': 3, // Orange
    '#FFD63A': 2, // Yellow
    '#33b5e5': 1, // Blue (Green class)
    '#706D54': 0 // Grey
};

const colorToClass = {
    '#8E1616': 'status-red',
    '#EA7300': 'status-orange',
    '#FFD63A': 'status-yellow',
    '#33b5e5': 'status-green',
    '#706D54': 'status-grey'
};

let phChart, humidChart, tempChart, moistChart;

function initCharts() {
    const initialMinuteData = Array(1440).fill(null);
    const minuteLabels = Array.from({length: 1440}, (_, i) => {
        const hours = Math.floor(i / 60);
        const mins = i % 60;
        return `${hours % 12 || 12}:${mins.toString().padStart(2, '0')} ${hours >= 12 ? 'PM' : 'AM'}`;
    });

    // pH Chart
    const phCtx = document.getElementById('phChart').getContext('2d');
    phChart = new Chart(phCtx, getChartConfig(
        'pH Levels', 
        'pH Value', 
        'rgb(255, 165, 0)', 
        'rgba(255, 165, 0, .1)', 
        4, 9,
        minuteLabels,
        initialMinuteData,
        Array(1440).fill(6.5)
    ));

    // Humidity Chart
    const humidCtx = document.getElementById('humidChart').getContext('2d');
    humidChart = new Chart(humidCtx, getChartConfig(
        'Humidity Levels', 
        'Humidity (%)', 
        'rgb(98, 98, 255)', 
        'rgba(98, 98, 255, .1)', 
        30, 90,
        minuteLabels,
        initialMinuteData,
        Array(1440).fill(65)
    ));

    // Temperature Chart
    const tempCtx = document.getElementById('tempChart').getContext('2d');
    tempChart = new Chart(tempCtx, getChartConfig(
        'Temperature Levels', 
        'Temperature (°C)', 
        'rgb(255, 69, 69)', 
        'rgba(255, 69, 69, 0.1)', 
        10, 35,
        minuteLabels,
        initialMinuteData,
        Array(1440).fill(25)
    ));

    // Moisture Chart
    const moistCtx = document.getElementById('moistChart').getContext('2d');
    moistChart = new Chart(moistCtx, getChartConfig(
        'Moisture Levels', 
        'Moisture (%)', 
        'rgb(0, 197, 7)', 
        'rgba(0, 197, 7, 0.1)', 
        15, 60,
        minuteLabels,
        initialMinuteData,
        Array(1440).fill(35)
    ));

    // Handle window resize
    window.addEventListener('resize', function() {
        [phChart, humidChart, tempChart, moistChart].forEach(chart => {
            if (chart) chart.resize();
        });
    });
}

function getChartConfig(title, yAxisTitle, borderColor, bgColor, minY, maxY, labels, data, idealData) {
    return {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: `${yAxisTitle.split(' (')[0]}`,
                    data: [...data],
                    borderColor: borderColor,
                    backgroundColor: bgColor,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'Ideal Range',
                    data: idealData,
                    borderColor: 'rgb(54, 162, 235)',
                    borderDash: [5, 5],
                    backgroundColor: 'transparent',
                    tension: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1000,
                easing: 'easeOutQuad'
            },
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: { size: 16 }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    labels: { boxWidth: 12, font: { size: 12 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: minY,
                    max: maxY,
                    title: { display: true, text: yAxisTitle },
                    ticks: { font: { size: 12 } }
                },
                x: {
                    grid: { display: true },
                    ticks: {
                        font: { size: 9 },
                        maxRotation: 90,
                        minRotation: 90,
                        autoSkip: true,
                        maxTicksLimit: 24,
                        callback: function(value, index) {
                            if (index % 60 === 0) {
                                const hours = Math.floor(index / 60);
                                return `${hours % 12 || 12} ${hours >= 12 ? 'PM' : 'AM'}`;
                            }
                            return null;
                        }
                    }
                }
            }
        }
    };
}

function startSensorPolling() {
    // Initial fetch
    fetchSensorData();
    
    // Set up polling
    setInterval(fetchSensorData, 5000);
}

function fetchSensorData() {
    fetch('/get-sensor-data/')
        .then(response => response.json())
        .then(data => {
            updateSensorDisplay('temperature', data.temperature);
            updateSensorDisplay('humidity', data.humidity);
            updateSensorDisplay('moisture', data.moisture);
            updateSensorDisplay('ph', data.ph_level);
            updateCharts();
        })
        .catch(error => {
            console.error('Error fetching sensor data:', error);
        });
}

function updateSensorDisplay(sensorType, data) {
    const display = document.getElementById(`${sensorType}Sensor`);
    const status = document.getElementById(`${sensorType}Status`);
    
    if (!display || !status) return;

    if (data.value === "-" || data.value === null) {
        display.innerText = "OFF";
        display.style.color = "#ff4444";
        display.style.fontStyle = "italic";
        status.innerText = "OFF";
        globalConditions[sensorType] = null;
    } else {
        const unit = sensorType === 'temperature' ? '°C' : sensorType === 'ph' ? '' : '%';
        display.innerText = data.value + unit;
        display.style.color = "";
        display.style.fontStyle = "";
        status.innerText = data.condition;

        const color = getStatusColor(data.condition);
        status.style.color = color;
        status.style.fontStyle = "normal";
        globalConditions[sensorType] = color;
    }
    updateNotificationDot();
}

function getStatusColor(condition) {
    switch (condition) {
        case "Very Cold":
        case "Cold":
        case "Very Hot":
        case "Hot":
        case "Very Dry":
        case "Dry":
        case "Submerged":
        case "Strongly Acidic":
        case "Strongly Alkaline":
            return "#8E1616";
        case "Warm":
        case "Moderately Acidic":
        case "Moderately Alkaline":
            return "#EA7300";
        case "Normal":
        case "Comfortable":
        case "Wet":
        case "Neutral":
            return "#33b5e5";
        case "Humid":
        case "Moist":
            return "#FFD63A";
        case "Idle":
            return "#706D54";
        default:
            return "#000";
    }
}

function updateNotificationDot() {
    const notificationDot = document.getElementById('notificationDot');
    if (!notificationDot) return;

    let highestPriority = -1;
    let highestColor = null;

    Object.values(globalConditions).forEach(color => {
        if (color && colorPriority[color] !== undefined) {
            const priority = colorPriority[color];
            if (priority > highestPriority) {
                highestPriority = priority;
                highestColor = color;
            }
        }
    });

    notificationDot.className = 'status-dot';
    if (highestColor !== null) {
        notificationDot.classList.add(colorToClass[highestColor], 'show');
        notificationDot.style.display = 'block';
    } else {
        notificationDot.style.display = 'none';
    }
}

function updateCharts() {
    const currentMinute = getCurrentMinute();
    
    updateChart(phChart, 'phSensor', currentMinute);
    updateChart(humidChart, 'humiditySensor', currentMinute);
    updateChart(tempChart, 'tempSensor', currentMinute);
    updateChart(moistChart, 'moistureSensor', currentMinute);
}

function getCurrentMinute() {
    const now = new Date();
    return now.getHours() * 60 + now.getMinutes();
}

function updateChart(chart, sensorId, currentMinute) {
    const element = document.getElementById(sensorId);
    if (!element || !chart) return;
    
    const text = element.innerText;
    if (text === "OFF" || text === "ERR") return;
    
    const value = parseFloat(text.replace(/[^0-9.-]/g, ''));
    if (isNaN(value)) return;
    
    chart.data.datasets[0].data[currentMinute] = value;
    
    if (currentMinute === 0) {
        chart.data.datasets[0].data = [...chart.data.datasets[0].data.slice(1440), ...Array(1440).fill(null)];
    }
    
    chart.update('none');
}