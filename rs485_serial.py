import serial
from time import sleep
import binascii

commands = {
    "header": "MJ",
    "status": "CS",
    "params": "PR",
    "timer": "TR",
    "params_list": {
        "01": (None, None),
        "03": (10, "rpm"),
        "04": (0.1, "A"),
        "05": (1, "°C"),
        "11": (10, "rpm"),
        "21": (1, "%"),
        "22": (1, "%"),
        "26": (1, "%"),
        "27": (1, "%"),
        "28": (1, "%"),
        "29": (1, "%"),
        "30": (1, "%")
    },
    "timer_list": {"01": (None, None)},
    "status_answer": {
        "NS": "stop",
        "NA": "acceleration",
        "NN": "normal",
        "NB": "deceleration",
        "FS": "failed_stop",
        "FF": "failed_free_run",
        "FR": "failed_regen_brake",
        "FB": "failed_deceleration"
    }
}


def add_checksum(command_str: str) -> bytes:
    """Adds a checksum to the end of a string by summing the ASCII codes of its characters.

    Args:
        command_str: A string to add a checksum to.

    Returns:
        bytearray with a checksum appended to it, in uppercase hexadecimal format.
    """
    # Convert each character of the string to its ASCII code, then to its hexadecimal representation.
    hex_codes = [hex(ord(char))[2:].zfill(2) for char in command_str]
    # Sum the hexadecimal codes as integers.
    checksum = hex(sum(int(h,
                           16) for h in hex_codes) & 0xff)[2:].zfill(2).upper()
    checksum_byte = bytes(checksum, 'utf-8')
    checksum_hex = str(binascii.hexlify(checksum_byte), 'ascii')
    # Append the checksum and CR to the original string.
    CR = '0d'
    hex_codes.append(checksum_hex + CR)
    hex_code_str = ''.join(hex_codes)
    return bytearray.fromhex(hex_code_str)


def ser_obj():
    return serial.Serial('COM4', baudrate=19200, bytesize=8,
                         parity=serial.PARITY_NONE, stopbits=1, timeout=0.5)


def check_status(station: int):
    header = commands["header"]
    function = commands["status"]
    # status_str = f"{header}{str(station).zfill(2)}{function}"
    # status_str = "MJ01PR03"
    listy = ["MJ01TR01", "MJ01PR03", "MJ01LS"]
    ser = ser_obj()
    for i in listy:
        status_command = add_checksum(i)

        # ser.open()
        ser.write(status_command)
        sleep(0.3)
        output = ser.read(10)
        print(output)
    ser.close()
    # return output


if __name__ == '__main__':

    # final_str = "MJ01PR03"
    # result = add_checksum(final_str)
    # print(result)
    # add_checksum(final_str)
    check_status(1)

