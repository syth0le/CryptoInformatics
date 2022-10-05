from abc import abstractmethod
from enum import Enum
from typing import Union, Optional


class Alphabet(Enum):
    RUS: str = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    ENG: str = 'abcdefghijklmnopqrstuvwxyz'

DIGITS: str = '1234567890'


class AbstractCipher:

    @abstractmethod
    def decrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        pass

    @abstractmethod
    def encrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        pass

    def _clean_text(self, text: str) -> str:
        return text.lower()

    # @abstractmethod
    # def auto_encrypt(self, text: str, alph: Alphabet = Alphabet.RUS) -> str:
    #     pass


class CaesaerCipher(AbstractCipher):
    class Action(str, Enum):
        ENCRYPTION = 'ENCRYPTION'
        DECRYPTION = 'DECRYPTION'

    def decrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        text = self._clean_text(text)
        length = len(alph)
        return self._process_string(text, length, alph, self.Action.DECRYPTION)

    def encrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        text = self._clean_text(text)
        length = len(alph)
        return self._process_string(text, length, alph, self.Action.ENCRYPTION)


    def _process_string(self, text: str, length: int, alph: Alphabet, action: Action) -> str:
        res = ''
        for i, item in enumerate(text):
            if item.isdigit():
                temp = shift % len(DIGITS)
                idx = DIGITS.index(item)
                curr = idx - temp if action == self.Action.ENCRYPTION else idx + temp
                res += DIGITS[curr]
            elif item.isalpha():
                temp = shift % length
                idx = alph.index(item)
                curr = idx - temp if action == self.Action.ENCRYPTION else idx + temp
                res += alph[curr]
            else:
                res += item
        return res


class VigenerCipher(AbstractCipher):
    class Action(str, Enum):
        ENCRYPTION = 'ENCRYPTION'
        DECRYPTION = 'DECRYPTION'

    def decrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        text = self._clean_text(text)
        length = len(alph)
        return self._process_string(text, length, alph, self.Action.DECRYPTION)

    def encrypt(self, text: str, shift: Union[str, int], alph: Alphabet = Alphabet.RUS.value) -> str:
        text = self._clean_text(text)
        length = len(alph)
        return self._process_string(text, length, alph, self.Action.ENCRYPTION)

    def _process_string(self, text: str, length: int, alph: Alphabet, action: Action) -> str:
        res = ''
        for i, item in enumerate(text):
            key_idx = i % len(shift)
            shift_idx = alph.index(shift[key_idx])
            if item.isalpha():
                idx = alph.index(item)
                if action == self.Action.ENCRYPTION:
                    curr = (idx + length - shift_idx) % length
                else:
                    curr = (idx + shift_idx) % length
                res += alph[curr]
            else:
                res += item
        return res


if __name__ == '__main__':
    cs = VigenerCipher()
    text = input('Enter your text: ')
    shift = input('Enter shift: ')
    decripted = cs.decrypt(text, shift, Alphabet.ENG.value)
    print(f'Decryption: {decripted}')
    encripted = cs.encrypt(decripted, shift, Alphabet.ENG.value)
    print(f'Encryption: {encripted}')
