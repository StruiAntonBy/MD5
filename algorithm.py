def md5(msg):
    constants = (  # Список констант
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
    )

    shift_values = (  # Величины сдвигов для каждой операции
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    )

    msg = bytearray(msg)  # Копирование входных данных в изменяемый тип данных
    len_in_bits = (8 * len(msg)) & 0xffffffffffffffff  # Начальная длинна сообщения в битах (для asci 1 символ = 1 байт)
    msg.append(0x80)  # Добавляем бит в конец сообщения

    while len(msg) % 64 != 56:  # Дописываем нулевые биты, пока длина сообщения не станет сравнима с 448 (448/8 = 56) по модулю 512(512/8 = 64)
        msg.append(0)
    msg += len_in_bits.to_bytes(8, byteorder="little")  # Дописываем остаток от деления изначальной длины сообщения на 2^64 (64/8 = 8)

    hash_pieces = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]  # Инициализация переменных: A, B, C, D
    for chunk in (msg[i:i + 64] for i in range(0, len(msg), 64)):  # Разбиваем подготовленное сообщение на 512-битные (512/8 = 64) "куски"
        a, b, c, d = hash_pieces  # Инициализируем переменные для текущего куска

        for i in range(64):  # Основные операции
            if 0 <= i <= 15:
                f, g = (b & c) | (~b & d), i  # (B and C) or ((not B) and D)
            elif 16 <= i <= 31:
                f, g = (d & b) | (~d & c), (5 * i + 1) % 16  # (D and B) or ((not D) and C)
            elif 32 <= i <= 47:
                f, g = b ^ c ^ d, (3 * i + 5) % 16  # B xor C xor D (xor = Исключающее или)
            else:
                f, g = c ^ (b | ~d), (7 * i) % 16  # C xor (B or (not D))

            f = (a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder="little")) & 0xFFFFFFFF  # chunk[4 * g:4 * g + 4] — 32-битный блок
            new_b = (b + ((f << shift_values[i]) | (f >> (32 - shift_values[i]))) & 0xFFFFFFFF) & 0xFFFFFFFF  # Выполняем битовый сдвиг
            a, b, c, d = d, new_b, b, c

        for i, val in enumerate((a, b, c, d)):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))
