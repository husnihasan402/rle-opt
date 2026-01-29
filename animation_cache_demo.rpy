# Animation Cache Demo
# Демонстрационный файл для системы кэширования анимаций
#
# Этот файл показывает примеры использования системы кэширования

# Пример 1: Предзагрузка анимаций при запуске сцены
label demo_preload_scene:
    
    # Предзагружаем анимации для персонажей, которые появятся в сцене
    $ preload_character_animations('Kitty')
    $ preload_character_animations('Rogue')
    
    # Теперь можно показывать персонажей - их изображения уже в кеше
    show Kitty_Sprite at center
    "Китти появляется на экране..."
    
    show Rogue_Sprite at left
    "Роуг присоединяется к разговору..."
    
    return

# Пример 2: Оптимизация памяти после сцены
label demo_cleanup_scene:
    
    "Сцена завершается..."
    
    # Очищаем кеш для персонажей, которые больше не нужны
    $ clear_animation_cache('Kitty')
    $ clear_animation_cache('Rogue')
    
    # Или оптимизируем всю память
    $ optimize_animation_memory()
    
    return

# Пример 3: Предзагрузка всех анимаций при инициализации
label demo_init_preload:
    
    # Предзагружаем анимации для всех персонажей
    # Полезно сделать один раз при запуске игры
    $ total = preload_all_animations()
    "Предзагружено изображений: [total]"
    
    return

# Пример 4: Автоматическая предзагрузка активных персонажей
label demo_auto_preload:
    
    # Автоматически предзагружает анимации для персонажей в ActiveGirls
    $ auto_preload_active_characters()
    
    "Анимации для активных персонажей загружены!"
    
    return

# Пример 5: Отладка - просмотр статистики кеша
label demo_cache_stats:
    
    # Просматриваем статистику использования кеша
    $ log_animation_cache_stats()
    
    # Или получаем статистику программно
    $ stats = get_animation_cache_stats()
    "Кешировано изображений: [stats['cached_images']]"
    "Всего предзагружено: [stats['preloaded']]"
    
    return

# Пример 6: Управление кешированием
label demo_cache_control:
    
    # Выключаем кеширование
    $ set_animation_cache_enabled(False)
    "Кеширование выключено"
    
    # Включаем обратно
    $ set_animation_cache_enabled(True)
    "Кеширование включено"
    
    return

# Пример 7: Оптимизированная загрузка сцены с несколькими персонажами
label demo_optimized_scene:
    
    # Предзагружаем анимации для всех персонажей сцены
    $ preload_character_animations('Kitty')
    $ preload_character_animations('Rogue')
    $ preload_character_animations('Emma')
    
    # Показываем сцену
    scene bg player
    show Kitty_Sprite at left
    show Rogue_Sprite at center
    show Emma_Sprite at right
    
    "Все персонажи загружаются быстро благодаря кешированию!"
    
    # После сцены очищаем кеш
    $ clear_animation_cache()
    
    return
