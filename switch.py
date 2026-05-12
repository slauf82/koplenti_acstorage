import asyncio

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    data = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([

        KoplentiSwitch(
            data,
            entry
        )

    ], True)


class KoplentiSwitch(SwitchEntity):

    def __init__(self, data, entry):

        self.data = data
        self.entry = entry

        self.coordinator = data["coordinator"]
        self.log_event = data["log_event"]
        self.run_cli = data["run_cli"]

        self.host = data["host"]
        self.password = data["password"]
        self.service_code = data["service_code"]

        last_octet = data["last_octet"]

        self._attr_name = f"Koplenti ACStorage ({last_octet})"
        self._attr_unique_id = f"{DOMAIN}_switch_{last_octet}"

        self._attr_is_on = False

        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_update(self):

        data = self.coordinator.data or {}

        self._attr_is_on = data.get("Active", False)

    async def async_turn_on(self):

        await self._set_state(True)

    async def async_turn_off(self):

        await self._set_state(False)

    async def _set_state(self, new_state):

        value = "1" if new_state else "0"

        cmd = (
            f"pykoplenti --host {self.host} "
            f"--password={self.password} "
            f"--service-code={self.service_code} "
            f"write-settings devices:local/EnergyMgmt:AcStorage={value}"
        )

        self.log_event("info", f"UI set {new_state}")

        self._attr_is_on = new_state

        self.async_write_ha_state()

        await self.run_cli(cmd)

        await asyncio.sleep(10)

        await self._verify()

    async def _verify(self):

        cmd = (
            f"pykoplenti --host {self.host} "
            f"--password={self.password} "
            f"--service-code={self.service_code} "
            f"read-settings devices:local/EnergyMgmt:AcStorage"
        )

        for attempt in range(3):

            output = await self.run_cli(cmd)

            for line in output.splitlines():

                if "AcStorage" in line and "=" in line:

                    parts = line.split("=", 1)

                    if len(parts) == 2:

                        state = parts[1].strip() in ["1", "true", "True"]

                        self._attr_is_on = state

                        self.coordinator.data = {"Active": state}

                        self.async_write_ha_state()

                        self.log_event("info", f"Verify OK: {state}")

                        return

            self.log_event("warning", f"Verify retry {attempt+1}")

            await asyncio.sleep(5)