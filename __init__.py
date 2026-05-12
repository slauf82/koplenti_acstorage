import logging
import asyncio
from datetime import timedelta
from collections import deque
from datetime import datetime

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import *

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    host = entry.data[CONF_HOST]
    password = entry.data[CONF_PASSWORD]
    service_code = entry.data.get(CONF_SERVICE_CODE)

    last_octet = host.split(".")[-1]

    log_buffer = deque(maxlen=MAX_LOG_ENTRIES)

    command_lock = asyncio.Lock()

    def log_event(level, message):

        ts = datetime.now().strftime("%H:%M:%S")

        line = f"{ts} [{level.upper()}] {message}"

        log_buffer.append(line)

        if level == "error":
            _LOGGER.error(f"[{last_octet}] {message}")
        elif level == "warning":
            _LOGGER.warning(f"[{last_octet}] {message}")
        else:
            _LOGGER.info(f"[{last_octet}] {message}")

    async def run_cli(cmd):

        async with command_lock:

            log_event("debug", f"CLI START: {cmd}")

            try:

                process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=CLI_TIMEOUT
                )

                stdout = stdout.decode(errors="ignore").strip()
                stderr = stderr.decode(errors="ignore").strip()

                if stderr:
                    log_event("error", stderr)

                return stdout

            except asyncio.TimeoutError:

                log_event("error", "CLI Timeout")

                return ""

            except Exception as e:

                log_event("error", f"CLI Fehler: {e}")

                return ""

    async def read_acstorage():

        cmd = (
            f"pykoplenti --host {host} "
            f"--password={password} "
            f"--service-code={service_code} "
            f"read-settings devices:local/EnergyMgmt:AcStorage"
        )

        output = await run_cli(cmd)

        state = False

        for line in output.splitlines():

            if "AcStorage" in line and "=" in line:

                parts = line.split("=", 1)

                if len(parts) == 2:

                    state = parts[1].strip() in ["1", "true", "True"]

        log_event("info", f"Polling Status: {state}")

        return state

    async def async_update_data():

        try:

            active = await read_acstorage()

            return {"Active": active}

        except Exception as e:

            log_event("error", f"Polling Fehler: {e}")

            raise UpdateFailed(e)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"koplenti_acstorage_{last_octet}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN][entry.entry_id] = {

        "coordinator": coordinator,
        "log_event": log_event,
        "log_buffer": log_buffer,
        "run_cli": run_cli,

        "host": host,
        "password": password,
        "service_code": service_code,
        "last_octet": last_octet,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok