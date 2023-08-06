"""
    Checks LabVIEW resource file(s) for given criteria
"""


import argparse
import fnmatch
import os
import queue
import sys
import threading

from pylavi.file import Resources
from pylavi.resource_types import Typevers, TypeLVSR, TypeBDPW
from pylavi.data_types import Version


def add_version_options(parser):
    """adds options related to LabVIEW version that saved the file"""
    parser.add_argument(
        "-l", "--lt", type=str, help="LabVIEW version must be less than this"
    )
    parser.add_argument(
        "-g", "--gt", type=str, help="LabVIEW version must be greater than this"
    )
    parser.add_argument("-e", "--eq", type=str, help="LabVIEW version must this")
    parser.add_argument(
        "-r",
        "--no-release",
        action="store_true",
        help="LabVIEW version must not be release",
    )
    parser.add_argument(
        "-b", "--no-beta", action="store_true", help="LabVIEW version must not be beta"
    )
    parser.add_argument(
        "-a",
        "--no-alpha",
        action="store_true",
        help="LabVIEW version must not be alpha",
    )
    parser.add_argument(
        "-d",
        "--no-development",
        action="store_true",
        help="LabVIEW version must not be development",
    )
    parser.add_argument(
        "-i",
        "--no-invalid",
        action="store_true",
        help="LabVIEW version must be a valid phase",
    )


def add_flag_options(parser):
    """add options for checking flags"""
    parser.add_argument("-c", "--no-code", action="count", help="Saved without code")
    parser.add_argument("--code", action="count", help="Saved with code")
    parser.add_argument(
        "--breakpoints", action="store_true", help="Not saved with breakpoints"
    )
    parser.add_argument(
        "--locked", action="count", help="File is locked (maybe with password)"
    )
    parser.add_argument("--not-locked", action="count", help="File is not locked")
    parser.add_argument(
        "--password-match", type=str, help="Ensure the password is exactly"
    )
    parser.add_argument(
        "--password", action="count", help="File is locked with a password"
    )
    parser.add_argument(
        "--no-password", action="count", help="File is not saved with a password"
    )
    parser.add_argument(
        "--clear-indicators", action="count", help="VI will clear indicators on run"
    )
    parser.add_argument(
        "--no-clear-indicators",
        action="count",
        help="VI will not clear indicators on run",
    )
    parser.add_argument("--run-on-open", action="count", help="VI will run when opened")
    parser.add_argument(
        "--no-run-on-open", action="count", help="VI will not run when opened"
    )
    parser.add_argument(
        "--suspend-on-run", action="count", help="VI will suspend on run"
    )
    parser.add_argument(
        "--no-suspend-on-run", action="count", help="VI will not suspend on run"
    )
    parser.add_argument("--debuggable", action="count", help="VI is debuggable")
    parser.add_argument("--not-debuggable", action="count", help="VI is not debuggable")
    parser.add_argument(
        "--autoerror",
        action="store_true",
        help="Not saved with auto error handling turned on",
    )


def parse_args(command_line=None):
    """Interpret command line arguments"""
    command_line = command_line or sys.argv[1:]
    parser = argparse.ArgumentParser(description="Validates LabVIEW resource files")
    add_version_options(parser)
    add_flag_options(parser)

    parser.add_argument(
        "--path-length",
        type=int,
        help="Maximum number of characters for the path",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        action="append",
        help="Path to scan for files (or a file path) (defaults to current directory)",
    )
    parser.add_argument(
        "-s",
        "--skip",
        type=str,
        action="append",
        help="Path to not scan for files (or a file to ignore)",
    )
    parser.add_argument(
        "-x",
        "--extension",
        type=str,
        action="append",
        help="File extensions to evaluate (defaults to all known)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        help="Reduce the output (multiple times reduces output more)",
    )
    args = parser.parse_args(args=command_line)
    args.path = args.path or ["."]
    args.skip = args.skip or []
    args.quiet = args.quiet or 0
    args.no_code = args.no_code or 0
    args.code = args.code or 0
    args.no_password = args.no_password or 0
    args.password = args.password or 0
    args.not_locked = args.not_locked or 0
    args.locked = args.locked or 0
    args.not_debuggable = args.not_debuggable or 0
    args.debuggable = args.debuggable or 0
    args.no_clear_indicators = args.no_clear_indicators or 0
    args.clear_indicators = args.clear_indicators or 0
    args.no_run_on_open = args.no_run_on_open or 0
    args.run_on_open = args.run_on_open or 0
    args.no_suspend_on_run = args.no_suspend_on_run or 0
    args.suspend_on_run = args.suspend_on_run or 0
    has_comparison = args.lt or args.gt or args.eq
    has_phase = (
        args.no_release
        or args.no_beta
        or args.no_alpha
        or args.no_development
        or args.no_invalid
    )
    has_code = args.no_code > 0 or args.code > 0
    has_locked = args.locked > 0 or args.not_locked > 0
    has_password = args.password > 0 or args.no_password > 0
    has_debuggable = args.debuggable > 0 or args.not_debuggable > 0
    has_binary = has_code or has_locked or has_password or has_debuggable
    has_other = (
        args.autoerror or args.breakpoints or args.password_match or args.path_length
    )

    if not has_comparison and not has_phase and not has_binary and not has_other:
        args.no_beta = True
        args.no_alpha = True
        args.no_development = True
        args.no_invalid = True
        args.path_length = 260

    if not args.extension:
        args.extension = Resources.EXTENSIONS

    return args


