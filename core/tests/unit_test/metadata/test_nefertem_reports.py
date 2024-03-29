from nefertem_core.metadata.report import NefertemProfile
from nefertem_inference.metadata.report import NefertemSchema
from nefertem_validation.metadata.report import NefertemReport


class TestNefertemReports:
    def test_profile(self):
        data = NefertemProfile("test", "test", 1.0, {}, {})
        expected_data = {
            "framework_name": "test",
            "framework_version": "test",
            "duration": 1.0,
            "stats": {},
            "fields": {},
            "metrics": [],
            "field_metrics": {},
        }
        assert data.to_dict() == expected_data

    def test_report(self):
        data = NefertemReport("test", "test", 1.0, {}, True, {})
        expected_data = {
            "framework_name": "test",
            "framework_version": "test",
            "duration": 1.0,
            "constraint": {},
            "valid": True,
            "errors": {},
        }
        assert data.to_dict() == expected_data

    def test_schema(self):
        data = NefertemSchema("test", "test", 1.0, [])
        expected_data = {
            "framework_name": "test",
            "framework_version": "test",
            "duration": 1.0,
            "fields": [],
        }
        assert data.to_dict() == expected_data
