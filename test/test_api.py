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

def get_available_categories():
    categories = [
        o.Actor,
        o.Currency,
        o.DQSystem,
        o.Epd,
        o.Flow,
        o.FlowProperty,
        o.ImpactCategory,
        o.ImpactMethod,
        o.Location,
        o.Parameter,
        o.Process,
        o.ProductSystem,
        o.Project,
        o.Result,
        o.SocialIndicator,
        o.Source,
        o.UnitGroup
    ]
    return categories

def test_get_all_descriptors():
    try:
        categories = get_available_categories()
        for category in categories:
            descriptors = client.get_descriptors(category)
            print(f"Descriptors for {category.__name__}:")
            for descriptor in descriptors[:3]:  # 只输出前3个描述符
                print(json.dumps(descriptor, default=custom_serializer, indent=2))
            print("\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_get_all_descriptors()