def find_files(found_queue, paths):
    """Find files in given paths and put them in the queue"""
    for path in paths:
        if os.path.isfile(path):
            found_queue.put(path)
        else:
            for root, _, files in os.walk(path):
                for file in files:
                    found_queue.put(os.path.join(root, file))

    found_queue.put(None)


def start_finding_files(paths):
    """Start the find_files function running in the background finding files"""
    found = queue.Queue()
    thread = threading.Thread(target=find_files, args=(found, paths), daemon=True)
    thread.start()
    return found


def validate_run(args, save_record: TypeLVSR, problems: list, next_path: str) -> bool:
    """validate run flags"""

    if (
        args.clear_indicators - args.no_clear_indicators < 0
        and save_record.clear_indicators()
    ):
        problems.append(("clear indicators", "", next_path))
        return True

    if args.run_on_open - args.no_run_on_open > 0 and not save_record.run_on_open():
        problems.append(("no run on open", "", next_path))
        return True

    if args.run_on_open - args.no_run_on_open < 0 and save_record.run_on_open():
        problems.append(("run on open", "", next_path))
        return True

    if (
        args.suspend_on_run - args.no_suspend_on_run > 0
        and not save_record.suspend_on_run()
    ):
        problems.append(("no suspend on run", "", next_path))
        return True

    if (
        args.suspend_on_run - args.no_suspend_on_run < 0
        and save_record.suspend_on_run()
    ):
        problems.append(("suspend on run", "", next_path))
        return True

    return False


def validate_code(args, save_record: TypeLVSR, problems: list, next_path: str) -> bool:
    """Validates if the separate code flags matches the command line arguments"""

    if args.code - args.no_code > 0 and save_record.separate_code():
        problems.append(("no code", "", next_path))
        return True

    if args.code - args.no_code < 0 and not save_record.separate_code():
        problems.append(("has code", "", next_path))
        return True

    if (
        args.clear_indicators - args.no_clear_indicators > 0
        and not save_record.clear_indicators()
    ):
        problems.append(("no clear indicators", "", next_path))
        return True

    if args.debuggable - args.not_debuggable > 0 and not save_record.debuggable():
        problems.append(("not debuggable", "", next_path))
        return True

    if args.debuggable - args.not_debuggable < 0 and save_record.debuggable():
        problems.append(("debuggable", "", next_path))
        return True

    return False


def validate_locked_password(
    args, save_record: TypeLVSR, password: TypeBDPW, problems: list, next_path: str
) -> bool:
    """Validates if the separate code flags matches the command line arguments"""
    if args.password_match and not password.password_matches(args.password_match):
        problems.append((f"password not {args.password_match}", "", next_path))
        return True

    if args.password - args.no_password > 0:
        if not save_record.locked() or not password.has_password():
            problems.append(("no password", "", next_path))
            return True

    if args.password - args.no_password < 0:
        if save_record.locked() and password.has_password():
            problems.append(("has password", "", next_path))
            return True

    if args.locked - args.not_locked > 0:
        if not save_record.locked():
            problems.append(("not locked", "", next_path))
            return True

    if args.locked - args.not_locked < 0:
        if save_record.locked():
            problems.append(("locked", "", next_path))
            return True

    return False


