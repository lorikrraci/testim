const User = require("../models/user");

const ErrorHandler = require("../utils/errorHandler");
const catchAsyncErrors = require("../middlewares/catchAsyncErrors");
const sendToken = require("../utils/jwtToken");
const sendEmail = require("../utils/sendEmail");

const crypto = require("crypto");

// Register a user => /api/v1/register
exports.registerUser = catchAsyncErrors(async (req, res, next) => {
  try {
    console.log("Registration request received:", req.body);

    const { name, email, password } = req.body;

    // Check if all required fields are provided
    if (!name || !email || !password) {
      console.log("Missing required fields:", {
        name: name ? "provided" : "missing",
        email: email ? "provided" : "missing",
        password: password ? "provided" : "missing",
      });
      return next(new ErrorHandler("Please provide all required fields", 400));
    }

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      console.log("User already exists with email:", email);
      return next(new ErrorHandler("User with this email already exists", 400));
    }

    // Set default avatar for all users
    const avatarData = {
      public_id: "avatars/default_avatar",
      url: "https://res.cloudinary.com/dxqnb8xjb/image/upload/v1602395872/avatars/default_avatar.jpg",
    };

    console.log("Creating user with data:", {
      name,
      email,
      passwordLength: password ? password.length : 0,
    });

    const user = await User.create({
      name,
      email,
      password,
      avatar: avatarData,
    });

    console.log("User created successfully:", user._id);

    sendToken(user, 200, res);
  } catch (error) {
    console.error("Registration error:", error);
    return next(new ErrorHandler(error.message, 500));
  }
});

//Login User => /api/v1/login
exports.loginUser = catchAsyncErrors(async (req, res, next) => {
  const { email, password } = req.body;

  console.log("Login attempt for:", email);

  //Checks if email and password is entered by user
  if (!email || !password) {
    console.log("Missing email or password");
    return next(new ErrorHandler("Please enter email & password", 400));
  }

  //Finding user in database
  const user = await User.findOne({ email }).select("+password");

  if (!user) {
    console.log("User not found in database");
    return next(new ErrorHandler("Invalid Email or Password", 401));
  }

  // Checks if password is correct or not
  const isPasswordMatched = await user.comparePassword(password);

  if (!isPasswordMatched) {
    console.log("Password does not match");
    return next(new ErrorHandler("Invalid Email or Password", 401));
  }

  console.log("Login successful for user:", user.email);
  sendToken(user, 200, res);
});
//Forgot password => /api/v1/password/forgot
exports.forgotPassword = catchAsyncErrors(async (req, res, next) => {
  const user = await User.findOne({ email: req.body.email });

  if (!user) {
    return next(new ErrorHandler("User not found with this email", 404));
  }

  //Get reset token
  const resetToken = user.getResetPasswordToken();

  await user.save({ validateBeforeSave: false });

  //Create reset password url
  const resetUrl = `${req.protocol}://${req.get(
    "host"
  )}/api/v1/password/reset/${resetToken}`;

  const message = `Your password reset token is as follow : \n\n${resetUrl}\n\nIf you have not requested this email, then ignore it.`;

  try {
    await sendEmail({
      email: user.email,
      subject: "ShopIT Password Recovery",
      message,
    });
    res.status(200).json({
      success: true,
      message: `Email sent to : ${user.email}`,
    });
  } catch (error) {
    user.resetPasswordToken = undefined;
    user.resetPasswordExpire = undefined;

    await user.save({ validateBeforeSave: false });

    return next(new ErrorHandler(error.message, 500));
  }
});

//Reset password => /api/v1/password/reset/:token
exports.resetPassword = catchAsyncErrors(async (req, res, next) => {
  //Hash the URL token
  const resetPasswordToken = crypto
    .createHash("sha256")
    .update(req.params.token)
    .digest("hex");

  const user = await User.findOne({
    resetPasswordToken,
    resetPasswordExpire: { $gt: Date.now() }, //expire date must be greater than date now
  });
  if (!user) {
    return next(
      new ErrorHandler(
        "Password reset token is invalid or has been expired.",
        400
      )
    );
  }

  if (req.body.password !== req.body.confirmPassword) {
    return next(new ErrorHandler("Password does not match", 400));
  }

  //Setup new password
  user.password = req.body.password;

  user.resetPasswordToken = undefined;
  user.resetPasswordExpire = undefined;

  await user.save();

  sendToken(user, 200, res);
});

