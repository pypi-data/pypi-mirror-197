import logging
import re
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Optional


def collect_requirements_txt(file: Path) -> Dict[str, Optional[str]]:
    requirements: Dict[str, Optional[str]] = {}

    # open file
    if file.is_file():
        # requirements file
        if file.name == 'requirements.txt':
            # open file
            with open(file) as file:
                # parse requirements
                for line in file:
                    match = re.match(r'^([A-Za-z0-9_-]+|git\+https://.*?)((==|~=|>=)(.+))?$', line.strip())
                    if not match:
                        raise ValueError(f'could not parse {file}')

                    package, version, _, _ = match.groups()
                    if package not in requirements:
                        requirements[package] = version
                    elif requirements[package] != version:
                        raise ValueError(f'{package} version {requirements[package]} conflicting with {version}')

    # open folder
    elif file.is_dir():
        # iterate over directory
        for f in sorted(file.iterdir()):
            # recursive calls
            rq = collect_requirements_txt(f)

            # merge requirements
            for package, version in rq.items():
                if package not in requirements:
                    requirements[package] = version
                elif requirements[package] != version:
                    raise ValueError(f'{package} version {requirements[package]} conflicting with {version}')

        # store in separate requirements.txt
        rq_file = file.joinpath('requirements.txt')
        if len(requirements) > 0 and not rq_file.exists():
            with open(rq_file, 'w') as f:
                for package, version in requirements.items():
                    f.write(package)
                    if version is not None:
                        f.write(version)
                    f.write('\n')

    return requirements


def collect_requirements_py(file: Path) -> List[str]:
    requirements: List[str] = []

    # open file
    if file.is_file():
        # requirements file
        if file.name == 'requirements.py':
            # open file
            with open(file) as file:
                # parse requirements
                for line in file:
                    # add lines that are not empty
                    line = line.strip()
                    if line and line not in requirements:
                        requirements.append(line)

    # open folder
    elif file.is_dir():
        # iterate over directory
        for f in sorted(file.iterdir()):
            # recursive calls
            rq = collect_requirements_py(f)

            # merge requirements
            for line in rq:
                if line not in requirements:
                    requirements.append(line)

        # store in separate requirements.py
        rq_file = file.joinpath('requirements.py')
        if len(requirements) > 0 and not rq_file.exists():
            with open(rq_file, 'w') as f:
                for line in requirements:
                    f.write(line)
                    f.write('\n')

    return requirements


def find_inline_tests(file: Path):
    # TODO find_inline_tests
    pass


def main():
    # parse command line arguments
    parser = ArgumentParser()

    parser.add_argument('folder', help='')
    parser.add_argument('-v', action='store_true', help='set logging level to INFO')

    args = parser.parse_args()

    # set logging
    level = logging.INFO if args.v else logging.WARNING
    logging.basicConfig(level=level, format='%(asctime)s %(name)s %(levelname)s: %(message)s')

    # get path
    path = Path(args.folder)

    # collect requirements
    collect_requirements_txt(path)
    collect_requirements_py(path)

    # check for tests
    find_inline_tests(path)


if __name__ == '__main__':
    main()
