import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const PredictionsChart = () => {
    const [chartData, setChartData] = useState(null); // Initialize as null for checking availability

    // Moved chartOptions definition here as a constant, not part of component state
    const chartOptions = {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Hours'
                }
            }
        },
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            },
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        animation: {
            tension: {
                duration: 1000,
                easing: 'linear',
                from: 1,
                to: 0,
                loop: true
            }
        }
    };

    useEffect(() => {
        axios.get('/api/predictions/')
            .then(response => {
                const jobRoles = response.data.map(data => data.job_role);
                const predictedHours = response.data.map(data => data.predicted_hours);
                setChartData({
                    labels: jobRoles,
                    datasets: [{
                        label: 'Predicted Work Hours',
                        data: predictedHours,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                    }]
                });
            })
            .catch(error => console.error('Error fetching predictions:', error));
    }, []);

    // Render the chart only if chartData is available
    return (
        <div>
            {chartData ? (
                <Bar data={chartData} options={chartOptions} />
            ) : (
                <p>Loading chart data...</p>
            )}
        </div>
    );
};

export default PredictionsChart;
