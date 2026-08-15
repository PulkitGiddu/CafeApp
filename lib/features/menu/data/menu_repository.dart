import 'package:dio/dio.dart';
import 'package:arthcafe_app/core/constants/api_constants.dart';
import '../models/category_model.dart';

class MenuRepository {
  final Dio _dio;

  MenuRepository(this._dio);

  Future<List<CategoryModel>> getMenu() async {
    final response = await _dio.get(ApiConstants.menu);
    final categories = (response.data['categories'] as List)
        .map((c) => CategoryModel.fromJson(c))
        .toList();
    return categories;
  }
}