//Get currently logged in user details => /ap/v1/me
exports.getUserProfile = catchAsyncErrors(async (req, res, next) => {
  const user = await User.findById(req.user.id);

  res.status(200).json({
    success: true,
    user,
  });
});

//Update / Change password => /api/v1/password/update
exports.updatePassword = catchAsyncErrors(async (req, res, next) => {
  const user = await User.findById(req.user.id).select("+password");

  // Check previous user password
  const isMatched = await user.comparePassword(req.body.oldPassword);
  if (!isMatched) {
    return next(new ErrorHandler("Old password is incorrect", 400));
  }
  user.password = req.body.password;
  await user.save();

  sendToken(user, 200, res);
});

// Update user profile => /api/v1/me/update
exports.updateProfile = catchAsyncErrors(async (req, res, next) => {
  const newUserData = {
    name: req.body.name,
    email: req.body.email,
  };

  //Update avatar: TODO

  const user = await User.findByIdAndUpdate(req.user.id, newUserData, {
    new: true,
    runValidators: true,
    useFindAndModify: false,
  });

  res.status(200).json({
    success: true,
  });
});

//Logout user => /api/v1/logout
exports.logout = catchAsyncErrors(async (req, res, next) => {
  res.cookie("token", null, {
    expires: new Date(Date.now()),
    httpOnly: true,
  });

  res.status(200).json({
    success: true,
    message: "Logged out",
  });
});

//Admin routes

//Get all users => /api/v1/admin/users
exports.allUsers = catchAsyncErrors(async (req, res, next) => {
  try {
    console.log("Fetching all users from database...");
    const users = await User.find();
    console.log(`Found ${users.length} users`);

    res.status(200).json({
      success: true,
      users,
    });
  } catch (error) {
    console.error("Error fetching users:", error);
    return next(new ErrorHandler("Error fetching users", 500));
  }
});

//Get user details => /api/v1/admin/user/:id
exports.getUserDetails = catchAsyncErrors(async (req, res, next) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    return next(
      new ErrorHandler(`'User not found with id : ${req.params.id}'`)
    );
  }

  res.status(200).json({
    success: true,
    user,
  });
});

// Update user profile => /api/v1/admin/users/:id
exports.updateUser = catchAsyncErrors(async (req, res, next) => {
  const newUserData = {
    name: req.body.name,
    email: req.body.email,
    role: req.body.role,
  };

  const user = await User.findByIdAndUpdate(req.params.id, newUserData, {
    new: true,
    runValidators: true,
    useFindAndModify: false,
  });

  res.status(200).json({
    success: true,
  });
});

//Delete user  => /api/v1/admin/user/:id
exports.deleteUser = catchAsyncErrors(async (req, res, next) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    return next(
      new ErrorHandler(`User not found with id : ${req.params.id}`, 400)
    );
  }

  //Remove avatar from cloudinary - TODO

  await User.deleteOne({ _id: req.params.id });

  res.status(200).json({
    success: true,
  });
});

// Delete user account (self) => /api/v1/me/delete
exports.deleteAccount = catchAsyncErrors(async (req, res, next) => {
  try {
    const user = await User.findById(req.user.id);

    if (!user) {
      return next(new ErrorHandler("User not found", 404));
    }

    // Remove avatar from cloudinary if exists and it's not the default avatar
    if (
      user.avatar &&
      user.avatar.public_id &&
      user.avatar.public_id !== "avatars/default_avatar"
    ) {
      try {
        // Check if cloudinary is properly imported
        const cloudinary = require("cloudinary");
        await cloudinary.v2.uploader.destroy(user.avatar.public_id);
      } catch (cloudinaryError) {
        console.error("Error deleting image from Cloudinary:", cloudinaryError);
        // Continue with account deletion even if image deletion fails
      }
    }

    // Delete the user
    await User.deleteOne({ _id: req.user.id });

    // Clear the token cookie
    res.cookie("token", null, {
      expires: new Date(Date.now()),
      httpOnly: true,
    });

    res.status(200).json({
      success: true,
      message: "Account deleted successfully",
    });
  } catch (error) {
    console.error("Account deletion error:", error);
    return next(new ErrorHandler(error.message, 500));
  }
});
