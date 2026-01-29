# Настройка кэширования для анимаций
# Animation caching configuration

init -5 python:
    """
    Этот файл содержит конфигурацию кэширования специфичную для анимаций.
    This file contains animation-specific caching configuration.
    """
    
    # Импортируем механизм кэширования из _caching.rpy
    # Import caching mechanism from _caching.rpy
    # (уже загружено через init -10) / (already loaded via init -10)
    
    # Настройки кэширования анимаций
    # Animation caching settings
    ANIMATION_CACHE_ENABLED = True
    ANIMATION_CACHE_SIZE_LIMIT = 200  # Максимальное количество кешированных элементов / Maximum cached items
    
    # Кеш для результатов ConditionSwitch
    # Cache for ConditionSwitch results  
    _condition_cache = {}
    _condition_cache_enabled = True
    
    class AnimationCacheManager:
        """
        Менеджер кэша для анимаций.
        Animation cache manager.
        """
        def __init__(self):
            self.cache = {}
            self.cache_hits = 0
            self.cache_misses = 0
            self.enabled = ANIMATION_CACHE_ENABLED
            self.size_limit = ANIMATION_CACHE_SIZE_LIMIT
        
        def get_stats(self):
            """Возвращает статистику использования кеша / Returns cache usage statistics"""
            total = self.cache_hits + self.cache_misses
            hit_rate = (self.cache_hits / total * 100) if total > 0 else 0
            return {
                'size': len(self.cache),
                'hits': self.cache_hits,
                'misses': self.cache_misses,
                'hit_rate': hit_rate
            }
        
        def clear(self):
            """Очищает кеш анимаций / Clears animation cache"""
            self.cache.clear()
            self.cache_hits = 0
            self.cache_misses = 0
        
        def ensure_cache_size(self):
            """
            Проверяет размер кеша и очищает старые элементы при превышении лимита.
            Checks cache size and clears old items if limit exceeded.
            """
            if len(self.cache) > self.size_limit:
                # Простое удаление половины кеша (можно улучшить с LRU)
                # Simple removal of half the cache (could be improved with LRU)
                keys_to_remove = list(self.cache.keys())[:len(self.cache) // 2]
                for key in keys_to_remove:
                    del self.cache[key]
    
    # Создаем глобальный менеджер кеша анимаций
    # Create global animation cache manager
    _animation_cache_manager = AnimationCacheManager()
    
    def cache_condition_result(condition_key, result):
        """
        Кеширует результат вычисления условия.
        Caches condition evaluation result.
        """
        if _condition_cache_enabled and _animation_cache_manager.enabled:
            _condition_cache[condition_key] = result
            _animation_cache_manager.ensure_cache_size()
    
    def get_cached_condition(condition_key):
        """
        Получает кешированный результат условия.
        Gets cached condition result.
        """
        if not _condition_cache_enabled or not _animation_cache_manager.enabled:
            return None
        
        if condition_key in _condition_cache:
            _animation_cache_manager.cache_hits += 1
            return _condition_cache[condition_key]
        
        _animation_cache_manager.cache_misses += 1
        return None
    
    def clear_condition_cache():
        """Очищает кеш условий / Clears condition cache"""
        _condition_cache.clear()
    
    def invalidate_animation_cache(char_name=None):
        """
        Инвалидирует кеш анимаций.
        Invalidates animation cache.
        
        Args:
            char_name: Имя персонажа для инвалидации (None = все) / 
                       Character name to invalidate (None = all)
        """
        if char_name:
            # Очищаем кеш для конкретного персонажа
            # Clear cache for specific character
            clear_character_recolor_cache(char_name)
            
            # Очищаем кеш условий для персонажа
            # Clear condition cache for character  
            keys_to_remove = [k for k in _condition_cache.keys() if char_name in str(k)]
            for key in keys_to_remove:
                del _condition_cache[key]
        else:
            # Очищаем весь кеш
            # Clear all caches
            clear_recolor_cache()
            clear_condition_cache()
            _animation_cache_manager.clear()
    
    def get_animation_cache_stats():
        """
        Возвращает статистику кеша анимаций.
        Returns animation cache statistics.
        """
        stats = _animation_cache_manager.get_stats()
        stats['recolor_cache_size'] = len(_recolor_cache)
        stats['condition_cache_size'] = len(_condition_cache)
        return stats
    
    # Хелперы для интеграции с существующей системой одежды
    # Helpers for integration with existing clothing system
    
    def mark_animation_dirty(char_obj):
        """
        Помечает анимации персонажа как требующие обновления.
        Marks character animations as needing update.
        
        Это должно вызываться при изменении одежды персонажа.
        This should be called when character's clothing changes.
        """
        if hasattr(char_obj, 'Tag'):
            invalidate_animation_cache(char_obj.Tag)
        
        # Также помечаем display cache как dirty
        # Also mark display cache as dirty
        if hasattr(char_obj, 'mark_display_dirty'):
            char_obj.mark_display_dirty()
    
    def setup_animation_cache_hooks():
        """
        Настраивает хуки для автоматической инвалидации кеша.
        Sets up hooks for automatic cache invalidation.
        """
        # Это можно расширить для автоматического отслеживания изменений
        # This can be extended for automatic change tracking
        pass
    
    # Инициализация
    # Initialization
    setup_animation_cache_hooks()
    
    # Логирование (опционально, для отладки)
    # Logging (optional, for debugging)
    if config.developer:
        def log_cache_stats():
            stats = get_animation_cache_stats()
            print("[Animation Cache] Size: {size}, Hits: {hits}, Misses: {misses}, Hit Rate: {hit_rate:.2f}%".format(**stats))
            print("[Animation Cache] Recolor Cache Size: {recolor_cache_size}, Condition Cache Size: {condition_cache_size}".format(**stats))
        
        # Можно вызывать log_cache_stats() для отладки
        # Can call log_cache_stats() for debugging
