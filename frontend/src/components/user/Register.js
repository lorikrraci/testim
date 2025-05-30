import React, { Fragment, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import MetaData from "../layout/MetaData";
import Loader from "../layout/Loader";
import { useAlert } from "react-alert";
import { useDispatch, useSelector } from "react-redux";
import { register, clearErrors } from "../../actions/userActions";

export const Register = () => {
  const [user, setUser] = useState({
    name: "",
    email: "",
    password: "",
  });

  const { name, email, password } = user;
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [passwordMatch, setPasswordMatch] = useState(true);
  const [formErrors, setFormErrors] = useState({});

  const alert = useAlert();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { isAuthenticated, error, loading } = useSelector(
    (state) => state.auth
  );

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/");
    }

    if (error) {
      alert.error(error);
      dispatch(clearErrors());
    }
  }, [dispatch, alert, isAuthenticated, error, navigate]);

  useEffect(() => {
    // Check if passwords match when either password field changes
    if (password || passwordConfirm) {
      setPasswordMatch(password === passwordConfirm);
    }
  }, [password, passwordConfirm]);

  const validateForm = () => {
    const errors = {};

    if (!name.trim()) {
      errors.name = "Name is required";
    }

    if (!email) {
      errors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      errors.email = "Email is invalid";
    }

    if (!password) {
      errors.password = "Password is required";
    } else if (password.length < 6) {
      errors.password = "Password must be at least 6 characters";
    }

    if (!passwordConfirm) {
      errors.passwordConfirm = "Please confirm your password";
    } else if (password !== passwordConfirm) {
      errors.passwordConfirm = "Passwords do not match";
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const submitHandler = (e) => {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
      return;
    }

    const userData = {
      name,
      email,
      password,
    };

    dispatch(register(userData));
  };

  const onChange = (e) => {
    setUser({ ...user, [e.target.name]: e.target.value });
  };

  return (
    <Fragment>
      <MetaData title={"Register User"} />

      {loading ? (
        <Loader />
      ) : (
        <div className="container container-fluid">
          <div className="row wrapper">
            <div className="col-10 col-lg-5">
              <form
                className="shadow-lg"
                onSubmit={submitHandler}
                encType="multipart/form-data"
              >
                <h1 className="mb-3 text-center">Create Account</h1>

                <div className="form-group">
                  <label htmlFor="name_field">Full Name</label>
                  <input
                    type="text"
                    id="name_field"
                    className={`form-control ${
                      formErrors.name ? "is-invalid" : ""
                    }`}
                    name="name"
                    placeholder="Enter your full name"
                    value={name}
                    onChange={onChange}
                  />
                  {formErrors.name && (
                    <div className="invalid-feedback">{formErrors.name}</div>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="email_field">Email</label>
                  <input
                    type="email"
                    id="email_field"
                    className={`form-control ${
                      formErrors.email ? "is-invalid" : ""
                    }`}
                    name="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={onChange}
                  />
                  {formErrors.email && (
                    <div className="invalid-feedback">{formErrors.email}</div>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="password_field">Password</label>
                  <input
                    type="password"
                    id="password_field"
                    className={`form-control ${
                      formErrors.password ? "is-invalid" : ""
                    }`}
                    name="password"
                    placeholder="Create a password"
                    value={password}
                    onChange={onChange}
                  />
                  {formErrors.password && (
                    <div className="invalid-feedback">
                      {formErrors.password}
                    </div>
                  )}
                  <small className="form-text text-muted">
                    Password must be at least 6 characters
                  </small>
                </div>

                <div className="form-group">
                  <label htmlFor="confirm_password_field">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirm_password_field"
                    className={`form-control ${
                      formErrors.passwordConfirm ? "is-invalid" : ""
                    }`}
                    name="passwordConfirm"
                    placeholder="Confirm your password"
                    value={passwordConfirm}
                    onChange={(e) => setPasswordConfirm(e.target.value)}
                  />
                  {formErrors.passwordConfirm && (
                    <div className="invalid-feedback">
                      {formErrors.passwordConfirm}
                    </div>
                  )}
                </div>

                <button
                  id="register_button"
                  type="submit"
                  className="btn btn-block py-3"
                  disabled={loading}
                >
                  {loading ? "Creating Account..." : "REGISTER"}
                </button>

                <div className="text-center mt-4">
                  <span className="text-muted">Already have an account? </span>
                  <Link to="/login" className="ml-1">
                    Login here
                  </Link>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </Fragment>
  );
};

export default Register;
