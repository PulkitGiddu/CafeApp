import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:arthcafe_app/core/network/dio_client.dart';
import 'package:arthcafe_app/core/constants/app_config.dart';
import 'package:arthcafe_app/core/mock/mock_data.dart';
import '../data/address_repository.dart';

final addressRepositoryProvider = Provider<AddressRepository>((ref) {
  return AddressRepository(ref.read(dioProvider));
});

final addressesProvider = FutureProvider<List<AddressModel>>((ref) async {
  if (kUseMockData) {
    await Future.delayed(const Duration(milliseconds: 300));
    return MockData.addresses;
  }
  final repo = ref.read(addressRepositoryProvider);
  return await repo.getAddresses();
});

class SelectedAddressNotifier extends Notifier<AddressModel?> {
  @override
  AddressModel? build() => null;

  void select(AddressModel address) {
    state = address;
  }

  void clear() {
    state = null;
  }
}

final selectedAddressProvider =
    NotifierProvider<SelectedAddressNotifier, AddressModel?>(
        SelectedAddressNotifier.new);
