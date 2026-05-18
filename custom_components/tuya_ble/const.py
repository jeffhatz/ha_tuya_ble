"""The Tuya BLE integration."""
from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Final

DOMAIN: Final = "tuya_ble"
TUYA_DOMAIN: Final = "tuya"

DEVICE_METADATA_UUIDS: Final = "uuids"

DEVICE_DEF_MANUFACTURER: Final = "Tuya"
SET_DISCONNECTED_DELAY = 10 * 60

CONF_UUID: Final = "uuid"
CONF_LOCAL_KEY: Final = "local_key"
CONF_ENDPOINT: Final = "endpoint"
CONF_ACCESS_ID: Final = "access_id"
CONF_ACCESS_SECRET: Final = "access_secret"
CONF_AUTH_TYPE: Final = "auth_type"
CONF_USERNAME: Final = "username"
CONF_PASSWORD: Final = "password"
CONF_COUNTRY_CODE: Final = "country_code"
CONF_APP_TYPE: Final = "app_type"
CONF_CATEGORY: Final = "category"
CONF_PRODUCT_ID: Final = "product_id"
CONF_DEVICE_NAME: Final = "device_name"
CONF_PRODUCT_MODEL: Final = "product_model"
CONF_PRODUCT_NAME: Final = "product_name"

TUYA_RESPONSE_CODE: Final = "code"
TUYA_RESPONSE_MSG: Final = "msg"
TUYA_RESPONSE_RESULT: Final = "result"
TUYA_RESPONSE_SUCCESS: Final = "success"

TUYA_SMART_APP: Final = "tuyaSmart"
SMARTLIFE_APP: Final = "smartlife"

TUYA_API_DEVICES_URL: Final = "/v1.0/users/%s/devices"
TUYA_API_FACTORY_INFO_URL: Final = "/v1.0/iot-03/devices/factory-infos?device_ids=%s"
TUYA_FACTORY_INFO_MAC: Final = "mac"


@dataclass(frozen=True)
class TuyaCountry:
    name: str
    country_code: str
    endpoint: str


TUYA_ENDPOINT_CHINA: Final = "https://openapi.tuyacn.com"
TUYA_ENDPOINT_AMERICA: Final = "https://openapi.tuyaus.com"
TUYA_ENDPOINT_EUROPE: Final = "https://openapi.tuyaeu.com"
TUYA_ENDPOINT_INDIA: Final = "https://openapi.tuyain.com"

TUYA_COUNTRIES: Final = [
    TuyaCountry("China", "86", TUYA_ENDPOINT_CHINA),
    TuyaCountry("France", "33", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("Germany", "49", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("India", "91", TUYA_ENDPOINT_INDIA),
    TuyaCountry("Italy", "39", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("Netherlands", "31", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("Spain", "34", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("United Kingdom", "44", TUYA_ENDPOINT_EUROPE),
    TuyaCountry("United States", "1", TUYA_ENDPOINT_AMERICA),
]

BATTERY_STATE_LOW: Final = "low"
BATTERY_STATE_NORMAL: Final = "normal"
BATTERY_STATE_HIGH: Final = "high"

BATTERY_NOT_CHARGING: Final = "not_charging"
BATTERY_CHARGING: Final = "charging"
BATTERY_CHARGED: Final = "charged"

CO2_LEVEL_NORMAL: Final = "normal"
CO2_LEVEL_ALARM: Final = "alarm"

FINGERBOT_MODE_PUSH: Final = "push"
FINGERBOT_MODE_SWITCH: Final = "switch"
FINGERBOT_MODE_PROGRAM: Final = "program"
FINGERBOT_BUTTON_EVENT: Final = "fingerbot_button_pressed"
