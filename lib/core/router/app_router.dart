import 'package:go_router/go_router.dart';

import '../../features/auth/screens/login_screen.dart';
import '../../features/menu/screens/home_screen.dart';
import '../../features/menu/screens/product_detail_screen.dart';
import '../../features/cart/screens/cart_screen.dart';
import '../../features/address/screens/address_screen.dart';
import '../../features/orders/screens/checkout_screen.dart';
import '../../features/orders/screens/order_success_screen.dart';
import '../../features/orders/screens/order_history_screen.dart';
import '../../features/orders/screens/order_tracking_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/home',
      name: 'home',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/product/:id',
      name: 'product-detail',
      builder: (context, state) => ProductDetailScreen(
        productId: state.pathParameters['id']!,
      ),
    ),
    GoRoute(
      path: '/cart',
      name: 'cart',
      builder: (context, state) => const CartScreen(),
    ),
    GoRoute(
      path: '/addresses',
      name: 'addresses',
      builder: (context, state) => const AddressScreen(),
    ),
    GoRoute(
      path: '/checkout',
      name: 'checkout',
      builder: (context, state) => const CheckoutScreen(),
    ),
    GoRoute(
      path: '/order-success/:orderId',
      name: 'order-success',
      builder: (context, state) => OrderSuccessScreen(
        orderId: state.pathParameters['orderId']!,
      ),
    ),
    GoRoute(
      path: '/orders',
      name: 'order-history',
      builder: (context, state) => const OrderHistoryScreen(),
    ),
    GoRoute(
      path: '/orders/:orderId',
      name: 'order-tracking',
      builder: (context, state) => OrderTrackingScreen(
        orderId: state.pathParameters['orderId']!,
      ),
    ),
  ],
);
