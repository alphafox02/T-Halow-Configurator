import serial
import argparse
import threading
import time
import sys
import termios
import tty
import select

# Global flags to control output display and typing status
display_output = True
is_typing_command = False
is_waiting_for_response = False
command_response = ""

def read_serial(serial_port):
    """Reads from the serial port."""
    global display_output, is_typing_command, is_waiting_for_response, command_response
    while True:
        try:
            if serial_port.in_waiting > 0:
                data = serial_port.readline().decode('utf-8').strip()

                # Only show data if we are not typing a command or if we are capturing a response
                if is_waiting_for_response:
                    command_response += data + "\n"
                elif display_output:
                    # Print continuous status updates when not typing
                    print(f"\rStatus Update: {data}\n", end="")
                    sys.stdout.write("> " + input_command)  # Redraw the input line
                    sys.stdout.flush()

        except Exception as e:
            print(f"Error reading from serial port: {e}")

def write_serial(serial_port, command):
    """Writes a command to the serial port."""
    global is_waiting_for_response, command_response
    try:
        # Flush input buffer to clear old data
        serial_port.reset_input_buffer()

        # Send the command
        serial_port.write(command.encode('utf-8') + b'\r\n')
        print(f"\nSent: {command}")

        # Enable response capturing
        is_waiting_for_response = True
        command_response = ""

        # Give some time for the response to arrive
        time.sleep(0.5)

        # Disable response capturing after a short wait
        is_waiting_for_response = False

        # Display the command response
        if command_response:
            print(f"Command Response:\n{command_response}")
        else:
            print("No response or response couldn't be captured.")
    except Exception as e:
        print(f"Error sending command: {e}")

def non_blocking_input():
    """Handles non-blocking input, allowing continuous status updates."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        if select.select([sys.stdin], [], [], 0.1)[0]:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    global display_output, is_typing_command, input_command

    parser = argparse.ArgumentParser(description="Serial Command Line Tool with Input Pausing")
    parser.add_argument("--port", required=True, help="Serial port (e.g. /dev/ttyUSB0)")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baudrate (default: 115200)")
    parser.add_argument("--command", help="Command to send (optional)")

    args = parser.parse_args()

    # Open the serial port
    try:
        serial_port = serial.Serial(args.port, args.baudrate, timeout=1)
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    # Start a thread to read from the serial port
    reader_thread = threading.Thread(target=read_serial, args=(serial_port,))
    reader_thread.daemon = True
    reader_thread.start()

    if args.command:
        # Send the command if provided
        write_serial(serial_port, args.command)

    # Allow user to manually enter commands
    input_command = ""
    try:
        while True:
            key = non_blocking_input()

            if key:
                # Handle Ctrl+D for exit
                if key == '\x04':
                    break

                # When the user presses enter, send the command
                if key == '\n':
                    display_output = False  # Stop output while sending the command
                    write_serial(serial_port, input_command.strip())
                    input_command = ""
                    display_output = True  # Resume output after sending the command
                    print("\n> ", end="", flush=True)
                else:
                    # Pause the output when typing starts
                    display_output = False
                    input_command += key
                    sys.stdout.write(key)
                    sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        serial_port.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
