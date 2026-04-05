"""Pytest shared configuration for the repository.

This file provides a fallback async test runner for environments where
``pytest-asyncio`` is not installed. If the plugin is present, pytest keeps
its native behavior.
"""

from __future__ import annotations

import asyncio
import inspect

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser: pytest.Parser) -> None:
    """Declare asyncio_mode ini option when pytest-asyncio is absent."""
    parser.addini("asyncio_mode", "Compatibility option for async test mode.", default="auto")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Register async marker to avoid unknown-mark warnings."""
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as asynchronous (handled by pytest-asyncio or local fallback).",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem: pytest.Function) -> bool | None:
    """Run async tests when pytest-asyncio plugin is unavailable."""
    pluginmanager = pyfuncitem.config.pluginmanager
    if pluginmanager.hasplugin("asyncio") or pluginmanager.hasplugin("pytest_asyncio"):
        return None

    if not inspect.iscoroutinefunction(pyfuncitem.obj):
        return None

    funcargs = {
        arg: pyfuncitem.funcargs[arg]
        for arg in pyfuncitem._fixtureinfo.argnames
        if arg in pyfuncitem.funcargs
    }
    asyncio.run(pyfuncitem.obj(**funcargs))
    return True
