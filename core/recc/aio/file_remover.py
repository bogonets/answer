# -*- coding: utf-8 -*-

import os
import sys
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from io import StringIO
from recc.logging.logging import recc_common_logger as logger


async def remove_dir_from_subprocess(directory: str, verbose=False) -> None:
    assert os.path.isdir(directory)

    proc = await create_subprocess_exec(
        sys.executable,
        "-c",
        f"from shutil import rmtree; rmtree('{directory}');",
        stdout=PIPE,
        stderr=PIPE,
    )

    code = await proc.wait()
    if code == 0:
        return

    if not verbose:
        return

    error_report = StringIO(f"Removing failure (exit code is {code})\n")

    if proc.stdout:
        stdout_bytes = await proc.stdout.read()
        stdout_lines = stdout_bytes.decode("utf-8").strip()
        if stdout_lines:
            error_report.write(f"[STDOUT]\n{stdout_lines}\n")

    if proc.stderr:
        stderr_bytes = await proc.stderr.read()
        stderr_lines = stderr_bytes.decode("utf-8").strip()
        if stderr_lines:
            error_report.write(f"[STDERR]\n{stderr_lines}\n")

    logger.error(error_report.getvalue())


async def remove_files_from_subprocess(*files: str, verbose=False) -> None:
    if len(files) == 0:
        return

    if verbose:
        logger.debug(f"Remove legacy files (Total {len(files)} files)")

    for i, f in enumerate(files):
        if verbose:
            logger.debug(f"Removing {i}/{len(files)} '{f}' ...")

        try:
            if os.path.isdir(f):
                await remove_dir_from_subprocess(f, verbose)
            else:
                os.remove(f)
        except BaseException as e:
            logger.error(f"Removing exception: {e}")

    if verbose:
        logger.debug("Remove legacy files done")
