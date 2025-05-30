import React from "react";
import { Link } from "react-router-dom";

const Product = ({ product }) => {
  return (
    <div className="col-sm-12 col-md-6 col-lg-3 my-3">
      <div className="card p-3 rounded">
        {product.images && product.images.length > 0 ? (
          <img
            className="card-img-top mx-auto"
            src={product.images[0].url}
            alt={product.name}
            style={{ height: "200px", objectFit: "contain" }}
          />
        ) : (
          <div className="text-center p-4 bg-light">No Image</div>
        )}
        <div className="card-body d-flex flex-column">
          <h5 className="card-title">
            <Link to={`/product/${product._id}`}>{product.name}</Link>
          </h5>
          <div className="ratings mt-auto">
            <div className="rating-outer">
              <div
                className="rating-inner"
                style={{ width: `${(product.ratings / 5) * 100}%` }}
              ></div>
            </div>
            <span id="no_of_reviews">({product.numOfReviews} Reviews)</span>
          </div>
          <p className="card-text">${product.price}</p>
          <Link
            to={`/product/${product._id}`}
            id="view_btn"
            className="btn btn-block"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Product;
