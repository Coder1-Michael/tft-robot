# 配置文件

# 屏幕捕获参数
SCREENSHOT_REGION = (0, 0, 1920, 1080)  # (left, top, width, height)
CAPTURE_INTERVAL = 0.5  # 捕获间隔(秒)

# 图像识别参数
MODEL_PATH = "./models/pretrained_model"
CONFIDENCE_THRESHOLD = 0.7
RECOGNITION_TIMEOUT = 5  # 识别超时时间(秒)

# 游戏参数
GAME_REGION = (200, 100, 1520, 880)  # 游戏区域
CARD_SELECT_REGION = (500, 300, 920, 480)  # 卡牌选择区域
ITEM_SELECT_REGION = (1000, 600, 420, 280)  # 物品选择区域

# 操作参数
ACTION_DELAY = 0.2  # 操作延迟(秒)
KEYBOARD_DELAY = 0.1  # 键盘操作延迟(秒)
MOUSE_DELAY = 0.2  # 鼠标操作延迟(秒)

# 日志参数
LOG_LEVEL = "INFO"
LOG_FILE = "./logs/log"

# 模型参数
USE_GPU = True
MAX_TOKENS = 512
TEMPERATURE = 0.7

# 游戏策略参数
PRIORITY_CHAMPIONS = ["金克丝", "蔚", "凯特琳", "维克兹", "卡西奥佩娅"]
PRIORITY_ITEMS = ["无尽之刃", "饮血剑", "狂徒铠甲", "鬼索的狂暴之刃", "朔极之矛"]

DIFY_API_KEY="app-NIyayh1g0hFaW7IvcB0ieNFZ"
DIFY_API_ENDPOINT="http://localhost/v1"