import React, { Fragment } from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { useAlert } from "react-alert";
import { logout } from "../../actions/userActions";
import Search from "./Search";

export const Header = () => {
  const alert = useAlert();
  const dispatch = useDispatch();

  const { cartItems } = useSelector((state) => state.cart);
  const { user, loading, isAuthenticated } = useSelector((state) => state.auth);

  const logoutHandler = () => {
    dispatch(logout());
    alert.success("Logged out successfully");
  };

  return (
    <Fragment>
      <nav className="navbar row">
        <div className="col-12 col-md-3">
          <div className="navbar-brand">
            <Link to="/">
              <img src="/images/shopit.logo.png" alt="Logo" />
            </Link>
          </div>
        </div>

        <div className="col-12 col-md-6 mt-2 mt-md-0">
          <Search />
        </div>

        <div className="col-12 col-md-3 mt-4 mt-md-0 text-center">
          {!isAuthenticated ? (
            <div className="auth-buttons d-flex justify-content-center">
              <Link to="/login" className="btn btn-auth mr-2">
                <i className="fa fa-sign-in-alt mr-1"></i> Login
              </Link>
              <Link to="/register" className="btn btn-auth">
                <i className="fa fa-user-plus mr-1"></i> Register
              </Link>
            </div>
          ) : (
            <div className="ml-4 dropdown d-inline">
              <Link
                to="#!"
                className="btn dropdown-toggle text-white mr-4"
                type="button"
                id="dropdownMenuButton"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                <figure className="avatar avatar-nav">
                  <img
                    src={user.avatar && user.avatar.url}
                    alt={user && user.name}
                    className="rounded-circle"
                  />
                </figure>
                <span>{user && user.name}</span>
              </Link>

              <div
                className="dropdown-menu"
                aria-labelledby="dropdownMenuButton"
              >
                {user && user.role === "admin" && (
                  <Link className="dropdown-item" to="/dashboard">
                    Dashboard
                  </Link>
                )}
                <Link className="dropdown-item" to="/profile">
                  Profile
                </Link>
                <Link className="dropdown-item" to="#!" onClick={logoutHandler}>
                  Logout
                </Link>
              </div>
            </div>
          )}

          <Link to="/cart" className="cart-link ml-3">
            <span id="cart" className="ml-3">
              Cart
            </span>
            <span className="ml-1" id="cart_count">
              {cartItems.length}
            </span>
          </Link>
        </div>
      </nav>
    </Fragment>
  );
};

export default Header;
