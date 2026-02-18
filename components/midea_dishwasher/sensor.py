import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_MINUTE,
    UNIT_PERCENT,
)
from . import MideaDishwasher

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_SYSTEM_MAIN_STATE = "system_main_state"
CONF_SYSTEM_SUB_STATE = "system_sub_state"
CONF_PROGRAM_PHASE = "program_phase"
CONF_OPERATION_STATE = "operation_state"
CONF_TIME_REMAINING = "time_remaining"
CONF_LIVE_TEMPERATURE = "live_temperature"
CONF_ERROR_CODE = "error_code"
CONF_WATER_HARDNESS = "water_hardness"
CONF_CYCLE_PROGRESS = "cycle_progress"
CONF_START_DELAY = "start_delay"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_SYSTEM_MAIN_STATE): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_SYSTEM_SUB_STATE): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_PROGRAM_PHASE): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_OPERATION_STATE): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_TIME_REMAINING): sensor.sensor_schema(
        accuracy_decimals=0,
        unit_of_measurement=UNIT_MINUTE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_LIVE_TEMPERATURE): sensor.sensor_schema(
        accuracy_decimals=0,
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_ERROR_CODE): sensor.sensor_schema(
        accuracy_decimals=0,
    ),
    cv.Optional(CONF_WATER_HARDNESS): sensor.sensor_schema(
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_CYCLE_PROGRESS): sensor.sensor_schema(
        accuracy_decimals=0,
        unit_of_measurement=UNIT_PERCENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_START_DELAY): sensor.sensor_schema(
        accuracy_decimals=0,
        unit_of_measurement=UNIT_MINUTE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
})


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_SYSTEM_MAIN_STATE in config:
        sens = await sensor.new_sensor(config[CONF_SYSTEM_MAIN_STATE])
        cg.add(parent.set_system_main_state(sens))

    if CONF_SYSTEM_SUB_STATE in config:
        sens = await sensor.new_sensor(config[CONF_SYSTEM_SUB_STATE])
        cg.add(parent.set_system_sub_state(sens))

    if CONF_PROGRAM_PHASE in config:
        sens = await sensor.new_sensor(config[CONF_PROGRAM_PHASE])
        cg.add(parent.set_program_phase(sens))

    if CONF_OPERATION_STATE in config:
        sens = await sensor.new_sensor(config[CONF_OPERATION_STATE])
        cg.add(parent.set_operation_state(sens))

    if CONF_TIME_REMAINING in config:
        sens = await sensor.new_sensor(config[CONF_TIME_REMAINING])
        cg.add(parent.set_time_remaining(sens))

    if CONF_LIVE_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_LIVE_TEMPERATURE])
        cg.add(parent.set_live_temperature(sens))

    if CONF_ERROR_CODE in config:
        sens = await sensor.new_sensor(config[CONF_ERROR_CODE])
        cg.add(parent.set_error_code(sens))

    if CONF_WATER_HARDNESS in config:
        sens = await sensor.new_sensor(config[CONF_WATER_HARDNESS])
        cg.add(parent.set_water_hardness(sens))

    if CONF_CYCLE_PROGRESS in config:
        sens = await sensor.new_sensor(config[CONF_CYCLE_PROGRESS])
        cg.add(parent.set_cycle_progress(sens))

    if CONF_START_DELAY in config:
        sens = await sensor.new_sensor(config[CONF_START_DELAY])
        cg.add(parent.set_start_delay(sens))
