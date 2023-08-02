// src/components/Leaderboard.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Leaderboard() {
  const [scores, setScores] = useState([]);

  useEffect(() => {
    // Fetch the leaderboard scores when the component mounts
    async function fetchScores() {
      try {
        const response = await axios.get('/api/score');
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
      <ul>
        {scores.map((score, index) => (
          <li key={index}>
            {index + 1}. {score.name} - {score.score}
          </li>
        ))}
      </ul>
    </>
  );
}

export default Leaderboard;
