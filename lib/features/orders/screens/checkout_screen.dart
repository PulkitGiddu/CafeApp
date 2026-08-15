import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:arthcafe_app/core/constants/app_colors.dart';
import 'package:arthcafe_app/core/constants/app_config.dart';
import '../../address/providers/address_provider.dart';
import '../../cart/providers/cart_provider.dart';
import '../providers/order_provider.dart';

class CheckoutScreen extends ConsumerStatefulWidget {
  const CheckoutScreen({super.key});

  @override
  ConsumerState<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends ConsumerState<CheckoutScreen> {
  String _paymentMethod = 'UPI';
  final _notesController = TextEditingController();
  bool _isPlacingOrder = false;

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final cartItems = ref.watch(cartProvider);
    final total = ref.watch(cartTotalProvider);
    final selectedAddress = ref.watch(selectedAddressProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Checkout')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Delivery Address
            const Text(
              'Delivery Address',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 12),
            GestureDetector(
              onTap: () => context.push('/addresses'),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: selectedAddress != null
                        ? AppColors.primary
                        : AppColors.textLight,
                  ),
                ),
                child: selectedAddress != null
                    ? Row(
                        children: [
                          const Icon(Icons.location_on, color: AppColors.primary),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  selectedAddress.city,
                                  style: const TextStyle(fontWeight: FontWeight.w600),
                                ),
                                Text(
                                  selectedAddress.fullAddress,
                                  style: const TextStyle(
                                    color: AppColors.textSecondary,
                                    fontSize: 13,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const Icon(Icons.chevron_right, color: AppColors.textLight),
                        ],
                      )
                    : const Row(
                        children: [
                          Icon(Icons.add_location_alt, color: AppColors.primary),
                          SizedBox(width: 12),
                          Text(
                            'Select delivery address',
                            style: TextStyle(color: AppColors.textSecondary),
                          ),
                          Spacer(),
                          Icon(Icons.chevron_right, color: AppColors.textLight),
                        ],
                      ),
              ),
            ),

            const SizedBox(height: 28),

            // Payment Method
            const Text(
              'Payment Method',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 12),
            ..._buildPaymentOptions(),

            const SizedBox(height: 28),

            // Notes
            const Text(
              'Order Notes (optional)',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _notesController,
              maxLines: 3,
              decoration: const InputDecoration(
                hintText: 'Any special instructions...',
              ),
            ),

            const SizedBox(height: 28),

            // Order Summary
            const Text(
              'Order Summary',
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
                  ...cartItems.map((item) => Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Text(
                                '${item.product.name} × ${item.quantity}',
                                style: const TextStyle(fontSize: 14),
                              ),
                            ),
                            Text(
                              '₹${item.totalPrice.toStringAsFixed(0)}',
                              style: const TextStyle(fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      )),
                  const Divider(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Total',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      Text(
                        '₹${total.toStringAsFixed(0)}',
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.w800,
                          color: AppColors.primary,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: SizedBox(
            height: 56,
            child: ElevatedButton(
              onPressed: _isPlacingOrder || selectedAddress == null
                  ? null
                  : _placeOrder,
              child: _isPlacingOrder
                  ? const SizedBox(
                      width: 24,
                      height: 24,
                      child: CircularProgressIndicator(
                        color: Colors.white,
                        strokeWidth: 2.5,
                      ),
                    )
                  : Text(
                      'Place Order — ₹${total.toStringAsFixed(0)}',
                      style: const TextStyle(fontSize: 16),
                    ),
            ),
          ),
        ),
      ),
    );
  }

  List<Widget> _buildPaymentOptions() {
    final options = [
      {'value': 'UPI', 'label': 'UPI', 'icon': Icons.phone_android},
      {'value': 'CARD', 'label': 'Card', 'icon': Icons.credit_card},
      {'value': 'COD', 'label': 'Cash on Delivery', 'icon': Icons.money},
    ];

    return options.map((opt) {
      final isSelected = _paymentMethod == opt['value'];
      return GestureDetector(
        onTap: () => setState(() => _paymentMethod = opt['value'] as String),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          margin: const EdgeInsets.only(bottom: 10),
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          decoration: BoxDecoration(
            color: isSelected
                ? AppColors.primary.withValues(alpha: 0.05)
                : AppColors.surface,
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: isSelected ? AppColors.primary : Colors.grey.shade200,
              width: isSelected ? 2 : 1,
            ),
          ),
          child: Row(
            children: [
              Icon(
                opt['icon'] as IconData,
                color: isSelected ? AppColors.primary : AppColors.textSecondary,
              ),
              const SizedBox(width: 12),
              Text(
                opt['label'] as String,
                style: TextStyle(
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
                  color: isSelected ? AppColors.primary : AppColors.textPrimary,
                ),
              ),
              const Spacer(),
              if (isSelected)
                const Icon(Icons.check_circle, color: AppColors.primary, size: 22),
            ],
          ),
        ),
      );
    }).toList();
  }

  Future<void> _placeOrder() async {
    setState(() => _isPlacingOrder = true);

    try {
      if (kUseMockData) {
        // Simulate network delay
        await Future.delayed(const Duration(seconds: 1));
        final mockOrderId = 'order-mock-${DateTime.now().millisecondsSinceEpoch}';

        ref.read(cartProvider.notifier).clear();
        ref.invalidate(ordersProvider);

        if (mounted) {
          context.go('/order-success/$mockOrderId');
        }
        return;
      }

      final repo = ref.read(orderRepositoryProvider);
      final cartItems = ref.read(cartProvider);
      final selectedAddress = ref.read(selectedAddressProvider);

      final response = await repo.createOrder(
        addressId: selectedAddress!.id,
        paymentMethod: _paymentMethod,
        notes: _notesController.text.trim().isEmpty
            ? null
            : _notesController.text.trim(),
        items: cartItems.map((item) => item.toOrderJson()).toList(),
      );

      ref.read(cartProvider.notifier).clear();
      ref.invalidate(ordersProvider);

      if (mounted) {
        context.go('/order-success/${response.orderId}');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to place order: $e'),
            backgroundColor: AppColors.error,
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _isPlacingOrder = false);
    }
  }
}
