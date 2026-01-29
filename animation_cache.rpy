# Animation Caching Module
# Модуль кэширования анимаций
# 
# Этот модуль предоставляет механизм кэширования для файлов анимаций (*_Animations.rpy)
# чтобы улучшить производительность загрузки и отображения изображений
#
# ПРИМЕЧАНИЕ: Модуль работает совместно со встроенным кешем изображений Ren'Py.
# Функции предзагрузки регистрируют изображения и настраивают параметры кеша
# для оптимальной производительности анимаций.

init -10 python:
    # Список всех анимационных персонажей
    _animation_characters = [
        'Kitty', 'Rogue', 'Emma', 'Jean', 'Laura', 'Storm', 
        'Jubes', 'Gwen', 'Betsy', 'Doreen', 'Wanda'
    ]
    
    # Глобальный кеш для предзагруженных изображений анимаций
    _animation_preload_cache = {}
    _animation_cache_enabled = True
    
    # Статистика использования кеша
    _animation_cache_stats = {
        'preloaded': 0,
        'cache_clears': 0,
        'last_clear_time': None
    }
    
    def preload_character_animations(character_name):
        """
        Предварительно загружает анимации для указанного персонажа.
        
        Args:
            character_name: Имя персонажа (например, 'Kitty', 'Rogue')
        """
        if not _animation_cache_enabled:
            return
            
        # Список основных анимационных изображений для предзагрузки
        animation_images = [
            character_name + '_Sprite',
            character_name + '_Head',
        ]
        
        # Добавляем дополнительные изображения специфичные для анимаций
        additional_images = [
            '_BJ_Animation',
            '_TJ_Animation', 
            '_HJ_Animation',
            '_Sex_Animation',
            '_Doggy_Animation',
            '_69_Animation',
            '_CUN_Animation'
        ]
        
        for suffix in additional_images:
            animation_images.append(character_name + suffix)
        
        # Попытка предзагрузить изображения
        preloaded_count = 0
        for img_name in animation_images:
            try:
                # Используем встроенную функцию Ren'Py для предзагрузки
                if renpy.has_image(img_name):
                    renpy.get_registered_image(img_name)
                    _animation_preload_cache[img_name] = True
                    preloaded_count += 1
            except Exception as e:
                # Если изображение не существует или не может быть загружено
                pass
        
        _animation_cache_stats['preloaded'] += preloaded_count
        return preloaded_count
    
    def preload_all_animations():
        """
        Предварительно загружает анимации для всех персонажей.
        """
        total_preloaded = 0
        for character in _animation_characters:
            total_preloaded += preload_character_animations(character)
        return total_preloaded
    
    def clear_animation_cache(character_name=None):
        """
        Очищает кеш анимаций.
        
        Args:
            character_name: Если указан, очищает только кеш для этого персонажа.
                          Если None, очищает весь кеш анимаций.
        """
        global _animation_preload_cache, _animation_cache_stats
        
        if character_name:
            # Очищаем кеш только для указанного персонажа
            keys_to_remove = [k for k in _animation_preload_cache.keys() 
                            if k.startswith(character_name)]
            for key in keys_to_remove:
                del _animation_preload_cache[key]
        else:
            # Очищаем весь кеш
            _animation_preload_cache.clear()
        
        _animation_cache_stats['cache_clears'] += 1
        _animation_cache_stats['last_clear_time'] = renpy.get_time()
        
        # Также очищаем встроенный кеш изображений Ren'Py
        renpy.free_memory()
    
    def get_animation_cache_stats():
        """
        Возвращает статистику кеширования анимаций.
        
        Returns:
            Словарь со статистикой использования кеша
        """
        stats = _animation_cache_stats.copy()
        stats['cached_images'] = len(_animation_preload_cache)
        stats['cache_enabled'] = _animation_cache_enabled
        return stats
    
    def set_animation_cache_enabled(enabled):
        """
        Включает или выключает кеширование анимаций.
        
        Args:
            enabled: True для включения, False для выключения
        """
        global _animation_cache_enabled
        _animation_cache_enabled = enabled
        if not enabled:
            clear_animation_cache()
    
    def optimize_animation_memory():
        """
        Оптимизирует использование памяти для анимаций.
        Освобождает неиспользуемые ресурсы и оптимизирует кеш.
        """
        # Очищаем неиспользуемые изображения из памяти
        renpy.free_memory()
        
        # Принудительно запускаем сборщик мусора Python
        import gc
        gc.collect()

# Дополнительные утилиты для работы с кешем
init python:
    def log_animation_cache_stats():
        """
        Выводит статистику кеша анимаций в консоль (для отладки).
        """
        stats = get_animation_cache_stats()
        print("=" * 50)
        print("Animation Cache Statistics:")
        print("-" * 50)
        print("  Cache Enabled: {}".format(stats['cache_enabled']))
        print("  Cached Images: {}".format(stats['cached_images']))
        print("  Total Preloaded: {}".format(stats['preloaded']))
        print("  Cache Clears: {}".format(stats['cache_clears']))
        if stats['last_clear_time']:
            print("  Last Clear: {}".format(stats['last_clear_time']))
        print("=" * 50)
    
    def auto_preload_active_characters():
        """
        Автоматически предзагружает анимации для активных персонажей в игре.
        Использует глобальную переменную ActiveGirls если она доступна.
        """
        try:
            if hasattr(store, 'ActiveGirls') and store.ActiveGirls:
                for girl in store.ActiveGirls:
                    if hasattr(girl, 'Tag'):
                        preload_character_animations(girl.Tag)
        except Exception as e:
            pass

# Конфигурация кеша для файлов анимаций
init -5:
    # Увеличиваем размер кеша изображений для анимаций
    # Это оптимизировано для файлов *_Animations.rpy
    if config.image_cache_size < 128:
        config.image_cache_size = 128
    
    # Включаем кеширование поверхностей для лучшей производительности анимаций
    # Это позволяет быстрее применять манипуляторы изображений
    config.cache_surfaces = True

# Пример использования:
# 
# В коде игры можно использовать следующие функции:
# 
# 1. Предзагрузка анимаций для одного персонажа:
#    $ preload_character_animations('Kitty')
# 
# 2. Предзагрузка анимаций для всех персонажей:
#    $ preload_all_animations()
# 
# 3. Очистка кеша для персонажа:
#    $ clear_animation_cache('Kitty')
# 
# 4. Очистка всего кеша:
#    $ clear_animation_cache()
# 
# 5. Оптимизация памяти:
#    $ optimize_animation_memory()
# 
# 6. Просмотр статистики:
#    $ log_animation_cache_stats()
# 
# 7. Автоматическая предзагрузка активных персонажей:
#    $ auto_preload_active_characters()
