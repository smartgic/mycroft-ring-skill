"""Ring entrypoint skill
"""
from datetime import datetime
from mycroft import MycroftSkill, intent_handler
from mycroft.util import play_mp3
from .utils import authenticate, discovery
from .constants import ALERTS_INTERVAL
from os.path import join, dirname


class Ring(MycroftSkill):
    """This is the place where all the magic happens for the Ring skill.
    """
    def __init__(self):
        """Constructor method
        """
        MycroftSkill.__init__(self)

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
        self.ding_alerts = self.settings.get('enable_ding')
        self.motion_alerts = self.settings.get('enable_motion')
        self.on_demand = self.settings.get('enable_on_demand')

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
        self.schedule_repeating_event(self._get_alerts, datetime.now(),
                                      ALERTS_INTERVAL)

    def _get_alerts(self):
        """Checks for active alerts on the devices.

        If an alert is detected and the type is "ding" then a sound will be
        played as well as a speak dialog message.

        If an alert is detected and the type is "motion" then a speak dialog
        message will be played.

        If an alert is detected and the type is "on_demand" then a speak dialog
        message will be played.

        This method is only triggered by a scheduled event
        (cf. on_settings_changed() method from above) and should NEVER be
        called directly.

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
                            if self.ding_alerts:
                                self.log.info("ding alert detected")
                                play_mp3(ding_sound).wait()
                                self.speak_dialog('ring.ding', data={
                                    'device': alert['doorbot_description']})
                                return
                        elif alert['kind'] == 'motion':
                            if self.motion_alerts:
                                self.log.info("motion alert detected")
                                self.speak_dialog('ring.motion', data={
                                    'device': alert['doorbot_description']})
                                return
                        elif alert['kind'] == 'on_demand':
                            if self.on_demand:
                                self.log.info("on-demand alert detected")
                                self.speak_dialog('ring.on_demand', data={
                                    'device': alert['doorbot_description']})
                                return
                except Exception as err:
                    self.log.error(err)
                    return
            return


def create_skill():
    """Main function to register the skill
    """
    return Ring()
