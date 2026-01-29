# Система кэширования анимаций / Animation Caching System

## Описание / Description

Эта система кэширования оптимизирует производительность анимаций персонажей в игре, кэшируя результаты вычисления цветовых трансформаций изображений.

This caching system optimizes character animation performance in the game by caching color transformation computation results.

## Структура файлов / File Structure

### `_caching.rpy`
Основной механизм кэширования. Содержит:
- `CachedRecolor` класс для управления кешем
- `Recolor()` функцию для применения цветовых трансформаций с кэшированием
- Функции управления кешем (очистка, инвалидация)

Main caching mechanism. Contains:
- `CachedRecolor` class for cache management
- `Recolor()` function for applying color transformations with caching
- Cache management functions (clearing, invalidation)

### `_animations.rpy`
Конфигурация кэширования специфичная для анимаций. Содержит:
- `AnimationCacheManager` для управления кешем анимаций
- Функции для кэширования результатов условий
- Хелперы для интеграции с системой одежды

Animation-specific caching configuration. Contains:
- `AnimationCacheManager` for animation cache management
- Functions for caching condition results
- Helpers for clothing system integration

### `_caching_test.rpy`
Тестовый файл для проверки работоспособности системы кэширования.

Test file to verify caching system functionality.

## Использование / Usage

### Функция Recolor / Recolor Function

Функция `Recolor` используется в файлах анимаций для применения цветовых трансформаций к изображениям:

The `Recolor` function is used in animation files to apply color transformations to images:

```python
Recolor("Rogue", "Over", "images/RogueSprite/Rogue_over_mesh1.png")
```

Параметры / Parameters:
- `char_name`: Имя персонажа (например, "Rogue", "Kitty") / Character name (e.g., "Rogue", "Kitty")
- `clothing_type`: Тип одежды (например, "Over", "Chest", "Panties") / Clothing type (e.g., "Over", "Chest", "Panties")
- `image_path`: Путь к изображению / Image path

### Управление кешем / Cache Management

#### Очистка всего кеша / Clear all cache
```python
clear_recolor_cache()
```

#### Очистка кеша персонажа / Clear character cache
```python
clear_character_recolor_cache("Rogue")
```

#### Инвалидация кеша анимаций / Invalidate animation cache
```python
invalidate_animation_cache("Rogue")  # Для конкретного персонажа / For specific character
invalidate_animation_cache()         # Для всех персонажей / For all characters
```

#### Включение/отключение кэширования / Enable/disable caching
```python
enable_recolor_cache()   # Включить / Enable
disable_recolor_cache()  # Отключить / Disable
```

### Статистика кеша / Cache Statistics

Получить статистику использования кеша / Get cache usage statistics:

```python
stats = get_animation_cache_stats()
print(stats)
```

Вывод / Output:
```python
{
    'size': 100,           # Размер кеша анимаций / Animation cache size
    'hits': 500,           # Попадания в кеш / Cache hits
    'misses': 50,          # Промахи кеша / Cache misses  
    'hit_rate': 90.9,      # Процент попаданий / Hit rate percentage
    'recolor_cache_size': 75,        # Размер кеша Recolor / Recolor cache size
    'condition_cache_size': 25       # Размер кеша условий / Condition cache size
}
```

## Интеграция с GirlClass / GirlClass Integration

Система автоматически интегрируется с классом `GirlClass`:

The system automatically integrates with the `GirlClass`:

### Инициализация / Initialization

При создании объекта девушки автоматически инициализируются:

When creating a girl object, the following are automatically initialized:

- `modItem`: Словарь для модификаций одежды / Dictionary for clothing modifications
- `skin_image`: Объект для путей к текстурам кожи / Object for skin texture paths

### Автоматическая инвалидация / Automatic Invalidation

При изменении одежды персонажа (через сеттеры свойств) автоматически вызывается `mark_display_dirty()`, который:

When character clothing changes (via property setters), `mark_display_dirty()` is automatically called, which:

1. Помечает display cache как dirty
2. Инвалидирует кеш анимаций для персонажа

1. Marks display cache as dirty
2. Invalidates animation cache for the character

## Конфигурация / Configuration

### Параметры в `_animations.rpy`

```python
ANIMATION_CACHE_ENABLED = True        # Включить кэширование / Enable caching
ANIMATION_CACHE_SIZE_LIMIT = 200      # Макс. элементов в кеше / Max cached items
```

### Параметры Ren'Py в `options.rpy`

```python
config.image_cache_size = 64          # Размер кеша изображений Ren'Py / Ren'Py image cache size
config.cache_surfaces = False         # Кэширование поверхностей / Cache surfaces
```

## Тестирование / Testing

Для проверки работоспособности системы запустите тесты из консоли Ren'Py:

To test the system functionality, run tests from Ren'Py console:

```python
run_all_caching_tests()
```

Или отдельные тесты / Or individual tests:

```python
test_recolor_cache()           # Тест Recolor кеша / Test Recolor cache
test_animation_cache()         # Тест кеша анимаций / Test animation cache
test_girl_class_integration()  # Тест интеграции с GirlClass / Test GirlClass integration
```

## Производительность / Performance

### Преимущества / Benefits

1. **Уменьшение вычислений матриц**: Матрицы цветовых трансформаций вычисляются один раз и кэшируются
2. **Быстрая отрисовка**: Кэшированные изображения используются напрямую без перерасчета
3. **Масштабируемость**: Размер кеша автоматически контролируется

1. **Reduced matrix computations**: Color transformation matrices are computed once and cached
2. **Fast rendering**: Cached images are used directly without recomputation
3. **Scalability**: Cache size is automatically controlled

### Когда кеш инвалидируется / When cache is invalidated

Кеш автоматически инвалидируется при:
- Изменении одежды персонажа
- Изменении состояния одежды (Uptop, Upskirt, PantiesDown)
- Ручном вызове функций инвалидации

Cache is automatically invalidated when:
- Character clothing changes
- Clothing state changes (Uptop, Upskirt, PantiesDown)
- Manual invocation of invalidation functions

## Отладка / Debugging

В режиме разработчика доступны дополнительные функции логирования:

Additional logging functions are available in developer mode:

```python
if config.developer:
    log_cache_stats()  # Вывести статистику кеша / Print cache statistics
```

## Примечания / Notes

- Система совместима с существующей системой одежды
- Кэш автоматически очищается при переполнении
- Все ошибки обрабатываются gracefully, возвращая оригинальное изображение

- System is compatible with existing clothing system
- Cache is automatically cleared when full
- All errors are handled gracefully, returning original image

## Авторы / Authors

Система кэширования разработана для оптимизации проекта rle-opt.

Caching system developed to optimize the rle-opt project.
