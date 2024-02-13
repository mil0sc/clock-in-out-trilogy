import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import PredictionsChart from './predictionsChart';
import PredictTheYearChart from './predict-the-year';
import WorkHoursChart from './WorkHoursChart'; // Import your WorkHoursChart component

function App() {
  return (
    <Router>
      <div>
        {/* Navigation Links */}
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/predictions">Predictions</Link>
            </li>
            <li>
              <Link to="/predict-the-year">Predict The Year</Link>
            </li>
            <li>
              <Link to="/work-hours">Employee Work Hours</Link> {/* Add a new link for the WorkHoursChart */}
            </li>
          </ul>
        </nav>

        {/* Route Setup */}
        <Routes>
          <Route path="/predictions" element={<PredictionsChart />} />
          <Route path="/predict-the-year" element={<PredictTheYearChart />} />
          <Route path="/work-hours" element={<WorkHoursChart />} /> {/* Add a new route for the WorkHoursChart */}
          <Route path="/" element={<div>Home Page - Learn React</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
