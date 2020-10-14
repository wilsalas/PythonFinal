FOLDER = "src/lib"
FILE = FOLDER + "/users.json"
FILE_TRANSACTION = FOLDER + "/transactions.json"
API = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
APIKEY = "ad513bbe-0abd-426a-b761-091d97811ecb"
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY':  APIKEY
}


def PSPrint(message, posColor=4):
    ENDC = '\33[0m'
    TERMINAL_COLOR_TYPE = (
        ("SUCCESS", '\33[92m'),
        ("WARNING", '\33[93m'),
        ("INFO", '\33[94m'),
        ("DANGER", '\33[91m')
    )
    color = ENDC
    if isinstance(posColor, int) and posColor <= 3:
        color = TERMINAL_COLOR_TYPE[posColor][1]
    print(f'\n {color} {message} {ENDC} \n')
