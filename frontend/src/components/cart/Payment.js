import React, { Fragment, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import MetaData from "../layout/MetaData";
import CheckoutSteps from "./CheckoutSteps";
import { useAlert } from "react-alert";
import { createOrder, clearErrors } from "../../actions/orderActions";
import { clearCart } from "../../actions/cartActions";

const Payment = () => {
  const alert = useAlert();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { shippingInfo, cartItems } = useSelector((state) => state.cart);

  const orderInfo = JSON.parse(sessionStorage.getItem("orderInfo"));

  const order = {
    orderItems: cartItems,
    shippingInfo,
  };

  if (orderInfo) {
    order.itemsPrice = orderInfo.itemsPrice;
    order.shippingPrice = orderInfo.shippingPrice;
    order.taxPrice = orderInfo.taxPrice;
    order.totalPrice = orderInfo.totalPrice;
  }

  const submitHandler = async (e) => {
    e.preventDefault();

    try {
      // Here you would normally process payment with a payment gateway
      // For this example, we'll just simulate a successful payment
      alert.success("Payment successful!");

      // Create the order
      dispatch(createOrder(order));

      // Clear cart after successful order
      dispatch(clearCart());

      // Redirect to success page
      navigate("/");
    } catch (error) {
      alert.error("Payment failed. Please try again.");
    }
  };

  return (
    <Fragment>
      <MetaData title={"Payment"} />
      <CheckoutSteps shipping confirmOrder payment />
      <div className="row wrapper">
        <div className="col-10 col-lg-5">
          <form className="shadow-lg" onSubmit={submitHandler}>
            <h1 className="mb-4">Card Info</h1>
            <div className="form-group">
              <label htmlFor="card_num_field">Card Number</label>
              <input
                type="text"
                id="card_num_field"
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="card_exp_field">Card Expiry</label>
              <input
                type="text"
                id="card_exp_field"
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="card_cvc_field">Card CVC</label>
              <input
                type="text"
                id="card_cvc_field"
                className="form-control"
                required
              />
            </div>
            <button id="pay_btn" type="submit" className="btn btn-block py-3">
              Pay {` - ${orderInfo && orderInfo.totalPrice}`}
            </button>
          </form>
        </div>
      </div>
    </Fragment>
  );
};

export default Payment;
