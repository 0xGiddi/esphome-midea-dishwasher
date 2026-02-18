# ESPHome Midea Dishwasher Component

ESPHome external component that decodes the UART protocol between a Midea countertop dishwasher's control board and display panel, exposing all interesting state to Home Assistant.

## Hardware
The ESP32 passively sniffs two 9600 baud UART lines (TX and RX) between the control board and the front panel. Both lines use **9600 baud, 8N1** (even parity). The ESP only reads — it does not inject packets.

## Setup
Place the component files in `components/midea_dishwasher/` relative to your ESPHome config or using git:

```
external_components:
  - source:
      type: git
      url: https://github.com/0xgiddi/esphome-midea-dishwasher
    components: [ midea_dishwasher ]
    refresh: 0s
```

Configure the UART sniffer ports:

```yaml
uart:
  - id: uart_dishwasher_tx
    rx_pin: GPIO16
    baud_rate: 9600
  - id: uart_dishwasher_rx
    rx_pin: GPIO17
    baud_rate: 9600

midea_dishwasher:
  tx_uart: uart_dishwasher_tx
  rx_uart: uart_dishwasher_rx
```

## Available Entities

All entities are optional — only include what you need.

### Text Sensors

```yaml
text_sensor:
  - platform: midea_dishwasher
    hr_status:
      name: "Status"
    current_program:
      name: "Program"
    hr_current_program_phase:
      name: "Cycle Stage"
    hr_system_operation:
      name: "Operation"
```

| Key | Description | Example Values |
|-----|-------------|---------------|
| `hr_status` | Human-readable system status combining system state, sub-state and cycle stage | Powered Off, Idle, Complete, Running - Pre-wash, Running - Main Wash, Running - Rinse, Running - Drying, Paused, Ending, Delay Start - Active, Delay Start - Paused, Error, Hardness Setting, Test Mode |
| `current_program` | Currently selected wash program | No Program, P1 Intensive, P2 Universal, P3 ECO, P4 Glass, P5 90 min, P6 Rapid, P7 Self-Clean |
| `hr_current_program_phase` | Current cycle stage | Idle, Pre-wash, Main Wash, Rinse, Dry, Complete |
| `hr_system_operation` | Active hardware operation (what the machine is physically doing) | Idle, Drain Pump, Water Inlet, Heater + Spray Pump, Spray Pump, Heater + Spray Pump + Rinse-aid, Heater + Spray Pump + Detergent, Wait, Pulsed Spray Pump, Regeneration Valve, Regeneration Drain, Program Select Display, End Program Display |

### Sensors

```yaml
sensor:
  - platform: midea_dishwasher
    time_remaining:
      name: "Time Remaining"
    live_temperature:
      name: "Water Temperature"
    cycle_progress:
      name: "Cycle Progress"
    water_hardness:
      name: "Water Hardness"
    error_code:
      name: "Error Code"
    start_delay:
      name: "Start Delay"
    operation_state:
      name: "Operation Code"
    system_main_state:
      name: "System State"
    system_sub_state:
      name: "Sub State"
    program_phase:
      name: "Phase Code"
```

| Key | Description | Unit | Range |
|-----|-------------|------|-------|
| `time_remaining` | Minutes remaining in current cycle | min | 0–230 |
| `live_temperature` | Current water temperature (NTC formula: raw × 2 + 20) | °C | 20–68 |
| `cycle_progress` | Estimated cycle progress based on time remaining vs initial time | % | 0–100 |
| `water_hardness` | Configured water hardness level | — | 1–6 |
| `error_code` | Error code (0 = OK, 1 = E1 water inlet, 3 = E3 heater, 4 = E4 overflow) | — | 0–13 |
| `start_delay` | Delay timer value from front panel (RX) | min | 0–1440 |
| `operation_state` | Raw TX4 operation code for automations | — | 0–66 |
| `system_main_state` | Raw TX3 high nibble (0=Off, 1=Idle, 2=Delay, 3=Running, 4=Error, 5=Hardness, 8=Test) | — | 0–8 |
| `system_sub_state` | Raw TX3 low nibble (1=Transition, 2=Normal, 3=Paused, 4=Ending) | — | 0–4 |
| `program_phase` | Raw cycle stage code (0=Idle, 1=Pre-wash, 2=Main, 3=Rinse, 4=Dry, 5=Complete) | — | 0–5 |