def validate_version(args, versions, problems, next_path):
    """Validates the version checking logic"""
    for version in versions:
        version_string = version.to_string()
        phase = version.phase()

        if args.gt and version < args.gt:
            problems.append((f"<{args.gt}", version_string, next_path))
            break

        if args.lt and not version < args.lt:
            problems.append((f">{args.lt}", version_string, next_path))
            break

        if args.eq and not version == args.eq:
            problems.append((f"!={args.eq}", version_string, next_path))
            break

        if args.no_release and phase == Version.RELEASE:
            problems.append(("no-release", version_string, next_path))
            break

        if args.no_beta and phase == Version.BETA:
            problems.append(("no-beta", version_string, next_path))
            break

        if args.no_alpha and phase == Version.ALPHA:
            problems.append(("no-alpha", version_string, next_path))
            break

        if args.no_development and phase == Version.DEVELOPMENT:
            problems.append(("no-development", version_string, next_path))
            break

        if args.no_invalid and (phase > Version.RELEASE or phase == 0):
            problems.append(("no-invalid", version_string, next_path))
            break


def validate(args, resources: Resources, problems: list, next_path: str):
    """Validate that the given resources file is valid"""
    version_resources = resources.get_resources("vers")
    save_record_resources = resources.get_resources("LVSR")
    password_resources = resources.get_resources("BDPW")
    assert len(save_record_resources) < 2
    versions = [Typevers().from_bytes(r[2]).version for r in version_resources]
    save_record = (
        TypeLVSR().from_bytes(save_record_resources[0][2])
        if save_record_resources
        else None
    )
    password_record = (
        TypeBDPW().from_bytes(password_resources[0][2]) if password_resources else None
    )
    problem_count = len(problems)
    invalid = False

    if save_record:
        versions.append(save_record.header.version)

    if not invalid and args.path_length and len(next_path) > args.path_length:
        problems.append(
            (f"path length {len(next_path)} > {args.path_length}", "", next_path)
        )
        invalid = True

    if not invalid and args.breakpoints and save_record:
        if save_record.has_breakpoints():
            number = save_record.breakpoint_count()
            plural = "" if number == 1 else "s"
            number = "" if number is None else f"{number} "
            problems.append((f"{number}breakpoint{plural} found", "", next_path))
            invalid = True

    if (
        not invalid
        and args.autoerror
        and save_record
        and save_record.auto_error_handling()
    ):
        problems.append(("auto error handling turned on", "", next_path))
        invalid = True

    if not invalid and save_record_resources:
        invalid = validate_code(args, save_record, problems, next_path)

    if not invalid and save_record_resources:
        invalid = validate_run(args, save_record, problems, next_path)

    if not invalid and save_record_resources and password_record:
        invalid = validate_locked_password(
            args, save_record, password_record, problems, next_path
        )

    if not invalid:
        validate_version(args, versions, problems, next_path)

    if len(problems) > problem_count and args.quiet < 1:
        print(
            f"FAIL: {problems[-1][0]} saved in version {problems[-1][1]}: {problems[-1][2]}"
        )


def should_skip(args, path):
    """Determine if the file should be skipped"""
    if os.path.splitext(path)[1] not in args.extension:
        return True

    return any(fnmatch.fnmatch(path, p) for p in ([] if not args.skip else args.skip))


def find_problems(args, files):
    """Searchs for problems files and returns them"""
    problems = []

    while True:
        next_path = files.get()

        if next_path is None:
            break

        if should_skip(args, next_path):
            continue

        try:
            validate(args, Resources.load(next_path), problems, next_path)

        except AssertionError as error:
            problems.append((error, "", next_path))
            if args.quiet < 2:
                print(
                    f"FAIL: {problems[-1][0]} saved in version {problems[-1][1]}: {problems[-1][2]}"
                )

    return problems


def main(args=None):
    """run the (dis)assembler"""
    args = args or parse_args()
    files = start_finding_files(args.path)
    problems = find_problems(args, files)

    if len(problems) > 0 and args.quiet < 3:
        print(f"{len(problems)} problems encounted")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(parse_args()))
