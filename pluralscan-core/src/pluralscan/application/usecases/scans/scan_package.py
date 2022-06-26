import pathlib
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from pluralscan.application.processors.executables.exec_runner import (
    AbstractExecRunnerFactory,
    ExecRunnerOptions,
)
from pluralscan.application.processors.reports.report_processor import (
    AbstractReportProcessor,
)
from pluralscan.domain.diagnosis.diagnosis import Diagnosis
from pluralscan.domain.diagnosis.diagnosis_repository import AbstractDiagnosisRepository
from pluralscan.domain.executable.executable import Executable
from pluralscan.domain.executable.executable_action import ExecutableAction
from pluralscan.domain.executable.executable_repository import (
    AbstractExecutableRepository,
)
from pluralscan.domain.package.package import Package
from pluralscan.domain.package.package_repository import AbstractPackageRepository
from pluralscan.domain.scans.scan import Scan
from pluralscan.domain.scans.scan_id import ScanId
from pluralscan.domain.scans.scan_repository import AbstractScanRepository
from pluralscan.domain.scans.scan_state import ScanState
from pluralscan.libs.utils.validable import Validable


@dataclass(frozen=True)
class ScanPackageCommand(Validable):
    """Run Analyzer Command"""

    scan_id: ScanId
    executable_action: ExecutableAction

    def __post_init__(self):
        if not self.scan_id:
            raise ValueError("A scan id must be defined.")


@dataclass
class ScanPackageResult:
    """Run Analyzer Result"""

    scan: Scan
    executable: Executable
    package: Package
    diagnosis: Diagnosis


class AbstractScanPackageUseCase(
    metaclass=ABCMeta
):  # pylint: disable=too-few-public-methods
    """AbstractScanPackageUseCase"""

    @abstractmethod
    def handle(self, command: ScanPackageCommand) -> ScanPackageResult:
        """Execute use case."""
        raise NotImplementedError


class ScanPackageUseCase(
    AbstractScanPackageUseCase
):  # pylint: disable=too-few-public-methods
    """ScanPackageUseCase"""

    def __init__(
        self,
        scan_repository: AbstractScanRepository,
        package_repository: AbstractPackageRepository,
        executable_repository: AbstractExecutableRepository,
        diagnosis_repository: AbstractDiagnosisRepository,
        exec_runner_factory: AbstractExecRunnerFactory,
        report_processor: AbstractReportProcessor,
    ):
        self._scan_repository = scan_repository
        self._package_repository = package_repository
        self._executable_repository = executable_repository
        self._diagnosys_repository = diagnosis_repository
        self._exec_runner_factory = exec_runner_factory
        self._report_processor = report_processor

    def handle(self, command: ScanPackageCommand) -> ScanPackageResult:
        # 1. Retrieve the scan aggregate.
        scan = self._scan_repository.find_by_id(command.scan_id)
        if scan is None:
            raise ValueError

        # 2. Retrieve executable used to perform code analysis.
        executable = self._executable_repository.find_by_id(scan.executable_id)
        if executable is None:
            raise ValueError

        # 3. Retrieve the package to analyze.
        package = self._package_repository.find_by_id(scan.package_id)
        if package is None:
            raise ValueError

        # 4. Execute analyzer process and wait for list of report files.
        arguments = [package.location]
        options = ExecRunnerOptions(executable, command.executable_action, arguments)
        process_result = self._exec_runner_factory.create(
            executable=executable, working_directory=scan.working_directory
        ).execute_with_report(options)
        if process_result.success is not True:
            raise RuntimeError

        # 5. Get list of report files to process.
        report_files = []
        for filepath in pathlib.Path(scan.working_directory).glob("**/*"):
            report_files.append(str(filepath))

        # 6. Transform reports into diagnosis.
        diagnosis = self._report_processor.transform_to_diagnosis(
            scan=scan, data=report_files
        )

        # 7. Persist diagnosis.
        diagnosis = self._diagnosys_repository.add(diagnosis)

        # 8. Update scan
        scan.state = ScanState.COMPLETED
        scan = self._scan_repository.update(scan)

        return ScanPackageResult(
            scan=scan, diagnosis=diagnosis, package=package, executable=executable
        )
