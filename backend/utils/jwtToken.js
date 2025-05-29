// Create and send token and save in cookie
const sendToken = (user, statusCode, res) => {
  // Create JWT Token
  const token = user.getJwtToken();

  // Options for cookie
  const options = {
    expires: new Date(
      Date.now() + process.env.COOKIE_EXPIRES_TIME * 24 * 60 * 60 * 1000
    ),
    httpOnly: true,
    secure: false, // Set to false for development
    sameSite: "lax", // Changed from strict to lax
    path: "/",
  };

  console.log("Setting cookie with token:", {
    token: token.substring(0, 10) + "...",
    options,
  });

  res.status(statusCode).cookie("token", token, options).json({
    success: true,
    token,
    user,
  });
};

module.exports = sendToken;
