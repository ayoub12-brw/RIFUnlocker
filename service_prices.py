# جدول الخدمات المتقدم (سعر، حالة، handler)
SERVICES = {
    'FRP Xiaomi':     {'price': 2, 'status': 'ON', 'handler': 'frp_xiaomi_handler'},
    'Samsung FRP':    {'price': 2, 'status': 'ON', 'handler': 'samsung_frp_handler'},
    'iCloud Check':   {'price': 1, 'status': 'ON', 'handler': 'icloud_check_handler'},
    'IMEI Info':      {'price': 1, 'status': 'ON', 'handler': 'imei_info_handler'},
    'MDM Status':     {'price': 1, 'status': 'ON', 'handler': 'mdm_status_handler'},
}

def get_service_price(service_name):
    s = SERVICES.get(service_name)
    return s['price'] if s else 1

def get_service_status(service_name):
    s = SERVICES.get(service_name)
    return s['status'] if s else 'OFF'

def get_service_handler(service_name):
    s = SERVICES.get(service_name)
    return s['handler'] if s else None
