# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: uac/Team.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ..uac import UACService_pb2 as uac_dot_UACService__pb2
from ..common import CommonService_pb2 as common_dot_CommonService__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='uac/Team.proto',
  package='ai.verta.uac',
  syntax='proto3',
  serialized_options=b'P\001Z:github.com/VertaAI/modeldb/protos/gen/go/protos/public/uac',
  serialized_pb=b'\n\x0euac/Team.proto\x12\x0c\x61i.verta.uac\x1a\x1cgoogle/api/annotations.proto\x1a\x14uac/UACService.proto\x1a\x1a\x63ommon/CommonService.proto\"\xf5\x01\n\x04Team\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06org_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x12\n\nshort_name\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x10\n\x08owner_id\x18\x05 \x01(\t\x12R\n\x13id_service_provider\x18\t \x01(\x0e\x32\x35.ai.verta.uac.IdServiceProviderEnum.IdServiceProvider\x12\x19\n\x11\x63reated_timestamp\x18\x06 \x01(\x03\x12\x19\n\x11updated_timestamp\x18\x07 \x01(\x03\"L\n\x0bGetTeamById\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x1a,\n\x08Response\x12 \n\x04team\x18\x01 \x01(\x0b\x32\x12.ai.verta.uac.Team\"`\n\rGetTeamByName\x12\x0e\n\x06org_id\x18\x01 \x01(\t\x12\x11\n\tteam_name\x18\x02 \x01(\t\x1a,\n\x08Response\x12 \n\x04team\x18\x01 \x01(\x0b\x32\x12.ai.verta.uac.Team\"f\n\x12GetTeamByShortName\x12\x0e\n\x06org_id\x18\x01 \x01(\t\x12\x12\n\nshort_name\x18\x02 \x01(\t\x1a,\n\x08Response\x12 \n\x04team\x18\x01 \x01(\x0b\x32\x12.ai.verta.uac.Team\"\x84\x01\n\x0bListMyTeams\x12/\n\npagination\x18\x01 \x01(\x0b\x32\x1b.ai.verta.common.Pagination\x1a\x44\n\x08Response\x12!\n\x05teams\x18\x01 \x03(\x0b\x32\x12.ai.verta.uac.Team\x12\x15\n\rtotal_records\x18\x02 \x01(\x03\"Y\n\x07SetTeam\x12 \n\x04team\x18\x01 \x01(\x0b\x32\x12.ai.verta.uac.Team\x1a,\n\x08Response\x12 \n\x04team\x18\x01 \x01(\x0b\x32\x12.ai.verta.uac.Team\"9\n\nDeleteTeam\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x1a\x1a\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x08\"\x85\x01\n\x0cListTeamUser\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x12/\n\npagination\x18\x02 \x01(\x0b\x32\x1b.ai.verta.common.Pagination\x1a\x33\n\x08Response\x12\x10\n\x08user_ids\x18\x01 \x03(\t\x12\x15\n\rtotal_records\x18\x02 \x01(\x03\"N\n\x0b\x41\x64\x64TeamUser\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x12\x12\n\nshare_with\x18\x03 \x01(\t\x1a\x1a\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x08\"Q\n\x0eRemoveTeamUser\x12\x0f\n\x07team_id\x18\x01 \x01(\t\x12\x12\n\nshare_with\x18\x02 \x01(\t\x1a\x1a\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\x08\x32\xf0\x07\n\x0bTeamService\x12j\n\x0bgetTeamById\x12\x19.ai.verta.uac.GetTeamById\x1a\".ai.verta.uac.GetTeamById.Response\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/team/getTeamById\x12r\n\rgetTeamByName\x12\x1b.ai.verta.uac.GetTeamByName\x1a$.ai.verta.uac.GetTeamByName.Response\"\x1e\x82\xd3\xe4\x93\x02\x18\x12\x16/v1/team/getTeamByName\x12\x86\x01\n\x12getTeamByShortName\x12 .ai.verta.uac.GetTeamByShortName\x1a).ai.verta.uac.GetTeamByShortName.Response\"#\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1/team/getTeamByShortName\x12j\n\x0blistMyTeams\x12\x19.ai.verta.uac.ListMyTeams\x1a\".ai.verta.uac.ListMyTeams.Response\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/team/listMyTeams\x12]\n\x07setTeam\x12\x15.ai.verta.uac.SetTeam\x1a\x1e.ai.verta.uac.SetTeam.Response\"\x1b\x82\xd3\xe4\x93\x02\x15\"\x10/v1/team/setTeam:\x01*\x12i\n\ndeleteTeam\x12\x18.ai.verta.uac.DeleteTeam\x1a!.ai.verta.uac.DeleteTeam.Response\"\x1e\x82\xd3\xe4\x93\x02\x18\"\x13/v1/team/deleteTeam:\x01*\x12h\n\tlistUsers\x12\x1a.ai.verta.uac.ListTeamUser\x1a#.ai.verta.uac.ListTeamUser.Response\"\x1a\x82\xd3\xe4\x93\x02\x14\x12\x12/v1/team/listUsers\x12\x65\n\x07\x61\x64\x64User\x12\x19.ai.verta.uac.AddTeamUser\x1a\".ai.verta.uac.AddTeamUser.Response\"\x1b\x82\xd3\xe4\x93\x02\x15\"\x10/v1/team/addUser:\x01*\x12q\n\nremoveUser\x12\x1c.ai.verta.uac.RemoveTeamUser\x1a%.ai.verta.uac.RemoveTeamUser.Response\"\x1e\x82\xd3\xe4\x93\x02\x18\"\x13/v1/team/removeUser:\x01*B>P\x01Z:github.com/VertaAI/modeldb/protos/gen/go/protos/public/uacb\x06proto3'
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,uac_dot_UACService__pb2.DESCRIPTOR,common_dot_CommonService__pb2.DESCRIPTOR,])




