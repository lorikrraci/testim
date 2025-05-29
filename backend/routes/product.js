const express = require("express");
const router = express.Router();
const upload = require("../middlewares/fileUpload");

const {
  getProducts,
  newProduct,
  getSingleProduct,
  updateProduct,
  deleteProduct,
  createProductReview,
  getProductReviews,
  deleteReview,
  getAdminProducts,
} = require("../controllers/productController");

const { isAuthenticatedUser, authorizeRoles } = require("../middlewares/auth");

router.route("/products").get(getProducts);
router.route("/products/:id").get(getSingleProduct);

router
  .route("/admin/products")
  .get(isAuthenticatedUser, authorizeRoles("admin"), getAdminProducts);

// Make sure this route is correctly defined for creating new products
router
  .route("/admin/products/new")
  .post(
    isAuthenticatedUser,
    authorizeRoles("admin"),
    upload.array("images", 10),
    newProduct
  );

router
  .route("/admin/products/:id")
  .put(
    isAuthenticatedUser,
    authorizeRoles("admin"),
    upload.array("images", 10),
    updateProduct
  )
  .delete(isAuthenticatedUser, authorizeRoles("admin"), deleteProduct);

router.route("/review").put(isAuthenticatedUser, createProductReview);
router.route("/reviews").get(isAuthenticatedUser, getProductReviews);
router.route("/reviews").delete(isAuthenticatedUser, deleteReview);

// Add a debug route to test file uploads
router.post("/test-upload", upload.array("images", 10), (req, res) => {
  console.log("Test upload received:");
  console.log("Body:", req.body);
  console.log("Files:", req.files?.map((f) => f.filename) || "No files");

  res.status(200).json({
    success: true,
    message: "Test upload received",
    body: req.body,
    files:
      req.files?.map((f) => ({
        filename: f.filename,
        path: f.path,
        size: f.size,
      })) || [],
  });
});

module.exports = router;
