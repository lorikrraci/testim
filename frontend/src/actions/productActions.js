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
    rating = 0
  ) =>
  async (dispatch) => {
    try {
      dispatch({ type: ALL_PRODUCTS_REQUEST });

      // Fix URL encoding for query parameters
      let link = `/api/v1/products?keyword=${encodeURIComponent(
        keyword
      )}&page=${currentPage}&price[lte]=${price[1]}&price[gte]=${
        price[0]
      }&ratings[gte]=${rating}`;

      if (category) {
        link = `/api/v1/products?keyword=${encodeURIComponent(
          keyword
        )}&page=${currentPage}&price[lte]=${price[1]}&price[gte]=${
          price[0]
        }&category=${encodeURIComponent(category)}&ratings[gte]=${rating}`;
      }

      console.log("API Request URL:", link);

      // Add withCredentials to ensure cookies are sent
      const response = await axios.get(link, { withCredentials: true });

      // Check if response exists before destructuring
      if (!response) {
        throw new Error("No response received from server");
      }

      const { data } = response;

      dispatch({
        type: ALL_PRODUCTS_SUCCESS,
        payload: data,
      });
    } catch (error) {
      console.error("Product fetch error:", error);
      dispatch({
        type: ALL_PRODUCTS_FAIL,
        payload:
          error.response && error.response.data && error.response.data.message
            ? error.response.data.message
            : error.message || "Unknown Error",
      });
    }
  };

export const getProductDetails = (id) => async (dispatch) => {
  try {
    dispatch({ type: PRODUCT_DETAILS_REQUEST });

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
    dispatch({
      type: PRODUCT_DETAILS_FAIL,
      payload:
        error.response && error.response.data && error.response.data.message
          ? error.response.data.message
          : error.message || "Unknown Error",
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
