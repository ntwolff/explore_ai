import unittest
from utils.service_registry import ServiceRegistry


class TestServiceRegistry(unittest.TestCase):

    def test_service_registration_and_retrieval(self):
        registry = ServiceRegistry()
        test_service = 'test_service_instance'
        registry.register_service('test_service', test_service)
        
        self.assertIs(registry.get_service('test_service'), test_service)
        self.assertIsNone(registry.get_service('nonexistent_service'))

    def test_unregister_service(self):
        registry = ServiceRegistry()
        test_service = 'test_service_instance'
        registry.register_service('test_service', test_service)
        registry.unregister_service('test_service')
        self.assertIsNone(registry.get_service('test_service'))

if __name__ == '__main__':
    unittest.main()