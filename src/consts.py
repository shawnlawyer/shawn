
# Constants

HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

IIS_7_SERVER_HEADER = "Microsoft-IIS/7.0"
NGINX_11_X_SERVER_HEADER = "nginx/1.2"

SERVER_HEADERS = [
    IIS_7_SERVER_HEADER,
    NGINX_11_X_SERVER_HEADER
]

INDEX_OF = "Index of /"
INDEX_OF_TRUE = "Found"
INDEX_OF_FALSE = "Not Found"

IP_ADDRESS_PATTERN = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
IP_ADDRESS_CIDR_PATTERN = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$"
IP_ADDRESS_URL = "http://{}/"
INTERNET_CONNECTION_ERROR = "Internet Connection Unavailable."
RESULT_HEADER_COLUMNS = ["IP Address", "Status", "Hostname", "Server"]

INPUT_ERROR = "Input Error: '{}' is not a valid ip address"
OUTPUT_COLUMN_FORMAT = " {:<16s} {} {} {}"

OPTION_TARGETS_HELP = "Comma seperated list of IP addresses with optional CIDR rules."

LINE = str('-' * 80)

MAX_THREADS_COUNT = 10000
