import '../../menu/models/product_model.dart';

class CartItemModel {
  final ProductModel product;
  int quantity;

  CartItemModel({required this.product, this.quantity = 1});

  double get totalPrice => product.price * quantity;

  Map<String, dynamic> toOrderJson() {
    return {
      'product_id': product.id,
      'quantity': quantity,
    };
  }
}
