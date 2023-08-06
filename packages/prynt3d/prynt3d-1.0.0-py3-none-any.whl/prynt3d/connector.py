import serial

import sys
import logging

from typing import List


class Connector:
    def __init__(self) -> None:
        self.filename = ""
        self.device = ""
    
    def load_file(self, filename: str) -> None:
        try:
            open(filename, "r").close()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} does not exist")
        
        self.filename = filename
    
    def set_device(self, device: str) -> None:
        self.device = device
    

    def send_file(self) -> None:
        if self.filename == "":
            raise ValueError("No file loaded")
        if self.device == "":
            raise ValueError("No device set")
        
        with open(self.filename, "r") as f:
            data = f.readlines()
        
        with serial.Serial(self.device, 115200) as ser:
            # Wait for the printer to boot
            while True:
                readline = ser.readline().decode("utf-8").strip()
                logging.debug(f"READ: {readline}")
                # print(f"READ: {readline}")
                if readline == "echo:SD init fail":
                    break
            
            for line in data:
                if line.startswith(";"):
                    continue

                line = line.split(";")[0]

                logging.debug(f"SEND: {line}")
                # print(f"SEND: {line}", file=sys.stderr)
                ser.write(f"{line.strip()}\r\n".encode("utf-8"))

                while True:
                    readline = ser.readline().decode("utf-8").strip()

                    logging.debug(f"READ: {readline}")
                    # print(f"READ: {readline}", file=sys.stderr)
                    if line.startswith("echo"):
                        print(readline)

                    if readline.strip() == "ok":
                        break


def _main(argc: int, argv: List[str]) -> int:
    if argc < 3:
        print("Usage: 3dprynt <device> <filename>", file=sys.stderr)
        return -1
    
    con = Connector()
    con.set_device(argv[1])
    con.load_file(argv[2])

    con.send_file()

    return 0
