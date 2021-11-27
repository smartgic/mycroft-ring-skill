"""This file contains functions related to extra operations
and are called by the handle_* methods from __init__.py
"""
import json
from .constants import TOKEN_CACHE_DIR, TOKEN_CACHE_FILE, USER_AGENT
from pathlib import Path
from oauthlib.oauth2 import MissingTokenError
from ring_doorbell import Ring, Auth

# This is not in a function because it is used by token_cache_update()
# and authenticate() functions.
token_cache_file = Path(TOKEN_CACHE_FILE)


def _token_cache_update(token):
    """Handle the token_cache.json file creation which contains the token
    and the refresh token.

    The token_cache_file file is created after the first successful
    authentication fromusername and password (and 2FA if enabled). This file
    prevent to re-authenticate at every API call performed by the Python
    ring_doorbell library.

    :raises Exception: Raise Exception
    """
    try:
        token_cache_dir = Path(TOKEN_CACHE_DIR)
        token_cache_dir.mkdir(parents=True, exist_ok=True)
        token_cache_file.write_text(json.dumps(token))
    except Exception as err:
        return err


def authenticate(self):
    """This function authenticates a user to the Ring API using a username,
    password.

    The Two-Factor Authentication (2FA) is supported as well and needs to be
    enabled on account.mycroft.ai as well as the One-Time Password (OTP).

    :raises MissingTokenError: Raise MissingTokenError
    """
    if token_cache_file.is_file():
        # Try to refresh the token if token_cache_file exists and is JSON
        # valid.
        token = json.loads(token_cache_file.read_text())
        try:
            auth = Auth(USER_AGENT, token, _token_cache_update)
            self.log.info('token refreshed')
            return Ring(auth)
        except MissingTokenError as err:
            self.log.error(err)
    else:
        # Authenticate to the Ring API using username and password.
        if self.username and self.password:
            try:
                auth = Auth(USER_AGENT, None, _token_cache_update)
                if not self.two_factor_status:
                    try:
                        auth.fetch_token(self.username, self.password)
                        self.log.info('token created')
                        return Ring(auth)
                    except MissingTokenError as err:
                        self.log.error(err)
                else:
                    # Authenticate with username, password and OTP if 2FA is
                    # enable and OTP is provided.
                    if self.two_factor_status and self.two_factor_code:
                        try:
                            auth.fetch_token(self.username, self.password,
                                             self.two_factor_code)
                            self.log.info('2FA token created')
                            return Ring(auth)
                        except MissingTokenError as err:
                            self.log.error(err)
            except MissingTokenError as err:
                self.log.error(err)


def discovery(self):
    """Discover Ring devices registered on the local network and
    add them to a list once the authentication has been successful.

    The discover handles all type of devices supported by the Python
    ring_doorbell library.

    :raises Exception: Raise Exception
    """
    if token_cache_file.is_file():
        ring = self.ring
        ring.update_data()

        devices = ring.devices()
        doorbells = devices['doorbots']
        chimes = devices["chimes"]
        stickup_cams = devices["stickup_cams"]

        # Make sure the device dict is emtpty before the discovery.
        self.devices = {}

        try:
            for device in doorbells + chimes + stickup_cams:
                self.devices[device.name] = device.family
        except Exception as err:
            self.log.error(err)

        if not self.devices:
            self.log.warning('unable to find ring devices')
            self.speak_dialog('error.discovery')
        else:
            self.log.info(
                '{} device(s) found'.format(len(self.devices)))


def check_device(self, ring_device):
    """Check if the device is part of the discovered devices.

    :param device: Which device to looking for
    :type device: string
    :return: Device name
    :rtype: str
    :raises Exception: Raise Exception
    """
    try:
        for device in self.devices:
            if ring_device in self.devices:
                return device
    except Exception as err:
        self.log.error(err)

    self.log.warning('{} device not found'.format(ring_device))
    self.speak_dialog('error.device', data={'device': ring_device})

    return None


def device_info(self, device):
    """Retrieve Ring device information

    :param device: Which device to retrieve information
    :type speaker: string
    :raises Exception: Raise Exception
    """
    try:
        device = check_device(self, device)
        if not device:
            return None
        ring = self.ring
        ring.update_devices()
        devices = ring.devices()
        for info in devices[self.devices[device]]:
            if device == info.name:
                self.speak_dialog('ring.device.info', data={
                                  'model': info.name,
                                  'kind': info.model_number,
                                  'firmware': info.kind.replace('_', ' '),
                                  'battery': info.battery_life})
    except Exception as err:
        self.log.error(err)
