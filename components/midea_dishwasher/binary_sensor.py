import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    DEVICE_CLASS_LOCK,
    DEVICE_CLASS_OPENING,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_RUNNING,
)
from . import MideaDishwasher

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_DOOR_OPEN = "door_open"
CONF_SALT_LOW = "salt_low"
CONF_RINSE_AID_LOW = "rinse_aid_low"
CONF_EXTRA_DRY = "extra_dry"
CONF_CHILD_LOCK = "child_lock"
CONF_CYCLE_COMPLETE = "cycle_complete"
CONF_ERROR = "error"
CONF_PAUSED = "paused"
CONF_RUNNING = "running"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_DOOR_OPEN): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_OPENING,
    ),
    cv.Optional(CONF_SALT_LOW): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_RINSE_AID_LOW): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_EXTRA_DRY): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_CHILD_LOCK): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_CYCLE_COMPLETE): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_ERROR): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_PAUSED): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_RUNNING): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_RUNNING,
    ),
})


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_DOOR_OPEN in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_DOOR_OPEN])
        cg.add(parent.set_door_open(sens))

    if CONF_SALT_LOW in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_SALT_LOW])
        cg.add(parent.set_salt_low(sens))

    if CONF_RINSE_AID_LOW in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_RINSE_AID_LOW])
        cg.add(parent.set_rinse_aid_low(sens))

    if CONF_EXTRA_DRY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_EXTRA_DRY])
        cg.add(parent.set_extra_dry(sens))

    if CONF_CHILD_LOCK in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHILD_LOCK])
        cg.add(parent.set_child_lock(sens))

    if CONF_CYCLE_COMPLETE in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CYCLE_COMPLETE])
        cg.add(parent.set_cycle_complete(sens))

    if CONF_ERROR in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_ERROR])
        cg.add(parent.set_error(sens))

    if CONF_PAUSED in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_PAUSED])
        cg.add(parent.set_paused(sens))

    if CONF_RUNNING in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_RUNNING])
        cg.add(parent.set_running(sens))
