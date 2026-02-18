#pragma once
#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"

namespace esphome::midea_dishwasher {
    static const char *TAG = "midea_dishwasher.component";
    static const uint8_t PREAMBLE = 0x55;
    static const uint8_t TX_PACKET_LEN = 0x1f;
    static const uint8_t RX_PACKET_LEN = 0x10;

    class MideaDishwasher : public Component {
        public:
            MideaDishwasher(uart::UARTComponent *tx_iface, uart::UARTComponent *rx_iface)
                : tx_iface_(tx_iface), rx_iface_(rx_iface) {}
            void setup() override;
            void loop() override;
            void set_door_open(binary_sensor::BinarySensor *s) { door_open_ = s; }
            void set_salt_low(binary_sensor::BinarySensor *s) { salt_low_ = s; }
            void set_rinse_aid_low(binary_sensor::BinarySensor *s) { rinse_aid_low_ = s; }
            void set_extra_dry(binary_sensor::BinarySensor *s) { extra_dry_ = s; }
            void set_child_lock(binary_sensor::BinarySensor *s) { child_lock_ = s; }
            void set_cycle_complete(binary_sensor::BinarySensor *s) { cycle_complete_ = s; }
            void set_error(binary_sensor::BinarySensor *s) { error_ = s; }
            void set_paused(binary_sensor::BinarySensor *s) { paused_ = s; }
            void set_system_main_state(sensor::Sensor *s) { system_main_state_ = s; }
            void set_system_sub_state(sensor::Sensor *s) { system_sub_state_ = s; }
            void set_program_phase(sensor::Sensor *s) { program_phase_ = s; }
            void set_operation_state(sensor::Sensor *s) { operation_state_ = s; }
            void set_time_remaining(sensor::Sensor *s) { time_remaining_ = s; }
            void set_live_temperature(sensor::Sensor *s) { live_temperature_ = s; }
            void set_error_code(sensor::Sensor *s) { error_code_ = s; }
            void set_water_hardness(sensor::Sensor *s) { water_hardness_ = s; }
            void set_cycle_progress(sensor::Sensor *s) { cycle_progress_ = s; }
            void set_start_delay(sensor::Sensor *s) { start_delay_ = s; }
            void set_current_program(text_sensor::TextSensor *s) { current_program_ = s; }
            void set_hr_current_program_phase(text_sensor::TextSensor *s) { hr_current_program_phase_ = s; }
            void set_running(binary_sensor::BinarySensor *s) { running_ = s; }
            void set_hr_status(text_sensor::TextSensor *s) { hr_status_ = s; }
            void set_hr_system_operation(text_sensor::TextSensor *s) { hr_system_operation_ = s; }

        protected:
            uart::UARTComponent *tx_iface_, *rx_iface_;
            std::vector<uint8_t> tx_iface_buffer_, rx_iface_buffer_;
            uint8_t cycle_total_minutes_{0};
            bool was_running_{false};

            binary_sensor::BinarySensor *door_open_{nullptr};
            binary_sensor::BinarySensor *salt_low_{nullptr};
            binary_sensor::BinarySensor *rinse_aid_low_{nullptr};
            binary_sensor::BinarySensor *extra_dry_{nullptr};
            binary_sensor::BinarySensor *child_lock_{nullptr};
            binary_sensor::BinarySensor *cycle_complete_{nullptr};
            binary_sensor::BinarySensor *error_{nullptr};
            binary_sensor::BinarySensor *paused_{nullptr};
            binary_sensor::BinarySensor *running_{nullptr};

            sensor::Sensor *system_main_state_{nullptr};
            sensor::Sensor *system_sub_state_{nullptr};
            sensor::Sensor *program_phase_{nullptr};
            sensor::Sensor *operation_state_{nullptr};
            sensor::Sensor *time_remaining_{nullptr};
            sensor::Sensor *live_temperature_{nullptr};
            sensor::Sensor *error_code_{nullptr};
            sensor::Sensor *water_hardness_{nullptr};
            sensor::Sensor *cycle_progress_{nullptr};
            sensor::Sensor *start_delay_{nullptr};

            text_sensor::TextSensor *current_program_{nullptr};
            text_sensor::TextSensor *hr_system_operation_{nullptr};
            text_sensor::TextSensor *hr_current_program_phase_{nullptr};
            text_sensor::TextSensor *hr_status_{nullptr};


            void read_uart_(uart::UARTComponent *uart, std::vector<uint8_t> &buffer);
            void process_buffer_(std::vector<uint8_t> &buffer, uint8_t data_len);
            void process_tx_packet_(std::vector<uint8_t> &buffer);
            void process_rx_packet_(std::vector<uint8_t> &buffer);
            
            template <typename T, typename V>
            void publish_state_(T *sensor, const V &value) {
                if (sensor != nullptr && (!sensor->has_state() || sensor->state != value))
                    sensor->publish_state(value);
            }
    };
}