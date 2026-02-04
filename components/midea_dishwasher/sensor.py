import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, binary_sensor, text_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_PROBLEM,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_MINUTE,
)
from . import MideaDishwasher, midea_dishwasher_ns

CONF_MIDEA_DISHWASHER_ID = 'midea_dishwasher_id'
CONF_DOOR_OPEN = 'door_open'
CONF_LOW_RINSE_AID = 'low_rinse_aid'
CONF_LOW_SALT = 'low_salt'
CONF_EXTRA_DRY = 'extra_dry'
CONF_CHILD_LOCK = 'child_lock'
CONF_OVERFLOW_ERROR = 'overflow_error'
CONF_INTAKE_ERROR = 'intake_error'
CONF_PROGRAM_END = 'program_end'
CONF_CURRENT_PROGRAM = 'current_program'
CONF_TIME_REMAINING = 'time_remaining'
CONF_START_DELAY = 'start_delay'
CONF_WATER_TEMPERATURE = 'water_temperature'
CONF_WATER_HARDNESS = 'water_hardness'
CONF_ERROR = 'error'

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
    cv.Optional(CONF_CURRENT_PROGRAM): text_sensor.text_sensor_schema(),
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
    
    if CONF_CURRENT_PROGRAM in config:
        sens = await text_sensor.new_text_sensor(config[CONF_CURRENT_PROGRAM])
        cg.add(parent.set_current_program(sens))
    
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