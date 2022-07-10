from pathlib import Path
from pluralscan.data.inmemory.analyzers.analyzer_repository import InMemoryAnalyzerRepository
from pluralscan.data.inmemory.analyzers.analyzer_seeder import InMemoryAnalyzerRepositorySeeder
from pluralscan.data.inmemory.executables.executable_repository import (
    InMemoryExecutableRepository,
)
from pluralscan.data.inmemory.executables.executable_seeder import (
    InMemoryExecutableRepositorySeeder,
)
from pluralscan.data.inmemory.packages.package_repository import (
    InMemoryPackageRepository,
)
from pluralscan.data.inmemory.packages.package_seeder import (
    InMemoryPackageRepositorySeeder,
)
from pluralscan.domain.executables.executable_action import ExecutableAction
from pluralscan.domain.executables.executable_id import ExecutableId
from pluralscan.domain.packages.package_id import PackageId

import pytest
from __tests__.test_helpers import REPORTS_DIR
from pluralscan.application.processors.executables.exec_runner import ExecRunnerOptions
from pluralscan.infrastructure.processor.executables.roslynator_exec_runner import (
    RoslynatorExecRunner,
)

@pytest.fixture
def memory_analyzer_repository():
    analyzer_repository = InMemoryAnalyzerRepository()
    InMemoryAnalyzerRepositorySeeder(analyzer_repository).seed()
    return analyzer_repository

@pytest.fixture
def memory_executable_repository(memory_analyzer_repository):
    executable_repository = InMemoryExecutableRepository()
    InMemoryExecutableRepositorySeeder(executable_repository, memory_analyzer_repository).seed()
    return executable_repository


@pytest.fixture
def memory_package_repository():
    package_repository = InMemoryPackageRepository()
    InMemoryPackageRepositorySeeder(package_repository).seed()
    return package_repository


def test_execute_with_output(
    memory_executable_repository: InMemoryExecutableRepository,
    memory_package_repository: InMemoryPackageRepository,
):
    # Arrange
    package = memory_package_repository.find_by_id(PackageId("AnalyzerTests"))
    executable = memory_executable_repository.find_by_id(ExecutableId("RoslynatorFork"))
    output_result_dir = Path.joinpath(REPORTS_DIR, "AnalyzerTests\ROSLYNATOR_RESULTS")
    report_path = str(Path.joinpath(output_result_dir, "RoslynatorResults.txt"))
    options = ExecRunnerOptions(executable, package, ExecutableAction.SCAN)
    process_runner = RoslynatorExecRunner(output_result_dir, report_path)

    # Act
    result = process_runner.execute_with_report(options)

    # Assert
    assert result is not None
    assert result.success is True


def test_execute(executable):
    options = ExecRunnerOptions(executable)
    process_runner = RoslynatorExecRunner()

    result = process_runner.execute(options)

    assert result is None
