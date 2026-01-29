# Основной механизм кэширования для анимаций и изображений
# Main caching mechanism for animations and images

init -10 python:
    # Глобальный кеш для Recolor
    # Global cache for Recolor
    _recolor_cache = {}
    _recolor_cache_enabled = True
    
    class CachedRecolor:
        """
        Класс для кэширования результатов Recolor и матриц изображений.
        Class for caching Recolor results and image matrices.
        """
        def __init__(self):
            self.matrix_cache = {}  # Кеш матриц изображений / Image matrix cache
            self.image_cache = {}   # Кеш результатов Recolor / Recolor result cache
            self.enabled = True     # Флаг включения кэширования / Caching enable flag
        
        def get_cache_key(self, char_name, clothing_type, image_path, char_obj=None):
            """
            Создает ключ кэша на основе параметров изображения.
            Creates a cache key based on image parameters.
            
            Args:
                char_name: Имя персонажа / Character name
                clothing_type: Тип одежды / Clothing type  
                image_path: Путь к изображению / Image path
                char_obj: Объект персонажа (опционально) / Character object (optional)
            
            Returns:
                Уникальный ключ кэша / Unique cache key
            """
            if char_obj:
                # Создаем хеш на основе состояния объекта персонажа
                # Create hash based on character object state
                try:
                    # Получаем атрибуты одежды для создания уникального ключа
                    # Get clothing attributes to create unique key
                    clothing_state = (
                        getattr(char_obj, clothing_type, None),
                        getattr(char_obj, 'Uptop', None),
                        getattr(char_obj, 'Upskirt', None),
                        getattr(char_obj, 'PantiesDown', None),
                    )
                    return (char_name, clothing_type, image_path, clothing_state)
                except:
                    pass
            
            return (char_name, clothing_type, image_path)
        
        def get_matrix_cache_key(self, char_obj, clothing_type, layer=1):
            """
            Создает ключ кэша для матрицы изображения.
            Creates a cache key for image matrix.
            """
            try:
                # Получаем значение одежды
                # Get clothing value
                base_key = "pubes" if clothing_type == "Pubes" else getattr(char_obj, clothing_type, None)
                key = base_key + (str(layer) if layer > 1 else "")
                
                # Создаем хеш, включающий тег персонажа и состояние одежды
                # Create hash including character tag and clothing state
                return (char_obj.Tag, clothing_type, key, layer)
            except:
                return None
        
        def get_image_matrix(self, char_obj, clothing_type, layer=1):
            """
            Получает кешированную матрицу изображения или вычисляет новую.
            Gets cached image matrix or computes new one.
            """
            if not self.enabled:
                return char_obj.calculate_image_matrix(clothing_type, layer)
            
            cache_key = self.get_matrix_cache_key(char_obj, clothing_type, layer)
            if cache_key is None:
                return char_obj.calculate_image_matrix(clothing_type, layer)
            
            if cache_key not in self.matrix_cache:
                self.matrix_cache[cache_key] = char_obj.calculate_image_matrix(clothing_type, layer)
            
            return self.matrix_cache[cache_key]
        
        def clear_cache(self):
            """Очищает весь кеш / Clears all caches"""
            self.matrix_cache.clear()
            self.image_cache.clear()
        
        def clear_character_cache(self, char_tag):
            """
            Очищает кеш для конкретного персонажа.
            Clears cache for specific character.
            """
            # Очищаем матрицы для персонажа
            # Clear matrices for character
            keys_to_remove = [k for k in self.matrix_cache.keys() if k[0] == char_tag]
            for key in keys_to_remove:
                del self.matrix_cache[key]
            
            # Очищаем изображения для персонажа
            # Clear images for character
            keys_to_remove = [k for k in self.image_cache.keys() if k[0] == char_tag]
            for key in keys_to_remove:
                del self.image_cache[key]
        
        def clear_clothing_cache(self, char_tag, clothing_type):
            """
            Очищает кеш для конкретного типа одежды персонажа.
            Clears cache for specific clothing type of character.
            """
            # Очищаем матрицы для типа одежды
            # Clear matrices for clothing type
            keys_to_remove = [k for k in self.matrix_cache.keys() 
                            if k[0] == char_tag and k[1] == clothing_type]
            for key in keys_to_remove:
                del self.matrix_cache[key]
            
            # Очищаем изображения для типа одежды
            # Clear images for clothing type
            keys_to_remove = [k for k in self.image_cache.keys() 
                            if k[0] == char_tag and k[1] == clothing_type]
            for key in keys_to_remove:
                del self.image_cache[key]
    
    # Создаем глобальный экземпляр кеша
    # Create global cache instance
    _cached_recolor = CachedRecolor()
    
    def Recolor(char_name, clothing_type, image_path):
        """
        Применяет цветовую трансформацию к изображению с кешированием.
        Applies color transformation to image with caching.
        
        Args:
            char_name: Имя персонажа (например, "Rogue") / Character name (e.g., "Rogue")
            clothing_type: Тип одежды (например, "Over", "Chest") / Clothing type (e.g., "Over", "Chest")
            image_path: Путь к изображению / Image path
        
        Returns:
            Трансформированное изображение / Transformed image
        """
        if not _recolor_cache_enabled:
            # Если кеширование отключено, просто возвращаем изображение
            # If caching is disabled, just return the image
            try:
                char_obj = eval(char_name + "X")
                matrix = char_obj.calculate_image_matrix(clothing_type)
                return im.MatrixColor(image_path, matrix)
            except:
                return image_path
        
        try:
            # Получаем объект персонажа
            # Get character object
            char_obj = eval(char_name + "X")
            
            # Создаем ключ кэша
            # Create cache key
            cache_key = _cached_recolor.get_cache_key(char_name, clothing_type, image_path, char_obj)
            
            # Проверяем кеш
            # Check cache
            if cache_key in _recolor_cache:
                return _recolor_cache[cache_key]
            
            # Вычисляем матрицу трансформации
            # Calculate transformation matrix
            matrix = char_obj.calculate_image_matrix(clothing_type)
            
            # Применяем матрицу к изображению
            # Apply matrix to image
            result = im.MatrixColor(image_path, matrix)
            
            # Сохраняем в кеше
            # Save to cache
            _recolor_cache[cache_key] = result
            
            return result
        except Exception as e:
            # В случае ошибки возвращаем оригинальное изображение
            # In case of error, return original image
            return image_path
    
    def clear_recolor_cache():
        """Очищает глобальный кеш Recolor / Clears global Recolor cache"""
        _recolor_cache.clear()
        _cached_recolor.clear_cache()
    
    def clear_character_recolor_cache(char_name):
        """
        Очищает кеш Recolor для конкретного персонажа.
        Clears Recolor cache for specific character.
        """
        try:
            char_obj = eval(char_name + "X")
            char_tag = char_obj.Tag
            
            # Очищаем глобальный кеш
            # Clear global cache
            keys_to_remove = [k for k in _recolor_cache.keys() if k[0] == char_name]
            for key in keys_to_remove:
                del _recolor_cache[key]
            
            # Очищаем кеш объекта
            # Clear object cache
            _cached_recolor.clear_character_cache(char_tag)
        except:
            pass
    
    def enable_recolor_cache():
        """Включает кеширование Recolor / Enables Recolor caching"""
        global _recolor_cache_enabled
        _recolor_cache_enabled = True
        _cached_recolor.enabled = True
    
    def disable_recolor_cache():
        """Отключает кеширование Recolor / Disables Recolor caching"""
        global _recolor_cache_enabled
        _recolor_cache_enabled = False
        _cached_recolor.enabled = False
