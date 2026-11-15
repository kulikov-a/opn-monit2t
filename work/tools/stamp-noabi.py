#!/usr/bin/env python3
"""Restamp an OPNsense .pkg as ABI-independent (FreeBSD:*:*).

pkg(8) accepts that string on every FreeBSD major (fnmatch against the
running ABI). File payloads and their sha256 sums are left unchanged.
"""

import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

ABI = "FreeBSD:*:*"
ARCH = "freebsd:*:*"


def stamp(pkg_path: Path, descr_path: Path) -> None:
    with tarfile.open(pkg_path, "r:xz") as archive:
        members = archive.getmembers()
        payloads = {
            member.name: archive.extractfile(member).read() for member in members
        }

    manifest = json.loads(payloads["+MANIFEST"])
    compact = json.loads(payloads["+COMPACT_MANIFEST"])
    manifest["abi"] = compact["abi"] = ABI
    manifest["arch"] = compact["arch"] = ARCH
    if descr_path.is_file():
        manifest["desc"] = compact["desc"] = descr_path.read_text()

    for path, digest in manifest["files"].items():
        payload = payloads[path]
        expect = "1$" + hashlib.sha256(payload).hexdigest()
        if digest != expect:
            raise SystemExit(f"checksum mismatch for {path}")

    payloads["+MANIFEST"] = json.dumps(
        manifest, separators=(",", ":"), ensure_ascii=True
    ).encode()
    payloads["+COMPACT_MANIFEST"] = json.dumps(
        compact, separators=(",", ":"), ensure_ascii=True
    ).encode()

    tmp = pkg_path.with_suffix(".pkg.tmp")
    with tarfile.open(tmp, "w:xz", format=tarfile.USTAR_FORMAT) as out:
        for member in members:
            data = payloads[member.name]
            info = tarfile.TarInfo(member.name)
            info.size = len(data)
            info.mtime = member.mtime
            info.mode = member.mode
            info.uid = 0
            info.gid = 0
            info.uname = "root"
            info.gname = "wheel"
            info.type = tarfile.REGTYPE
            out.addfile(info, io.BytesIO(data))
    tmp.replace(pkg_path)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(f"usage: {sys.argv[0]} PACKAGE.pkg pkg-descr")
    stamp(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
