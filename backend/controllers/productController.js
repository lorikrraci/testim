const Product = require("../models/products");
const ErrorHandler = require("../utils/errorHandler");
const catchAsyncErrors = require("../middlewares/catchAsyncErrors");
const APIFeatures = require("../utils/apiFeatures");
const mongoose = require("mongoose");

// Get all products => /api/v1/products
exports.getProducts = catchAsyncErrors(async (req, res, next) => {
  try {
    const resPerPage = 4;
    const productCount = await Product.countDocuments();

    const apiFeatures = new APIFeatures(Product.find(), req.query)
      .search()
      .filter()
      .pagination(resPerPage);

    const products = await apiFeatures.query;

    console.log(`Found ${products.length} products`);

    res.status(200).json({
      success: true,
      productCount,
      resPerPage,
      products,
    });
  } catch (error) {
    console.error("Error fetching products:", error);
    return next(new ErrorHandler("Error fetching products", 500));
  }
});

//Create new product => /api/v1/admin/products/new
exports.newProduct = catchAsyncErrors(async (req, res, next) => {
  try {
    console.log("Creating new product with data:", {
      name: req.body.name,
      price: req.body.price,
      description: req.body.description?.substring(0, 30) + "...",
      category: req.body.category,
      stock: req.body.stock,
      seller: req.body.seller,
    });

    // Log received files
    if (req.files) {
      console.log(
        `Received ${req.files.length} files:`,
        req.files.map((f) => ({
          fieldname: f.fieldname,
          originalname: f.originalname,
          mimetype: f.mimetype,
          size: f.size,
          filename: f.filename || "no filename",
        }))
      );
    } else {
      console.log("No files received");
    }

    // Set user ID from authenticated user
    req.body.user = req.user.id;

    // Handle image uploads
    if (req.files && req.files.length > 0) {
      const images = [];

      req.files.forEach((file) => {
        // Create a URL that points to your uploads directory
        const fileUrl = `/uploads/${file.filename}`;

        images.push({
          public_id: file.filename,
          url: fileUrl,
        });

        console.log(`Added image: ${fileUrl}`);
      });

      req.body.images = images;
    } else {
      // If no images provided, return error
      return next(
        new ErrorHandler("Please provide at least one product image", 400)
      );
    }

    // Create the product
    const product = new Product(req.body);
    const savedProduct = await product.save();

    console.log("Product created successfully with ID:", savedProduct._id);

    res.status(201).json({
      success: true,
      message: "Product created successfully",
      product: savedProduct,
    });
  } catch (error) {
    console.error("Product creation error:", error);
    return next(
      new ErrorHandler("Product creation failed: " + error.message, 500)
    );
  }
});
//Get single product details => /api/v1/products/:id
exports.getSingleProduct = catchAsyncErrors(async (req, res, next) => {
  try {
    const productId = req.params.id;

    // Validate if the ID is a valid ObjectId
    if (!mongoose.Types.ObjectId.isValid(productId)) {
      return res.status(400).json({
        success: false,
        message: "Invalid Product ID format",
      });
    }

    const product = await Product.findById(productId);

    if (!product) {
      return next(new ErrorHandler("Product not found", 404));
    }

    res.status(200).json({
      success: true,
      product,
    });
  } catch (error) {
    console.error("Error fetching product:", error);
    res.status(500).json({
      success: false,
      message: "Server Error",
      error: error.message,
    });
  }
});

// update product => /api/v1/admin/product/:id

exports.updateProduct = catchAsyncErrors(async (req, res, next) => {
  let product = await Product.findById(req.params.id);

  if (!product) {
    return next(new ErrorHandler("Product not found", 404));
  }

  product = await Product.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
    runValidators: true,
    useFindAndModify: false,
  });
  res.status(200).json({
    success: true,
    product,
  });
});

// Delete product => /api/v1/admin/products/:id
exports.deleteProduct = catchAsyncErrors(async (req, res, next) => {
  try {
    const product = await Product.findById(req.params.id);

    if (!product) {
      return next(new ErrorHandler("Product not found", 404));
    }

    await product.deleteOne(); // Use deleteOne instead of remove

    res.status(200).json({
      success: true,
      message: "Product is deleted.",
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Server Error",
      error: error.message,
    });
  }
});

//Create new review => /api/v1/revies
exports.createProductReview = catchAsyncErrors(async (req, res, next) => {
  const { rating, comment, productId } = req.body;

  const review = {
    user: req.user._id,
    name: req.user.name,
    rating: Number(rating),
    comment,
  };

  const product = await Product.findById(productId);

  const isReviewed = product.reviews.find(
    (r) => r.user.toString() === req.user._id.toString()
  );
  if (isReviewed) {
    product.reviews.forEach((review) => {
      if (review.user.toString() === req.user._id.toString()) {
        review.comment = comment;
        review.rating = rating;
      }
    });
  } else {
    product.reviews.push(review);
    product.numOfReviews = product.reviews.length;
  }
  product.ratings =
    product.reviews.reduce((acc, item) => item.rating + acc, 0) /
    product.reviews.length;

  await product.save({ validateBeforeSave: false });

  res.status(200).json({
    success: true,
  });
});

//Get Product Reviews => /api/v1/reviews
exports.getProductReviews = catchAsyncErrors(async (req, res, next) => {
  const product = await Product.findById(req.query.id);

  res.status(200).json({
    success: true,
    reviews: product.reviews,
  });
});

//Delete Product Reviews => /api/v1/reviews
exports.deleteReview = catchAsyncErrors(async (req, res, next) => {
  const product = await Product.findById(req.query.productId);

  const reviews = product.reviews.filter(
    (review) => review._id.toString() !== req.query.id.toString()
  );

  const numOfReviews = reviews.length;

  const ratings =
    product.reviews.reduce((acc, item) => item.rating + acc, 0) /
    reviews.length;

  await Product.findByIdAndUpdate(
    req.query.productId,
    {
      reviews,
      ratings,
      numOfReviews,
    },
    {
      new: true,
      runValidators: true,
      useFindAndModify: false,
    }
  );

  res.status(200).json({
    success: true,
  });
});

// Get all products (Admin) => /api/v1/admin/products
exports.getAdminProducts = catchAsyncErrors(async (req, res, next) => {
  const products = await Product.find();

  res.status(200).json({
    success: true,
    products,
  });
});
