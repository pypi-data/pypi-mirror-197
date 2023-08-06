#!/usr/bin/env python

from typing import Union

# TODO: what is a nice pythonic way of storing those?
#       also does some version:: namespace thing make sense?
PACKETFLAG7_CONTROL = 1
PACKETFLAG7_RESEND = 2
PACKETFLAG7_COMPRESSION = 4
PACKETFLAG7_CONNLESS = 8

class PrettyPrint():
    def __repr__(self):
        return "<class: '" + str(self.__class__.__name__) + "'>"
    def __str__(self):
        return "<class: '" + str(self.__class__.__name__) + "'>: " + str(self.__dict__)

class BaseMessage(PrettyPrint):
    def __init__(self, name):
        self.name = name

class CtrlMessage(BaseMessage):
    pass

class GameMessage(BaseMessage):
    pass

class SysMessage(BaseMessage):
    pass

class PacketFlags7(PrettyPrint):
    def __init__(self):
        self.control = False
        self.resend = False
        self.compression = False
        self.connless = False

class PacketFlags6(PrettyPrint):
    def __init__(self):
        self.token = False
        self.control = False
        self.resend = False
        self.compression = False
        self.connless = False

class Header(PrettyPrint):
    def __init__(self) -> None:
        self.flags: PacketFlags7 = PacketFlags7()
        self.size: int = 0
        self.ack: int = 0
        self.token: bytes = b'\xff\xff\xff\xff'
        self.num_chunks: int = 0

class TwPacket(PrettyPrint):
    def __init__(self) -> None:
        self.version: str = 'unknown'
        self.header: Header = Header()
        self.messages: list[Union[CtrlMessage, GameMessage, SysMessage]] = []

class PacketParser():
    # TODO: move this to another class?
    def parse_flags7(self, data: bytes) -> PacketFlags7:
        # FFFF FFaa
        flag_bits = (data[0] & 0xfc) >> 2
        flags = PacketFlags7()
        flags.control = (flag_bits & PACKETFLAG7_CONTROL) != 0
        flags.resend = (flag_bits & PACKETFLAG7_RESEND) != 0
        flags.compression = (flag_bits & PACKETFLAG7_COMPRESSION) != 0
        flags.connless = (flag_bits & PACKETFLAG7_CONNLESS) != 0
        return flags

    # TODO: move this to another class?
    def parse_ack(self, header_bytes: bytes) -> int:
        # ffAA AAAA AAAA
        return ((header_bytes[0] & 0x3) << 8) | header_bytes[1]

    # TODO: move this to another class?
    def parse_num_chunks(self, header_bytes: bytes) -> int:
        # TODO: not sure if this is correct
        return header_bytes[2]

    def parse_token(self, header_bytes: bytes) -> bytes:
        return header_bytes[3:7]

    # TODO: move this to another class?
    def parse_header(self, data: bytes) -> Header:
        header = Header()
        # bits 2..5
        header.flags = self.parse_flags7(data)
        # bits 6..16
        header.ack = self.parse_ack(data)
        # bits 17..25
        header.num_chunks = self.parse_num_chunks(data)
        # bits 16..57
        header.token = self.parse_token(data)
        return header

    def parse7(self, data: bytes) -> TwPacket:
        pck = TwPacket()
        pck.version = '0.7'
        pck.header = self.parse_header(data)
        if pck.header.flags.control:
            if data[7] == 0x04: # close
                msg_dc = CtrlMessage('close')
                pck.messages.append(msg_dc)
                return pck
        return pck

def parse(data: bytes) -> TwPacket:
    # TODO: think about api
    #       do we have `parse6` and `parse7` and `parse_detect`
    #       or just `parse` that does detect
    return PacketParser().parse7(data)
