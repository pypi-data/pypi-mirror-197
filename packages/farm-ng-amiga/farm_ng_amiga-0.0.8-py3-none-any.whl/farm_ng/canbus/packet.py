# Copyright (c) farm-ng, inc.
#
# Licensed under the Amiga Development Kit License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/farm-ng/amiga-dev-kit/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
from enum import IntEnum
from struct import pack
from struct import unpack
from typing import Optional

from farm_ng.canbus import canbus_pb2
from farm_ng.core.stamp import timestamp_from_monotonic
from farm_ng.core.timestamp_pb2 import Timestamp

DASHBOARD_NODE_ID = 0xE
PENDANT_NODE_ID = 0xF
BRAIN_NODE_ID = 0x1F
SDK_NODE_ID = 0x2A


class AmigaControlState(IntEnum):
    """State of the Amiga vehicle control unit (VCU)"""

    STATE_BOOT = 0
    STATE_MANUAL_READY = 1
    STATE_MANUAL_ACTIVE = 2
    STATE_CC_ACTIVE = 3
    STATE_AUTO_READY = 4
    STATE_AUTO_ACTIVE = 5
    STATE_ESTOPPED = 6


class Packet:
    """Base class inherited by all CAN message data structures."""

    @classmethod
    def from_can_data(cls, data, stamp: float):
        """Unpack CAN data directly into CAN message data structure."""
        obj = cls()  # Does not call __init__
        obj.decode(data)
        obj.stamp_packet(stamp)
        return obj

    def stamp_packet(self, stamp: float):
        """Time most recent message was received."""
        self.stamp: Timestamp = timestamp_from_monotonic("canbus/packet", stamp)

    def fresh(self, thresh_s: float = 0.5):
        """Returns False if the most recent message is older than ``thresh_s`` in seconds."""
        return self.age() < thresh_s

    def age(self):
        """Age of the most recent message."""
        return time.monotonic() - self.stamp.stamp


def make_amiga_rpdo1_proto(
    state_req: AmigaControlState, cmd_speed: float, cmd_ang_rate: float
) -> canbus_pb2.RawCanbusMessage:
    """Creates a canbus_pb2.RawCanbusMessage, using the AmigaRpdo1 structure and formatting, that can be sent
    directly to the canbus service to be formatted and send on the CAN bus."""
    return canbus_pb2.RawCanbusMessage(
        id=AmigaRpdo1.cob_id + DASHBOARD_NODE_ID,
        data=AmigaRpdo1(state_req=state_req, cmd_speed=cmd_speed, cmd_ang_rate=cmd_ang_rate).encode(),
    )


class AmigaRpdo1(Packet):
    """State, speed, and angular rate command (request) sent to the Amiga vehicle control unit (VCU)"""

    cob_id = 0x200

    def __init__(
        self,
        state_req: AmigaControlState = AmigaControlState.STATE_ESTOPPED,
        cmd_speed: float = 0.0,
        cmd_ang_rate: float = 0.0,
    ):
        self.format = "<Bhh"
        self.state_req = state_req
        self.cmd_speed = cmd_speed
        self.cmd_ang_rate = cmd_ang_rate

        self.stamp_packet(time.monotonic())

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(self.format, self.state_req, int(self.cmd_speed * 1000.0), int(self.cmd_ang_rate * 1000.0))

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""
        (self.state_req, cmd_speed, cmd_ang_rate) = unpack(self.format, data)
        self.cmd_speed = cmd_speed / 1000.0
        self.cmd_ang_rate = cmd_ang_rate / 1000.0

    def __str__(self):
        return "AMIGA RPDO1 Request state {} Command speed {:0.3f} Command angular rate {:0.3f}".format(
            self.state_req, self.cmd_speed, self.cmd_ang_rate
        )


class AmigaTpdo1(Packet):
    """State, speed, and angular rate of the Amiga vehicle control unit (VCU)"""

    cob_id = 0x180

    def __init__(
        self,
        state: AmigaControlState = AmigaControlState.STATE_ESTOPPED,
        meas_speed: float = 0.0,
        meas_ang_rate: float = 0.0,
    ):
        self.format = "<Bhh"
        self.state = state
        self.meas_speed = meas_speed
        self.meas_ang_rate = meas_ang_rate

        self.stamp_packet(time.monotonic())

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(self.format, self.state, int(self.meas_speed * 1000.0), int(self.meas_ang_rate * 1000.0))

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""
        (self.state, meas_speed, meas_ang_rate) = unpack(self.format, data)
        self.meas_speed = meas_speed / 1000.0
        self.meas_ang_rate = meas_ang_rate / 1000.0

    def __str__(self):
        return "AMIGA TPDO1 Amiga state {} Measured speed {:0.3f} Measured angular rate {:0.3f} @ time {}".format(
            self.state, self.meas_speed, self.meas_ang_rate, self.stamp.stamp
        )


def parse_amiga_tpdo1_proto(message: canbus_pb2.RawCanbusMessage) -> Optional[AmigaTpdo1]:
    """Parses a canbus_pb2.RawCanbusMessage, IFF the message came from the dashboard and contains AmigaTpdo1
    structure, formatting, and cobid.

    Otherwise returns None.
    """
    if message.id != AmigaTpdo1.cob_id + DASHBOARD_NODE_ID:
        return None
    return AmigaTpdo1.from_can_data(message.data, stamp=message.stamp)


class MotorControllerStatus(IntEnum):
    PRE_OPERATIONAL = 0
    IDLE = 1
    POST_OPERATIONAL = 2
    RUN = 3
    FAULT = 4


class MotorState:
    """Values representing the state of the motor.

    Amalgamates values from multiple CAN packets.
    """

    def __init__(
        self,
        id: int = 0,
        status: MotorControllerStatus = MotorControllerStatus.FAULT,
        rpm: int = 0,
        voltage: float = 0.0,
        current: float = 0.0,
        temperature: int = 0,
        timestamp: float = time.monotonic(),
    ):
        self.id: int = id
        self.status: MotorControllerStatus = status
        self.rpm: int = rpm
        self.voltage: float = voltage
        self.current: float = current
        self.temperature: int = temperature
        self.timestamp: float = timestamp

    def to_proto(self) -> canbus_pb2.MotorState:
        """Returns the data contained by the class encoded as CAN message data."""
        proto = canbus_pb2.MotorState(
            id=self.id,
            status=self.status.value,
            rpm=self.rpm,
            voltage=self.voltage,
            current=self.current,
            temperature=self.temperature,
            stamp=self.timestamp,
        )
        return proto

    @classmethod
    def from_proto(cls, proto: canbus_pb2.MotorState):
        obj = cls()  # Does not call __init__
        obj.id = proto.id
        obj.status = MotorControllerStatus(proto.status)
        obj.rpm = proto.rpm
        obj.voltage = proto.voltage
        obj.current = proto.current
        obj.temperature = proto.temperature
        obj.timestamp = proto.stamp
        return obj

    def __str__(self):
        return "Motor state - id {:01X} status {} rpm {} voltage {} current {} temperature {} @ time {}".format(
            self.id, self.status.name, self.rpm, self.voltage, self.current, self.temperature, self.timestamp
        )
