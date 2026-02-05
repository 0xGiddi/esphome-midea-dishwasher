import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, switch
from esphome.const import CONF_ID

CODEOWNERS = ["@0xgiddi"]
DEPENDENCIES = ["uart", "switch"]
MULTI_CONF = False

CONF_TX_UART = "tx_uart"
CONF_RX_UART = "rx_uart"
CONF_DEBUG_MODE = "debug_mode"
CONF_DEBUG_IP = "debug_ip"
CONF_DEBUG_PORT = "debug_port"
CONF_DEBUG_SWITCH = "debug_switch"

midea_dishwasher_ns = cg.esphome_ns.namespace("midea_dishwasher")
MideaDishwasher = midea_dishwasher_ns.class_("MideaDishwasher", cg.Component)
DebugSwitch = midea_dishwasher_ns.class_("DebugSwitch", switch.Switch)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(MideaDishwasher),
    cv.Required(CONF_TX_UART): cv.use_id(uart.UARTComponent),
    cv.Required(CONF_RX_UART): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_DEBUG_MODE, default=False): cv.boolean,
    cv.Optional(CONF_DEBUG_IP, default=""): cv.string,
    cv.Optional(CONF_DEBUG_PORT, default=9595): cv.port,
    cv.Optional(CONF_DEBUG_SWITCH): switch.switch_schema(DebugSwitch),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    tx_uart = await cg.get_variable(config[CONF_TX_UART])
    rx_uart = await cg.get_variable(config[CONF_RX_UART])
    var = cg.new_Pvariable(config[CONF_ID], tx_uart, rx_uart)
    await cg.register_component(var, config)
    
    # Always set IP and port if provided
    if config[CONF_DEBUG_IP]:
        cg.add(var.set_debug_ip(config[CONF_DEBUG_IP]))
    cg.add(var.set_debug_port(config[CONF_DEBUG_PORT]))
    
    # Set initial debug mode
    cg.add(var.set_debug_mode(config[CONF_DEBUG_MODE]))
    
    if CONF_DEBUG_SWITCH in config:
        sw = await switch.new_switch(config[CONF_DEBUG_SWITCH])
        cg.add(var.set_debug_switch(sw))