class AuditReport:

    def validate_dataset(self, dataset):

        report = {
            "duplicates": 0,
            "missing_fields": 0,
            "broken_references": 0,
            "invalid_units": 0,
            "outdated_guidelines": 0,
            "quality_score": 100
        }

        return report

    def source_quality(self, source):

        trusted = {
            "WHO": 100,
            "CDC": 100,
            "NICE": 100,
            "FDA": 100,
            "ICMR": 100,
            "PubMed": 100
        }

        return trusted.get(source, "Rejected")