_TEAM = _descriptor.Descriptor(
  name='Team',
  full_name='ai.verta.uac.Team',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ai.verta.uac.Team.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='org_id', full_name='ai.verta.uac.Team.org_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='ai.verta.uac.Team.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name', full_name='ai.verta.uac.Team.short_name', index=3,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='ai.verta.uac.Team.description', index=4,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='ai.verta.uac.Team.owner_id', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id_service_provider', full_name='ai.verta.uac.Team.id_service_provider', index=6,
      number=9, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_timestamp', full_name='ai.verta.uac.Team.created_timestamp', index=7,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='updated_timestamp', full_name='ai.verta.uac.Team.updated_timestamp', index=8,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=358,
)


_GETTEAMBYID_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.GetTeamById.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='ai.verta.uac.GetTeamById.Response.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=436,
)

_GETTEAMBYID = _descriptor.Descriptor(
  name='GetTeamById',
  full_name='ai.verta.uac.GetTeamById',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_id', full_name='ai.verta.uac.GetTeamById.team_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETTEAMBYID_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=360,
  serialized_end=436,
)


_GETTEAMBYNAME_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.GetTeamByName.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='ai.verta.uac.GetTeamByName.Response.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=436,
)

_GETTEAMBYNAME = _descriptor.Descriptor(
  name='GetTeamByName',
  full_name='ai.verta.uac.GetTeamByName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='org_id', full_name='ai.verta.uac.GetTeamByName.org_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='team_name', full_name='ai.verta.uac.GetTeamByName.team_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETTEAMBYNAME_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=438,
  serialized_end=534,
)


_GETTEAMBYSHORTNAME_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.GetTeamByShortName.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='ai.verta.uac.GetTeamByShortName.Response.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=436,
)

_GETTEAMBYSHORTNAME = _descriptor.Descriptor(
  name='GetTeamByShortName',
  full_name='ai.verta.uac.GetTeamByShortName',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='org_id', full_name='ai.verta.uac.GetTeamByShortName.org_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='short_name', full_name='ai.verta.uac.GetTeamByShortName.short_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETTEAMBYSHORTNAME_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=536,
  serialized_end=638,
)


_LISTMYTEAMS_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.ListMyTeams.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='teams', full_name='ai.verta.uac.ListMyTeams.Response.teams', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_records', full_name='ai.verta.uac.ListMyTeams.Response.total_records', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=705,
  serialized_end=773,
)

_LISTMYTEAMS = _descriptor.Descriptor(
  name='ListMyTeams',
  full_name='ai.verta.uac.ListMyTeams',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pagination', full_name='ai.verta.uac.ListMyTeams.pagination', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LISTMYTEAMS_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=641,
  serialized_end=773,
)


_SETTEAM_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.SetTeam.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='ai.verta.uac.SetTeam.Response.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=392,
  serialized_end=436,
)

