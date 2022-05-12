class UnknownColumnNameGenerator:

    _flag_count = 0
    _key_count = 0
    _keys_count = 0
    _data_count = 0
    _unknown_count = 0

    def next_name(self, column) -> str:
        if column.type == "bool":
            name = f"Flag{self._flag_count}"
            self._flag_count += 1
        elif column.array:
            if column.type == "foreignrow":
                name = f"Keys{self._keys_count}"
                self._keys_count += 1
            else:
                name = f"Data{self._data_count}"
                self._data_count += 1
        elif column.type == "foreignrow":
            name = f"Key{self._key_count}"
            self._key_count += 1
        else:
            name = f"Unknown{self._unknown_count}"
            self._unknown_count += 1
        return name
