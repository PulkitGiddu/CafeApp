import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:arthcafe_app/core/network/dio_client.dart';
import 'package:arthcafe_app/core/constants/app_config.dart';
import 'package:arthcafe_app/core/mock/mock_data.dart';
import '../data/order_repository.dart';

final orderRepositoryProvider = Provider<OrderRepository>((ref) {
  return OrderRepository(ref.read(dioProvider));
});

final ordersProvider = FutureProvider<List<OrderModel>>((ref) async {
  if (kUseMockData) {
    await Future.delayed(const Duration(milliseconds: 400));
    return MockData.orders;
  }
  final repo = ref.read(orderRepositoryProvider);
  return await repo.getOrders();
});

final orderDetailProvider =
    FutureProvider.family<Map<String, dynamic>, String>((ref, orderId) async {
  if (kUseMockData) {
    await Future.delayed(const Duration(milliseconds: 300));
    return MockData.orderDetail(orderId);
  }
  final repo = ref.read(orderRepositoryProvider);
  return await repo.getOrderDetail(orderId);
});
