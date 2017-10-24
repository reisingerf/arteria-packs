import mock
import json
from datetime import datetime

from st2tests.base import BaseSensorTestCase

from incoming_sensor import IncomingSensor

host_id = "54f798b2a525"
client_link = "http://runfolder_ws/api/1.0/runfolders/path/opt/monitored-folder/run3"
runfolder = "/opt/monitored-folder/run3"

client_response_dict = {
    "response" : {
        "path": runfolder,
        "host": host_id,
        "link": client_link,
        "state": "ready",
        "service_version": "1.0.1"
    },
    "requesturl" : "http://foo.com"
}

trigger_payload = {
  "timestamp": "1900-12-31T00:00:00",
  "destination": "",
  "host": host_id,
  "link": client_link,
  "runfolder": runfolder,
  "runfolder_name": "run3"
}


class IncomingSensorTestCase(BaseSensorTestCase):
    sensor_cls = IncomingSensor

    @mock.patch('runfolder_sensor.datetime')
    def test_poll(self, mock_dt):
        mock_dt.utcnow = mock.Mock(return_value=datetime(1900, 12, 31))

        sensor = self.get_sensor_instance()
        sensor._client = mock.Mock()
        sensor._client.next_ready.return_value = client_response_dict
        sensor._hostconfigs = []

        sensor.poll()
        self.assertEqual(len(self.get_dispatched_triggers()), 1)
        self.assertTriggerDispatched(trigger='arteria.incoming_ready',
                                     payload=trigger_payload)
