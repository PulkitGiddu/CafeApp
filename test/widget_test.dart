import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:arthcafe_app/app.dart';

void main() {
  testWidgets('App starts correctly', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: ArthCafeApp(),
      ),
    );
    // Basic smoke test
    expect(find.text('ArthCafe'), findsOneWidget);
  });
}
