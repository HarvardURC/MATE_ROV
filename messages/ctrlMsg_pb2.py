# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ctrlMsg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ctrlMsg.proto',
  package='mateROV',
  syntax='proto2',
  serialized_pb=_b('\n\rctrlMsg.proto\x12\x07mateROV\"t\n\x07\x43trlMsg\x12\t\n\x01x\x18\x01 \x02(\x02\x12\t\n\x01y\x18\x02 \x02(\x02\x12\t\n\x01z\x18\x03 \x02(\x02\x12\x0c\n\x04roll\x18\x04 \x02(\x02\x12\r\n\x05pitch\x18\x05 \x02(\x02\x12\x0b\n\x03yaw\x18\x06 \x02(\x02\x12\x0e\n\x06servoX\x18\x07 \x02(\x05\x12\x0e\n\x06servoY\x18\x08 \x02(\x05')
)




_CTRLMSG = _descriptor.Descriptor(
  name='CtrlMsg',
  full_name='mateROV.CtrlMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='mateROV.CtrlMsg.x', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='mateROV.CtrlMsg.y', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='mateROV.CtrlMsg.z', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='roll', full_name='mateROV.CtrlMsg.roll', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pitch', full_name='mateROV.CtrlMsg.pitch', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='yaw', full_name='mateROV.CtrlMsg.yaw', index=5,
      number=6, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='servoX', full_name='mateROV.CtrlMsg.servoX', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='servoY', full_name='mateROV.CtrlMsg.servoY', index=7,
      number=8, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=142,
)

DESCRIPTOR.message_types_by_name['CtrlMsg'] = _CTRLMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CtrlMsg = _reflection.GeneratedProtocolMessageType('CtrlMsg', (_message.Message,), dict(
  DESCRIPTOR = _CTRLMSG,
  __module__ = 'ctrlMsg_pb2'
  # @@protoc_insertion_point(class_scope:mateROV.CtrlMsg)
  ))
_sym_db.RegisterMessage(CtrlMsg)


# @@protoc_insertion_point(module_scope)
