class SourceTracker:
    def __init__(self):
        self.sources = []

    def add_source(
        self,
        source,
        version,
        publication_date,
        reviewed_by,
        approval_status
    ):
        self.sources.append({
            "source": source,
            "version": version,
            "publication_date": publication_date,
            "reviewed_by": reviewed_by,
            "approval_status": approval_status
        })

    def get_sources(self):
        return self.sources