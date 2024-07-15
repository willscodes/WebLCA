import olca_ipc as ipc
import olca_schema as o
from googletrans import Translator
import logging
import json
import copy
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='translation.log', filemode='w')

# 创建IPC客户端
client = ipc.Client(8080)

# 创建翻译器实例
translator = Translator()

# 记录成功翻译和更新的流数量
success_count = 0
error_count = 0

# 存储已翻译的流名称
translated_flows = []

# 获取所有流数据的描述符
flow_descriptors = client.get_descriptors(o.Flow)

logging.info("开始获取流数据描述符")

def update_flow_data(flow, translated_name):
    """
    更新流数据中的名称并返回更新后的数据
    """
    try:
        logging.info(f"原始 flow_data: {flow.__dict__}")

        # 确保 flow_data 是可变的
        if isinstance(flow, dict):
            flow_data_mutable = copy.deepcopy(flow)
        else:
            flow_data_mutable = copy.deepcopy(flow.__dict__)

        # 更新可变副本
        flow_data_mutable['name'] = translated_name

        # 打印成功更新的日志
        logging.info(f"成功更新 flow_data ID={flow_data_mutable['id']}")

    except AttributeError as e:
        logging.error(f"更新 flow_data ID={flow['id']} 时出错: {e}")

    return flow_data_mutable

def process_flow(descriptor):
    global success_count, error_count
    try:
        flow = client.get(o.Flow, descriptor.id)
        if flow is None:
            logging.error(f"获取流数据失败: ID={descriptor.id}, 返回None")
            error_count += 1
            return

        # 记录源数据
        logging.info(f"源数据: {flow.__dict__}")

        logging.info(f"获取到流数据: ID={descriptor.id}, Name={flow.name}")

        # 获取流的名称并翻译
        original_name = flow.name
        if not original_name:
            logging.error(f"流数据ID={descriptor.id}的名称为空，跳过翻译")
            error_count += 1
            return

        # 检查是否已经包含翻译后缀，避免重复翻译
        if "(已翻译)" not in original_name:
            translation_result = translator.translate(original_name, src='en', dest='zh-cn')
            # 检查翻译结果
            if translation_result and translation_result.text:
                translated_name = f"{translation_result.text} (已翻译)"

                # 更新流数据
                try:
                    updated_flow_data = update_flow_data(flow, translated_name)
                    flow_json = json.dumps(updated_flow_data, default=lambda o: o.__dict__)
                    response = client.update(json.loads(flow_json))
                    logging.info(f"成功更新流数据: ID={updated_flow_data['id']}, 新名称={updated_flow_data['name']}")
                    success_count += 1

                    # 将已翻译的流名称添加到列表
                    translated_flows.append(translated_name)

                except Exception as update_error:
                    logging.error(f"更新流数据ID={flow.id}时发生错误: {update_error}")
                    error_count += 1
            else:
                logging.error(f"翻译结果为空: ID={descriptor.id}, Name={original_name}")
                error_count += 1
        else:
            logging.info(f"流数据ID={descriptor.id}已经包含翻译后缀，跳过翻译")
            success_count += 1
    except Exception as e:
        logging.error(f"处理流数据ID={descriptor.id}时发生错误: {e}")
        error_count += 1

# 使用ThreadPoolExecutor来并行处理流数据
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_flow, descriptor) for descriptor in flow_descriptors[:50]]  # 这里只处理前500个流数据作为示例
    for future in as_completed(futures):
        pass

logging.info(f"翻译和更新完成。成功翻译和更新的数据数量: {success_count}，发生错误的数据数量: {error_count}")

# 打印所有已翻译的流名称
print("已翻译的流名称:")
for name in translated_flows:
    print(name)
