import React, { Fragment, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { useAlert } from "react-alert";
import Pagination from "react-js-pagination";

import MetaData from "./layout/MetaData";
import Product from "./product/Product";
import Loader from "./layout/Loader";
import { getProducts } from "../actions/productActions";

const Home = () => {
  const dispatch = useDispatch();
  const alert = useAlert();
  const {
    loading,
    products,
    error,
    productCount,
    resPerPage,
    filteredProductsCount,
  } = useSelector((state) => state.products);
  const { keyword } = useParams();
  const [currentPage, setCurrentPage] = useState(1);
  const [price, setPrice] = useState([1, 5000]);
  const [category, setCategory] = useState("");
  const [rating, setRating] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(4); // Default to 4 items per page

  useEffect(() => {
    if (error) {
      alert.error(error);
      return;
    }

    dispatch(
      getProducts(keyword, currentPage, price, category, rating, itemsPerPage)
    );
  }, [
    dispatch,
    alert,
    error,
    keyword,
    currentPage,
    price,
    category,
    rating,
    itemsPerPage,
  ]);

  function setCurrentPageNo(pageNumber) {
    setCurrentPage(pageNumber);
  }

  const handleViewAllToggle = () => {
    if (itemsPerPage === 4) {
      setItemsPerPage(100); // Show a large number to get all products
      setCurrentPage(1); // Reset to first page
    } else {
      setItemsPerPage(4); // Reset to default
      setCurrentPage(1); // Reset to first page
    }
  };

  let count = productCount;
  if (keyword) {
    count = filteredProductsCount;
  }

  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : (
        <Fragment>
          <MetaData title={"Buy Best Products Online"} />

          <div className="d-flex justify-content-between align-items-center mb-4">
            <h1 id="products_heading">Latest Products</h1>
            <button
              className="btn btn-outline-primary"
              onClick={handleViewAllToggle}
            >
              {itemsPerPage === 4 ? "View All" : "Show Less"}
            </button>
          </div>

          <section id="products" className="container mt-5">
            <div className="row">
              {products && products.length > 0 ? (
                products.map((product) => (
                  <Product key={product._id} product={product} col={3} />
                ))
              ) : (
                <div className="col-12 text-center">
                  <h3>No Products Found</h3>
                </div>
              )}
            </div>
          </section>

          {resPerPage < count && itemsPerPage !== 100 && (
            <div className="d-flex justify-content-center mt-5">
              <Pagination
                activePage={currentPage}
                itemsCountPerPage={resPerPage}
                totalItemsCount={productCount}
                onChange={setCurrentPageNo}
                nextPageText={"Next"}
                prevPageText={"Prev"}
                firstPageText={"First"}
                lastPageText={"Last"}
                itemClass="page-item"
                linkClass="page-link"
              />
            </div>
          )}
        </Fragment>
      )}
    </Fragment>
  );
};

export default Home;
