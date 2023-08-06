from __future__ import annotations

from typing import Optional, Union

import strangeworks as sw
from braket.annealing.problem import Problem
from braket.aws.aws_device import Device
from braket.circuits import Circuit
from braket.ir.openqasm import Program as OpenQasmProgram
from braket.tasks.quantum_task import QuantumTask

from strangeworks_braket.task import StrangeworksQuantumTask


class StrangeworksDevice(Device):
    def __init__(
        self,
        arn: str,
        name: Optional[str] = None,
        status: Optional[str] = None,
        slug: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(name, status)
        self.arn = arn
        self.slug = slug

    def run(
        self,
        task_specification: Union[Circuit, Problem, OpenQasmProgram],
        shots: Optional[int],
        *args,
        **kwargs,
    ) -> QuantumTask:
        """Run a task on the device.

        Parameters
        ----------
        task_specification: Union[Circuit, Problem, OpenQasmProgram]
            The task specification.
        shots: Optional[int]
            The number of shots to run the task for. Defaults to 1000.

        Returns
        -------
        task: QuantumTask (StrangeworksQuantumTask)
            The task that was run.
        """
        return StrangeworksQuantumTask.create(
            self.arn, task_specification, shots or 1000, *args, **kwargs
        )

    @staticmethod
    def get_devices(
        arns: Optional[list[str]] = None,
        names: Optional[list[str]] = None,
        statuses: Optional[list[str]] = None,
    ) -> list[StrangeworksDevice]:
        """Get a list of devices.

        Parameters
        ----------
        arns: Optional[list[str]
            Filter by list of device ARNs. Defaults to None.
        names: Optional[list[str]]
            Filter by list of device names. Defaults to None.
        statuses: Optional[list[str]]
            Filter by list of device statuses. Defaults to None.

        Returns
        -------
        devices: list[SwDevice]
            List of devices that match the provided filters.
        """
        backends = sw.backends(product_slugs=["amazon-braket"])
        devices = []
        for backend in backends:
            if arns and backend.remote_backend_id not in arns:
                continue
            if names and backend.name not in names:
                continue
            if statuses and backend.remote_status not in statuses:
                continue

            devices.append(
                StrangeworksDevice(
                    backend.remote_backend_id,
                    backend.name,
                    backend.remote_status,
                    backend.slug,
                )
            )

        return devices
