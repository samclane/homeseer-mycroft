"""
    homeseer-mycroft: Skill for Mycroft allowing HomeSeer hub connectivity
    Copyright (C) 2018 Sawyer McLane

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from test.integrationtests.skills.skill_tester import SkillTest
from mock import MagicMock


class MockDevice():
    def __init__(self, location=None, location2=None, name=None):
        self.location = location or 'location'
        self.location2 = location2 or 'location2'
        self.name = name or 'name'
        self.ref = 1


class MockEvent():
    def __init__(self, location=None, location2=None, name=None):
        self.name = name or 'name'


status_json = {
    'Devices': [{'status': 'good'}]
}

def test_runner(skill, example, emitter, loader):

    s = [s for s in loader.skills if s and s.root_dir == skill][0]

    # Create a device list for the test
    s.device_list = [MockDevice(name='light')]
    # Create an event list for the test
    s.event_list = [MockEvent(name='party mode')]

    # mock out the homeseer object for the test
    s.hs = MagicMock()
    # Using the same status for all tests, however this can be set for
    # the individual test case
    s.hs.get_status.return_value = status_json
    return SkillTest(skill, example, emitter).run(loader)
