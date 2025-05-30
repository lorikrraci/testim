const jwt = require("jsonwebtoken");
const User = require("../models/user");
const ErrorHandler = require("../utils/errorHandler");
const catchAsyncErrors = require("./catchAsyncErrors");

// Check if user is authenticated
exports.isAuthenticatedUser = catchAsyncErrors(async (req, res, next) => {
  console.log("Checking authentication...");
  console.log("Cookies:", req.cookies);

  const { token } = req.cookies;

  // Also check for token in headers for API clients
  const authHeader = req.headers.authorization;
  const headerToken =
    authHeader && authHeader.startsWith("Bearer ")
      ? authHeader.split(" ")[1]
      : null;

  const finalToken = token || headerToken;

  if (!finalToken) {
    console.log("No token found in cookies or headers");
    return next(new ErrorHandler("Login first to access this resource", 401));
  }

  try {
    const decoded = jwt.verify(finalToken, process.env.JWT_SECRET);
    console.log("Token verified, user ID:", decoded.id);

    req.user = await User.findById(decoded.id);

    if (!req.user) {
      console.log("User not found in database");
      return next(new ErrorHandler("User not found", 404));
    }

    console.log("User authenticated:", req.user.email);
    next();
  } catch (error) {
    console.error("Token verification error:", error);
    return next(new ErrorHandler("Invalid token", 401));
  }
});

// Handling user roles
exports.authorizeRoles = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return next(
        new ErrorHandler(
          `Role (${req.user.role}) is not allowed to access this resource`,
          403
        )
      );
    }
    next();
  };
};
