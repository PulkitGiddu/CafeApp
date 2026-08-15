import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:arthcafe_app/core/network/dio_client.dart';
import 'package:arthcafe_app/core/constants/app_config.dart';
import '../data/auth_repository.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(ref.read(dioProvider));
});

enum AuthStatus { initial, otpSent, loading, authenticated, error }

class AuthState {
  final AuthStatus status;
  final String? errorMessage;
  final String? userId;
  final bool isNewUser;

  const AuthState({
    this.status = AuthStatus.initial,
    this.errorMessage,
    this.userId,
    this.isNewUser = false,
  });

  AuthState copyWith({
    AuthStatus? status,
    String? errorMessage,
    String? userId,
    bool? isNewUser,
  }) {
    return AuthState(
      status: status ?? this.status,
      errorMessage: errorMessage,
      userId: userId ?? this.userId,
      isNewUser: isNewUser ?? this.isNewUser,
    );
  }
}

class AuthNotifier extends Notifier<AuthState> {
  @override
  AuthState build() => const AuthState();

  AuthRepository get _repo => ref.read(authRepositoryProvider);

  Future<void> sendOtp(String phone) async {
    state = state.copyWith(status: AuthStatus.loading);

    if (kUseMockData) {
      await Future.delayed(const Duration(milliseconds: 800));
      state = state.copyWith(status: AuthStatus.otpSent);
      return;
    }

    try {
      await _repo.sendOtp(phone);
      state = state.copyWith(status: AuthStatus.otpSent);
    } catch (e) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: 'Failed to send OTP. Please try again.',
      );
    }
  }

  Future<void> verifyOtp(String phone, String otp) async {
    state = state.copyWith(status: AuthStatus.loading);

    if (kUseMockData) {
      await Future.delayed(const Duration(milliseconds: 800));
      if (otp == '1234' || otp == '123456') {
        state = state.copyWith(
          status: AuthStatus.authenticated,
          userId: 'mock-user-001',
          isNewUser: false,
        );
      } else {
        state = state.copyWith(
          status: AuthStatus.error,
          errorMessage: 'Invalid OTP. Use 1234 for testing.',
        );
      }
      return;
    }

    try {
      final data = await _repo.verifyOtp(phone, otp);
      state = state.copyWith(
        status: AuthStatus.authenticated,
        userId: data['user_id'],
        isNewUser: data['is_new_user'] ?? false,
      );
    } catch (e) {
      state = state.copyWith(
        status: AuthStatus.error,
        errorMessage: 'Invalid OTP. Please try again.',
      );
    }
  }

  Future<void> checkAuth() async {
    if (kUseMockData) return; // Always show login in mock mode
    final isLoggedIn = await _repo.isLoggedIn();
    if (isLoggedIn) {
      final userId = await _repo.getUserId();
      state = state.copyWith(
        status: AuthStatus.authenticated,
        userId: userId,
      );
    }
  }

  Future<void> logout() async {
    if (!kUseMockData) await _repo.logout();
    state = const AuthState();
  }
}

final authProvider = NotifierProvider<AuthNotifier, AuthState>(AuthNotifier.new);
