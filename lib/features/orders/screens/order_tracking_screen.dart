 import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/constants/app_colors.dart';
import '../providers/order_provider.dart';

class OrderTrackingScreen extends ConsumerWidget {
  final String orderId;

  const OrderTrackingScreen({super.key, required this.orderId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orderAsync = ref.watch(orderDetailProvider(orderId));

    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (Navigator.of(context).canPop()) {
              Navigator.of(context).pop();
            } else {
              context.go('/home');
            }
          },
        ),
        title: Text('Order #${orderId.substring(0, 8)}'),
        actions: [
          TextButton.icon(
            onPressed: () => context.go('/home'),
            icon: const Icon(Icons.home_outlined, size: 20),
            label: const Text('Home'),
          ),
        ],
      ),
      body: orderAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (_, __) => const Center(child: Text('Failed to load order details')),
        data: (order) {
          final status = order['status'] as String;
          final items = order['items'] as List? ?? [];
          final total = (order['total_amount'] as num).toDouble();

          return SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Status tracker
                _buildStatusTracker(status),

                const SizedBox(height: 32),

                // Order items
                const Text(
                  'Order Items',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    children: [
                      ...items.map((item) => Padding(
                            padding: const EdgeInsets.only(bottom: 10),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Text(
                                    '${item['product_name'] ?? 'Item'} × ${item['quantity']}',
                                    style: const TextStyle(fontSize: 14),
                                  ),
                                ),
                                Text(
                                  '₹${((item['price'] as num).toDouble() * (item['quantity'] as num).toInt()).toStringAsFixed(0)}',
                                  style: const TextStyle(fontWeight: FontWeight.w600),
                                ),
                              ],
                            ),
                          )),
                      const Divider(height: 20),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Total',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          Text(
                            '₹${total.toStringAsFixed(0)}',
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w800,
                              color: AppColors.primary,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                // Payment info
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.payment, color: AppColors.primary),
                      const SizedBox(width: 12),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Payment: ${order['payment_method'] ?? 'N/A'}',
                            style: const TextStyle(fontWeight: FontWeight.w600),
                          ),
                          Text(
                            'Status: ${order['payment_status'] ?? 'N/A'}',
                            style: const TextStyle(
                              color: AppColors.textSecondary,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatusTracker(String currentStatus) {
    final steps = [
      {'key': 'PLACED', 'label': 'Placed', 'icon': Icons.receipt_long},
      {'key': 'PREPARING', 'label': 'Preparing', 'icon': Icons.restaurant},
      {'key': 'OUT_FOR_DELIVERY', 'label': 'On the Way', 'icon': Icons.delivery_dining},
      {'key': 'DELIVERED', 'label': 'Delivered', 'icon': Icons.check_circle},
    ];

    final statusOrder = ['PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED'];
    final currentIndex = statusOrder.indexOf(currentStatus);
    final isCancelled = currentStatus == 'CANCELLED';

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(20),
      ),
      child: isCancelled
          ? Center(
              child: Column(
                children: [
                  const Icon(Icons.cancel, size: 48, color: AppColors.error),
                  const SizedBox(height: 12),
                  const Text(
                    'Order Cancelled',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: AppColors.error,
                    ),
                  ),
                ],
              ),
            )
          : Column(
              children: List.generate(steps.length, (index) {
                final step = steps[index];
                final isCompleted = index <= currentIndex;
                final isCurrent = index == currentIndex;

                return Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Timeline dot + line
                    Column(
                      children: [
                        Container(
                          width: 36,
                          height: 36,
                          decoration: BoxDecoration(
                            color: isCompleted
                                ? AppColors.primary
                                : AppColors.surfaceVariant,
                            shape: BoxShape.circle,
                            boxShadow: isCurrent
                                ? [
                                    BoxShadow(
                                      color: AppColors.primary.withValues(alpha: 0.3),
                                      blurRadius: 8,
                                    ),
                                  ]
                                : [],
                          ),
                          child: Icon(
                            step['icon'] as IconData,
                            color: isCompleted ? Colors.white : AppColors.textLight,
                            size: 18,
                          ),
                        ),
                        if (index < steps.length - 1)
                          Container(
                            width: 2,
                            height: 32,
                            color: isCompleted
                                ? AppColors.primary
                                : AppColors.surfaceVariant,
                          ),
                      ],
                    ),
                    const SizedBox(width: 14),
                    // Label
                    Padding(
                      padding: const EdgeInsets.only(top: 6),
                      child: Text(
                        step['label'] as String,
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight:
                              isCurrent ? FontWeight.w700 : FontWeight.w500,
                          color: isCompleted
                              ? AppColors.textPrimary
                              : AppColors.textLight,
                        ),
                      ),
                    ),
                  ],
                );
              }),
            ),
    );
  }
}
