from nefertem.metadata.nefertem_reports import (
    NefertemProfile,
    NefertemReport,
    NefertemSchema,
)


class TestNefertemReports:
    def test_profile(self):
        data = NefertemProfile("test", "test", 1.0, {}, {})
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "stats": {},
            "fields": {},
        }
        assert data.to_dict() == expected_data

    def test_report(self):
        data = NefertemReport("test", "test", 1.0, {}, True, {})
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "constraint": {},
            "valid": True,
            "errors": {},
        }
        assert data.to_dict() == expected_data

    def test_schema(self):
        data = NefertemSchema("test", "test", 1.0, [])
        expected_data = {
            "lib_name": "test",
            "lib_version": "test",
            "duration": 1.0,
            "fields": [],
        }
        assert data.to_dict() == expected_data
