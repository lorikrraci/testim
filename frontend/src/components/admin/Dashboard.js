import React, { Fragment, useEffect } from "react";
import { Link } from "react-router-dom";
import MetaData from "../layout/MetaData";
import Sidebar from "./Sidebar";
import Loader from "../layout/Loader";
import { useDispatch, useSelector } from "react-redux";
import { getAdminProducts } from "../../actions/productActions";
import { allOrders } from "../../actions/orderActions";
import { allUsers } from "../../actions/userActions";

const Dashboard = () => {
  const dispatch = useDispatch();

  const { products, loading: productsLoading } = useSelector(
    (state) => state.products || {}
  );
  const {
    orders,
    totalAmount,
    loading: ordersLoading,
    error: ordersError,
  } = useSelector((state) => state.allOrders || {});
  const {
    users,
    loading: usersLoading,
    error: usersError,
  } = useSelector((state) => state.allUsers || {});

  useEffect(() => {
    dispatch(getAdminProducts());
    dispatch(allOrders());
    dispatch(allUsers());
  }, [dispatch]);

  // Debug logs
  console.log("Dashboard state:", {
    products: products ? products.length : 0,
    orders: orders ? orders.length : 0,
    totalAmount,
    users: users ? users.length : 0,
    productsLoading,
    ordersLoading,
    ordersError,
    usersLoading,
    usersError,
  });

  let outOfStock = 0;
  products &&
    products.forEach((product) => {
      if (product.stock === 0) {
        outOfStock += 1;
      }
    });

  return (
    <Fragment>
      <MetaData title={"Admin Dashboard"} />

      <div className="row">
        <div className="col-12 col-md-2">
          <Sidebar />
        </div>

        <div className="col-12 col-md-10">
          <h1 className="my-4">Dashboard</h1>

          {productsLoading || ordersLoading || usersLoading ? (
            <Loader />
          ) : (
            <Fragment>
              <div className="row pr-4">
                <div className="col-xl-3 col-sm-6 mb-3">
                  <div className="card text-white bg-success o-hidden h-100">
                    <div className="card-body">
                      <div className="text-center card-font-size">
                        Products
                        <br /> <b>{products && products.length}</b>
                      </div>
                    </div>
                    <Link
                      className="card-footer text-white clearfix small z-1"
                      to="/admin/products"
                    >
                      <span className="float-left">View Details</span>
                      <span className="float-right">
                        <i className="fa fa-angle-right"></i>
                      </span>
                    </Link>
                  </div>
                </div>

                <div className="col-xl-3 col-sm-6 mb-3">
                  <div className="card text-white bg-danger o-hidden h-100">
                    <div className="card-body">
                      <div className="text-center card-font-size">
                        Orders
                        <br /> <b>{orders && orders.length}</b>
                      </div>
                    </div>
                    <Link
                      className="card-footer text-white clearfix small z-1"
                      to="/admin/orders"
                    >
                      <span className="float-left">View Details</span>
                      <span className="float-right">
                        <i className="fa fa-angle-right"></i>
                      </span>
                    </Link>
                  </div>
                </div>

                <div className="col-xl-3 col-sm-6 mb-3">
                  <div className="card text-white bg-info o-hidden h-100">
                    <div className="card-body">
                      <div className="text-center card-font-size">
                        Users
                        <br /> <b>{users && users.length}</b>
                      </div>
                    </div>
                    <Link
                      className="card-footer text-white clearfix small z-1"
                      to="/admin/users"
                    >
                      <span className="float-left">View Details</span>
                      <span className="float-right">
                        <i className="fa fa-angle-right"></i>
                      </span>
                    </Link>
                  </div>
                </div>

                <div className="col-xl-3 col-sm-6 mb-3">
                  <div className="card text-white bg-warning o-hidden h-100">
                    <div className="card-body">
                      <div className="text-center card-font-size">
                        Out of Stock
                        <br /> <b>{outOfStock}</b>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="row pr-4">
                <div className="col-xl-12 col-sm-12 mb-3">
                  <div className="card text-white bg-primary o-hidden h-100">
                    <div className="card-body">
                      <div className="text-center card-font-size">
                        Total Amount
                        <br /> <b>${totalAmount && totalAmount.toFixed(2)}</b>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </Fragment>
          )}
        </div>
      </div>
    </Fragment>
  );
};

export default Dashboard;
