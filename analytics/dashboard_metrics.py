class DashboardMetrics:
    def __init__(self):
        self.metrics = {
            "documents": 0,
            "images": 0,
            "datasets": 0
        }

    def update(self, documents, images, datasets):
        self.metrics["documents"] = documents
        self.metrics["images"] = images
        self.metrics["datasets"] = datasets

    def summary(self):
        return self.metrics