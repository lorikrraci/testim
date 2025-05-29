import React, { Fragment, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAlert } from "react-alert";
import { useDispatch, useSelector } from "react-redux";
import { newProduct, clearErrors } from "../../actions/productActions";
import { NEW_PRODUCT_RESET } from "../../constants/productConstants";

import MetaData from "../layout/MetaData";
import Sidebar from "./Sidebar";

const NewProduct = () => {
  const [name, setName] = useState("");
  const [price, setPrice] = useState(0);
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [stock, setStock] = useState(0);
  const [seller, setSeller] = useState("");
  const [images, setImages] = useState([]);
  const [imagesPreview, setImagesPreview] = useState([]);
  const [formSubmitted, setFormSubmitted] = useState(false);

  const categories = [
    "Electronics",
    "Cameras",
    "Laptops",
    "Accessories",
    "Headphones",
    "Food",
    "Books",
    "Clothes/Shoes",
    "Beauty/Health",
    "Sports",
    "Outdoor",
    "Home",
  ];

  const alert = useAlert();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { loading, error, success } = useSelector(
    (state) => state.newProduct || {}
  );

  useEffect(() => {
    if (error) {
      alert.error(error);
      dispatch(clearErrors());
      setFormSubmitted(false);
    }

    if (success) {
      navigate("/admin/products");
      alert.success("Product created successfully");
      dispatch({ type: NEW_PRODUCT_RESET });
    }
  }, [dispatch, alert, error, success, navigate]);

  const submitHandler = (e) => {
    e.preventDefault();
    setFormSubmitted(true);

    // Validation
    if (!name || !description || !category || !seller) {
      alert.error("Please fill all required fields");
      setFormSubmitted(false);
      return;
    }

    if (price <= 0) {
      alert.error("Price must be greater than 0");
      setFormSubmitted(false);
      return;
    }

    if (stock < 0) {
      alert.error("Stock cannot be negative");
      setFormSubmitted(false);
      return;
    }

    if (images.length === 0) {
      alert.error("Please add at least one product image");
      setFormSubmitted(false);
      return;
    }

    const formData = new FormData();
    formData.set("name", name);
    formData.set("price", price);
    formData.set("description", description);
    formData.set("category", category);
    formData.set("stock", stock);
    formData.set("seller", seller);

    images.forEach((image) => {
      formData.append("images", image);
    });

    console.log("Submitting new product with data:", {
      name,
      price,
      description,
      category,
      stock,
      seller,
      imagesCount: images.length,
    });

    // Dispatch the action and handle the promise
    dispatch(newProduct(formData))
      .then(() => {
        console.log("Product created successfully");
      })
      .catch((error) => {
        console.error("Error creating product:", error);
        setFormSubmitted(false);
      });
  };

  const onChange = (e) => {
    const files = Array.from(e.target.files);

    // Validate file types
    const validFiles = files.filter(
      (file) =>
        file.type === "image/png" ||
        file.type === "image/jpeg" ||
        file.type === "image/jpg"
    );

    if (validFiles.length !== files.length) {
      alert.error("Please upload only PNG, JPEG or JPG images");
      return;
    }

    // Validate file sizes (max 2MB per file)
    const oversizedFiles = validFiles.filter(
      (file) => file.size > 2 * 1024 * 1024
    );
    if (oversizedFiles.length > 0) {
      alert.error("Some images exceed 2MB size limit");
      return;
    }

    setImagesPreview([]);
    setImages([]);

    validFiles.forEach((file) => {
      const reader = new FileReader();

      reader.onload = () => {
        if (reader.readyState === 2) {
          setImagesPreview((oldArray) => [...oldArray, reader.result]);
          setImages((oldArray) => [...oldArray, file]); // Store the actual file object
        }
      };

      reader.readAsDataURL(file);
    });
  };

  return (
    <Fragment>
      <MetaData title={"New Product"} />
      <div className="row">
        <div className="col-12 col-md-2">
          <Sidebar />
        </div>

        <div className="col-12 col-md-10">
          <Fragment>
            <div className="wrapper my-5">
              <form
                className="shadow-lg"
                onSubmit={submitHandler}
                encType="multipart/form-data"
              >
                <h1 className="mb-4">New Product</h1>

                <div className="form-group">
                  <label htmlFor="name_field">
                    Name <span className="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    id="name_field"
                    className="form-control"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="price_field">
                    Price <span className="text-danger">*</span>
                  </label>
                  <input
                    type="number"
                    id="price_field"
                    className="form-control"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    min="1"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="description_field">
                    Description <span className="text-danger">*</span>
                  </label>
                  <textarea
                    className="form-control"
                    id="description_field"
                    rows="8"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                  ></textarea>
                </div>

                <div className="form-group">
                  <label htmlFor="category_field">
                    Category <span className="text-danger">*</span>
                  </label>
                  <select
                    className="form-control"
                    id="category_field"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    required
                  >
                    <option value="">Select</option>
                    {categories.map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="stock_field">
                    Stock <span className="text-danger">*</span>
                  </label>
                  <input
                    type="number"
                    id="stock_field"
                    className="form-control"
                    value={stock}
                    onChange={(e) => setStock(e.target.value)}
                    min="0"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="seller_field">
                    Seller Name <span className="text-danger">*</span>
                  </label>
                  <input
                    type="text"
                    id="seller_field"
                    className="form-control"
                    value={seller}
                    onChange={(e) => setSeller(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>
                    Images <span className="text-danger">*</span>
                  </label>
                  <div className="custom-file">
                    <input
                      type="file"
                      name="product_images"
                      className="custom-file-input"
                      id="customFile"
                      onChange={onChange}
                      multiple
                      accept="image/png, image/jpeg, image/jpg"
                      required={images.length === 0}
                    />
                    <label className="custom-file-label" htmlFor="customFile">
                      Choose Images (PNG, JPEG, JPG, max 2MB each)
                    </label>
                  </div>

                  {imagesPreview.length > 0 && (
                    <div className="mt-3">
                      <h6>Selected Images:</h6>
                      <div className="d-flex flex-wrap">
                        {imagesPreview.map((img, index) => (
                          <div key={index} className="mr-2 mb-2">
                            <img
                              src={img}
                              alt={`Preview ${index}`}
                              width="55"
                              height="52"
                              className="mt-3 mr-2"
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <button
                  id="create_button"
                  type="submit"
                  className="btn btn-block py-3"
                  disabled={loading || formSubmitted}
                >
                  {loading ? "Creating..." : "CREATE PRODUCT"}
                </button>
              </form>
            </div>
          </Fragment>
        </div>
      </div>
    </Fragment>
  );
};

export default NewProduct;
