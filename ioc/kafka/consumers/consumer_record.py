class ConsumerRecord:
    def __init__(self, key: str, value: str) -> None:
        self._key = key
        self._value = value

    def get_key(self) -> str:
        return self._key

    def get_value(self) -> str:
        return self._value
