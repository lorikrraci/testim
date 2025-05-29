import React, { Fragment, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getProducts } from "../actions/productActions";
import { useAlert } from "react-alert";
import { useParams } from "react-router-dom";
import MetaData from "./layout/MetaData";
import ApiTest from "./ApiTest";

const Home = () => {
  const dispatch = useDispatch();
  const alert = useAlert();
  const { loading, products, error, productCount, resPerPage } = useSelector(
    (state) => state.products
  );
  const { keyword } = useParams();
  const [currentPage, setCurrentPage] = useState(1);
  const [price, setPrice] = useState([1, 5000]);
  const [category, setCategory] = useState("");
  const [rating, setRating] = useState(0);

  useEffect(() => {
    if (error) {
      alert.error(error);
      return; // Fix: Don't return anything from useEffect
    }

    dispatch(getProducts(keyword, currentPage, price, category, rating));
  }, [dispatch, alert, error, keyword, currentPage, price, category, rating]);

  return (
    <Fragment>
      {loading ? (
        <div className="loader">Loading...</div>
      ) : (
        <Fragment>
          <MetaData title={"Buy Best Products Online"} />

          {/* Add the API test component */}
          <ApiTest />

          <h1 id="products_heading" className="my-5">
            Latest Products
          </h1>

          <section id="products" className="container mt-5">
            <div className="row">
              {products && products.length > 0 ? (
                products.map((product) => (
                  <div
                    key={product._id}
                    className="col-sm-12 col-md-6 col-lg-3 my-3"
                  >
                    <div className="card p-3 rounded">
                      {product.images && product.images.length > 0 && (
                        <img
                          className="card-img-top mx-auto"
                          src={product.images[0].url}
                          alt={product.name}
                        />
                      )}
                      <div className="card-body d-flex flex-column">
                        <h5 className="card-title">{product.name}</h5>
                        <div className="ratings mt-auto">
                          <div className="rating-outer">
                            <div
                              className="rating-inner"
                              style={{
                                width: `${(product.ratings / 5) * 100}%`,
                              }}
                            ></div>
                          </div>
                          <span id="no_of_reviews">
                            ({product.numOfReviews} Reviews)
                          </span>
                        </div>
                        <p className="card-text">${product.price}</p>
                        <a
                          href={`/product/${product._id}`}
                          className="btn btn-primary"
                        >
                          View Details
                        </a>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="col-12 text-center">
                  <h3>No Products Found</h3>
                </div>
              )}
            </div>
          </section>
        </Fragment>
      )}
    </Fragment>
  );
};

export default Home;
