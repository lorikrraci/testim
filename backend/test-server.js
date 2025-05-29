const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Server is running!');
});

app.get('/api/test', (req, res) => {
  res.json({ message: 'API test successful' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Test server running on port ${PORT}`);
});