const path = require('path');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'form.html'));
});

app.post('/submit', async (req, res) => {
  const data = req.body;
  try {
    // Forward the form data to the Flask backend within the docker network
    const resp = await fetch('http://backend:5000/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await resp.json();
    return res.sendFile(path.join(__dirname, 'views', 'success.html'));
  } catch (err) {
    console.error('Error forwarding to backend:', err.message);
    return res.status(500).send('Error contacting backend: ' + err.message);
  }
});

app.listen(PORT, () => console.log(`Express frontend listening on ${PORT}`));
