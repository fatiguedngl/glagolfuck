import sys

# Словарь перевода глаголицы в стандартные команды Brainfuck
GLAGOL_MAP = {
    'Ⱄ': '>',  # Слово -> Вперед
    'Ⱅ': '<',  # Твердо -> Назад
    'Ⰰ': '+',  # Аз -> Плюс
    'Ⰱ': '-',  # Веди -> Минус
    'Ⱈ': '.',  # Херъ -> Вывод
    'Ⱉ': ',',  # Омега -> Ввод
    'Ⰺ': '[',  # Иже -> Цикл старт
    'Ⰻ': ']'   # И -> Цикл энд
}

def run_glagolfuck(code):
    # Очищаем от комментариев и пробелов, оставляем только наши команды
    bf_code = [GLAGOL_MAP[char] for char in code if char in GLAGOL_MAP]
    
    if not bf_code:
        print("Ошибка: В файле не найдено валидных глаголических команд!")
        return

    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    
    # Парсинг циклов с защитой от вылета
    loop_map = {}
    stack = []
    try:
        for i, char in enumerate(bf_code):
            if char == '[':
                stack.append(i)
            elif char == ']':
                start = stack.pop()
                loop_map[start] = i
                loop_map[i] = start
        if stack:
            raise IndexError
    except IndexError:
        print("Ошибка синтаксиса: Обнаружены незакрытые или лишние циклы (тут не вся глаголица, Онфим недоволен)!")
        return

    # Выполнение
    while code_ptr < len(bf_code):
        cmd = bf_code[code_ptr]
        
        if cmd == '>':
            ptr = (ptr + 1) % 30000
        elif cmd == '<':
            ptr = (ptr - 1) % 30000
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            sys.stdout.write(chr(tape[ptr]))
            sys.stdout.flush()
        elif cmd == ',':
            char = sys.stdin.read(1)
            tape[ptr] = ord(char) if char else 0
        elif cmd == '[':
            if tape[ptr] == 0:
                code_ptr = loop_map[code_ptr]
        elif cmd == ']':
            if tape[ptr] != 0:
                code_ptr = loop_map[code_ptr]
                
        code_ptr += 1
    print() # Перенос строки в конце вывода

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python glagolfuck.py <privetnah.gf>")
    else:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                source_code = f.read()
            run_glagolfuck(source_code)
        except FileNotFoundError:
            print(f"Ошибка: Онфим '{sys.argv[1]}' пропишет тебе лещей.")
