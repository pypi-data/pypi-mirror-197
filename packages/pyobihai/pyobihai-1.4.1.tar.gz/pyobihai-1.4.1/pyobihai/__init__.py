"""PyOBihai interface."""

from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urljoin

import requests
from defusedxml.ElementTree import fromstring

from .const import (
    DEFAULT_CALL_STATUS_PATH,
    DEFAULT_LINE_PATH,
    DEFAULT_REBOOT_PATH,
    DEFAULT_STATUS_PATH,
    LOGGER,
)
from .parsing import parse_call_direction, parse_last_reboot, parse_status


class PyObihai:
    """Represents an Obihai"""

    def __init__(self, host: str, username: str, password: str):
        """Initialize connection."""

        self._username = username
        self._password = password
        if self._username == "user":
            host = host + "/user/"
        self._server = f"http://{host}"
        self._last_reboot = datetime.now(timezone.utc)

    def get_state(self) -> dict[str, Any]:
        """Get the state for services sensors, phone sensor and last reboot."""

        services: dict[str, Any] = {}
        resp = self._get_request(DEFAULT_STATUS_PATH)
        if isinstance(resp, requests.Response):
            root = fromstring(resp.text)
            for models in root.iter("model"):
                if "reboot_req" in models.attrib and models.attrib["reboot_req"]:
                    services["Reboot required"] = models.attrib["reboot_req"]
            for obj in root.findall("object"):
                name = obj.attrib.get("name", "")
                if "Service Status" in name:
                    status = parse_status(name, obj)
                    if isinstance(status, str):
                        services[
                            name.replace("Service Status", "service status")
                        ] = status
                if "Product Information" in name:
                    state = parse_last_reboot(obj)
                    if abs(self._last_reboot - state) > timedelta(seconds=5):
                        self._last_reboot = state
                    services["Last reboot"] = self._last_reboot

        return services

    def get_line_state(self) -> dict[str, Any]:
        """Get the state of the port connection and last caller info."""

        services = {}
        resp = self._get_request(DEFAULT_LINE_PATH)
        if isinstance(resp, requests.Response):
            root = fromstring(resp.text)
            for obj in root.findall("object"):
                name = obj.attrib.get("name", "")
                subtitle = obj.attrib.get("subtitle", "").replace("Port", "port")
                if "Port Status" in name:
                    for exc in obj.findall("./parameter[@name='State']/value"):
                        state = exc.attrib.get("current")
                        services[subtitle] = state
                    for val in obj.findall("./parameter[@name='LastCallerInfo']/value"):
                        state = val.attrib.get("current", "")
                        services[subtitle + " last caller info"] = state.replace(
                            "'", ""
                        ).strip()

        return services

    def get_device_mac(self) -> str:
        """Get the device mac address."""
        return self._get_status("WAN Status", "MACAddress")

    def get_model_name(self) -> str:
        """Get ModelName."""
        return self._get_status("Product Information", "ModelName")

    def get_hardware_version(self) -> str:
        """Get HardwareVersion."""
        return self._get_status("Product Information", "HardwareVersion")

    def get_software_version(self) -> str:
        """Get SoftwareVersion."""
        return self._get_status("Product Information", "SoftwareVersion")

    def get_device_serial(self) -> str:
        """Get Device Serial Number."""
        return self._get_status("Product Information", "SerialNumber")

    def _get_status(self, find_name: str, parameter: str) -> str:
        """Get and parse the device Product Information."""

        result = ""
        resp = self._get_request(DEFAULT_STATUS_PATH)
        if isinstance(resp, requests.Response):
            root = fromstring(resp.text)
            for obj in root.findall("object"):
                name = obj.attrib.get("name", "")
                if find_name in name:
                    for exc in obj.findall(f"./parameter[@name='{parameter}']/value"):
                        result = exc.attrib.get("current", "")

        return result

    def _get_request(self, api_url: str) -> requests.Response | bool:
        """Get a URL from the Obihai."""

        url = urljoin(self._server, api_url)
        try:
            response = requests.get(
                url,
                auth=requests.auth.HTTPDigestAuth(self._username, self._password),
                timeout=2,
            )
            if response.status_code == 200:
                return response
        except requests.RequestException as exc:
            LOGGER.error(exc)

        return False

    def get_call_direction(self) -> dict[str, str]:
        """Get the call direction."""

        call_direction = {"Call direction": "No Active Calls"}
        response = self._get_request(DEFAULT_CALL_STATUS_PATH)
        if isinstance(response, requests.Response):
            result = parse_call_direction(response.text)
            if isinstance(result, str):
                call_direction["Call direction"] = result

        return call_direction

    def check_account(self) -> bool:
        """Check account credentials."""

        response = self._get_request(DEFAULT_STATUS_PATH)

        if isinstance(response, requests.Response):
            return True

        LOGGER.error("Invalid credentials")
        return False

    def call_reboot(self) -> bool:
        """Send request to reboot."""

        response = self._get_request(DEFAULT_REBOOT_PATH)
        if isinstance(response, requests.Response):
            return True

        return False
