import React from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import PredictionsChart from './predictionsChart';

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
          </ul>
        </nav>

        {/* Route Switch */}
        <Switch>
          <Route path="/predictions">
            <PredictionsChart />
          </Route>
          <Route path="/">
            {/* Your Home Component or content here */}
            <div>Home Page - Learn React</div>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
