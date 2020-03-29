"""
This file contains all the functionality required to generate C code from our
.dbc file
"""
import logging
import sys
import argparse

from scripts.utilities.supported_boards import get_board_names
from scripts.codegen.CAN.cantools_codegen import *
from scripts.codegen.CAN.canrx_codegen import *
from scripts.codegen.CAN.cantx_codegen import *

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    supported_boards = get_board_names()
    parser.add_argument(
        '--board',
        help='Choose one of the following: ' + ' '.join(supported_boards))
    parser.add_argument(
        '--app_can_tx_source_output',
        help='Path to the output CAN TX source file for the App layer')
    parser.add_argument(
        '--app_can_tx_header_output',
        help='Path to the output CAN TX header file for the App layer')
    parser.add_argument(
        '--io_can_tx_source_output',
        help='Path to the output CAN TX source file for the IO layer')
    parser.add_argument(
        '--io_can_tx_header_output',
        help='Path to the output CAN TX header file for the IO layer')
    parser.add_argument(
        '--io_can_rx_source_output',
        help='Path to the output CAN RX source file for the IO layer')
    parser.add_argument(
        '--io_can_rx_header_output',
        help='Path to the output CAN RX header file for the IO layer')
    parser.add_argument(
        '--cantools_source_output',
        help='Path to the output source file generated by cantools '
             'for the APP layer')
    parser.add_argument(
        '--cantools_header_output',
        help='Path to the output header file generated by cantools '
             'for the APP layer')
    parser.add_argument(
        '--dbc',
        help='Path to the DBC file')
    args = parser.parse_args()
    if args.board not in supported_boards:
        print('Error: Invalid board name. Valid options: '
              + ' '.join(supported_boards))
        sys.exit(1)

    # Configure logging level
    logging.basicConfig(level=logging.DEBUG)

    # DBC name without the file extension
    database_name = os.path.basename(args.dbc).replace('.dbc', '')

    # Load DBC in preparation of cantools
    database = load_file(args.dbc, database_format="dbc")
    for msg in list(msg for msg in map(Message, database.messages)):
        for signal in msg.signals:
            # We don't worry about non-periodic messages because those aren't
            # store in a global table and thus don't have race condition.
            if signal.type_length > 32 and msg.cycle_time != 0:
                raise Exception(
                    "[%s] -> [%s] must be less than 32-bit to ensure atomic access on our 32-bit microcontrollers!"
                    % (msg.snake_name, signal.snake_name))

    # Generate CAN TX code for the App layer
    app_cantx_source = AppCanTxSourceFileGenerator(
        database=database,
        output_path=args.app_can_tx_source_output,
        sender=args.board,
        function_prefix='App_CanTx')
    app_cantx_source.generateSource()
    app_cantx_header = AppCanTxHeaderFileGenerator(
        database=database,
        output_path=args.app_can_tx_header_output,
        sender=args.board,
        function_prefix='App_CanTx')
    app_cantx_header.generateHeader()

    # Generate CAN TX code for the IO layer
    io_cantx_source = IoCanTxSourceFileGenerator(
        database=database,
        output_path=args.io_can_tx_source_output,
        sender=args.board,
        function_prefix='Io_CanTx')
    io_cantx_source.generateSource()
    io_cantx_header = IoCanTxHeaderFileGenerator(
        database=database,
        output_path=args.io_can_tx_header_output,
        sender=args.board,
        function_prefix='Io_CanTx')
    io_cantx_header.generateHeader()

    # Generate CAN RX code for the IO layer
    io_canrx_source = CanRxSourceFileGenerator(
        database=database,
        output_path=args.io_can_rx_source_output,
        receiver=args.board,
        function_prefix='Io_CanRx')
    io_canrx_source.generateSource()
    io_canrx_header = CanRxHeaderFileGenerator(
        database=database,
        output_path=args.io_can_rx_header_output,
        receiver=args.board,
        function_prefix='Io_CanRx')
    io_canrx_header.generateHeader()

    # Generate code using cantools
    generate_cantools_c_code(
        database=database,
        database_name=database_name,
        source_path=args.cantools_source_output,
        header_path=args.cantools_header_output)