import React, { Fragment, useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useAlert } from "react-alert";
import { Link } from "react-router-dom";

import { forgotPassword, clearErrors } from "../../actions/userActions";
import MetaData from "../layout/MetaData";
import Loader from "../layout/Loader";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const alert = useAlert();
  const dispatch = useDispatch();

  const { error, loading, message } = useSelector(
    (state) => state.forgotPassword
  );

  useEffect(() => {
    if (error) {
      alert.error(error);
      dispatch(clearErrors());
    }

    if (message) {
      alert.success(message);
      setSubmitted(true);
    }
  }, [dispatch, alert, error, message]);

  const submitHandler = (e) => {
    e.preventDefault();

    // Simple validation
    if (!email || !email.includes("@")) {
      return alert.error("Please enter a valid email address");
    }

    // Use a simple object instead of FormData
    const emailData = { email };
    console.log("Submitting forgot password with email:", email);

    dispatch(forgotPassword(emailData));
  };

  return (
    <Fragment>
      <MetaData title={"Forgot Password"} />

      {loading ? (
        <Loader />
      ) : (
        <div className="row wrapper">
          <div className="col-10 col-lg-5">
            <form className="shadow-lg" onSubmit={submitHandler}>
              <h1 className="mb-3">Forgot Password</h1>

              {submitted && message ? (
                <div className="alert alert-success mt-3">
                  {message}
                  <p className="mt-2">
                    Please check your email for password reset instructions.
                  </p>
                </div>
              ) : (
                <Fragment>
                  <div className="form-group">
                    <label htmlFor="email_field">Enter Email</label>
                    <input
                      type="email"
                      id="email_field"
                      className="form-control"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>

                  <button
                    id="forgot_password_button"
                    type="submit"
                    className="btn btn-block py-3"
                    disabled={loading}
                  >
                    {loading ? "Sending..." : "Send Email"}
                  </button>
                </Fragment>
              )}

              <div className="mt-3 text-center">
                <Link to="/login">Back to Login</Link>
              </div>
            </form>
          </div>
        </div>
      )}
    </Fragment>
  );
};

export default ForgotPassword;
