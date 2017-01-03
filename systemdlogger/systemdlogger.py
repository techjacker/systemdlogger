#!/usr/bin/env python3
import argparse
from systemdlogger.runner import Runner


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Exports systemd logs to different storage backends'
            ', eg cloudwatch/elasticsearch.'
        )
    )
    parser.add_argument(
        'config',
        type=str,
        help='path to config file'
    )
    args = parser.parse_args()

    runner = Runner(
        config_path=args.config
    )
    runner.run()


if __name__ == '__main__':
    main()
