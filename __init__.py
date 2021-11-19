"""Ring entrypoint skill
"""
from datetime import datetime
from mycroft import intent_handler
from mycroft.skills.common_play_skill import CommonPlaySkill
from .utils import authenticate, discovery
from .constants import DING_INTERVAL, DING_AUDIO_INTERVAL, AUDIO_MIME_TYPE
from os.path import join, dirname
from time import sleep


class Ring(CommonPlaySkill):
    """This is the place where all the magic happens for the Ring skill.
    """
    def __init__(self):
        """Constructor method
        """
        CommonPlaySkill.__init__(self)

        # Initialize variables with empty or None values
        self.ring = None
        self.devices = []

    def _setup(self):
        """Provision initialized variables and retrieve configuration
        from home.mycroft.ai.
        """
        self.username = self.settings.get('username')
        self.password = self.settings.get('password')
        self.two_factor_status = self.settings.get('2fa_enabled')
        self.two_factor_code = self.settings.get('2fa_code')
        self.ding_sound = self.settings.get('ding_sound', 'doorbell_1.mp3')

    @intent_handler('ring.discovery.intent')
    def _handle_device_discovery(self):
        """Handle the Ring devices discovery triggered by intents
        It's only used by the user to get the device names.
        """
        if self.devices:
            self.speak_dialog('ring.discovery', data={
                              'total': len(self.devices)})
            list_device = self.ask_yesno('ring.list')
            if list_device == 'yes':
                for device in self.devices:
                    self.speak(device.lower())

    def initialize(self):
        """The initialize method is called after the Skill is fully
        constructed and registered with the system. It is used to perform
        any final setup for the Skill including accessing Skill settings.
        https://tinyurl.com/4pevkdhj
        """
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()

    def on_settings_changed(self):
        """Each Mycroft device will check for updates to a users settings
        regularly, and write these to the Skills settings.json.
        https://tinyurl.com/f2bkymw
        """
        self._setup()
        self.ring = authenticate(self)
        discovery(self)

        # Because infinite loop will freeze the skill service, we  need
        # to schedule an event every DING_INTERVAL seconds.
        # https://bit.ly/3FCwFEd
        self.schedule_repeating_event(self._get_dings, datetime.now(),
                                      DING_INTERVAL)

    def _get_dings(self):
        """Checks for active alerts, if an alert is detected and the type is
        "ding" then a sound will be played as well as a speak dialog message.

        This method is only triggered by a scheduled event
        (cf. on_settings_changed() method from above) and should NEVER be
        called directly.

        The method uses the CommonPlaySkill implementation to leveragethe
        audio backend system.
        https://bit.ly/2Z2f0G6

        :raises Exception: Raise Exception
        """
        if len(self.devices) > 0:
            ring = self.ring
            ding_sound = join(dirname(__file__), 'assets', self.ding_sound)

            ring.update_dings()
            if ring.active_alerts() != []:
                try:
                    for alert in ring.active_alerts():
                        if alert['kind'] == 'ding':
                            self.log.info("ding detected")
                            self.CPS_play((f'file://{ding_sound}',
                                           AUDIO_MIME_TYPE))
                            sleep(DING_AUDIO_INTERVAL)
                            self.speak_dialog('ring.ding')
                            return
                except Exception as err:
                    self.log.error(err)
                    return
            return

    def CPS_start(self):
        """Required by https://bit.ly/2Z2f0G6
        """
        pass

    def CPS_match_query_phrase(self):
        """Required by https://bit.ly/2Z2f0G6
        """
        pass


def create_skill():
    """Main function to register the skill
    """
    return Ring()
