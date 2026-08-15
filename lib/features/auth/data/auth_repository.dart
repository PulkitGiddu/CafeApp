import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:arthcafe_app/core/constants/api_constants.dart';

class AuthRepository {
  final Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  AuthRepository(this._dio);

  Future<void> sendOtp(String phone) async {
    await _dio.post(ApiConstants.sendOtp, data: {'phone': phone});
  }

  Future<Map<String, dynamic>> verifyOtp(String phone, String otp) async {
    final response = await _dio.post(
      ApiConstants.verifyOtp,
      data: {'phone': phone, 'otp': otp},
    );
    final data = response.data;

    // Store token securely
    await _storage.write(key: 'access_token', value: data['access_token']);
    await _storage.write(key: 'user_id', value: data['user_id']);

    return data;
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }

  Future<String?> getUserId() async {
    return await _storage.read(key: 'user_id');
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }
}
