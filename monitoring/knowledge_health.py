class KnowledgeHealth:
    def __init__(self):
        self.status = {
            "documents": "Healthy",
            "datasets": "Healthy",
            "images": "Healthy"
        }

    def update_status(self, component, status):
        if component in self.status:
            self.status[component] = status

    def get_status(self):
        return self.status