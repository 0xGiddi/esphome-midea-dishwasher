import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_PROBLEM,
)
from . import MideaDishwasher, midea_dishwasher_ns

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_DOOR_OPEN = "door_open"
CONF_LOW_RINSE_AID = "low_rinse_aid"
CONF_LOW_SALT = "low_salt"
CONF_EXTRA_DRY = "extra_dry"
CONF_CHILD_LOCK = "child_lock"
CONF_OVERFLOW_ERROR = "overflow_error"
CONF_INTAKE_ERROR = "intake_error"
CONF_PROGRAM_END = "program_end"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_DOOR_OPEN): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_OPENING,
    ),
    cv.Optional(CONF_LOW_RINSE_AID): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_LOW_SALT): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_EXTRA_DRY): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_CHILD_LOCK): binary_sensor.binary_sensor_schema(),
    cv.Optional(CONF_OVERFLOW_ERROR): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_INTAKE_ERROR): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM,
    ),
    cv.Optional(CONF_PROGRAM_END): binary_sensor.binary_sensor_schema(),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_DOOR_OPEN in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_DOOR_OPEN])
        cg.add(parent.set_door_open(sens))

    if CONF_LOW_RINSE_AID in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_LOW_RINSE_AID])
        cg.add(parent.set_low_rinse_aid(sens))

    if CONF_LOW_SALT in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_LOW_SALT])
        cg.add(parent.set_low_salt(sens))

    if CONF_EXTRA_DRY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_EXTRA_DRY])
        cg.add(parent.set_extra_dry(sens))

    if CONF_CHILD_LOCK in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHILD_LOCK])
        cg.add(parent.set_child_lock(sens))

    if CONF_OVERFLOW_ERROR in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_OVERFLOW_ERROR])
        cg.add(parent.set_overflow_error(sens))

    if CONF_INTAKE_ERROR in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_INTAKE_ERROR])
        cg.add(parent.set_intake_error(sens))

    if CONF_PROGRAM_END in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_PROGRAM_END])
        cg.add(parent.set_program_end(sens))