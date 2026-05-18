"""The Tuya BLE valve platform."""
from __future__ import annotations

from dataclasses import dataclass

import logging
from typing import Any, Callable

from homeassistant.components.valve import (
    ValveDeviceClass,
    ValveEntity,
    ValveEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .devices import TuyaBLEData, TuyaBLEEntity, TuyaBLEProductInfo
from .tuya_ble import TuyaBLEDataPointType, TuyaBLEDevice

_LOGGER = logging.getLogger(__name__)


TuyaBLEValveIsAvailable = Callable[["TuyaBLEValve", TuyaBLEProductInfo], bool] | None


@dataclass
class TuyaBLEValveMapping:
    dp_id: int
    description: ValveEntityDescription
    force_add: bool = True
    dp_type: TuyaBLEDataPointType | None = None
    is_available: TuyaBLEValveIsAvailable = None


@dataclass
class TuyaBLECategoryValveMapping:
    products: dict[str, list[TuyaBLEValveMapping]] | None = None
    mapping: list[TuyaBLEValveMapping] | None = None


mapping: dict[str, TuyaBLECategoryValveMapping] = {
    "sfkzq": TuyaBLECategoryValveMapping(
        products={
            "1fcnd8xk": [  # Valve Controller
                TuyaBLEValveMapping(
                    dp_id=1,
                    description=ValveEntityDescription(
                        key="valve",
                        device_class=ValveDeviceClass.WATER,
                    ),
                ),
            ],
        },
    ),
}


def get_mapping_by_device(device: TuyaBLEDevice) -> list[TuyaBLEValveMapping]:
    category = mapping.get(device.category)
    if category is not None and category.products is not None:
        product_mapping = category.products.get(device.product_id)
        if product_mapping is not None:
            return product_mapping
        if category.mapping is not None:
            return category.mapping
    return []


class TuyaBLEValve(TuyaBLEEntity, ValveEntity):
    """Representation of a Tuya BLE valve."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: DataUpdateCoordinator,
        device: TuyaBLEDevice,
        product: TuyaBLEProductInfo,
        mapping: TuyaBLEValveMapping,
    ) -> None:
        super().__init__(hass, coordinator, device, product, mapping.description)
        self._mapping = mapping
        self.entity_id = generate_entity_id(
            "valve.{}", self._attr_unique_id, hass=hass
        )

    @property
    def reports_position(self) -> bool:
        """Return if the valve reports its position."""
        return False

    @property
    def is_closed(self) -> bool | None:
        """Return if the valve is closed."""
        datapoint = self._device.datapoints[self._mapping.dp_id]
        if datapoint:
            return not bool(datapoint.value)
        return None

    def open_valve(self, **kwargs: Any) -> None:
        """Open the valve."""
        datapoint = self._device.datapoints.get_or_create(
            self._mapping.dp_id,
            TuyaBLEDataPointType.DT_BOOL,
            True,
        )
        if datapoint:
            self._hass.create_task(datapoint.set_value(True))

    def close_valve(self, **kwargs: Any) -> None:
        """Close the valve."""
        datapoint = self._device.datapoints.get_or_create(
            self._mapping.dp_id,
            TuyaBLEDataPointType.DT_BOOL,
            False,
        )
        if datapoint:
            self._hass.create_task(datapoint.set_value(False))

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        result = super().available
        if result and self._mapping.is_available:
            result = self._mapping.is_available(self, self._product)
        return result


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Tuya BLE valves."""
    data: TuyaBLEData = hass.data[DOMAIN][entry.entry_id]
    mappings = get_mapping_by_device(data.device)
    entities: list[TuyaBLEValve] = []
    for mapping in mappings:
        if mapping.force_add or data.device.datapoints.has_id(
            mapping.dp_id, mapping.dp_type
        ):
            entities.append(
                TuyaBLEValve(
                    hass,
                    data.coordinator,
                    data.device,
                    data.product,
                    mapping,
                )
            )
    async_add_entities(entities)
