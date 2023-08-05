# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2023 David Seaward and contributors

from carmine import cli


def test_invoke():
    result = cli.invoke()
    assert result is None
