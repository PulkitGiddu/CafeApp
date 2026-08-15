import 'product_model.dart';

class CategoryModel {
  final String id;
  final String name;
  final String? description;
  final List<ProductModel> products;

  const CategoryModel({
    required this.id,
    required this.name,
    this.description,
    required this.products,
  });

  factory CategoryModel.fromJson(Map<String, dynamic> json) {
    return CategoryModel(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      products: (json['products'] as List)
          .map((p) => ProductModel.fromJson(p))
          .toList(),
    );
  }
}
