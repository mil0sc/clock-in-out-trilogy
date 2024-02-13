import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const WorkHoursChart = () => {
    const [chartData, setChartData] = useState({
      datasets: [], // Ensure datasets is always an array
    });

    useEffect(() => {
        const fetchAndSetChartData = async () => {
            try {
                const response = await axios.get('/api/employee-hours/');
                const data = response.data;

                if (data && data.length > 0) { // Check if data is not empty
                    // Modify chartLabels to include both employee name and job role
                    const chartLabels = data.map(item => `${item.employee_name} (${item.job_role})`);
                    const chartDatasetData = data.map(item => item.work_hours);

                    setChartData({
                        labels: chartLabels,
                        datasets: [
                            {
                                label: 'Total Work Hours',
                                data: chartDatasetData,
                                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            }
                        ]
                    });
                }
            } catch (error) {
                console.error('Error fetching employee hours data:', error);
            }
        };

        fetchAndSetChartData();
    }, []);

    return (
        <div>
            <h2>Employee Work Hours</h2>
            {chartData.datasets.length > 0 ? (
                <Bar data={chartData} options={{
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Hours'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                // Optionally, you can customize tooltip labels further if needed
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed.y !== null) {
                                        label += context.parsed.y;
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }} />
            ) : (
                <p>Loading chart data...</p>
            )}
        </div>
    );
};

export default WorkHoursChart;
