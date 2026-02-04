import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from . import MideaDishwasher, midea_dishwasher_ns

CONF_MIDEA_DISHWASHER_ID = "midea_dishwasher_id"
CONF_CURRENT_PROGRAM = "current_program"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_MIDEA_DISHWASHER_ID): cv.use_id(MideaDishwasher),
    cv.Optional(CONF_CURRENT_PROGRAM): text_sensor.text_sensor_schema(),
})

async def to_code(config):
    parent = await cg.get_variable(config[CONF_MIDEA_DISHWASHER_ID])

    if CONF_CURRENT_PROGRAM in config:
        sens = await text_sensor.new_text_sensor(config[CONF_CURRENT_PROGRAM])
        cg.add(parent.set_current_program(sens))