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

// Public routes
router.route("/products").get(getProducts);
router.route("/products/:id").get(getSingleProduct);

// Admin routes
router
  .route("/admin/products")
  .get(isAuthenticatedUser, authorizeRoles("admin"), getAdminProducts);

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

// Review routes
router.route("/review").put(isAuthenticatedUser, createProductReview);
router.route("/reviews").get(isAuthenticatedUser, getProductReviews);
router.route("/reviews").delete(isAuthenticatedUser, deleteReview);

module.exports = router;
