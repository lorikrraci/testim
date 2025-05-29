const express = require("express");
const app = express();
const cors = require("cors");
const cookieParser = require("cookie-parser");
const bodyparser = require("body-parser");
const cloudinary = require("cloudinary");

const errorMiddleware = require("./middlewares/errors");

// CORS configuration - ensure this is first
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "http://localhost:3000");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept, Authorization"
  );
  res.header("Access-Control-Allow-Credentials", "true");

  // Handle preflight requests
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  next();
});

// Then use the cors middleware
app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization", "Set-Cookie"],
    exposedHeaders: ["Set-Cookie"],
  })
);

// Parsers after CORS
app.use(express.json());
app.use(cookieParser());
app.use(bodyparser.urlencoded({ extended: true }));

// Serve static files
const path = require("path");
app.use(express.static(path.join(__dirname, "public")));

// Add a test endpoint at the top of your routes
app.get("/api/test", (req, res) => {
  res.status(200).json({
    success: true,
    message: "API is working",
  });
});

// Log all requests for debugging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.originalUrl}`);
  next();
});

// Import all routes
const products = require("./routes/product");
const auth = require("./routes/auth");
const order = require("./routes/order");

app.use("/api/v1", products);
app.use("/api/v1", auth);
app.use("/api/v1", order);

//Middleware to handle errors
app.use(errorMiddleware);

module.exports = app;
