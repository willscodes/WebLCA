import olca_ipc as ipc
import olca_schema as o
import json

# 配置文件名和接口信息
# api_file_name = "test_lca_api.py"
api_config = {
    "host": "localhost",
    "port": 8080,
}

# 打印文件名和接口配置信息
print(f"接口配置: {api_config}")

# 创建IPC客户端
client = ipc.Client(api_config['port'])


def custom_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, o.FlowType):
        return obj.value
    elif isinstance(obj, o.Ref):
        return obj.__dict__
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)


def test_api_operations():
    try:
        # 创建一个新的 flow 对象
        flow = o.Flow()
        flow.name = "test_flow"
        flow.flow_type = o.FlowType.ELEMENTARY_FLOW

        # 测试 put 操作（添加测试数据）
        put_response = client.put(flow)
        print('Put Response (add): ID =', put_response.id)
        print('流数据添加成功！')

        # 获取新创建的 flow 对象的 ID
        flow_id = put_response.id

        # 测试 get 操作（检索测试数据）
        get_response = client.get(o.Flow, flow_id)
        print('Get Response: ID =', get_response.id)
        print('流数据查询成功！')

        # 更新 flow 对象的名称
        flow.name = "updated_test_flow"
        flow.id = flow_id  # 确保 ID 一致

        # 测试 put 操作（更新测试数据）
        put_response_2 = client.put(flow)
        print('Put Response (update): ID =', put_response_2.id)
        print('流数据更新成功！')

        # 测试 delete 操作（删除测试数据）
        delete_response = client.delete(flow)
        print('Delete Response: ID =', flow.id)
        print('流数据删除成功！')
    except Exception as e:
        print(f"接口测试失败！！错误信息: {e}")


if __name__ == "__main__":
    test_api_operations()
