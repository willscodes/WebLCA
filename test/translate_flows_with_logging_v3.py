import olca_ipc as ipc
import olca_schema as o
from googletrans import Translator
import logging
import json

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='translation.log',
                    filemode='w')

# 创建IPC客户端
client = ipc.Client(8080)

# 创建翻译器实例
translator = Translator()

# 记录成功翻译和更新的流数量
success_count = 0
error_count = 0

# 获取所有流数据的描述符
flow_descriptors = client.get_descriptors(o.Flow)

logging.info("开始获取流数据描述符")

# 遍历流数据并翻译
for descriptor in flow_descriptors[:50]:  # 这里只处理前50个流数据作为示例
    try:
        flow = client.get(o.Flow, descriptor.id)
        if flow is None:
            logging.error(f"获取流数据失败: ID={descriptor.id}, 返回None")
            error_count += 1
            continue

        # 记录源数据
        logging.info(f"源数据: {flow.__dict__}")

        logging.info(f"获取到流数据: ID={descriptor.id}, Name={flow.name}")

        # 获取流的名称并翻译
        original_name = flow.name
        if not original_name:
            logging.error(f"流数据ID={descriptor.id}的名称为空，跳过翻译")
            error_count += 1
            continue

        # 检查是否已经包含翻译后缀，避免重复翻译
        if "(已翻译)" not in original_name:
            translation_result = translator.translate(original_name, src='en', dest='zh-cn')
            # 检查翻译结果
            if translation_result and translation_result.text:
                translated_name = translation_result.text
                flow.name = f"{translated_name} (已翻译)"

                # 打印翻译后的名称并记录日志
                logging.info(f"原名称: {original_name}, 翻译后名称: {flow.name}")

                # 更新流数据
                try:
                    flow_json = json.dumps(flow, default=lambda o: o.__dict__)
                    response = client.update(json.loads(flow_json))
                    logging.info(f"成功更新流数据: ID={flow.id}, 新名称={flow.name}")
                    success_count += 1
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

logging.info(f"翻译和更新完成。成功翻译和更新的数据数量: {success_count}，发生错误的数据数量: {error_count}")
