from enum import Enum
from language_parser.tokenizer.consts import (
    single_char_tokens,
    reserved,
    NUMBER,
    IDENTIFICATOR,
    NEWLINE
)


class State(Enum):
    INITIAL = 1
    UPPERCASE = 2
    LOWERCASE = 3


class Token:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'{self.key}: {self.value}'

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value


class Tokenizer:
    @staticmethod
    def tokenize(code):
        tokens = []
        state = State.INITIAL
        lexeme = ''
        pos = 0

        while pos < len(code):
            ch = code[pos]
            if state == State.INITIAL:
                if ch.isspace():
                    if '\n' in ch and tokens:
                        tokens.append(
                            Token(
                                key=NEWLINE,
                                value=ch
                            )
                        )

                    pos += 1
                    continue

                if ch in single_char_tokens:
                    tokens.append(
                        Token(
                            key=single_char_tokens[ch],
                            value=ch
                        )
                    )
                    pos += 1
                    continue

                if ch.isalpha():
                    if ch.islower():
                        state = State.LOWERCASE
                    else:
                        state = State.UPPERCASE
                    lexeme = ch
                    pos += 1
                    continue

                raise ValueError(f'Unexpected character: {ch}')

            elif state == State.LOWERCASE:
                if pos < len(code) and code[pos].islower():
                    lexeme += code[pos]
                    pos += 1
                else:
                    tokens.append(
                        Token(
                            key=IDENTIFICATOR,
                            value=lexeme
                        )
                    )
                    lexeme = ''
                    state = State.INITIAL

                continue

            elif state == State.UPPERCASE:
                if pos < len(code) and code[pos].isalpha():
                    lexeme += code[pos]
                    pos += 1
                else:
                    token_type = Tokenizer.__process_uppercase(lexeme)
                    tokens.append(
                        Token(
                            key=token_type,
                            value=lexeme
                        )
                    )
                    lexeme = ''
                    state = State.INITIAL

                continue

        if lexeme:
            tokens.append(
                Token(
                    key=IDENTIFICATOR,
                    value=lexeme
                )
            )

        return tokens

    @staticmethod
    def __process_uppercase(lexeme):
        if lexeme in reserved:
            return reserved[lexeme]
        elif Tokenizer.__is_roman_number(lexeme):
            return NUMBER
        else:
            raise ValueError(f'Unknown uppercase token: {lexeme}')

    @staticmethod
    def __is_roman_number(lexeme):
        for ch in lexeme:
            if ch not in lexeme:
                return False

        return True
