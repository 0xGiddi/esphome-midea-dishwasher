# Midea dishwasher ESPHome component

This is an experimental ESPHome component for getting status information from Midea/Electra dishwashers. All information is based on sniffing and analyzing of the main board and display board protocol.



---
**Notes to self**:


Packet: ------- H  L  B0 Bn CS \
TX=34 Bytes - 55 1F ..... XX \
RX=19 Bytes - 55 10 ..... XX

TX byte 13 3 - Door status: 1 open, 0 closed\
TX byte 13 5 - Rinse Aid status: 1 low, 0 full\
TX byte 13 4 - Salt status: 1 low, 0 full\
TX byte 15 1 - Extra Dry status: 1 on, 0 off\
\
RX byte 15 3 - Panel Lock status: 1 on, 0 off\
RX byte 12 - Start timer (min) low\
RX byte 13 - Start timer (min) high\
RX byte 16 - Water hardness setting\
\
TX byte 11 - Program Number: P1-2 Intensive, P2-3 Universal, \P3-4 ECO, P4-5 Glass, P5-6 90 Min, P6-7 Rapid, P7-10 Self Clean\
TX byte 05 - Program Time Remaining (min)\
TX byte 06 - Cycle Time Remaining (min)\
TX byte 16 - Water hardness setting\
TX byte 10 - Error 0-clear, 1-No water, 4-Leak sensor \(Assumed 3 heater problem)
\
\
TODO:\
- Timer started\
- Idle/Run/Finish indicator\
- Heater/Sprayer Pump/Drain Pump/Water Inlet indicator\
\
TX Byte 3: lsb=01 Timer on, 10 Timer unset? NO.\
TX Byte 8: Raw NTC value (val * 2 + 20 = deg C)\
TX Btye 12: Cycle Type? changes per cycle type? (Idle-32, \MainWash - 34, 35 - Rinse, 37-?, 32-Idle)




---