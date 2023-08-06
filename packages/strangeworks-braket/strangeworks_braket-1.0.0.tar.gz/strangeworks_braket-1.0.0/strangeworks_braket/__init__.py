"""Strangeworks Braket SDK"""
import importlib.metadata


__version__ = importlib.metadata.version("strangeworks-braket")


from .device import StrangeworksDevice  # noqa: F401
from .task import StrangeworksQuantumTask  # noqa: F401
