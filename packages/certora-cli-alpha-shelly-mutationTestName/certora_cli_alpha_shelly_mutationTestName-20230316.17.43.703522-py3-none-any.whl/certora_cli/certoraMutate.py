import sys
import subprocess
from pathlib import Path
from typing import Optional, List
import site


def find_mutation_test_jar_in(path_strs: List[str]) -> Optional[Path]:
    for path_str in path_strs:
        python_pkg = Path(path_str)
        mutation_test_jar = python_pkg / "certora_jars" / "MutationTest.jar"
        if mutation_test_jar.exists():
            return mutation_test_jar
    return None


def gambit_entry_point(mutation_conf: str) -> None:
    paths_to_look_for = site.getsitepackages()
    paths_to_look_for.append(site.getusersitepackages())
    mutation_test_jar = find_mutation_test_jar_in(paths_to_look_for)
    if mutation_test_jar is None:
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
        sys.exit("Usage: certoraMutate CONFIG.conf. Missing conf file.")
    elif not Path(sys.argv[1]).exists():
        sys.exit("Conf file does not exist.")
    elif Path(sys.argv[1]).suffix != ".conf":
        sys.exit("Conf file must end with .conf extension.")
    gambit_entry_point(sys.argv[1])


if __name__ == '__main__':
    ext_gambit_entry_point()
