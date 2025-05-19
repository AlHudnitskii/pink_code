import unittest
import datetime
from custom_json_serializer import custom_json_serializer 

class Testcustom_json_serializer(unittest.TestCase):

    def test_serialize_none(self):
        self.assertEqual(custom_json_serializer.serialize(None), "null")

    def test_deserialize_none(self):
        self.assertEqual(custom_json_serializer.deserialize("null"), None)

    def test_serialize_bool(self):
        self.assertEqual(custom_json_serializer.serialize(True), "true")
        self.assertEqual(custom_json_serializer.serialize(False), "false")

    def test_deserialize_bool(self):
        self.assertEqual(custom_json_serializer.deserialize("true"), True)
        self.assertEqual(custom_json_serializer.deserialize("false"), False)

    def test_serialize_int(self):
        self.assertEqual(custom_json_serializer.serialize(123), "123")
        self.assertEqual(custom_json_serializer.serialize(-45), "-45")

    def test_deserialize_int(self):
        self.assertEqual(custom_json_serializer.deserialize("123"), 123)
        self.assertEqual(custom_json_serializer.deserialize("-45"), -45)

    def test_serialize_float(self):
        self.assertEqual(custom_json_serializer.serialize(3.14), "3.14")
        self.assertEqual(custom_json_serializer.serialize(-0.5), "-0.5")

    def test_deserialize_float(self):
        self.assertEqual(custom_json_serializer.deserialize("3.14"), 3.14)
        self.assertEqual(custom_json_serializer.deserialize("-0.5"), -0.5)

    def test_serialize_string(self):
        self.assertEqual(custom_json_serializer.serialize("hello"), '"hello"')
        self.assertEqual(custom_json_serializer.serialize("string with \"quotes\""), '"string with \\"quotes\\""')
        self.assertEqual(custom_json_serializer.serialize("path\\to\\file"), '"path\\\\to\\\\file"')

    def test_deserialize_string(self):
        self.assertEqual(custom_json_serializer.deserialize('"hello"'), "hello")
        self.assertEqual(custom_json_serializer.deserialize('"string with \\"quotes\\""'), 'string with "quotes"')
        self.assertEqual(custom_json_serializer.deserialize('"path\\\\to\\\\file"'), 'path\\to\\file')

    def test_serialize_list(self):
        self.assertEqual(custom_json_serializer.serialize([1, "two", True]), "[1,\"two\",true]")
        self.assertEqual(custom_json_serializer.serialize([]), "[]")

    def test_deserialize_list(self):
        self.assertEqual(custom_json_serializer.deserialize("[1,\"two\",true]"), [1, "two", True])
        self.assertEqual(custom_json_serializer.deserialize("[]"), [])

    def test_serialize_dict(self):
        data = {"name": "Alice", "age": 30}
        self.assertEqual(custom_json_serializer.serialize(data), '{"name":"Alice","age":30}')

    def test_deserialize_dict(self):
        json_str = '{"name":"Alice","age":30}'
        self.assertEqual(custom_json_serializer.deserialize(json_str), {"name": "Alice", "age": 30})
        self.assertEqual(custom_json_serializer.deserialize("{}"), {})

    def test_serialize_datetime(self):
        dt = datetime.datetime(2025, 5, 20, 10, 30, 0)
        self.assertEqual(custom_json_serializer.serialize(dt), '"2025-05-20T10:30:00"')

    def test_serialize_date(self):
        date = datetime.date(2025, 5, 20)
        self.assertEqual(custom_json_serializer.serialize(date), '"2025-05-20"')

    def test_serialize_unsupported_type(self):
        with self.assertRaises(TypeError):
            custom_json_serializer.serialize(object())

if __name__ == '__main__':
    unittest.main()