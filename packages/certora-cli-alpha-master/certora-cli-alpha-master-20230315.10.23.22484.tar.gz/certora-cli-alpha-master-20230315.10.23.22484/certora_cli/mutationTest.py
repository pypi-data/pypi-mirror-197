import sys
import subprocess
from pathlib import Path
from distutils.sysconfig import get_python_lib


def gambit_entry_point(mutation_conf: str) -> None:
    python_pkg_path = Path(get_python_lib())
    mutation_test_jar = python_pkg_path / "certora_jars" / "MutationTest.jar"
    if not mutation_test_jar.exists():
        sys.exit("MutationTest.jar does not exist. Try to reinstall certora-cli.")
    try:
        exitcode = subprocess.run(["java", "-jar", str(mutation_test_jar), mutation_conf]).returncode
        if exitcode:
            raise Exception("MutationTest.jar execution failed, exitcode: ", exitcode)
    except Exception:
        print("Something went wrong when running mutation testing. Make sure you have the jar."
              " If not, reinstall certora-cli.")
    else:
        print("Successfully ran mutation testing.")


def ext_gambit_entry_point() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python mutationTest.py CONFIG.conf. Missing conf file.")
    elif not Path(sys.argv[1]).exists():
        sys.exit("Conf file does not exist.")
    elif Path(sys.argv[1]).suffix != ".conf":
        sys.exit("Conf file must end with .conf extension.")
    gambit_entry_point(sys.argv[1])


if __name__ == '__main__':
    ext_gambit_entry_point()
