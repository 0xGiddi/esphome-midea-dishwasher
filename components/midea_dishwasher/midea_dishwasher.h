#pragma once
#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"

#ifdef USE_ESP_IDF
#include "lwip/sockets.h"
#include "lwip/netdb.h"
#else
#include <WiFiUdp.h>
#endif

namespace esphome {
namespace midea_dishwasher {

class MideaDishwasher : public Component {
 public:
  MideaDishwasher(uart::UARTComponent *tx_iface, uart::UARTComponent *rx_iface)
      : tx_iface_(tx_iface), rx_iface_(rx_iface) {}

  void setup() override {
    buffer_tx_iface_.reserve(128);
    buffer_rx_iface_.reserve(128);

    if (debug_mode_ && !debug_ip_.empty()) {
#ifdef USE_ESP_IDF
    udp_socket_ = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udp_socket_ >= 0) {
      memset(&dest_addr_, 0, sizeof(dest_addr_));
      dest_addr_.sin_family = AF_INET;
      dest_addr_.sin_port = htons(debug_port_);
      inet_aton(debug_ip_.c_str(), &dest_addr_.sin_addr);
    }
#else
    udp_.begin(debug_port_);
#endif
    s}
}

  void loop() override {
    read_uart_(tx_iface_, buffer_tx_iface_);
    process_buffer_(buffer_tx_iface_, 0x1f);

    read_uart_(rx_iface_, buffer_rx_iface_);
    process_buffer_(buffer_rx_iface_, 0x10);
  }

  // Setters
  void set_door_open(binary_sensor::BinarySensor *sensor) { door_open_ = sensor; }
  void set_low_rinse_aid(binary_sensor::BinarySensor *sensor) { low_rinse_aid_ = sensor; }
  void set_low_salt(binary_sensor::BinarySensor *sensor) { low_salt_ = sensor; }
  void set_extra_dry(binary_sensor::BinarySensor *sensor) { extra_dry_ = sensor; }
  void set_child_lock(binary_sensor::BinarySensor *sensor) { child_lock_ = sensor; }
  void set_overflow_error(binary_sensor::BinarySensor *sensor) { overflow_error_ = sensor; }
  void set_intake_error(binary_sensor::BinarySensor *sensor) { intake_error_ = sensor; }
  void set_program_end(binary_sensor::BinarySensor *sensor) { program_end_ = sensor; }
  void set_current_program(text_sensor::TextSensor *sensor) { current_program_ = sensor; }
  void set_time_remaining(sensor::Sensor *sensor) { time_remaining_ = sensor; }
  void set_start_delay(sensor::Sensor *sensor) { start_delay_ = sensor; }
  void set_water_temperature(sensor::Sensor *sensor) { water_temperature_ = sensor; }
  void set_water_hardness(sensor::Sensor *sensor) { water_hardness_ = sensor; }
  void set_error(sensor::Sensor *sensor) { error_ = sensor; }
  void set_debug_mode(bool mode) { debug_mode_ = mode; }
  void set_debug_ip(const std::string &ip) { debug_ip_ = ip; }
  void set_debug_port(uint16_t port) { debug_port_ = port; }

 protected:
  uart::UARTComponent *tx_iface_;
  uart::UARTComponent *rx_iface_;
  std::vector<uint8_t> buffer_tx_iface_;
  std::vector<uint8_t> buffer_rx_iface_;

  binary_sensor::BinarySensor *door_open_{nullptr};
  binary_sensor::BinarySensor *low_rinse_aid_{nullptr};
  binary_sensor::BinarySensor *low_salt_{nullptr};
  binary_sensor::BinarySensor *extra_dry_{nullptr};
  binary_sensor::BinarySensor *child_lock_{nullptr};
  binary_sensor::BinarySensor *overflow_error_{nullptr};
  binary_sensor::BinarySensor *intake_error_{nullptr};
  binary_sensor::BinarySensor *program_end_{nullptr};
  text_sensor::TextSensor *current_program_{nullptr};
  sensor::Sensor *time_remaining_{nullptr};
  sensor::Sensor *start_delay_{nullptr};
  sensor::Sensor *water_temperature_{nullptr};
  sensor::Sensor *water_hardness_{nullptr};
  sensor::Sensor *error_{nullptr};

