// Handle uncaught exceptions
process.on("uncaughtException", (err) => {
  console.log(`ERROR: ${err.stack}`);
  console.log("Shutting down due to uncaught exception");
  process.exit(1);
});

// Setting up config file
if (process.env.NODE_ENV !== "PRODUCTION") {
  require("dotenv").config({ path: "backend/config/config.env" });
}

const app = require("./app");
const connectDatabase = require("./config/database");

// Connecting to database
connectDatabase();

const server = app.listen(process.env.PORT || 5000, () => {
  const port = server.address().port;
  console.log(
    `Server started on PORT: ${port} in ${
      process.env.NODE_ENV || "DEVELOPMENT"
    } mode.`
  );
  console.log(`API base URL: http://localhost:${port}`);
});

// Handle unhandled promise rejections
process.on("unhandledRejection", (err) => {
  console.log(`ERROR: ${err.message}`);
  console.log("Shutting down the server due to Unhandled Promise rejection");
  server.close(() => {
    process.exit(1);
  });
});

module.exports = app;
