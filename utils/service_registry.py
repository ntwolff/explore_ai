class ServiceRegistry:
    def __init__(self):
        self.services = {}

    def register_service(self, key, service):
        self.services[key] = service

    def get_service(self, key):
        return self.services[key]

# Instantiate the registry globally for access across different parts of the application
service_registry = ServiceRegistry()