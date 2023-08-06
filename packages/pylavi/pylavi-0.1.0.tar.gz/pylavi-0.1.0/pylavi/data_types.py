"""
    Common data types for LabVIEW resources
"""


import ctypes
import re
import string
import struct


class Structure(ctypes.BigEndianStructure):
    """Common parent of all structures in the resource file"""

    def to_bytes(self):
        """Get the raw bytes as they are in the file"""
        data = ctypes.create_string_buffer(self.size())
        ctypes.memmove(data, ctypes.addressof(self), self.size())
        return data.raw

    def from_bytes(self, data: bytes, offset: int = 0):
        """Take raw bytes from the file and interpret them.
        offset - the offset in data to start parsing the bytes
        """
        size = self.size()
        subset = data[offset : offset + size]
        assert len(subset) >= size, f"Expected {size} bytes: found {len(subset)}"
        ctypes.memmove(ctypes.addressof(self), subset, size)
        return self

    def size(self) -> int:
        """the number of bytes in the file"""
        return ctypes.sizeof(self)

    def __str__(self) -> str:
        return self.to_string()


class FourCharCode(Structure):
    """Four-byte ascii code"""

    DISPLAYABLE = (string.ascii_letters + string.digits + " ").encode("ascii")
    _pack_ = 1
    _fields_ = [
        ("b1", ctypes.c_byte),
        ("b2", ctypes.c_byte),
        ("b3", ctypes.c_byte),
        ("b4", ctypes.c_byte),
    ]

    def __init__(self, value: str = None):
        if value is not None:
            value_bytes = value.encode("ascii")
            assert len(value_bytes) == 4
            kwargs = {
                "b1": value_bytes[0],
                "b2": value_bytes[1],
                "b3": value_bytes[2],
                "b4": value_bytes[3],
            }
        else:
            kwargs = {}

        super().__init__(**kwargs)

    def to_string(self):
        """Get the four characters as a string"""
        if any(
            (256 + b) % 256 not in FourCharCode.DISPLAYABLE
            for b in [self.b1, self.b2, self.b3, self.b4]
        ):
            return (
                f"x{(256 + self.b1)%256:02x}"
                + f"{(256 + self.b2)%256:02x}"
                + f"{(256 + self.b3)%256:02x}"
                + f"{(256 + self.b4)%256:02x}"
            )

        return bytes([self.b1, self.b2, self.b3, self.b4]).decode("ascii")

    def __repr__(self) -> str:
        return f"FourCharCode('{self.to_string()}')"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.to_string() == other

        if isinstance(other, bytes):
            return self.to_bytes() == other

        return (
            self.b1 == other.b1
            and self.b2 == other.b2
            and self.b3 == other.b3
            and self.b4 == other.b4
        )


