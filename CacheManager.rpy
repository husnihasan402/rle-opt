## Image Cache Manager for Sprites and Animations
## Основной механизм кэширования изображений для оптимизации производительности

init -1 python:
    import threading
    
    # Глобальный словарь кэша изображений
    image_cache = {}
    
    # Счетчики для мониторинга эффективности кэша
    cache_hits = 0
    cache_misses = 0
    
    # Блокировка для потокобезопасности
    cache_lock = threading.RLock()
    
    # Максимальный размер кэша (количество элементов)
    # При превышении удаляются старые элементы
    MAX_CACHE_SIZE = 2000
    
    def _evict_old_entries():
        """
        Удалить старые записи из кэша, если он превысил максимальный размер.
        Использует простую стратегию FIFO (First In First Out).
        """
        if len(image_cache) > MAX_CACHE_SIZE:
            # Удаляем 20% старых записей
            num_to_remove = len(image_cache) // 5
            keys_to_remove = list(image_cache.keys())[:num_to_remove]
            for key in keys_to_remove:
                del image_cache[key]
    
    def get_cached_image(image_path):
        """
        Получить закэшированное изображение или загрузить новое.
        
        Args:
            image_path: Путь к файлу изображения (строка)
        
        Returns:
            Displayable объект изображения
        """
        global cache_hits, cache_misses
        
        with cache_lock:
            # Проверяем, есть ли изображение в кэше
            if image_path in image_cache:
                cache_hits += 1
                return image_cache[image_path]
            
            # Если нет в кэше, загружаем и кэшируем
            try:
                cached_img = Image(image_path)
                _evict_old_entries()
                image_cache[image_path] = cached_img
                cache_misses += 1
                return cached_img
            except Exception as e:
                # Логируем ошибку для отладки, но не падаем
                # В Ren'Py многие ошибки не критичны
                return Null()
    
    def get_cached_recolor(char_name, color_type, image_path):
        """
        Получить закэшированное перекрашенное изображение.
        
        Args:
            char_name: Имя персонажа (например, "Storm", "Kitty")
            color_type: Тип цвета (например, "Legs", "Panties")
            image_path: Путь к базовому изображению
        
        Returns:
            Displayable объект с примененной перекраской
        """
        global cache_hits, cache_misses
        
        with cache_lock:
            # Формируем уникальный ключ для кэша
            cache_key = f"recolor_{char_name}_{color_type}_{image_path}"
            
            # Проверяем наличие в кэше
            if cache_key in image_cache:
                cache_hits += 1
                return image_cache[cache_key]
            
            # Создаем новый объект с перекраской и кэшируем
            try:
                recolored_img = Recolor(char_name, color_type, image_path)
                _evict_old_entries()
                image_cache[cache_key] = recolored_img
                cache_misses += 1
                return recolored_img
            except Exception as e:
                return Null()
    
    def get_cached_alphamask(image_displayable, mask_displayable):
        """
        Получить закэшированное изображение с альфа-маской.
        
        Args:
            image_displayable: Изображение или имя изображения (строка)
            mask_displayable: Маска или имя маски (строка)
        
        Returns:
            Displayable объект с примененной маской
        """
        global cache_hits, cache_misses
        
        with cache_lock:
            # Формируем уникальный ключ
            # Используем строковое представление для ключа
            cache_key = f"alphamask_{str(image_displayable)}_{str(mask_displayable)}"
            
            if cache_key in image_cache:
                cache_hits += 1
                return image_cache[cache_key]
            
            try:
                masked_img = AlphaMask(image_displayable, mask_displayable)
                _evict_old_entries()
                image_cache[cache_key] = masked_img
                cache_misses += 1
                return masked_img
            except Exception as e:
                return Null()
    
    def get_cache_stats():
        """
        Получить статистику использования кэша.
        
        Returns:
            Словарь со статистикой
        """
        global cache_hits, cache_misses
        
        with cache_lock:
            total_requests = cache_hits + cache_misses
            hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "cache_size": len(image_cache),
                "max_cache_size": MAX_CACHE_SIZE,
                "hits": cache_hits,
                "misses": cache_misses,
                "hit_rate": hit_rate
            }
    
    def clear_image_cache():
        """
        Очистить кэш изображений (для освобождения памяти при необходимости).
        Следует вызывать при переходах между большими разделами игры
        или при необходимости освободить память.
        """
        global image_cache, cache_hits, cache_misses
        
        with cache_lock:
            image_cache.clear()
            cache_hits = 0
            cache_misses = 0
    
    def preload_character_images(char_name, image_paths, recolor_paths=None, alphamask_tuples=None):
        """
        Предзагрузить изображения персонажа в кэш.
        
        Args:
            char_name: Имя персонажа
            image_paths: Список путей к изображениям для предзагрузки
            recolor_paths: Опциональный список кортежей (color_type, image_path) для перекраски
            alphamask_tuples: Опциональный список кортежей (image, mask) для альфа-масок
        """
        # Загружаем обычные изображения
        for path in image_paths:
            get_cached_image(path)
        
        # Загружаем перекрашенные изображения
        if recolor_paths:
            for color_type, path in recolor_paths:
                get_cached_recolor(char_name, color_type, path)
        
        # Загружаем изображения с альфа-масками
        if alphamask_tuples:
            for image, mask in alphamask_tuples:
                get_cached_alphamask(image, mask)
