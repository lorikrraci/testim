const express = require("express");
const cors = require("cors");
const app = express();

// Enable CORS
app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
  })
);

app.get("/", (req, res) => {
  res.send("Server is running!");
});

app.get("/api/test", (req, res) => {
  res.json({
    message: "API test successful",
    timestamp: new Date().toISOString(),
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Test server running on port ${PORT}`);
});
