def solve_backpack_problem():
    # Данные о предметах (очки указаны как положительные, но не взятые предметы будут вычитаться)
    items = {
        'r': {'name': 'Винтовка', 'size': 3, 'points': 25},
        'p': {'name': 'Пистолет', 'size': 2, 'points': 15},
        'a': {'name': 'Боекомплект', 'size': 2, 'points': 15},
        'm': {'name': 'Аптечка', 'size': 2, 'points': 20},
        'i': {'name': 'Ингалятор', 'size': 1, 'points': 5},
        'k': {'name': 'Нож', 'size': 1, 'points': 15},
        'x': {'name': 'Топор', 'size': 3, 'points': 20},
        't': {'name': 'Оберег', 'size': 1, 'points': 25},
        'f': {'name': 'Фляжка', 'size': 1, 'points': 15},
        'd': {'name': 'Антидот', 'size': 1, 'points': 10},
        's': {'name': 'Еда', 'size': 2, 'points': 20},
        'c': {'name': 'Арбалет', 'size': 2, 'points': 20}
    }
    
    # Параметры задачи
    backpack_width = 2
    backpack_height = 4
    total_cells = backpack_width * backpack_height
    start_points = 20
    illness = "астма"
    
    print(f"Ячейки {backpack_width}x{backpack_height}. Болезнь: {illness}. Стартовые очки: {start_points}")
    print()
    
    # Обязательные предметы
    required_items = ['i'] if illness == "астма" else (['d'] if illness == "паранойя" else [])
    
    # Общее количество очков всех предметов (для вычисления штрафов)
    total_all_points = sum(item['points'] for item in items.values())
    
    # Используем алгоритм рюкзака 0-1
    item_list = [(name, data['size'], data['points']) for name, data in items.items()]
    n = len(item_list)
    
    # DP таблица: dp[i][w] = максимальные очки для i первых предметов и w ячеек
    dp = [[-float('inf')] * (total_cells + 1) for _ in range(n + 1)]
    selected = [[[] for _ in range(total_cells + 1)] for _ in range(n + 1)]
    
    # Инициализация
    for w in range(total_cells + 1):
        dp[0][w] = start_points - total_all_points  # начальные очки минус все предметы
        selected[0][w] = []
    
    for i in range(1, n + 1):
        name, size, points = item_list[i-1]
        for w in range(total_cells + 1):
            # Не берем предмет - очки не меняются (уже учтен штраф в начальном значении)
            dp[i][w] = dp[i-1][w]
            selected[i][w] = selected[i-1][w][:]
            
            # Берем предмет, если помещается
            if w >= size:
                # Когда берем предмет, мы убираем штраф за него (+2*points: убираем -points и добавляем +points)
                new_score = dp[i-1][w-size] + 2 * points
                if new_score > dp[i][w]:
                    dp[i][w] = new_score
                    selected[i][w] = selected[i-1][w-size] + [name]
    
    # Ищем лучшую комбинацию с обязательными предметами (не обязательно заполнять все ячейки!)
    best_score = -float('inf')
    best_combination = []
    best_size = 0
    
    for w in range(total_cells + 1):
        combination = selected[n][w]
        # Проверяем обязательные предметы
        if all(req in combination for req in required_items):
            score = dp[n][w]
            if score > best_score:
                best_score = score
                best_combination = combination
                best_size = w  # запоминаем сколько ячеек использовано
    
    # Выводим результат
    if best_combination:
        print("🎯 ОПТИМАЛЬНОЕ РЕШЕНИЕ НАЙДЕНО!")
        print("\nОптимальный набор предметов:")
        taken_points = 0
        total_size_used = sum(items[item]['size'] for item in best_combination)
        
        for item in best_combination:
            item_info = items[item]
            points = item_info['points']
            size = item_info['size']
            taken_points += points
            print(f"  {item_info['name']} ({item}) - {size} яч., +{points} оч.")
        
        # Вычисляем не взятые предметы
        not_taken_items = [item for item in items.keys() if item not in best_combination]
        penalty_points = sum(items[item]['points'] for item in not_taken_items)
        
        if not_taken_items:
            print(f"\nНе взятые предметы (штраф):")
            for item in not_taken_items:
                item_info = items[item]
                points = item_info['points']
                print(f"  {item_info['name']} ({item}) - -{points} оч.")
        
        print(f"\n📊 СВОДКА:")
        print(f"  Использовано ячеек: {total_size_used}/{total_cells}")
        print(f"  Очки от взятых предметов: +{taken_points}")
        print(f"  Штраф за не взятые предметы: -{penalty_points}")
        print(f"  Стартовые очки: +{start_points}")
        print(f"  ИТОГО: {best_score} очков")
        
        # Визуализация рюкзака
        print("\n🎒 РАСПОЛОЖЕНИЕ В РЮКЗАКЕ:")
        backpack = [['[ ]' for _ in range(backpack_width)] for _ in range(backpack_height)]
        
        current_row, current_col = 0, 0
        for item in best_combination:
            size = items[item]['size']
            for i in range(size):
                if current_col >= backpack_width:
                    current_col = 0
                    current_row += 1
                if current_row < backpack_height:
                    backpack[current_row][current_col] = f'[{item}]'
                    current_col += 1
        
        for row in backpack:
            print(' '.join(row))
        
        if best_score > 0:
            print(f"\n✅ Том выживет с положительным счетом! ({best_score} очков)")
        else:
            print(f"\n❌ Внимание: итоговый счет отрицательный! ({best_score} очков)")
    else:
        print("Не удалось найти подходящий набор предметов!")

    # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ
    print("\n" + "="*60)
    print("ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ")
    print("="*60)
    
    solve_extra_problems(items, start_points, illness)