### Binary Sensors

```yaml
binary_sensor:
  - platform: midea_dishwasher
    running:
      name: "Running"
    door_open:
      name: "Door"
    paused:
      name: "Paused"
    error:
      name: "Error"
    cycle_complete:
      name: "Cycle Complete"
    salt_low:
      name: "Salt Low"
    rinse_aid_low:
      name: "Rinse-Aid Low"
    extra_dry:
      name: "Extra Dry"
    child_lock:
      name: "Child Lock"
```

| Key | Description | Source |
|-----|-------------|--------|
| `running` | Cycle is actively running | TX3 high nibble = 3 |
| `door_open` | Door is open | TX13 bit 3 |
| `paused` | Cycle or delay timer is paused (door open or button) | TX3: running + lo=3, or delay + lo=2 |
| `error` | Machine is in error state | TX3 high nibble = 4 |
| `cycle_complete` | Cycle has finished (stage = Complete) | TX12 stage = 5 |
| `salt_low` | Water softener salt reservoir low | TX13 bit 4 |
| `rinse_aid_low` | Rinse-aid reservoir low | TX13 bit 5 |
| `extra_dry` | Extra dry option enabled | TX15 bit 1 |
| `child_lock` | Child lock active (from front panel) | RX15 bit 3 |

## Full Example Configuration

```yaml
esphome:
  name: dishwasher
  friendly_name: Dishwasher

esp32:
  board: esp32dev
  framework:
    type: esp-idf

external_components:
  - source:
      type: git
      url: https://github.com/0xgiddi/esphome-midea-dishwasher
    components: [ midea_dishwasher ]
    refresh: 0s

logger:

api:
  encryption:
    key: !secret api_key

ota:
  - platform: esphome
    password: !secret ota_password

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
    ssid: "Dishwasher Fallback"
    password: !secret fallback_password

captive_portal:
text:
number:

uart:
  - id: uart_dishwasher_tx
    rx_pin: GPIO33
    baud_rate: 9600
  - id: uart_dishwasher_rx
    rx_pin: GPIO23
    baud_rate: 9600

midea_dishwasher:
  tx_uart: uart_dishwasher_tx
  rx_uart: uart_dishwasher_rx

text_sensor:
  - platform: midea_dishwasher
    hr_status:
      name: "Dishwasher Status"
    current_program:
      name: "Dishwasher Program"
    hr_current_program_phase:
      name: "Dishwasher Cycle Stage"
    hr_system_operation:
      name: "Dishwasher Operation"

sensor:
  - platform: midea_dishwasher
    time_remaining:
      name: "Dishwasher Time Remaining"
    live_temperature:
      name: "Dishwasher Temperature"
    cycle_progress:
      name: "Dishwasher Progress"
    water_hardness:
      name: "Dishwasher Hardness"
    error_code:
      name: "Dishwasher Error Code"
    start_delay:
      name: "Dishwasher Delay"
    operation_state:
      name: "Dishwasher Operation Code"
    system_main_state:
      name: "Dishwasher System State"
    system_sub_state:
      name: "Dishwasher Sub State"
    program_phase:
      name: "Dishwasher Phase Code"

binary_sensor:
  - platform: midea_dishwasher
    running:
      name: "Dishwasher Running"
    door_open:
      name: "Dishwasher Door"
    error:
      name: "Dishwasher Error"
    paused:
      name: "Dishwasher Paused"
    cycle_complete:
      name: "Dishwasher Complete"
    salt_low:
      name: "Dishwasher Salt Low"
    rinse_aid_low:
      name: "Dishwasher Rinse-Aid Low"
    extra_dry:
      name: "Dishwasher Extra Dry"
    child_lock:
      name: "Dishwasher Child Lock"
```
