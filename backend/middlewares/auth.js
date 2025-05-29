const User = require("../models/user");
const jwt = require("jsonwebtoken");
const ErrorHandler = require("../utils/errorHandler");
const catchAsyncErrors = require("./catchAsyncErrors");

//Checks if user is authenticated or not
exports.isAuthenticatedUser = catchAsyncErrors(async (req, res, next) => {
  console.log("Checking authentication...");
  console.log("Cookies:", req.cookies);

  // Check if req.cookies exists
  if (!req.cookies) {
    console.log("No cookies found in request");
    return next(new ErrorHandler("Login first to access this resource.", 401));
  }

  const { token } = req.cookies;

  if (!token) {
    console.log("No token found in cookies");
    return next(new ErrorHandler("Login first to access this resource.", 401));
  }

  try {
    console.log("Verifying token...");
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    console.log("Token verified, user ID:", decoded.id);

    const user = await User.findById(decoded.id);

    if (!user) {
      console.log("User not found in database");
      return next(new ErrorHandler("User not found", 404));
    }

    console.log("User authenticated:", user.email);
    req.user = user;
    next();
  } catch (error) {
    console.error("Token verification error:", error.message);
    return next(new ErrorHandler("Invalid token. Please login again.", 401));
  }
});

// Handling users roles
exports.authorizeRoles = (...roles) => {
  return (req, res, next) => {
    console.log("Checking role authorization...");
    console.log("User role:", req.user.role);
    console.log("Required roles:", roles);

    if (!roles.includes(req.user.role)) {
      return next(
        new ErrorHandler(
          `Role (${req.user.role}) is not allowed to access this resource`,
          403
        )
      );
    }
    console.log("Role authorized");
    next();
  };
};