_SETTEAM = _descriptor.Descriptor(
  name='SetTeam',
  full_name='ai.verta.uac.SetTeam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team', full_name='ai.verta.uac.SetTeam.team', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_SETTEAM_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=775,
  serialized_end=864,
)


_DELETETEAM_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.DeleteTeam.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ai.verta.uac.DeleteTeam.Response.status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=897,
  serialized_end=923,
)

_DELETETEAM = _descriptor.Descriptor(
  name='DeleteTeam',
  full_name='ai.verta.uac.DeleteTeam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_id', full_name='ai.verta.uac.DeleteTeam.team_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_DELETETEAM_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=866,
  serialized_end=923,
)


_LISTTEAMUSER_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.ListTeamUser.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_ids', full_name='ai.verta.uac.ListTeamUser.Response.user_ids', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_records', full_name='ai.verta.uac.ListTeamUser.Response.total_records', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1008,
  serialized_end=1059,
)

_LISTTEAMUSER = _descriptor.Descriptor(
  name='ListTeamUser',
  full_name='ai.verta.uac.ListTeamUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_id', full_name='ai.verta.uac.ListTeamUser.team_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pagination', full_name='ai.verta.uac.ListTeamUser.pagination', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_LISTTEAMUSER_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=926,
  serialized_end=1059,
)


_ADDTEAMUSER_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.AddTeamUser.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ai.verta.uac.AddTeamUser.Response.status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=897,
  serialized_end=923,
)

_ADDTEAMUSER = _descriptor.Descriptor(
  name='AddTeamUser',
  full_name='ai.verta.uac.AddTeamUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_id', full_name='ai.verta.uac.AddTeamUser.team_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='share_with', full_name='ai.verta.uac.AddTeamUser.share_with', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ADDTEAMUSER_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1061,
  serialized_end=1139,
)


_REMOVETEAMUSER_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='ai.verta.uac.RemoveTeamUser.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='ai.verta.uac.RemoveTeamUser.Response.status', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=897,
  serialized_end=923,
)

_REMOVETEAMUSER = _descriptor.Descriptor(
  name='RemoveTeamUser',
  full_name='ai.verta.uac.RemoveTeamUser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='team_id', full_name='ai.verta.uac.RemoveTeamUser.team_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='share_with', full_name='ai.verta.uac.RemoveTeamUser.share_with', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REMOVETEAMUSER_RESPONSE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1141,
  serialized_end=1222,
)

_TEAM.fields_by_name['id_service_provider'].enum_type = uac_dot_UACService__pb2._IDSERVICEPROVIDERENUM_IDSERVICEPROVIDER
_GETTEAMBYID_RESPONSE.fields_by_name['team'].message_type = _TEAM
_GETTEAMBYID_RESPONSE.containing_type = _GETTEAMBYID
_GETTEAMBYNAME_RESPONSE.fields_by_name['team'].message_type = _TEAM
_GETTEAMBYNAME_RESPONSE.containing_type = _GETTEAMBYNAME
_GETTEAMBYSHORTNAME_RESPONSE.fields_by_name['team'].message_type = _TEAM
_GETTEAMBYSHORTNAME_RESPONSE.containing_type = _GETTEAMBYSHORTNAME
_LISTMYTEAMS_RESPONSE.fields_by_name['teams'].message_type = _TEAM
_LISTMYTEAMS_RESPONSE.containing_type = _LISTMYTEAMS
_LISTMYTEAMS.fields_by_name['pagination'].message_type = common_dot_CommonService__pb2._PAGINATION
_SETTEAM_RESPONSE.fields_by_name['team'].message_type = _TEAM
_SETTEAM_RESPONSE.containing_type = _SETTEAM
_SETTEAM.fields_by_name['team'].message_type = _TEAM
_DELETETEAM_RESPONSE.containing_type = _DELETETEAM
_LISTTEAMUSER_RESPONSE.containing_type = _LISTTEAMUSER
_LISTTEAMUSER.fields_by_name['pagination'].message_type = common_dot_CommonService__pb2._PAGINATION
_ADDTEAMUSER_RESPONSE.containing_type = _ADDTEAMUSER
_REMOVETEAMUSER_RESPONSE.containing_type = _REMOVETEAMUSER
DESCRIPTOR.message_types_by_name['Team'] = _TEAM
DESCRIPTOR.message_types_by_name['GetTeamById'] = _GETTEAMBYID
DESCRIPTOR.message_types_by_name['GetTeamByName'] = _GETTEAMBYNAME
DESCRIPTOR.message_types_by_name['GetTeamByShortName'] = _GETTEAMBYSHORTNAME
DESCRIPTOR.message_types_by_name['ListMyTeams'] = _LISTMYTEAMS
DESCRIPTOR.message_types_by_name['SetTeam'] = _SETTEAM
DESCRIPTOR.message_types_by_name['DeleteTeam'] = _DELETETEAM
DESCRIPTOR.message_types_by_name['ListTeamUser'] = _LISTTEAMUSER
DESCRIPTOR.message_types_by_name['AddTeamUser'] = _ADDTEAMUSER
DESCRIPTOR.message_types_by_name['RemoveTeamUser'] = _REMOVETEAMUSER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Team = _reflection.GeneratedProtocolMessageType('Team', (_message.Message,), {
  'DESCRIPTOR' : _TEAM,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.Team)
  })