def solve_extra_problems(items, start_points, illness):
    """Решает дополнительные задания"""
    
    total_all_points = sum(item['points'] for item in items.values())
    
    def calculate_score(combination):
        taken_points = sum(items[item]['points'] for item in combination)
        return start_points + taken_points - (total_all_points - taken_points)
    
    # Задание 1: Решение для 7 ячеек
    print("\n1. ПОИСК РЕШЕНИЯ ДЛЯ 7 ЯЧЕЕК")
    print("-" * 40)
    
    from itertools import combinations
    
    required_items = ['i'] if illness == "астма" else (['d'] if illness == "паранойя" else [])
    all_items = list(items.keys())
    solutions_7 = []
    
    # Перебираем все комбинации для 7 ячеек
    for r in range(1, len(all_items) + 1):
        for combo in combinations(all_items, r):
            if not all(req in combo for req in required_items):
                continue
            
            total_size = sum(items[item]['size'] for item in combo)
            if total_size == 7:
                score = calculate_score(combo)
                if score > 0:
                    solutions_7.append((combo, score))
    
    if solutions_7:
        print(f"✅ Найдено решений: {len(solutions_7)}")
        solutions_7.sort(key=lambda x: x[1], reverse=True)
        
        print("\nЛучшее решение:")
        best_combo, best_score = solutions_7[0]
        print(f"Очки: {best_score}")
        print("Предметы:")
        for item in best_combo:
            item_info = items[item]
            print(f"  {item_info['name']} ({item}) - {item_info['size']} яч.")
        
        # Визуализация
        print("\nРасположение (7 ячеек):")
        backpack = [''] * 7
        pos = 0
        for item in best_combo:
            size = items[item]['size']
            for j in range(size):
                if pos < 7:
                    backpack[pos] = f'[{item}]'
                    pos += 1
        print(' '.join(backpack[:4]))
        print(' '.join(backpack[4:]))
    else:
        print("❌ Решений для 7 ячеек не найдено!")
        
        # Доказываем невозможность
        print("\n🔍 АНАЛИЗ ПРИЧИН НЕВОЗМОЖНОСТИ:")
        print(f"Общая сумма очков всех предметов: {total_all_points}")
        print(f"Стартовые очки: {start_points}")
        
        # Найдем максимально возможный счет для 7 ячеек
        max_possible_score = -float('inf')
        best_possible_combo = None
        
        for r in range(1, len(all_items) + 1):
            for combo in combinations(all_items, r):
                if not all(req in combo for req in required_items):
                    continue
                total_size = sum(items[item]['size'] for item in combo)
                if total_size == 7:
                    score = calculate_score(combo)
                    if score > max_possible_score:
                        max_possible_score = score
                        best_possible_combo = combo
        
        if best_possible_combo:
            print(f"Максимальный возможный счет для 7 ячеек: {max_possible_score}")
            if max_possible_score <= 0:
                print("✅ ДОКАЗАНО: даже лучшая комбинация дает неположительный счет")
                
            # Покажем лучшую комбинацию для анализа
            print("\nЛучшая комбинация для 7 ячеек (хотя счет отрицательный):")
            for item in best_possible_combo:
                item_info = items[item]
                print(f"  {item_info['name']} ({item}) - {item_info['size']} яч.")
            
            taken_points = sum(items[item]['points'] for item in best_possible_combo)
            penalty = total_all_points - taken_points
            print(f"\nОчки: +{start_points} (старт) + {taken_points} (предметы) - {penalty} (штраф) = {max_possible_score}")
        else:
            print("Невозможно упаковать обязательные предметы в 7 ячеек")
    
    # Задание 2: Все решения для 8 ячеек
    print("\n2. ВСЕ РЕШЕНИЯ ДЛЯ 8 ЯЧЕЕК С ПОЛОЖИТЕЛЬНЫМ СЧЕТОМ")
    print("-" * 50)
    
    solutions_8 = []
    # Ищем комбинации, которые используют НЕ БОЛЕЕ 8 ячеек (а не ровно 8!)
    for r in range(1, len(all_items) + 1):
        for combo in combinations(all_items, r):
            if not all(req in combo for req in required_items):
                continue
            
            total_size = sum(items[item]['size'] for item in combo)
            if total_size <= 8:  # Изменили на <= вместо ==
                score = calculate_score(combo)
                if score > 0:
                    solutions_8.append((combo, score, total_size))
    
    if solutions_8:
        # Группируем по количеству использованных ячеек
        solutions_8_exact = [s for s in solutions_8 if s[2] == 8]
        solutions_8_less = [s for s in solutions_8 if s[2] < 8]
        
        print(f"✅ Всего решений с положительным счетом: {len(solutions_8)}")
        print(f"   - Используют ровно 8 ячеек: {len(solutions_8_exact)}")
        print(f"   - Используют менее 8 ячеек: {len(solutions_8_less)}")
        
        # Покажем лучшее решение (с максимальными очками)
        best_solution = max(solutions_8, key=lambda x: x[1])
        best_combo, best_score, best_size = best_solution
        
        print(f"\n🎯 ЛУЧШЕЕ РЕШЕНИЕ ({best_score} очков, используется {best_size}/8 ячеек):")
        print("Предметы:", ', '.join(sorted(best_combo)))
        
        # Визуализация лучшего решения
        backpack = [['[ ]' for _ in range(4)] for _ in range(2)]
        pos = 0
        for item in best_combo:
            size = items[item]['size']
            for j in range(size):
                row = pos // 4
                col = pos % 4
                if row < 2:
                    backpack[row][col] = f'[{item}]'
                pos += 1
        
        print("Расположение:")
        for row in backpack:
            print(' '.join(row))
        
        # Группируем все решения по очкам
        from collections import defaultdict
        grouped = defaultdict(list)
        for combo, score, size in solutions_8:
            grouped[score].append((combo, size))
        
        print(f"\n📈 ВСЕ ВАРИАНТЫ С ПОЛОЖИТЕЛЬНЫМ СЧЕТОМ:")
        print(f"Уникальные значения очков: {sorted(grouped.keys(), reverse=True)}")
        
        for score in sorted(grouped.keys(), reverse=True):
            solutions = grouped[score]
            print(f"\n--- {score} очков ({len(solutions)} вариантов) ---")
            
            for i, (combo, size) in enumerate(solutions[:3], 1):  # Покажем 3 примера
                print(f"Пример {i} (использовано {size}/8 ячеек): {', '.join(sorted(combo))}")
    else:
        print("❌ Решений для 8 ячеек не найдено!")

# Запускаем программу
if __name__ == "__main__":
    solve_backpack_problem()