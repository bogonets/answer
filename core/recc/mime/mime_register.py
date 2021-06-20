# -*- coding: utf-8 -*-

import os
from typing import List
from recc.mime.mime_type import MimeType


def read_csv_mimes(csv_path: str, encoding="utf-8", start_line=1) -> List[MimeType]:
    result = list()
    with open(csv_path, "r", encoding=encoding) as f:
        for line in f.readlines()[start_line:]:
            items = line.split(",")
            if len(items) != 3:
                continue

            name = items[0].strip()
            template = items[1].strip()
            reference = items[2].strip()
            try:
                result.append(MimeType.parse(template, name, reference))
            except:  # noqa
                continue
    return result


def read_csv_mimes_by_default(name: str) -> List[MimeType]:
    csv_path = os.path.join(os.path.dirname(__file__), f"{name}.csv")
    try:
        return read_csv_mimes(csv_path)
    except BaseException as e:  # noqa
        return list()


TYPE_APPLICATION = "application"
TYPE_AUDIO = "audio"
TYPE_FONT = "font"
TYPE_EXAMPLE = "example"
TYPE_IMAGE = "image"
TYPE_MESSAGE = "message"
TYPE_MODEL = "model"
TYPE_MULTIPART = "multipart"
TYPE_TEXT = "text"
TYPE_VIDEO = "video"

REGISTERED_TYPES = (
    TYPE_APPLICATION,
    TYPE_AUDIO,
    TYPE_FONT,
    TYPE_EXAMPLE,
    TYPE_IMAGE,
    TYPE_MESSAGE,
    TYPE_MODEL,
    TYPE_MULTIPART,
    TYPE_TEXT,
    TYPE_VIDEO,
)
REGISTERED_MIMES = {t: read_csv_mimes_by_default(t) for t in REGISTERED_TYPES}