_sym_db.RegisterMessage(Team)

GetTeamById = _reflection.GeneratedProtocolMessageType('GetTeamById', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _GETTEAMBYID_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamById.Response)
    })
  ,
  'DESCRIPTOR' : _GETTEAMBYID,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamById)
  })
_sym_db.RegisterMessage(GetTeamById)
_sym_db.RegisterMessage(GetTeamById.Response)

GetTeamByName = _reflection.GeneratedProtocolMessageType('GetTeamByName', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _GETTEAMBYNAME_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamByName.Response)
    })
  ,
  'DESCRIPTOR' : _GETTEAMBYNAME,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamByName)
  })
_sym_db.RegisterMessage(GetTeamByName)
_sym_db.RegisterMessage(GetTeamByName.Response)

GetTeamByShortName = _reflection.GeneratedProtocolMessageType('GetTeamByShortName', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _GETTEAMBYSHORTNAME_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamByShortName.Response)
    })
  ,
  'DESCRIPTOR' : _GETTEAMBYSHORTNAME,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.GetTeamByShortName)
  })
_sym_db.RegisterMessage(GetTeamByShortName)
_sym_db.RegisterMessage(GetTeamByShortName.Response)

ListMyTeams = _reflection.GeneratedProtocolMessageType('ListMyTeams', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _LISTMYTEAMS_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.ListMyTeams.Response)
    })
  ,
  'DESCRIPTOR' : _LISTMYTEAMS,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.ListMyTeams)
  })
_sym_db.RegisterMessage(ListMyTeams)
_sym_db.RegisterMessage(ListMyTeams.Response)

SetTeam = _reflection.GeneratedProtocolMessageType('SetTeam', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _SETTEAM_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.SetTeam.Response)
    })
  ,
  'DESCRIPTOR' : _SETTEAM,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.SetTeam)
  })
_sym_db.RegisterMessage(SetTeam)
_sym_db.RegisterMessage(SetTeam.Response)

DeleteTeam = _reflection.GeneratedProtocolMessageType('DeleteTeam', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _DELETETEAM_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.DeleteTeam.Response)
    })
  ,
  'DESCRIPTOR' : _DELETETEAM,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.DeleteTeam)
  })
_sym_db.RegisterMessage(DeleteTeam)
_sym_db.RegisterMessage(DeleteTeam.Response)

ListTeamUser = _reflection.GeneratedProtocolMessageType('ListTeamUser', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _LISTTEAMUSER_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.ListTeamUser.Response)
    })
  ,
  'DESCRIPTOR' : _LISTTEAMUSER,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.ListTeamUser)
  })
_sym_db.RegisterMessage(ListTeamUser)
_sym_db.RegisterMessage(ListTeamUser.Response)

AddTeamUser = _reflection.GeneratedProtocolMessageType('AddTeamUser', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _ADDTEAMUSER_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.AddTeamUser.Response)
    })
  ,
  'DESCRIPTOR' : _ADDTEAMUSER,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.AddTeamUser)
  })
_sym_db.RegisterMessage(AddTeamUser)
_sym_db.RegisterMessage(AddTeamUser.Response)

