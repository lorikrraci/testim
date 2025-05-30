import axios from "axios";

import {
  ALL_PRODUCTS_REQUEST,
  ALL_PRODUCTS_SUCCESS,
  ALL_PRODUCTS_FAIL,
  PRODUCT_DETAILS_REQUEST,
  PRODUCT_DETAILS_SUCCESS,
  PRODUCT_DETAILS_FAIL,
  CLEAR_ERRORS,
  ADMIN_PRODUCTS_REQUEST,
  ADMIN_PRODUCTS_SUCCESS,
  ADMIN_PRODUCTS_FAIL,
  NEW_PRODUCT_REQUEST,
  NEW_PRODUCT_SUCCESS,
  NEW_PRODUCT_FAIL,
  UPDATE_PRODUCT_REQUEST,
  UPDATE_PRODUCT_SUCCESS,
  UPDATE_PRODUCT_FAIL,
  DELETE_PRODUCT_REQUEST,
  DELETE_PRODUCT_SUCCESS,
  DELETE_PRODUCT_FAIL,
} from "../constants/productConstants";

export const getProducts =
  (
    keyword = "",
    currentPage = 1,
    price = [1, 5000],
    category = "",
    rating = 0,
    limit = 4 // Changed default from 8 to 4
  ) =>
  async (dispatch) => {
    try {
      dispatch({ type: ALL_PRODUCTS_REQUEST });

      // Fix URL encoding for query parameters
      let link = `/api/v1/products?keyword=${encodeURIComponent(
        keyword
      )}&page=${currentPage}&price[lte]=${price[1]}&price[gte]=${
        price[0]
      }&ratings[gte]=${rating}&limit=${limit}`;

      if (category) {
        link = `/api/v1/products?keyword=${encodeURIComponent(
          keyword
        )}&page=${currentPage}&price[lte]=${price[1]}&price[gte]=${
          price[0]
        }&category=${encodeURIComponent(
          category
        )}&ratings[gte]=${rating}&limit=${limit}`;
      }

      console.log("API Request URL:", link);

      const { data } = await axios.get(link);

      dispatch({
        type: ALL_PRODUCTS_SUCCESS,
        payload: data,
      });
    } catch (error) {
      console.log("Product fetch error:", error);
      dispatch({
        type: ALL_PRODUCTS_FAIL,
        payload: error.response.data.message,
      });
    }
  };

export const getProductDetails = (id) => async (dispatch) => {
  try {
    dispatch({ type: PRODUCT_DETAILS_REQUEST });

    console.log(`Fetching product details for ID: ${id}`);

    // Validate ID before making request
    if (!id || id === "undefined") {
      throw new Error("Invalid product ID");
    }

    // Same pattern - avoid destructuring directly
    const response = await axios.get(`/api/v1/products/${id}`);

    if (!response) {
      throw new Error("No response received from server");
    }

    const { data } = response;

    dispatch({
      type: PRODUCT_DETAILS_SUCCESS,
      payload: data.product,
    });
  } catch (error) {
    console.error("Product details fetch error:", error);

    // More detailed error handling
    let errorMessage = "Unknown Error";

    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      errorMessage =
        error.response.data.message || `Server error: ${error.response.status}`;
      console.error("Server response:", error.response.data);
    } else if (error.request) {
      // The request was made but no response was received
      errorMessage = "No response from server";
      console.error("Request made but no response received");
    } else {
      // Something happened in setting up the request
      errorMessage = error.message;
      console.error("Error setting up request:", error.message);
    }

    dispatch({
      type: PRODUCT_DETAILS_FAIL,
      payload: errorMessage,
    });
  }
};

//Clear errors
export const clearErrors = () => async (dispatch) => {
  dispatch({
    type: CLEAR_ERRORS,
  });
};

// Get all products for admin
export const getAdminProducts = () => async (dispatch) => {
  try {
    dispatch({ type: ADMIN_PRODUCTS_REQUEST });

    const { data } = await axios.get(`/api/v1/admin/products`);

    dispatch({
      type: ADMIN_PRODUCTS_SUCCESS,
      payload: data.products,
    });
  } catch (error) {
    dispatch({
      type: ADMIN_PRODUCTS_FAIL,
      payload: error.response.data.message,
    });
  }
};

// Create new product - ADMIN
export const newProduct = (productData) => async (dispatch) => {
  try {
    dispatch({ type: NEW_PRODUCT_REQUEST });

    console.log("Creating new product...");

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };

    // Log the form data keys to debug
    for (let key of productData.keys()) {
      console.log(`Form contains key: ${key}`);
    }

    // Log image files
    const imageFiles = productData.getAll("images");
    console.log(
      `Uploading ${imageFiles.length} images:`,
      imageFiles.map((file) => ({
        name: file.name,
        type: file.type,
        size: file.size,
      }))
    );

    // Fix the URL - make sure it's the correct admin endpoint
    const { data } = await axios.post(
      `/api/v1/admin/products/new`,
      productData,
      config
    );

    console.log("Product creation response:", data);

    dispatch({
      type: NEW_PRODUCT_SUCCESS,
      payload: data,
    });

    return data;
  } catch (error) {
    console.error("Product creation error:", error);
    console.error("Error details:", error.response?.data);

    dispatch({
      type: NEW_PRODUCT_FAIL,
      payload: error.response?.data?.message || "Failed to create product",
    });

    throw error;
  }
};

// Update Product - ADMIN
export const updateProduct = (id, productData) => async (dispatch) => {
  try {
    dispatch({ type: UPDATE_PRODUCT_REQUEST });

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };

    const { data } = await axios.put(
      `/api/v1/admin/products/${id}`,
      productData,
      config
    );

    dispatch({
      type: UPDATE_PRODUCT_SUCCESS,
      payload: data.success,
    });
  } catch (error) {
    dispatch({
      type: UPDATE_PRODUCT_FAIL,
      payload: error.response.data.message,
    });
  }
};

// Delete product - ADMIN
export const deleteProduct = (id) => async (dispatch) => {
  try {
    dispatch({ type: DELETE_PRODUCT_REQUEST });

    const { data } = await axios.delete(`/api/v1/admin/products/${id}`);

    dispatch({
      type: DELETE_PRODUCT_SUCCESS,
      payload: data.success,
    });
  } catch (error) {
    dispatch({
      type: DELETE_PRODUCT_FAIL,
      payload: error.response.data.message,
    });
  }
};
