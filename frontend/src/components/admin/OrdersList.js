import React, { Fragment, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import MetaData from "../layout/MetaData";
import Loader from "../layout/Loader";
import Sidebar from "./Sidebar";
import { useAlert } from "react-alert";
import { useDispatch, useSelector } from "react-redux";
import {
  allOrders,
  deleteOrder,
  clearErrors,
} from "../../actions/orderActions";
import { DELETE_ORDER_RESET } from "../../constants/orderConstants";

const OrdersList = () => {
  const alert = useAlert();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const {
    user,
    loading: authLoading,
    isAuthenticated,
  } = useSelector((state) => state.auth);
  const {
    loading,
    error,
    orders = [],
  } = useSelector((state) => state.allOrders || {});
  const { isDeleted } = useSelector((state) => state.order || {});

  useEffect(() => {
    // Check if user is authenticated and is an admin
    if (isAuthenticated && user && user.role === "admin") {
      dispatch(allOrders());
    } else if (
      !authLoading &&
      (!isAuthenticated || (user && user.role !== "admin"))
    ) {
      // Redirect if not authenticated or not an admin
      navigate("/login");
      alert.error("You must be logged in as an admin to access this page");
    }

    if (error) {
      alert.error(error);
      dispatch(clearErrors());
    }

    if (isDeleted) {
      alert.success("Order deleted successfully");
      navigate("/admin/orders");
      dispatch({ type: DELETE_ORDER_RESET });
    }
  }, [
    dispatch,
    alert,
    error,
    isDeleted,
    navigate,
    isAuthenticated,
    user,
    authLoading,
  ]);

  console.log("OrdersList - orders:", orders);

  const deleteOrderHandler = (id) => {
    dispatch(deleteOrder(id));
  };

  return (
    <Fragment>
      <MetaData title={"All Orders"} />
      <div className="row">
        <div className="col-12 col-md-2">
          <Sidebar />
        </div>

        <div className="col-12 col-md-10">
          <Fragment>
            <h1 className="my-5">All Orders</h1>

            {loading || authLoading ? (
              <Loader />
            ) : error ? (
              <p className="alert alert-danger">{error}</p>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-bordered">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>No of Items</th>
                      <th>Amount</th>
                      <th>Status</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders && orders.length > 0 ? (
                      orders.map((order) => (
                        <tr key={order._id}>
                          <td>{order._id}</td>
                          <td>{order.orderItems.length}</td>
                          <td>${order.totalPrice}</td>
                          <td>
                            <span
                              className={
                                order.orderStatus &&
                                String(order.orderStatus).includes("Delivered")
                                  ? "text-success"
                                  : "text-danger"
                              }
                            >
                              {order.orderStatus}
                            </span>
                          </td>
                          <td>
                            <Link
                              to={`/admin/order/${order._id}`}
                              className="btn btn-primary py-1 px-2 mr-2"
                            >
                              <i className="fa fa-eye"></i>
                            </Link>
                            <button
                              className="btn btn-danger py-1 px-2"
                              onClick={() => deleteOrderHandler(order._id)}
                            >
                              <i className="fa fa-trash"></i>
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="5" className="text-center">
                          No orders found
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            )}
          </Fragment>
        </div>
      </div>
    </Fragment>
  );
};

export default OrdersList;