class Version(Structure):
    """LabVIEW version number"""

    DEVELOPMENT = 1
    ALPHA = 2
    BETA = 3
    RELEASE = 4
    PHASES = "?dabf"
    PATTERN = re.compile(r"((\d+)(\.(\d+)(\.(\d+))?)?)(([abdfABDF]|{\d})(\d+)?)?")
    _pack_ = 1
    _fields_ = [
        ("bytes", ctypes.c_uint),
    ]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        major_or_str: any = None,
        minor: int = None,
        patch: int = None,
        phase: int = None,
        build: int = None,
    ):
        kwargs = {}

        if major_or_str is not None:
            if isinstance(major_or_str, str):
                final = Version.PHASES[Version.RELEASE]
                correct_format = Version.PATTERN.match(major_or_str)
                assert correct_format, f"Incorrect version string: '{major_or_str}'"
                assert minor is None
                assert patch is None
                assert phase is None
                assert build is None
                major = int(correct_format.group(2))
                minor = int(correct_format.group(4)) if correct_format.group(4) else 0
                patch = int(correct_format.group(6)) if correct_format.group(6) else 0
                phase_str = (
                    correct_format.group(8) if correct_format.group(8) else final
                )
                build = int(correct_format.group(9)) if correct_format.group(9) else 0

                if phase_str.startswith("{") and phase_str.endswith("}"):
                    phase = int(phase_str[1:-1])
                else:
                    phase = Version.PHASES.find(phase_str)

            elif isinstance(major_or_str, bytes):
                assert minor is None
                assert patch is None
                assert phase is None
                assert build is None
                kwargs = {
                    "bytes": int.from_bytes(major_or_str, "big"),
                }
            elif major_or_str <= 99:
                major = major_or_str
                minor = minor or 0
                patch = patch or 0
                phase = Version.RELEASE if phase is None else phase
                build = build or 0
            else:
                assert minor is None
                assert patch is None
                assert phase is None
                assert build is None
                kwargs = {
                    "bytes": major_or_str,
                }

            if not kwargs:
                assert major <= 99, major_or_str
                assert minor <= 9, major_or_str
                assert patch <= 9, major_or_str
                assert build <= 1999, major_or_str
                kwargs = {
                    "bytes": (
                        (int(major / 10) << 28)
                        + ((major % 10) << 24)
                        + (minor << 20)
                        + (patch << 16)
                        + (phase << 13)
                        + (int(build / 1000) << 12)
                        + (int(build % 1000 / 100) << 8)
                        + (int(build % 100 / 10) << 4)
                        + ((build % 10) << 0)
                    ),
                }

        super().__init__(**kwargs)

    def __lt__(self, other):
        if isinstance(other, Version):
            return self.bytes < other.bytes

        return self.bytes < Version(other).bytes

    def __eq__(self, other):
        if isinstance(other, Version):
            return self.bytes == other.bytes

        return self.bytes == Version(other).bytes

    def __hash__(self):
        return self.bytes

    def major(self):
        """get the major version"""
        return (self.bytes >> 28 & 0xF) * 10 + (self.bytes >> 24 & 0xF)

    def minor(self):
        """get the minor version"""
        return int(self.bytes >> 20 & 0xF)

    def patch(self):
        """get the patch version"""
        return int(self.bytes >> 16 & 0xF)

    def phase(self):
        """get the version phase"""
        return self.bytes >> 13 & 0x7

    def build(self):
        """get the build number"""
        return (
            1000 * (self.bytes >> 12 & 0x01)
            + 100 * (self.bytes >> 8 & 0xF)
            + 10 * int(self.bytes >> 4 & 0xF)
            + (self.bytes >> 0 & 0xF)
        )

    def to_string(self):
        """Get the version string"""
        major = self.major()
        minor = self.minor()
        patch = self.patch()
        phase = self.phase()
        build = self.build()
        version_string = str(major)

        if minor > 0 or patch > 0:
            version_string += f".{minor}"

            if patch > 0:
                version_string += f".{patch}"

        if phase != Version.RELEASE or build > 0:
            if Version.DEVELOPMENT <= phase <= Version.RELEASE:
                phase_str = Version.PHASES[phase]
            else:
                phase_str = f"{{{phase}}}"

            version_string += phase_str

            if build > 0:
                version_string += str(build)

        return version_string

    def __repr__(self) -> str:
        return f"Version('{self.to_string()}')"


class PString:
    """A byte-length prefixed string"""

    def __init__(self, data: bytes = b""):
        assert len(data) <= 255, f"data is {len(data)} bytes"
        self.string = data

    def to_bytes(self) -> bytes:
        """Get the raw bytes as they are in the file"""
        return struct.pack("B", len(self.string)) + self.string

    def from_bytes(self, data: bytes, offset: int = 0):
        """Take raw bytes from the file and interpret them.
        offset - the offset in data to start parsing the bytes
        """
        size = data[offset]
        self.string = data[offset + 1 : offset + 1 + size]
        assert (
            len(self.string) >= size
        ), f"Expected {size} bytes: found {len(self.string)}"
        return self

    def size(self) -> int:
        """the number of bytes in the file"""
        return 1 + len(self.string)

    def to_string(self) -> str:
        """Convert the string to a str"""
        return str(self.string)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return f"PString({self.to_string()})"

    def __eq__(self, other) -> bool:
        return self.string == other.string
