import unittest
import olca_schema as o
from config import client


class ParamTest(unittest.TestCase):
    def test_global_params(self):
        # 创建参数 X 和 Y
        x = o.Parameter()
        x.name = "X"
        x.value = 4.0
        x.parameter_scope = o.ParameterScope.GLOBAL_SCOPE

        y = o.Parameter()
        y.name = "Y"
        y.formula = "X * 10"
        y.parameter_scope = o.ParameterScope.GLOBAL_SCOPE

        # 打印参数 X 和 Y
        print("Created parameters:")
        print("X:", x)
        print("Y:", y)

        # 将参数放入 openLCA
        client.put(x)
        client.put(y)

        # 获取参数并验证属性
        x = client.get(o.Parameter, x.id)
        y = client.get(o.Parameter, y.id)

        print("Fetched parameters from openLCA:")
        print("X:", x)
        print("Y:", y)

        self.assertEqual("X", x.name)
        self.assertEqual(o.ParameterScope.GLOBAL_SCOPE, x.parameter_scope)
        self.assertEqual(4, x.value)
        self.assertTrue(x.is_input_parameter)

        # 删除参数 X
        client.delete(x)
        print("Deleted parameter X")

        self.assertEqual("Y", y.name)
        self.assertEqual("X * 10", y.formula)
        self.assertEqual(o.ParameterScope.GLOBAL_SCOPE, y.parameter_scope)
        self.assertFalse(y.is_input_parameter)

        # 删除参数 Y
        client.delete(y)
        print("Deleted parameter Y")


if __name__ == "__main__":
    unittest.main()
