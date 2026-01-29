# Animation Cache System / Система кэширования анимаций

## Overview / Обзор

This module provides a caching system for animation files (*_Animations.rpy) to improve loading and display performance of images in the game.

Этот модуль предоставляет систему кэширования для файлов анимаций (*_Animations.rpy) для улучшения производительности загрузки и отображения изображений в игре.

## Files / Файлы

- **animation_cache.rpy** - Main caching module / Основной модуль кэширования
- **\*_Animations.rpy** - Animation files that use the caching system / Файлы анимаций, использующие систему кэширования

## Features / Возможности

### 1. Preloading / Предзагрузка

The system can preload animation images for characters before they are displayed:

Система может предзагрузить изображения анимаций для персонажей до их отображения:

```python
# Preload animations for a single character
$ preload_character_animations('Kitty')

# Preload animations for all characters
$ preload_all_animations()

# Automatically preload animations for active characters
$ auto_preload_active_characters()
```

### 2. Cache Management / Управление кешем

Clear cache to free up memory:

Очистка кеша для освобождения памяти:

```python
# Clear cache for a specific character
$ clear_animation_cache('Kitty')

# Clear entire cache
$ clear_animation_cache()

# Optimize memory usage
$ optimize_animation_memory()
```

### 3. Cache Statistics / Статистика кеша

View cache usage statistics:

Просмотр статистики использования кеша:

```python
# Print cache statistics to console
$ log_animation_cache_stats()

# Get statistics as a dictionary
$ stats = get_animation_cache_stats()
```

### 4. Configuration / Конфигурация

The system automatically configures Ren'Py caching settings:

Система автоматически настраивает параметры кэширования Ren'Py:

- Increases `config.image_cache_size` to 128 (if less)
- Enables `config.cache_surfaces` for better performance
- Optimized specifically for animation files

## Usage Examples / Примеры использования

### Example 1: Preload before scene / Пример 1: Предзагрузка перед сценой

```python
label my_scene:
    # Preload Kitty's animations before the scene
    $ preload_character_animations('Kitty')
    
    # Show Kitty
    show Kitty_Sprite
    
    # Rest of the scene...
```

### Example 2: Memory optimization / Пример 2: Оптимизация памяти

```python
label after_scene:
    # Clear unused character cache
    $ clear_animation_cache('Kitty')
    
    # Or optimize all memory
    $ optimize_animation_memory()
```

### Example 3: Debug cache performance / Пример 3: Отладка производительности кеша

```python
label debug_menu:
    # Show cache statistics
    $ log_animation_cache_stats()
```

## Integration / Интеграция

All animation files have been updated with caching system integration comments:

Все файлы анимаций обновлены с комментариями об интеграции системы кэширования:

- Betsy_Animations.rpy
- Doreen_Animations.rpy
- Emma_Animations.rpy
- Gwen_Animations.rpy
- Jean_Animations.rpy
- Jubes_Animations.rpy
- Kitty_Animations.rpy
- Laura_Animations.rpy
- Rogue_Animations.rpy
- Storm_Animations.rpy
- Wanda_Animations.rpy

Each file includes instructions on how to preload and clear cache for that specific character.

Каждый файл включает инструкции о том, как предзагрузить и очистить кеш для этого конкретного персонажа.

## Technical Details / Технические детали

### Cache Storage / Хранение кеша

The system maintains:
- `_animation_preload_cache` - Dictionary of preloaded images
- `_animation_cache_stats` - Statistics about cache usage
- `_animation_cache_enabled` - Flag to enable/disable caching

### Performance Benefits / Преимущества производительности

1. **Faster image loading** - Images are preloaded and cached
2. **Better memory management** - Controlled cache with manual clearing
3. **Reduced disk I/O** - Images stay in memory when cached
4. **Optimized for animations** - Special handling for animation files

## API Reference / Справочник API

### Functions / Функции

#### `preload_character_animations(character_name)`
Preload animations for a specific character.

**Parameters:**
- `character_name` (str): Name of the character (e.g., 'Kitty', 'Rogue')

**Returns:** Number of images preloaded

#### `preload_all_animations()`
Preload animations for all characters.

**Returns:** Total number of images preloaded

#### `clear_animation_cache(character_name=None)`
Clear animation cache.

**Parameters:**
- `character_name` (str, optional): If specified, only clears cache for this character

#### `get_animation_cache_stats()`
Get cache statistics.

**Returns:** Dictionary with cache statistics

#### `set_animation_cache_enabled(enabled)`
Enable or disable caching.

**Parameters:**
- `enabled` (bool): True to enable, False to disable

#### `optimize_animation_memory()`
Optimize memory usage for animations.

**Returns:** True on success

#### `log_animation_cache_stats()`
Print cache statistics to console.

#### `auto_preload_active_characters()`
Automatically preload animations for active characters.

## Notes / Примечания

- The caching system works with Ren'Py's built-in image cache
- Images with dynamic content (ConditionSwitch) are cached per state
- Cache size can be adjusted in animation_cache.rpy
- For best performance, preload animations before scenes that use them

## Branch / Ветка

This implementation is in the branch: `copilot/setup-caching-for-animation-files`

Эта реализация находится в ветке: `copilot/setup-caching-for-animation-files`