  bool debug_mode_{false};
  std::string debug_ip_;
  uint16_t debug_port_{9595};
#ifdef USE_ESP_IDF
  int udp_socket_{-1};
  struct sockaddr_in dest_addr_;
#else
  WiFiUDP udp_;
#endif

void send_debug_packet_(std::vector<uint8_t> &buffer, size_t len, uint8_t source) {
    if (!debug_mode_ || debug_ip_.empty())
      return;
    
    // Prepend source byte: 0x01 = TX, 0x02 = RX
    std::vector<uint8_t> packet;
    packet.push_back(source);
    packet.insert(packet.end(), buffer.begin(), buffer.begin() + len);
    
#ifdef USE_ESP_IDF
    if (udp_socket_ >= 0) {
      sendto(udp_socket_, packet.data(), packet.size(), 0, 
             (struct sockaddr *)&dest_addr_, sizeof(dest_addr_));
    }
#else
    udp_.beginPacket(debug_ip_.c_str(), debug_port_);
    udp_.write(packet.data(), packet.size());
    udp_.endPacket();
#endif
  }

  void publish_binary_(binary_sensor::BinarySensor *sensor, bool state) {
    if (sensor != nullptr && (!sensor->has_state() || sensor->state != state))
      sensor->publish_state(state);
  }

  void publish_value_(sensor::Sensor *sensor, float value) {
    if (sensor != nullptr && (!sensor->has_state() || sensor->state != value))
      sensor->publish_state(value);
  }

  void publish_string_(text_sensor::TextSensor *sensor, const std::string &value) {
    if (sensor != nullptr && (!sensor->has_state() || sensor->state != value))
      sensor->publish_state(value);
  }

  void read_uart_(uart::UARTComponent *uart, std::vector<uint8_t> &buffer) {
    int count = 0;
    while (uart->available() && count < 64) {
      uint8_t byte;
      uart->read_byte(&byte);
      buffer.push_back(byte);
      count++;
    }
    if (buffer.size() > 150)
      buffer.clear();
  }

  void process_buffer_(std::vector<uint8_t> &buffer, uint8_t data_len) {
    size_t packet_size = 2 + data_len + 1;
    while (buffer.size() > 0) {
      if (buffer[0] != 0x55) {
        buffer.erase(buffer.begin());
        continue;
      }
      if (buffer.size() < 2)
        return;
      if (buffer[1] != data_len) {
        buffer.erase(buffer.begin());
        continue;
      }
      if (buffer.size() < packet_size)
        return;

      uint8_t checksum = 0;
      for (size_t i = 0; i < data_len; i++) {
        checksum += buffer[2 + i];
      }

      if (checksum != buffer[packet_size - 1]) {
        buffer.erase(buffer.begin());
        continue;
      } else {
        if (data_len == 0x1f)
          parse_tx_packet_(buffer);
        if (data_len == 0x10)
          parse_rx_packet_(buffer);

        uint8_t source = (data_len == 0x1f) ? 0x01 : 0x02;
        send_debug_packet_(buffer, packet_size, source);
        buffer.erase(buffer.begin(), buffer.begin() + packet_size);
      }
    }
  }

  void parse_tx_packet_(std::vector<uint8_t> &buffer) {
    uint8_t *data = buffer.data();
    publish_binary_(door_open_, data[13] & 0x08);
    publish_binary_(low_rinse_aid_, data[13] & 0x10);
    publish_binary_(low_salt_, data[13] & 0x20);
    publish_binary_(extra_dry_, data[15] & 0x02);
    publish_value_(time_remaining_, data[5]);
    publish_value_(water_temperature_, (data[8] * 2) + 20);
    publish_value_(water_hardness_, data[16]);
    publish_binary_(overflow_error_, data[10] == 0x04);
    publish_binary_(intake_error_, data[10] == 0x01);
    publish_value_(error_, data[10]);
    publish_binary_(program_end_, data[12] == 0x34);

    std::string program;
    switch (data[11]) {
      case 0x02: program = "Intensive"; break;
      case 0x03: program = "Universal"; break;
      case 0x04: program = "ECO"; break;
      case 0x05: program = "Glass"; break;
      case 0x06: program = "90-Min"; break;
      case 0x07: program = "Rapid"; break;
      case 0x10: program = "Self-Clean"; break;
      default: program = "Unknown"; break;
    }
    publish_string_(current_program_, program);
  }

  void parse_rx_packet_(std::vector<uint8_t> &buffer) {
    uint8_t *data = buffer.data();
    uint16_t delay_val = data[12] | (static_cast<uint16_t>(data[13]) << 8);
    publish_value_(start_delay_, delay_val);
    publish_binary_(child_lock_, data[15] & 0x08);
  }
};

}
} 