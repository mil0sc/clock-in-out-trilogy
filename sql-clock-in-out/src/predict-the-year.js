import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function WorkHoursDisplay() {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        fetch('/api/calculated-hours/')
            .then(response => response.json())
            .then(data => {
                const preparedData = prepareChartData(data);
                setChartData(preparedData);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    return (
        <div>
            <h2>Work Hours Data Visualization</h2>
            {chartData && Object.keys(chartData).length > 0 ? (
              <Bar data={chartData} options={chartOptions} />
            ) : (
              <p>Loading data...</p>
            )}
        </div>
    );
}

function prepareChartData(data) {
    const jobRoles = data.map(item => item.job_role);
    const hoursSoFar = data.map(item => item.hours_so_far);
    const predictedTotalHours = data.map(item => item.predicted_total_hours);
    const targetHours = data.map(item => item.target_hours);
    const monthsPassed = data[0]?.months_passed; // Safely access months_passed from the first item

    return {
        labels: jobRoles,
        datasets: [
            {
                label: `Hours So Far in ${monthsPassed} Month${monthsPassed > 1 ? 's' : ''}`,
                data: hoursSoFar,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
            {
                label: 'Year-End Predicted Hours',
                data: predictedTotalHours,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
            },
            {
                label: 'Annual Target Hours',
                data: targetHours,
                backgroundColor: 'rgba(255, 206, 86, 0.5)',
            },
        ],
    };
}


const chartOptions = {
    responsive: true,
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                // Use a callback to format the tick labels without commas
                callback: function(value) {
                    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "");
                }
            }
        },
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
        },
        tooltip: {
            callbacks: {
                // Use a callback to format the tooltip labels without commas
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    if (context.parsed.y !== null) {
                        label += context.parsed.y.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "");
                    }
                    return label;
                }
            }
        }
    },
};

export default WorkHoursDisplay;
