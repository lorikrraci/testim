import React, { Fragment, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { useAlert } from "react-alert";

import { deleteAccount, clearErrors } from "../../actions/userActions";
import { LOGOUT_SUCCESS } from "../../constants/userConstants";
import MetaData from "../layout/MetaData";
import Loader from "../layout/Loader";

const Profile = () => {
  const { user, loading } = useSelector((state) => state.auth);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const dispatch = useDispatch();
  const alert = useAlert();
  const navigate = useNavigate();

  const deleteAccountHandler = () => {
    dispatch(deleteAccount())
      .then(() => {
        alert.success("Your account has been deleted successfully");
        dispatch({ type: LOGOUT_SUCCESS });
        navigate("/");
      })
      .catch((error) => {
        alert.error(error || "Account deletion failed");
        dispatch(clearErrors());
      });
  };

  return (
    <Fragment>
      {loading ? (
        <Loader />
      ) : (
        <Fragment>
          <MetaData title={"Your Profile"} />

          <h2 className="mt-5 ml-5">My Profile</h2>
          <div className="row justify-content-around mt-5 user-info">
            <div className="col-12 col-md-3">
              <figure className="avatar avatar-profile">
                <img
                  className="rounded-circle img-fluid"
                  src={user.avatar && user.avatar.url}
                  alt={user.name}
                />
              </figure>
              <Link
                to="/me/update"
                id="edit_profile"
                className="btn btn-primary btn-block my-5"
              >
                Edit Profile
              </Link>
            </div>

            <div className="col-12 col-md-5">
              <h4>Full Name</h4>
              <p>{user.name}</p>

              <h4>Email Address</h4>
              <p>{user.email}</p>

              <h4>Joined On</h4>
              <p>{String(user.createdAt).substring(0, 10)}</p>

              {user.role !== "admin" && (
                <Link to="/orders/me" className="btn btn-danger btn-block mt-5">
                  My Orders
                </Link>
              )}

              <Link
                to="/password/update"
                className="btn btn-primary btn-block mt-3"
              >
                Change Password
              </Link>

              <button
                className="btn btn-danger btn-block mt-3"
                onClick={() => setShowConfirmation(true)}
              >
                Delete Account
              </button>

              {showConfirmation && (
                <div className="mt-3 p-3 border border-danger rounded">
                  <p className="text-danger">
                    Are you sure you want to delete your account? This action
                    cannot be undone.
                  </p>
                  <div className="d-flex justify-content-between">
                    <button
                      className="btn btn-danger"
                      onClick={deleteAccountHandler}
                    >
                      Yes, Delete My Account
                    </button>
                    <button
                      className="btn btn-secondary"
                      onClick={() => setShowConfirmation(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Fragment>
      )}
    </Fragment>
  );
};

export default Profile;
