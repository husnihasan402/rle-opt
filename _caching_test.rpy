# Тестовый файл для проверки системы кэширования
# Test file for caching system verification

init 999 python:
    """
    Этот файл содержит тесты для проверки работы системы кэширования.
    This file contains tests to verify caching system functionality.
    """
    
    def test_recolor_cache():
        """Тест базовой функциональности Recolor"""
        print("\n=== Testing Recolor Cache ===")
        
        try:
            # Проверяем, что функция Recolor существует
            # Check that Recolor function exists
            if 'Recolor' not in globals():
                print("ERROR: Recolor function not defined!")
                return False
            
            print("✓ Recolor function is defined")
            
            # Проверяем, что кеш существует
            # Check that cache exists
            if '_recolor_cache' not in globals():
                print("ERROR: _recolor_cache not defined!")
                return False
            
            print("✓ Global recolor cache is defined")
            
            # Проверяем CachedRecolor класс
            # Check CachedRecolor class
            if '_cached_recolor' not in globals():
                print("ERROR: _cached_recolor not defined!")
                return False
            
            print("✓ CachedRecolor instance is defined")
            
            # Проверяем методы кеша
            # Check cache methods
            if not hasattr(_cached_recolor, 'clear_cache'):
                print("ERROR: clear_cache method not found!")
                return False
            
            print("✓ Cache methods are available")
            
            print("\n=== Recolor Cache Tests Passed ===\n")
            return True
            
        except Exception as e:
            print(f"ERROR in test_recolor_cache: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_animation_cache():
        """Тест функциональности кэша анимаций"""
        print("\n=== Testing Animation Cache ===")
        
        try:
            # Проверяем AnimationCacheManager
            # Check AnimationCacheManager
            if '_animation_cache_manager' not in globals():
                print("ERROR: _animation_cache_manager not defined!")
                return False
            
            print("✓ Animation cache manager is defined")
            
            # Проверяем функции инвалидации
            # Check invalidation functions
            if 'invalidate_animation_cache' not in globals():
                print("ERROR: invalidate_animation_cache function not defined!")
                return False
            
            print("✓ Cache invalidation functions are available")
            
            # Проверяем функцию статистики
            # Check statistics function
            if 'get_animation_cache_stats' not in globals():
                print("ERROR: get_animation_cache_stats function not defined!")
                return False
            
            stats = get_animation_cache_stats()
            print(f"✓ Cache statistics: {stats}")
            
            print("\n=== Animation Cache Tests Passed ===\n")
            return True
            
        except Exception as e:
            print(f"ERROR in test_animation_cache: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_girl_class_integration():
        """Тест интеграции с GirlClass"""
        print("\n=== Testing GirlClass Integration ===")
        
        try:
            # Создаем тестовый объект девушки
            # Create test girl object
            test_girl = GirlClass("TestGirl", 0, 0, 0, 0)
            
            # Проверяем наличие modItem
            # Check modItem presence
            if not hasattr(test_girl, 'modItem'):
                print("ERROR: modItem not initialized in GirlClass!")
                return False
            
            print("✓ modItem is initialized")
            
            # Проверяем наличие skin_image
            # Check skin_image presence
            if not hasattr(test_girl, 'skin_image'):
                print("ERROR: skin_image not initialized in GirlClass!")
                return False
            
            print("✓ skin_image is initialized")
            
            # Проверяем, что skin_image имеет атрибут skin_path
            # Check that skin_image has skin_path attribute
            if not hasattr(test_girl.skin_image, 'skin_path'):
                print("ERROR: skin_image.skin_path not found!")
                return False
            
            print(f"✓ skin_image.skin_path is available: '{test_girl.skin_image.skin_path}'")
            
            # Проверяем метод calculate_image_matrix
            # Check calculate_image_matrix method
            if not hasattr(test_girl, 'calculate_image_matrix'):
                print("ERROR: calculate_image_matrix method not found!")
                return False
            
            print("✓ calculate_image_matrix method is available")
            
            # Проверяем mark_display_dirty
            # Check mark_display_dirty
            if not hasattr(test_girl, 'mark_display_dirty'):
                print("ERROR: mark_display_dirty method not found!")
                return False
            
            # Вызываем mark_display_dirty для проверки интеграции с кешем
            # Call mark_display_dirty to check cache integration
            test_girl.mark_display_dirty()
            print("✓ mark_display_dirty works with cache integration")
            
            print("\n=== GirlClass Integration Tests Passed ===\n")
            return True
            
        except Exception as e:
            print(f"ERROR in test_girl_class_integration: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_all_caching_tests():
        """Запускает все тесты кэширования"""
        print("\n" + "="*50)
        print("RUNNING CACHING SYSTEM TESTS")
        print("="*50)
        
        tests = [
            ("Recolor Cache", test_recolor_cache),
            ("Animation Cache", test_animation_cache),
            ("GirlClass Integration", test_girl_class_integration)
        ]
        
        results = []
        for test_name, test_func in tests:
            result = test_func()
            results.append((test_name, result))
        
        print("\n" + "="*50)
        print("TEST RESULTS SUMMARY")
        print("="*50)
        
        for test_name, result in results:
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name}: {status}")
        
        all_passed = all(result for _, result in results)
        
        print("="*50)
        if all_passed:
            print("ALL TESTS PASSED!")
        else:
            print("SOME TESTS FAILED!")
        print("="*50 + "\n")
        
        return all_passed
    
    # Можно вызвать run_all_caching_tests() из консоли для тестирования
    # Can call run_all_caching_tests() from console for testing
