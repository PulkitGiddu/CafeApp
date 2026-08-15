import 'package:dio/dio.dart';
import 'package:arthcafe_app/core/constants/api_constants.dart';

class OrderModel {
  final String id;
  final String status;
  final String paymentStatus;
  final String? paymentMethod;
  final double totalAmount;
  final String? notes;
  final int itemsCount;
  final DateTime createdAt;
  final DateTime updatedAt;

  const OrderModel({
    required this.id,
    required this.status,
    required this.paymentStatus,
    this.paymentMethod,
    required this.totalAmount,
    this.notes,
    this.itemsCount = 0,
    required this.createdAt,
    required this.updatedAt,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'],
      status: json['status'],
      paymentStatus: json['payment_status'],
      paymentMethod: json['payment_method'],
      totalAmount: (json['total_amount'] as num).toDouble(),
      notes: json['notes'],
      itemsCount: json['items_count'] ?? 0,
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
    );
  }
}

class OrderCreateResponse {
  final String orderId;
  final double totalAmount;
  final String status;
  final String paymentStatus;
  final Map<String, dynamic>? razorpay;

  const OrderCreateResponse({
    required this.orderId,
    required this.totalAmount,
    required this.status,
    required this.paymentStatus,
    this.razorpay,
  });

  factory OrderCreateResponse.fromJson(Map<String, dynamic> json) {
    return OrderCreateResponse(
      orderId: json['order_id'],
      totalAmount: (json['total_amount'] as num).toDouble(),
      status: json['status'],
      paymentStatus: json['payment_status'],
      razorpay: json['razorpay'],
    );
  }
}

class OrderRepository {
  final Dio _dio;

  OrderRepository(this._dio);

  Future<OrderCreateResponse> createOrder({
    required String addressId,
    required String paymentMethod,
    String? notes,
    required List<Map<String, dynamic>> items,
  }) async {
    final response = await _dio.post(ApiConstants.orders, data: {
      'address_id': addressId,
      'payment_method': paymentMethod,
      if (notes != null) 'notes': notes,
      'items': items,
    });
    return OrderCreateResponse.fromJson(response.data);
  }

  Future<List<OrderModel>> getOrders() async {
    final response = await _dio.get(ApiConstants.orders);
    return (response.data as List)
        .map((o) => OrderModel.fromJson(o))
        .toList();
  }

  Future<Map<String, dynamic>> getOrderDetail(String orderId) async {
    final response = await _dio.get('${ApiConstants.orders}/$orderId');
    return response.data;
  }
}
