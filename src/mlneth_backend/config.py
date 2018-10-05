import os

WORK_DIR = os.path.dirname(__file__) + '/'

# DB
DB_PATH = 'db.db'
MAX_QUERRY_SIZE = 1000

DOWNLOAD_FOLDER = "banners/orig/"
BANNERS_FOLDER = "banners/"
BIG_PICTURE_LOCAL_PATH = "big_pics/"
BIG_PICTURE_BG = "utils/0.png"

NO_IMG_IMG = WORK_DIR + "10x10-no-img-img.jpg"

IMAGE_FORMATS = ("jpeg", "jpg", "png")

# RPC_ADDRESS = {"host": '127.0.0.1', "port": 8545, "tls": False}  # local geth client
RPC_ADDRESS = {"host": 'mainnet.infura.io/5GyJwkluzWFwhA7RI9XY', "port": 443, "tls": True}  # infura
ETHERSCAN_KEY = "FE4E99ZU8XU9ENPCUMK1JT8VQZ8UK5BD5K"
BLOCKCHAIN_REQUEST_PERIOD = 60  # seconds



# ERROR HANDLING
WRONG_HREF_SUBSTITUTE = "/wrong_href"

# DEBUG
IMGUR_ENABLED = True
APP_ENGINE_ENABLED = True
# DATA_BASE_ENABLED = False
# IMG_EVENTS_CSV = "events/dummies/bw_images_10000.csv"
# IMG_EVENTS_CSV = "events/dummies/color_images_10000.csv"
IMG_EVENTS_CSV = WORK_DIR + "events/dummies/imgur_test.csv"

# ADMIN
CSV_SEPARATOR = ","
