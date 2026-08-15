import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:arthcafe_app/core/network/dio_client.dart';
import 'package:arthcafe_app/core/constants/app_config.dart';
import 'package:arthcafe_app/core/mock/mock_data.dart';
import '../data/menu_repository.dart';
import '../models/category_model.dart';
import '../models/product_model.dart';

final menuRepositoryProvider = Provider<MenuRepository>((ref) {
  return MenuRepository(ref.read(dioProvider));
});

final menuProvider = FutureProvider<List<CategoryModel>>((ref) async {
  if (kUseMockData) {
    await Future.delayed(const Duration(milliseconds: 500));
    return MockData.menuCategories;
  }
  final repo = ref.read(menuRepositoryProvider);
  return await repo.getMenu();
});

/// Get a specific product by ID from the cached menu data
final productByIdProvider = Provider.family<ProductModel?, String>((ref, id) {
  final menuAsync = ref.watch(menuProvider);
  return menuAsync.whenOrNull(
    data: (categories) {
      for (final cat in categories) {
        for (final product in cat.products) {
          if (product.id == id) return product;
        }
      }
      return null;
    },
  );
});
