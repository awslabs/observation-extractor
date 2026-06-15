# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os

MODEL = os.environ.get(
    "OBSERVATION_EXTRACTOR_MODEL",
    "bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
)
MAX_TOKENS = int(os.environ.get("OBSERVATION_EXTRACTOR_MAX_TOKENS", "1024"))
