import React from "react";
import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import Loader from "../layout/Loader";

const ProtectedRoute = ({ children, isAdmin = false }) => {
  const { isAuthenticated, loading, user } = useSelector((state) => state.auth);

  console.log("ProtectedRoute - auth state:", {
    isAuthenticated,
    loading,
    userId: user?._id,
    path: window.location.pathname,
  });

  if (loading) {
    return <Loader />;
  }

  if (!isAuthenticated) {
    console.log("User not authenticated, redirecting to login");
    return (
      <Navigate to="/login" state={{ redirect: window.location.pathname }} />
    );
  }

  if (isAdmin && user.role !== "admin") {
    console.log("User not admin, redirecting to home");
    return <Navigate to="/" />;
  }

  console.log("User authenticated, rendering protected content");
  return children;
};

export default ProtectedRoute;
