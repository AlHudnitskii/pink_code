import datetime


class custom_json_serializer:
    @staticmethod
    def serialize(obj):
        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, int):
            return str(obj)
        elif isinstance(obj, float):
            return str(obj)
        elif isinstance(obj, str):
            return f'"{custom_json_serializer._escape_string(obj)}"'
        elif isinstance(obj, list):
            elements = [custom_json_serializer.serialize(item) for item in obj]
            return f"[{','.join(elements)}]"
        elif isinstance(obj, dict):
            pairs = [f'{custom_json_serializer.serialize(key)}:{custom_json_serializer.serialize(value)}' for key, value in obj.items()]
            return f"{{{','.join(pairs)}}}"
        elif isinstance(obj, datetime.datetime):
            return f'"{obj.isoformat()}"'
        elif isinstance(obj, datetime.date):
            return f'"{obj.isoformat()}"'
        else:
            raise TypeError(f"Тип {type(obj)} не поддерживается сериализацией.")

    @staticmethod
    def _escape_string(s):
        return s.replace('\\', '\\\\').replace('"', '\\"')
    @staticmethod
    def deserialize(s):
        s = s.strip()
        if s == "null":
            return None
        elif s == "true":
            return True
        elif s == "false":
            return False
        elif s.startswith('"') and s.endswith('"'):
            return custom_json_serializer._unescape_string(s[1:-1])
        elif s.startswith('[') and s.endswith(']'):
            if len(s) > 2:
                elements_str = s[1:-1].split(',')
                elements = [custom_json_serializer.deserialize(elem.strip()) for elem in elements_str if elem.strip()]
                return elements
            else:
                return []
        elif s.startswith('{') and s.endswith('}'):
            if len(s) > 2:
                pairs_str = s[1:-1].split(',')
                result = {}
                for pair_str in pairs_str:
                    if ":" in pair_str:
                        key_str, value_str = pair_str.split(':', 1)
                        key = custom_json_serializer.deserialize(key_str.strip())
                        value = custom_json_serializer.deserialize(value_str.strip())
                        result[key] = value
                return result
            else:
                return {}
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                try:
                    return datetime.datetime.fromisoformat(s.strip('"'))
                except ValueError:
                    try:
                        return datetime.date.fromisoformat(s.strip('"'))
                    except ValueError:
                        raise ValueError(f"Невозможно десериализовать строку: {s}")

    @staticmethod
    def _unescape_string(s):
        return s.replace('\\"', '"').replace('\\\\', '\\')