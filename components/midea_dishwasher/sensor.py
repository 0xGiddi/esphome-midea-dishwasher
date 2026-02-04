import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_MINUTE,
)
from . import MideaDishwasher, midea_dishwasher_ns

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_TIME_REMAINING = "time_remaining"
CONF_START_DELAY = "start_delay"
CONF_WATER_TEMPERATURE = "water_temperature"
CONF_WATER_HARDNESS = "water_hardness"
CONF_ERROR = "error"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_TIME_REMAINING): sensor.sensor_schema(
        unit_of_measurement=UNIT_MINUTE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_START_DELAY): sensor.sensor_schema(
        unit_of_measurement=UNIT_MINUTE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_WATER_TEMPERATURE): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_WATER_HARDNESS): sensor.sensor_schema(
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_ERROR): sensor.sensor_schema(),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_TIME_REMAINING in config:
        sens = await sensor.new_sensor(config[CONF_TIME_REMAINING])
        cg.add(parent.set_time_remaining(sens))

    if CONF_START_DELAY in config:
        sens = await sensor.new_sensor(config[CONF_START_DELAY])
        cg.add(parent.set_start_delay(sens))

    if CONF_WATER_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_WATER_TEMPERATURE])
        cg.add(parent.set_water_temperature(sens))

    if CONF_WATER_HARDNESS in config:
        sens = await sensor.new_sensor(config[CONF_WATER_HARDNESS])
        cg.add(parent.set_water_hardness(sens))

    if CONF_ERROR in config:
        sens = await sensor.new_sensor(config[CONF_ERROR])
        cg.add(parent.set_error(sens))