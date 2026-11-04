import sys
import os

# Карты соответствия (двунаправленные)
BF_TO_TRANSLIT = {
    '>': 'Slovo ',
    '<': 'Tverdo ',
    '+': 'Az ',
    '-': 'Vedi ',
    '.': 'Her ',
    ',': 'Omega ',
    '[': 'Izhe ',
    ']': 'I '
}

BF_TO_GLAGOL = {
    '>': 'Ⱄ', '<': 'Ⱅ', '+': 'Ⰰ', '-': 'Ⰱ', '.': 'Ⱈ', ',': 'Ⱉ', '[': 'Ⰺ', ']': 'Ⰻ'
}

# Обратные карты для расшифровки
TRANSLIT_TO_BF = {v.strip(): k for k, v in BF_TO_TRANSLIT.items()}
GLAGOL_TO_BF = {v: k for k, v in BF_TO_GLAGOL.items()}

def to_slavonic(bf_code, use_utf8=False):
    """Переводит чистый Brainfuck в славянский стиль"""
    result = []
    for char in bf_code:
        if use_utf8 and char in BF_TO_GLAGOL:
            result.append(BF_TO_GLAGOL[char])
        elif not use_utf8 and char in BF_TO_TRANSLIT:
            result.append(BF_TO_TRANSLIT[char])
    return "".join(result).strip()

def from_slavonic(slav_code):
    """Переводит славянский код обратно в понятный Brainfuck"""
    bf_code = []
    # Сначала проверяем на токены транслита (разбиваем по пробельным символам)
    words = slav_code.split()
    
    # Если в файле в основном слова вроде Az, Slovo
    if any(w in TRANSLIT_TO_BF for w in words):
        for word in words:
            if word in TRANSLIT_TO_BF:
                bf_code.append(TRANSLIT_TO_BF[word])
    else:
        # Иначе обрабатываем как посимвольную UTF-8 глаголицу
        for char in slav_code:
            if char in GLAGOL_TO_BF:
                bf_code.append(GLAGOL_TO_BF[char])
                
    return "".join(bf_code)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование:")
        print("  В славянский транслит:  python transglagol.py to-translit <howdy.bf>")
        print("  В реальную глаголицу:   python transglagol.py to-glagol <howdy.bf>")
        print("  Из славянского в BF:    python transglagol.py from-slav <privetnah.gf>")
        sys.exit(1)
        
    mode = sys.argv[1]
    input_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл '{input_file}' не найден.")
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if mode == 'to-translit':
        output = to_slavonic(content, use_utf8=False)
        ext = '.gf'
    elif mode == 'to-glagol':
        output = to_slavonic(content, use_utf8=True)
        ext = '.gf'
    elif mode == 'from-slav':
        output = from_slavonic(content)
        ext = '.bf'
    else:
        print("Неизвестный режим. Используй: to-translit, to-glagol или from-slav")
        sys.exit(1)
        
    # Формируем имя нового файла (добавляем к старому имени новую кодировку)
    base_name, _ = os.path.splitext(input_file)
    output_file = f"{base_name}_converted{ext}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
        
    print(f"Успешно! Результат сохранен в древний свиток: {output_file}")
