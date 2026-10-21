"""Command-line entrypoint: `uv run ndhu-course-rush --name Alice`.

Wires the layers together: read config, set up logging (run id, files in DATA_DIR/logs),
call the service, print the result. Only entrypoints may `print`; everything else logs.
"""

from __future__ import annotations

import argparse
import logging

from ndhu_course_rush.config.logging_setup import setup_logging
from ndhu_course_rush.config.settings import load_config
from ndhu_course_rush.domain.models import GreetingRequest
from ndhu_course_rush.services.greeting import create_greeting

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, run the greeting service and print the message.

    Args:
        argv: Command-line arguments; defaults to `sys.argv[1:]`.

    Returns:
        Process exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description="ndhu-course-rush command-line interface")
    parser.add_argument("--name", default="", help="Name of the user to greet")
    args = parser.parse_args(argv)
    config = load_config()
    setup_logging(config.log_level, config.logs_dir if config.log_to_file else None)
    logger.info("cli start args=%s env=%s data_dir=%s", vars(args), config.app_env, config.data_dir)
    result = create_greeting(GreetingRequest(user_name=args.name), config)
    logger.info("cli done env=%s", result.environment)
    print(result.message)  # the CLI's real output (stdout); logs go to stderr / files
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
