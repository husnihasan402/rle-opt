## Image Cache Manager for Sprites and Animations
## Основной механизм кэширования изображений для оптимизации производительности

init -1 python:
    # Глобальный словарь кэша изображений
    image_cache = {}
    
    # Счетчики для мониторинга эффективности кэша
    cache_hits = 0
    cache_misses = 0
    
    def get_cached_image(image_path):
        """
        Получить закэшированное изображение или загрузить новое.
        
        Args:
            image_path: Путь к файлу изображения (строка)
        
        Returns:
            Displayable объект изображения
        """
        global cache_hits, cache_misses
        
        # Проверяем, есть ли изображение в кэше
        if image_path in image_cache:
            cache_hits += 1
            return image_cache[image_path]
        
        # Если нет в кэше, загружаем и кэшируем
        try:
            cached_img = Image(image_path)
            image_cache[image_path] = cached_img
            cache_misses += 1
            return cached_img
        except:
            # Если не удалось загрузить, возвращаем Null
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
        
        # Формируем уникальный ключ для кэша
        cache_key = f"recolor_{char_name}_{color_type}_{image_path}"
        
        # Проверяем наличие в кэше
        if cache_key in image_cache:
            cache_hits += 1
            return image_cache[cache_key]
        
        # Создаем новый объект с перекраской и кэшируем
        try:
            recolored_img = Recolor(char_name, color_type, image_path)
            image_cache[cache_key] = recolored_img
            cache_misses += 1
            return recolored_img
        except:
            return Null()
    
    def get_cached_alphamask(image_displayable, mask_displayable):
        """
        Получить закэшированное изображение с альфа-маской.
        
        Args:
            image_displayable: Изображение или имя изображения
            mask_displayable: Маска или имя маски
        
        Returns:
            Displayable объект с примененной маской
        """
        global cache_hits, cache_misses
        
        # Формируем уникальный ключ
        cache_key = f"alphamask_{image_displayable}_{mask_displayable}"
        
        if cache_key in image_cache:
            cache_hits += 1
            return image_cache[cache_key]
        
        try:
            masked_img = AlphaMask(image_displayable, mask_displayable)
            image_cache[cache_key] = masked_img
            cache_misses += 1
            return masked_img
        except:
            return Null()
    
    def get_cache_stats():
        """
        Получить статистику использования кэша.
        
        Returns:
            Словарь со статистикой
        """
        total_requests = cache_hits + cache_misses
        hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(image_cache),
            "hits": cache_hits,
            "misses": cache_misses,
            "hit_rate": hit_rate
        }
    
    def clear_image_cache():
        """
        Очистить кэш изображений (для освобождения памяти при необходимости).
        """
        global image_cache, cache_hits, cache_misses
        image_cache.clear()
        cache_hits = 0
        cache_misses = 0
    
    def preload_character_images(char_name, image_paths):
        """
        Предзагрузить изображения персонажа в кэш.
        
        Args:
            char_name: Имя персонажа
            image_paths: Список путей к изображениям для предзагрузки
        """
        for path in image_paths:
            get_cached_image(path)
