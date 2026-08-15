import '../../features/menu/models/category_model.dart';
import '../../features/menu/models/product_model.dart';
import '../../features/address/data/address_repository.dart';
import '../../features/orders/data/order_repository.dart';

class MockData {
  static final List<CategoryModel> menuCategories = [
    CategoryModel(
      id: 'cat-1',
      name: 'Hot Beverages',
      description: 'Freshly brewed hot drinks',
      products: [
        const ProductModel(
          id: 'prod-1',
          name: 'Cappuccino',
          description: 'Rich espresso with steamed milk foam',
          price: 180.00,
          imageUrl: 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-2',
          name: 'Latte',
          description: 'Smooth espresso with velvety steamed milk',
          price: 200.00,
          imageUrl: 'https://images.unsplash.com/photo-1561882468-9110e9e0e536?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-3',
          name: 'Americano',
          description: 'Bold espresso diluted with hot water',
          price: 150.00,
          imageUrl: 'https://images.unsplash.com/photo-1551030173-122aabc4489c?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-4',
          name: 'Masala Chai',
          description: 'Traditional Indian spiced tea with aromatic herbs',
          price: 80.00,
          imageUrl: 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-5',
          name: 'Hot Chocolate',
          description: 'Rich and creamy Belgian chocolate drink',
          price: 220.00,
          imageUrl: 'https://images.unsplash.com/photo-1517578239113-b03992dcdd25?w=400',
          isAvailable: true,
        ),
      ],
    ),
    CategoryModel(
      id: 'cat-2',
      name: 'Cold Beverages',
      description: 'Refreshing cold drinks',
      products: [
        const ProductModel(
          id: 'prod-6',
          name: 'Iced Coffee',
          description: 'Chilled coffee with ice and creamy milk',
          price: 200.00,
          imageUrl: 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-7',
          name: 'Cold Brew',
          description: 'Slow-steeped cold coffee concentrate, smooth and bold',
          price: 250.00,
          imageUrl: 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-8',
          name: 'Mango Smoothie',
          description: 'Fresh Alphonso mango blended with creamy yogurt',
          price: 180.00,
          imageUrl: 'https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-9',
          name: 'Fresh Lime Soda',
          description: 'Sparkling lime with fresh mint leaves',
          price: 120.00,
          imageUrl: 'https://images.unsplash.com/photo-1513558161293-cdaf765ed514?w=400',
          isAvailable: true,
        ),
      ],
    ),
    CategoryModel(
      id: 'cat-3',
      name: 'Snacks',
      description: 'Light bites and quick eats',
      products: [
        const ProductModel(
          id: 'prod-10',
          name: 'Veg Sandwich',
          description: 'Grilled sandwich with fresh seasonal vegetables',
          price: 150.00,
          imageUrl: 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-11',
          name: 'Paneer Wrap',
          description: 'Tandoori paneer in a warm, soft tortilla wrap',
          price: 180.00,
          imageUrl: 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-12',
          name: 'French Fries',
          description: 'Crispy golden fries served with spicy dip',
          price: 120.00,
          imageUrl: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-13',
          name: 'Garlic Bread',
          description: 'Toasted artisan bread with garlic herb butter',
          price: 130.00,
          imageUrl: 'https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=400',
          isAvailable: true,
        ),
      ],
    ),
    CategoryModel(
      id: 'cat-4',
      name: 'Desserts',
      description: 'Sweet treats to end your meal',
      products: [
        const ProductModel(
          id: 'prod-14',
          name: 'Chocolate Brownie',
          description: 'Warm, fudgy brownie served with vanilla ice cream',
          price: 200.00,
          imageUrl: 'https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-15',
          name: 'Cheesecake',
          description: 'Creamy New York style baked cheesecake',
          price: 250.00,
          imageUrl: 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400',
          isAvailable: true,
        ),
        const ProductModel(
          id: 'prod-16',
          name: 'Gulab Jamun',
          description: 'Soft, warm milk-solid dumplings soaked in rose syrup',
          price: 100.00,
          imageUrl: 'https://images.unsplash.com/photo-1666190050103-e44a193114e1?w=400',
          isAvailable: false,
        ),
      ],
    ),
  ];

  static final List<AddressModel> addresses = [
    const AddressModel(
      id: 'addr-1',
      addressLine: '42, MG Road, Near City Mall',
      city: 'Pune',
      state: 'Maharashtra',
      latitude: 18.5204,
      longitude: 73.8567,
      isDefault: true,
    ),
    const AddressModel(
      id: 'addr-2',
      addressLine: '15, FC Road, Opposite Cafe Zone',
      city: 'Pune',
      state: 'Maharashtra',
      latitude: 18.5314,
      longitude: 73.8446,
      isDefault: false,
    ),
  ];

  static final List<OrderModel> orders = [
    OrderModel(
      id: 'order-a1b2c3d4-mock',
      status: 'DELIVERED',
      paymentStatus: 'SUCCESS',
      paymentMethod: 'UPI',
      totalAmount: 560.00,
      notes: null,
      itemsCount: 3,
      createdAt: DateTime.now().subtract(const Duration(days: 2)),
      updatedAt: DateTime.now().subtract(const Duration(days: 2)),
    ),
    OrderModel(
      id: 'order-e5f6g7h8-mock',
      status: 'PREPARING',
      paymentStatus: 'SUCCESS',
      paymentMethod: 'CARD',
      totalAmount: 380.00,
      notes: 'Extra sugar please',
      itemsCount: 2,
      createdAt: DateTime.now().subtract(const Duration(hours: 1)),
      updatedAt: DateTime.now().subtract(const Duration(minutes: 30)),
    ),
    OrderModel(
      id: 'order-i9j0k1l2-mock',
      status: 'PLACED',
      paymentStatus: 'PENDING',
      paymentMethod: 'COD',
      totalAmount: 250.00,
      notes: null,
      itemsCount: 1,
      createdAt: DateTime.now().subtract(const Duration(minutes: 10)),
      updatedAt: DateTime.now().subtract(const Duration(minutes: 10)),
    ),
  ];

  static Map<String, dynamic> orderDetail(String orderId) {
    return {
      'id': orderId,
      'status': orderId.contains('a1b2') ? 'DELIVERED' :
                orderId.contains('e5f6') ? 'PREPARING' : 'PLACED',
      'payment_status': orderId.contains('i9j0') ? 'PENDING' : 'SUCCESS',
      'payment_method': 'UPI',
      'total_amount': 560.00,
      'notes': 'Extra sugar please',
      'created_at': DateTime.now().subtract(const Duration(hours: 1)).toIso8601String(),
      'updated_at': DateTime.now().toIso8601String(),
      'items': [
        {
          'id': 'oi-1',
          'product_id': 'prod-1',
          'product_name': 'Cappuccino',
          'quantity': 2,
          'price': 180.00,
        },
        {
          'id': 'oi-2',
          'product_id': 'prod-14',
          'product_name': 'Chocolate Brownie',
          'quantity': 1,
          'price': 200.00,
        },
      ],
    };
  }
}