RemoveTeamUser = _reflection.GeneratedProtocolMessageType('RemoveTeamUser', (_message.Message,), {

  'Response' : _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
    'DESCRIPTOR' : _REMOVETEAMUSER_RESPONSE,
    '__module__' : 'uac.Team_pb2'
    # @@protoc_insertion_point(class_scope:ai.verta.uac.RemoveTeamUser.Response)
    })
  ,
  'DESCRIPTOR' : _REMOVETEAMUSER,
  '__module__' : 'uac.Team_pb2'
  # @@protoc_insertion_point(class_scope:ai.verta.uac.RemoveTeamUser)
  })
_sym_db.RegisterMessage(RemoveTeamUser)
_sym_db.RegisterMessage(RemoveTeamUser.Response)


DESCRIPTOR._options = None

_TEAMSERVICE = _descriptor.ServiceDescriptor(
  name='TeamService',
  full_name='ai.verta.uac.TeamService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1225,
  serialized_end=2233,
  methods=[
  _descriptor.MethodDescriptor(
    name='getTeamById',
    full_name='ai.verta.uac.TeamService.getTeamById',
    index=0,
    containing_service=None,
    input_type=_GETTEAMBYID,
    output_type=_GETTEAMBYID_RESPONSE,
    serialized_options=b'\202\323\344\223\002\026\022\024/v1/team/getTeamById',
  ),
  _descriptor.MethodDescriptor(
    name='getTeamByName',
    full_name='ai.verta.uac.TeamService.getTeamByName',
    index=1,
    containing_service=None,
    input_type=_GETTEAMBYNAME,
    output_type=_GETTEAMBYNAME_RESPONSE,
    serialized_options=b'\202\323\344\223\002\030\022\026/v1/team/getTeamByName',
  ),
  _descriptor.MethodDescriptor(
    name='getTeamByShortName',
    full_name='ai.verta.uac.TeamService.getTeamByShortName',
    index=2,
    containing_service=None,
    input_type=_GETTEAMBYSHORTNAME,
    output_type=_GETTEAMBYSHORTNAME_RESPONSE,
    serialized_options=b'\202\323\344\223\002\035\022\033/v1/team/getTeamByShortName',
  ),
  _descriptor.MethodDescriptor(
    name='listMyTeams',
    full_name='ai.verta.uac.TeamService.listMyTeams',
    index=3,
    containing_service=None,
    input_type=_LISTMYTEAMS,
    output_type=_LISTMYTEAMS_RESPONSE,
    serialized_options=b'\202\323\344\223\002\026\022\024/v1/team/listMyTeams',
  ),
  _descriptor.MethodDescriptor(
    name='setTeam',
    full_name='ai.verta.uac.TeamService.setTeam',
    index=4,
    containing_service=None,
    input_type=_SETTEAM,
    output_type=_SETTEAM_RESPONSE,
    serialized_options=b'\202\323\344\223\002\025\"\020/v1/team/setTeam:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='deleteTeam',
    full_name='ai.verta.uac.TeamService.deleteTeam',
    index=5,
    containing_service=None,
    input_type=_DELETETEAM,
    output_type=_DELETETEAM_RESPONSE,
    serialized_options=b'\202\323\344\223\002\030\"\023/v1/team/deleteTeam:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='listUsers',
    full_name='ai.verta.uac.TeamService.listUsers',
    index=6,
    containing_service=None,
    input_type=_LISTTEAMUSER,
    output_type=_LISTTEAMUSER_RESPONSE,
    serialized_options=b'\202\323\344\223\002\024\022\022/v1/team/listUsers',
  ),
  _descriptor.MethodDescriptor(
    name='addUser',
    full_name='ai.verta.uac.TeamService.addUser',
    index=7,
    containing_service=None,
    input_type=_ADDTEAMUSER,
    output_type=_ADDTEAMUSER_RESPONSE,
    serialized_options=b'\202\323\344\223\002\025\"\020/v1/team/addUser:\001*',
  ),
  _descriptor.MethodDescriptor(
    name='removeUser',
    full_name='ai.verta.uac.TeamService.removeUser',
    index=8,
    containing_service=None,
    input_type=_REMOVETEAMUSER,
    output_type=_REMOVETEAMUSER_RESPONSE,
    serialized_options=b'\202\323\344\223\002\030\"\023/v1/team/removeUser:\001*',
  ),
])
_sym_db.RegisterServiceDescriptor(_TEAMSERVICE)

DESCRIPTOR.services_by_name['TeamService'] = _TEAMSERVICE

# @@protoc_insertion_point(module_scope)
