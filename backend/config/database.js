const mongoose = require("mongoose");

const connectDatabase = async () => {
  try {
    const conn = await mongoose.connect(process.env.DB_URI, {
      useUnifiedTopology: true,
      serverSelectionTimeoutMS: 5000,
      maxPoolSize: 10,
    });

    console.log(
      `MongoDB Database connected with HOST: ${conn.connection.host}`
    );
    return conn;
  } catch (err) {
    console.error("MongoDB connection error:", err);
    console.error("DB_URI:", process.env.DB_URI);
    process.exit(1);
  }
};

module.exports = connectDatabase;
