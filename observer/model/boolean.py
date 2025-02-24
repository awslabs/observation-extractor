# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from pydantic import BaseModel


class Boolean(BaseModel):
    """Data class for unpacking boolean results"""
    result: bool

class Booleans(BaseModel):
    """Data class to support a list of booleans as the return type"""
    results: list[bool]