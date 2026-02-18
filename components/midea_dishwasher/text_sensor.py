import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from . import MideaDishwasher

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_CURRENT_PROGRAM = "current_program"
CONF_HR_CURRENT_PROGRAM_PHASE = "hr_current_program_phase"
CONF_HR_STATUS = "hr_status"
CONF_HR_SYSTEM_OPERATION = "hr_system_operation"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_CURRENT_PROGRAM): text_sensor.text_sensor_schema(),
    cv.Optional(CONF_HR_CURRENT_PROGRAM_PHASE): text_sensor.text_sensor_schema(),
    cv.Optional(CONF_HR_STATUS): text_sensor.text_sensor_schema(),
    cv.Optional(CONF_HR_SYSTEM_OPERATION): text_sensor.text_sensor_schema(),
})


async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_CURRENT_PROGRAM in config:
        sens = await text_sensor.new_text_sensor(config[CONF_CURRENT_PROGRAM])
        cg.add(parent.set_current_program(sens))

    if CONF_HR_CURRENT_PROGRAM_PHASE in config:
        sens = await text_sensor.new_text_sensor(config[CONF_HR_CURRENT_PROGRAM_PHASE])
        cg.add(parent.set_hr_current_program_phase(sens))

    if CONF_HR_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_HR_STATUS])
        cg.add(parent.set_hr_status(sens))

    if CONF_HR_SYSTEM_OPERATION in config:
        sens = await text_sensor.new_text_sensor(config[CONF_HR_SYSTEM_OPERATION])
        cg.add(parent.set_hr_system_operation(sens))
