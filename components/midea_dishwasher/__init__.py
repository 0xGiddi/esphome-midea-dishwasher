import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, switch, text, number
from esphome.const import CONF_ID, ENTITY_CATEGORY_DIAGNOSTIC, CONF_MODE

CODEOWNERS = ["@0xgiddi"]
DEPENDENCIES = ["uart", "switch", "text", "number"]
MULTI_CONF = False

CONF_TX_UART = "tx_uart"
CONF_RX_UART = "rx_uart"
CONF_DEBUG_MODE = "debug_mode"
CONF_DEBUG_IP = "debug_ip"
CONF_DEBUG_PORT = "debug_port"
CONF_DEBUG_SWITCH = "debug_switch"
CONF_DEBUG_IP_TEXT = "debug_ip_text"
CONF_DEBUG_PORT_NUMBER = "debug_port_number"

midea_dishwasher_ns = cg.esphome_ns.namespace("midea_dishwasher")
MideaDishwasher = midea_dishwasher_ns.class_("MideaDishwasher", cg.Component)
DebugSwitch = midea_dishwasher_ns.class_("DebugSwitch", switch.Switch)
DebugIPText = midea_dishwasher_ns.class_("DebugIPText", text.Text)
DebugPortNumber = midea_dishwasher_ns.class_("DebugPortNumber", number.Number)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MideaDishwasher),
    cv.Required(CONF_TX_UART): cv.use_id(uart.UARTComponent),
    cv.Required(CONF_RX_UART): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_DEBUG_MODE, default=False): cv.boolean,
    cv.Optional(CONF_DEBUG_IP, default=""): cv.string,
    cv.Optional(CONF_DEBUG_PORT, default=9595): cv.port,
    cv.Optional(CONF_DEBUG_SWITCH): switch.switch_schema(
        DebugSwitch,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_DEBUG_IP_TEXT): text.text_schema(
        DebugIPText,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    cv.Optional(CONF_DEBUG_PORT_NUMBER): number.number_schema(
        DebugPortNumber,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    tx_uart = await cg.get_variable(config[CONF_TX_UART])
    rx_uart = await cg.get_variable(config[CONF_RX_UART])
    var = cg.new_Pvariable(config[CONF_ID], tx_uart, rx_uart)
    await cg.register_component(var, config)
    
    if config[CONF_DEBUG_IP]:
        cg.add(var.set_debug_ip(config[CONF_DEBUG_IP]))
    cg.add(var.set_debug_port(config[CONF_DEBUG_PORT]))
    cg.add(var.set_debug_mode(config[CONF_DEBUG_MODE]))
    
    if CONF_DEBUG_SWITCH in config:
        sw = await switch.new_switch(config[CONF_DEBUG_SWITCH])
        cg.add(var.set_debug_switch(sw))
    
    if CONF_DEBUG_IP_TEXT in config:
        t = await text.new_text(config[CONF_DEBUG_IP_TEXT])
        cg.add(t.traits.set_mode(text.TextMode.TEXT))
        cg.add(var.set_debug_ip_text(t))
    
    if CONF_DEBUG_PORT_NUMBER in config:
        n = await number.new_number(config[CONF_DEBUG_PORT_NUMBER], min_value=1, max_value=65535, step=1)
        cg.add(var.set_debug_port_number(n))