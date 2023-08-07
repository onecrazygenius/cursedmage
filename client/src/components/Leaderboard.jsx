// src/components/Leaderboard.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Leaderboard() {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    // Fetch the leaderboard scores when the component mounts
    async function fetchScores() {
      try {
        const response = await axios.get('http://localhost:5000/api/score');
        console.log(response.data)
        setScores(response.data);
      } catch (error) {
        console.error("Error fetching the scores:", error);
      }
    }

    fetchScores();
  }, []);

  return (
    <>
      <h2 className="title">
        Leaderboard
      </h2>
      <h2 style={{ marginTop: '-0.5em' }}>
        {scores.map((score, index) => (
          <>
            {/* Only div every 3 scores */}
            {index % 3 === 0 && index !== 0 && <br />}
            <span
              style={{
                width: '33%',
                display: 'inline-block',
                textAlign: 'center',
              }}
            >{index + 1}. {score.name} - {score.score}</span>
          </>
        ))}
      </h2>
    </>
  );
}

export default Leaderboard;
