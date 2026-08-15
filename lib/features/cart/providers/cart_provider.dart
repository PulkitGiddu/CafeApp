import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../menu/models/product_model.dart';
import '../models/cart_item_model.dart';

class CartNotifier extends Notifier<List<CartItemModel>> {
  @override
  List<CartItemModel> build() => [];

  void addItem(ProductModel product) {
    final index = state.indexWhere((item) => item.product.id == product.id);
    if (index >= 0) {
      state = [
        for (int i = 0; i < state.length; i++)
          if (i == index)
            CartItemModel(product: state[i].product, quantity: state[i].quantity + 1)
          else
            state[i],
      ];
    } else {
      state = [...state, CartItemModel(product: product)];
    }
  }

  void removeItem(String productId) {
    state = state.where((item) => item.product.id != productId).toList();
  }

  void updateQuantity(String productId, int quantity) {
    if (quantity <= 0) {
      removeItem(productId);
      return;
    }
    state = [
      for (final item in state)
        if (item.product.id == productId)
          CartItemModel(product: item.product, quantity: quantity)
        else
          item,
    ];
  }

  void incrementQuantity(String productId) {
    state = [
      for (final item in state)
        if (item.product.id == productId)
          CartItemModel(product: item.product, quantity: item.quantity + 1)
        else
          item,
    ];
  }

  void decrementQuantity(String productId) {
    final item = state.firstWhere((i) => i.product.id == productId);
    if (item.quantity <= 1) {
      removeItem(productId);
    } else {
      updateQuantity(productId, item.quantity - 1);
    }
  }

  void clear() {
    state = [];
  }

  double get totalAmount =>
      state.fold(0.0, (sum, item) => sum + item.totalPrice);
}

final cartProvider =
    NotifierProvider<CartNotifier, List<CartItemModel>>(CartNotifier.new);

final cartTotalProvider = Provider<double>((ref) {
  final items = ref.watch(cartProvider);
  return items.fold(0.0, (sum, item) => sum + item.totalPrice);
});
