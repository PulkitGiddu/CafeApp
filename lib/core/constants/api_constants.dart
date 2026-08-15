class ApiConstants {
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1'; // Android emulator
  // static const String baseUrl = 'http://localhost:8000/api/v1'; // iOS simulator

  // Auth
  static const String sendOtp = '/auth/send-otp';
  static const String verifyOtp = '/auth/verify-otp';

  // Menu
  static const String menu = '/menu';

  // Addresses
  static const String addresses = '/addresses';

  // Orders
  static const String orders = '/orders';

  // Payments
  static const String verifyPayment = '/payments/verify';
}
