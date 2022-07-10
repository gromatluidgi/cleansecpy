from pathlib import Path

import pytest
from pluralscan.domain.analyzer.analyzer_id import AnalyzerId
from pluralscan.domain.diagnosis.diagnosis_id import DiagnosisId
from pluralscan.infrastructure.processor.reports.sarif_report_processor import (
    SarifReportProcessor,
)

@pytest.mark.parametrize("analyzer_id", [AnalyzerId("Test"), None])
def test_transform_to_diagnosys(analyzer_id):
    path = Path.joinpath(Path(__file__).parent, "fixtures/NodeGoat.sarif")
    processor = SarifReportProcessor()

    diagnosis = processor.transform_to_diagnosis(analyzer_id, DiagnosisId("test"), [path])

    assert diagnosis is not None

@pytest.mark.parametrize("analyzer_id", [AnalyzerId("Test"), None])
def test_read_report(analyzer_id):
    path = Path.joinpath(Path(__file__).parent, "fixtures/NodeGoat.sarif")
    processor = SarifReportProcessor()

    issues = processor._read_report(path, analyzer_id)

    assert issues is not None
