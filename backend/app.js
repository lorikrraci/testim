const express = require("express");
const app = express();
const cors = require("cors");
const cookieParser = require("cookie-parser");
const errorMiddleware = require("./middlewares/errors");

// Import all routes
const products = require("./routes/product");
const auth = require("./routes/auth");
const order = require("./routes/order");
// other route imports

// Middleware
app.use(express.json());
app.use(cookieParser());
app.use(
  cors({
    origin: "http://localhost:3000",
    credentials: true,
  })
);

// Mount routes
app.use("/api/v1", products);
app.use("/api/v1", auth);
app.use("/api/v1", order);
// other route mounts

// Add a test endpoint
app.get("/api/test", (req, res) => {
  res.json({ message: "API is working!" });
});

// Add debug endpoints
app.get("/api/debug", (req, res) => {
  res.json({
    message: "Debug endpoint is working",
    env: process.env.NODE_ENV,
    timestamp: new Date().toISOString(),
    routes: {
      products: "/api/v1/products",
      login: "/api/v1/login",
      register: "/api/v1/register",
      profile: "/api/v1/me",
    },
  });
});

// Log all requests for debugging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.originalUrl}`);
  next();
});

// Error Middleware
app.use(errorMiddleware);

module.exports = app;
