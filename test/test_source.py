import olca_ipc as ipc
import olca_schema as o
import json

# 创建IPC客户端
client = ipc.Client(8080)

def custom_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, o.FlowType):
        return obj.value
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)

def test_get_process_details():
    try:
        descriptors = client.get_descriptors(o.Process)
        print("Details for Process:")
        for descriptor in descriptors[:20]:  # 只输出前3个描述符
            detailed_info = client.get(o.Process, descriptor.id)
            if detailed_info.process_documentation and detailed_info.process_documentation.data_set_owner:
                data_set_owner = detailed_info.process_documentation.data_set_owner
                if data_set_owner.name == "Tiangong LCI Data Working Group":
                    print(f"Name: {data_set_owner.name}")
        print("\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_get_process_details()
