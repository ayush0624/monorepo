import sys
import pytest

if __name__ == "__main__":
    pytest_args = ["--color=yes"]
    pytest_args.extend(sys.argv[1:])
    sys.argv = ["pytest"] + pytest_args

    retval = pytest.console_main()
    if retval != 0:
        raise SystemExit(retval)
