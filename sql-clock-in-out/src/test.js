import React, { useState, useEffect } from 'react';

function TimeEntries() {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/time-entries/')
      .then(response => response.json())
      .then(data => {
        setEntries(data);
      });
  }, []);

  return (
    <div>
      <h2>Time Entry List</h2>
      <ul>
        {entries.map(entry => (
          <li key={entry.clock_in}>
            Employee ID: {entry.employee}, Clock In: {entry.clock_in}, Clock Out: {entry.clock_out || 'N/A'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TimeEntries;
