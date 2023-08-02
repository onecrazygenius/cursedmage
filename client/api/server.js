const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs-extra');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(bodyParser.json());

const DATA_FILE_PATH = path.join(__dirname, 'leaderboard.json');

const readLeaderboard = async () => {
    try {
        const rawData = await fs.readFile(DATA_FILE_PATH, 'utf-8');
        const data = JSON.parse(rawData);
        // Sort the data and return
        return data.sort((a, b) => b.score - a.score);
    } catch (error) {
        // If file doesn't exist, return an empty array
        return [];
    }
};


const writeLeaderboard = async (data) => {
    await fs.writeFile(DATA_FILE_PATH, JSON.stringify(data, null, 2), 'utf-8');
};

app.get('/api/score', async (req, res) => {
    const leaderboard = await readLeaderboard();
    res.json(leaderboard.slice(0, 10)); // Return only the top 10 scores
});

app.post('/api/score', async (req, res) => {
    const { name, score } = req.body;
    console.log(req.body);
    if (!name || typeof score !== 'number') {
        return res.status(400).json({ error: 'Name and score are required' });
    }

    let leaderboard = await readLeaderboard();
    leaderboard.push({ name, score });
    leaderboard.sort((a, b) => b.score - a.score);

    await writeLeaderboard(leaderboard);

    res.status(201).json({ message: 'Score added successfully!' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
