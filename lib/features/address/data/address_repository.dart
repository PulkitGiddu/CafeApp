import 'package:dio/dio.dart';
import 'package:arthcafe_app/core/constants/api_constants.dart';

class AddressModel {
  final String id;
  final String addressLine;
  final String city;
  final String state;
  final double? latitude;
  final double? longitude;
  final bool isDefault;

  const AddressModel({
    required this.id,
    required this.addressLine,
    required this.city,
    required this.state,
    this.latitude,
    this.longitude,
    this.isDefault = false,
  });

  factory AddressModel.fromJson(Map<String, dynamic> json) {
    return AddressModel(
      id: json['id'],
      addressLine: json['address_line'] ?? '',
      city: json['city'] ?? '',
      state: json['state'] ?? '',
      latitude: json['latitude'] != null ? double.tryParse(json['latitude'].toString()) : null,
      longitude: json['longitude'] != null ? double.tryParse(json['longitude'].toString()) : null,
      isDefault: json['is_default'] ?? false,
    );
  }

  String get fullAddress => '$addressLine, $city, $state';
}

class AddressRepository {
  final Dio _dio;

  AddressRepository(this._dio);

  Future<List<AddressModel>> getAddresses() async {
    final response = await _dio.get(ApiConstants.addresses);
    return (response.data as List)
        .map((a) => AddressModel.fromJson(a))
        .toList();
  }

  Future<AddressModel> createAddress({
    required String addressLine,
    required String city,
    required String state,
    double? latitude,
    double? longitude,
    bool isDefault = false,
  }) async {
    final response = await _dio.post(ApiConstants.addresses, data: {
      'address_line': addressLine,
      'city': city,
      'state': state,
      if (latitude != null) 'latitude': latitude,
      if (longitude != null) 'longitude': longitude,
      'is_default': isDefault,
    });
    return AddressModel.fromJson(response.data);
  }

  Future<void> deleteAddress(String addressId) async {
    await _dio.delete('${ApiConstants.addresses}/$addressId');
  }
}
