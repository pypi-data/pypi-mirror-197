from enum import Enum


class ReturnCodes(Enum):
    """
    Keys for API return code
    """
    SUCCESS = 'Success'


class ResponseKeys(Enum):
    """
    Keys for response data, level 0
    """
    CODE = 'code'
    MESSAGE = 'message'
    DATA = 'data'


class DataKeys(Enum):
    """
    Keys for success response data, level 1
    """
    ITEMS = 'items'
    CURSOR = 'next_cursor'
    STATUS = 'status'


class GroupKey(Enum):
    """
    Keys for group data
    """
    ID = 'id'
    NAME = 'name'


class ConnectorKey(Enum):
    """
    Keys for connector data level 0
    """
    ID = 'id'
    STATUS = 'status'
    SUCCEEDED_AT = 'succeeded_at'
    FAILED_AT = 'failed_at'
    SYNC_FREQUENCY = 'sync_frequency'
    DAILY_SYNC_TIME = 'daily_sync_time'
    SCHEDULE_TYPE = 'schedule_type'


class StatusKey(Enum):
    """
    Keys for connector data status block
    """
    SETUP_STATE = 'setup_state'
    SCHEMA_STATUS = 'schema_status'
    SYNC_STATE = 'sync_state'
    UPDATE_STATE = 'update_state'
    IS_HISTORICAL_SYNC = 'is_historical_sync'
    TASKS = 'tasks'
    WARNINGS = 'warnings'


class SetupState(Enum):
    BROKEN = 'broken'  # the setup config is incomplete, the setup tests never
    # succeeded;
    CONNECT = 'connect'  # the connector is properly set up;
    INCOMPLETE = 'incomplete'  # the connector setup config is broken;


class SyncState(Enum):
    SCHEDULED = 'scheduled'  # the sync is waiting to be run;
    SYNCING = 'syncing'  # the sync is currently running;
    PAUSED = 'paused'  # the sync is currently paused;
    RESCHEDULED = 'rescheduled'  # the sync is waiting until more API calls are
    # available in the source service.


class UpdateState(Enum):
    ON_SCHEDULE = 'on_schedule'  # the sync is running smoothly, no delays;
    DELAYED = 'delayed'  # the data is delayed for a longer time than expected
    # for the update.


class ScheduleType(Enum):
    """
    Valid values for a schedule_type properties
    """
    AUTO = 'auto'
    MANUAL = 'manual'


class Timeframe(Enum):
    """
    Valid values for a time_frame properties
    """
    DEPTH_3_MONTHS = 'THREE'
    DEPTH_6_MONTHS = 'SIX'
    DEPTH_1_YEAR = 'TWELVE'
    DEPTH_2_YEARS = 'TWENTY_FOUR'
    DEPTH_ALL = 'ALL_TIME'


class SyncFrequency(Enum):
    """
    Valid values for a sync_frequency properties
    """
    EVERY_5_MIN = 5
    EVERY_15_MIN = 15
    EVERY_30_MIN = 30
    EVERY_HOUR = 60
    EVERY_2_HOURS = 120
    EVERY_3_HOURS = 180
    EVERY_6_HOURS = 360
    EVERY_8_HOURS = 480
    EVERY_12_HOURS = 720
    EVERY_24_HOURS = 1440


class SchemaStatus(Enum):
    """
    Valid values for a schema status properties
    """
    READY = 'ready'  # the schema is ready
    BLOCKED_ON_CAPTURE = 'blocked_on_capture'  # the schema is blocked for
    # schema capturing
    BLOCKED_ON_CUSTOMER = 'blocked_on_customer'  # the schema has been captured
    # and is waiting for the user to review the schema

