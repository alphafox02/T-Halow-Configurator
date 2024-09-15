# T-Halow Configurator

**T-Halow Configurator** is a command-line tool designed to interact with and configure LilyGO T-Halow devices over a serial connection. The tool allows users to send AT commands and receive device responses while handling continuous status updates without interrupting user input.

## Features
- Interactive command-line interface (CLI) for sending AT commands to T-Halow devices.
- Continuous status updates from the device are displayed without interrupting command input.
- Supports sending commands with real-time responses.
- Non-blocking input allows for seamless command input while the device streams status data.

## Prerequisites
- Python 3.x
- `pySerial` for serial communication

To install the required packages, run:

```bash
pip install pyserial
```

## Usage

### Command-Line Interface (CLI)

1. **Connect the T-Halow device** to your system using a serial connection (e.g., `/dev/ttyUSB0`).
2. **Run the tool** to interactively send commands and view status updates:

```bash
python3 t_halow_configurator.py --port /dev/ttyUSB0
```

3. **Sending AT commands**:
   - You can type AT commands directly in the terminal while the tool handles the continuous status stream from the device.
   - For example, to send an AT command to debug the low-level MAC layer:

   ```bash
   AT+SYSDBG=LMAC,0
   ```

4. **Predefined Command**:
   - To send a command directly when running the tool:

   ```bash
   python3 t_halow_configurator.py --port /dev/ttyUSB0 --command "AT+SYSDBG=LMAC,0"
   ```

5. **Exiting**:
   - To exit the interactive mode, press `Ctrl+D` or type `exit`.

## Supported AT Commands

The T-Halow Configurator supports all standard AT commands for configuring T-Halow devices. Examples include:

- `AT+MODE=ap/sta/group/apsta` - Set the working mode
- `AT+SSID=ssid_char` - Set the SSID
- `AT+KEYMGMT=WPA-PSK/NONE` - Set encryption mode
- `AT+PSK=psk_char` - Set encryption password
- `AT+PAIR=0/1` - Pairing control
- `AT+BSS_BW=1/2/4/8` - Set BSS bandwidth
- `AT+FREQ_RANGE=start,end` - Set working frequency range
- `AT+CHAN_LIST=freq1,freq2` - Set working channel list
- `AT+RSSI?` - Check RSSI (signal quality)
- `AT+CONN_STATE` - Check connection state
- `AT+TXPOWER=txpower` - Set max transmit power
- `AT+ACKTMO=timeout` - Set ACK timeout
- `AT+HEART_INT=interval` - Set heartbeat interval
- `AT+SYSDBG=LMAC,0` - Debug low-level MAC layer
- `AT+JOINGROUP=group_addr,AID` - Join a multicast group

## Troubleshooting

- **Device Not Found**: Ensure the correct serial port is specified (e.g., `/dev/ttyUSB0` for Linux).
- **No Response to Commands**: Make sure the device is properly connected and powered on.

---

*Configure your LilyGO T-Halow devices with ease using the T-Halow Configurator!*
