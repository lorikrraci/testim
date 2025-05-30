const express = require('express')
const router = express.Router();

const { newOrder, 
        getSingleOrder, 
        myOrders,
        allOrders, 
        updateOrders,
        deleteOrder} = require('../controllers/orderController')

const { isAuthenticatedUser, authorizeRoles } = require('../middlewares/auth')

router.route('/order/new').post(isAuthenticatedUser, newOrder);

router.route('/order/me').get(isAuthenticatedUser, myOrders);
router.route('/order/:id').get(isAuthenticatedUser, getSingleOrder);

router.route('/admin/order').get(isAuthenticatedUser,authorizeRoles('admin'), allOrders);
router.route('/admin/order/:id')
    .put(isAuthenticatedUser,authorizeRoles('admin'), updateOrders)
    .delete(isAuthenticatedUser,authorizeRoles('admin'), deleteOrder);


module.exports = router;