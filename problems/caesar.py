class CaesarCipher:
    def __init__(self, shift: int):
        self.shift = shift % 26

    def encrypt(self, plaintext: str) -> str:
        return self._transform(plaintext, self.shift)

    def decrypt(self, ciphertext: str) -> str:
        return self._transform(ciphertext, -self.shift)

    def _transform(self, text: str, shift: int) -> str:
        result = []
        for char in text:
            if char.isalpha():
                shifted_char = self._shift_char(char, shift)
                result.append(shifted_char)
            else:
                result.append(char)
        return ''.join(result)

    def _shift_char(self, char: str, shift: int) -> str:
        if char.islower():
            start = ord('a')
        else:
            start = ord('A')

        shifted_position = (ord(char) - start + shift) % 26
        return chr(start + shifted_position)



if __name__ == "__main__":

    cipher = CaesarCipher(shift=3)
    plaintext = "Hello, World!"

    ciphertext = cipher.encrypt(plaintext)
    print(f"Encrypted: {ciphertext}")  

    decrypted_text = cipher.decrypt(ciphertext)
    print(f"Decrypted: {decrypted_text}") 