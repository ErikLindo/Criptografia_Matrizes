# Importando bibliotecas necessárias
import numpy as np

def text_to_numbers(text):
    # Converte texto para números (A=0, B=1, ..., Z=25)
    text = text.upper().replace(" ", "")
    return [ord(char) - ord('A') for char in text]

def numbers_to_text(numbers):
    # Converte números de volta para texto
    return ''.join(chr(num % 26 + ord('A')) for num in numbers)

def create_matrix_key():
    # Cria uma matriz 2x2 como chave (exemplo)
    return np.array([[6, 24], [1, 16]])

def mod_inverse(a, m):
    # Calcula o inverso modular de a módulo m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_inverse_mod(matrix, mod):
    # Calcula a inversa da matriz módulo 26
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        raise ValueError("Matriz não tem inversa modular")
    
    # Calcula a matriz adjunta
    adj = np.array([[matrix[1,1], -matrix[0,1]], [-matrix[1,0], matrix[0,0]]])
    return (det_inv * adj) % mod

def remove_consecutive_repeats(text):
    # Remove letras consecutivas iguais, substituindo a segunda por próxima letra válida
    numbers = text_to_numbers(text)
    result = numbers.copy()
    for i in range(1, len(numbers)):
        # Verifica se a letra atual é igual à anterior
        if result[i] == result[i-1]:
            # Tenta a próxima letra no alfabeto (módulo 26)
            new_value = (result[i] + 1) % 26
            # Garante que a nova letra não repita com a anterior ou seguinte
            while (new_value == result[i-1] or 
                   (i < len(numbers)-1 and new_value == result[i+1])):
                new_value = (new_value + 1) % 26
            result[i] = new_value
    return numbers_to_text(result), numbers != result

def restore_consecutive_repeats(cipher_text, original_numbers, was_modified):
    # Restaura o texto criptografado original para descriptografia correta
    if not was_modified:
        return cipher_text
    # Como sabemos que a substituição foi feita, usamos os números originais
    return numbers_to_text(original_numbers)

def encrypt(plain_text, key_matrix):
    # Criptografa o texto usando a cifra de Hill
    numbers = text_to_numbers(plain_text)
    # Garante que o tamanho do texto seja par
    if len(numbers) % 2 != 0:
        numbers.append(0)  # Adiciona 'A' como padding
    
    encrypted = []
    for i in range(0, len(numbers), 2):
        vector = np.array(numbers[i:i+2])
        result = np.dot(key_matrix, vector) % 26
        encrypted.extend(result)
    
    # Converte para texto e remove repetições consecutivas
    cipher_text = numbers_to_text(encrypted)
    modified_text, was_modified = remove_consecutive_repeats(cipher_text)
    return modified_text, encrypted, was_modified



def main():
    # Exemplo de uso
    key = create_matrix_key()
    print("Matriz chave:\n", key)
    
    # Texto a ser criptografado
    plain_text = input("Digite o texto a ser criptografado: ")
    
    # Criptografar
    cipher_text, original_numbers, was_modified = encrypt(plain_text, key)
    print("Texto criptografado:", cipher_text)

if __name__ == "__main__":
    main()