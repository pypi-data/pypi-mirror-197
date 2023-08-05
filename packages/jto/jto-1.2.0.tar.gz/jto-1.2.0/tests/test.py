from jto.dataclass_generator import ClassesTemplate

data = {
  "Id": 12345,
  "Customer": "John Smith",
  "Quantity": 1,
  "Price": 10.00
}

test_classes = ClassesTemplate()
test_classes.build_classes('Request', data)
print(test_classes.build_classes_string())





# from dataclasses import dataclass, field, asdict
#
# class Undefined:
#     pass
#
# @dataclass
# class Test:
#     f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': False})
#
# result = asdict(Test())
# print(result, result['f1'] == Undefined)
