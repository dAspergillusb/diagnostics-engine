def encrypt_string(data: str) -> str:
    encrypted: list[str] = []
    for char in data:
        encrypted.append(f"{ord(char)}")
    return "#".join(encrypted)


def decrypt_string(_encrypted_data: str) -> str:
    decrypted: list[str] = []
    for code in map(int, _encrypted_data.split("#")):
        decrypted.append(chr(code))
    return "".join(decrypted)


def encrypted_data(data: str) -> str:
    return encrypt_string(data=data)


def decrypted_data(data: str) -> str:
    return decrypt_string(_encrypted_data=data)


if __name__ == '__main__':
    # for _ in range(10**10):
    #     c = shuffle_chars()
    #     if "\\n" in c:
    #         print(c)
    _chars = "154c4L4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y/Е4ы4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y/Е4U4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y/Е4B4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y/Е4.4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y/Е4@r4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/ЕcrNЕ@/Е@NЕ@/ЕONЕ@/ЕпNЕ@/Е7NЕ@/ЕLNЕ@;Y/Е4@@4NЕъюCзбМyъlzyЫИzМзaaЕ4ljy4R/Еc;Y;"
    print(decrypted_data(_chars))