import unittest
from unittest.mock import patch
from services.openai_assistant_service import OpenAIAssistantService


class TestOpenAIAssistantService(unittest.TestCase):

    @patch('services.openai_assistant_service.openai')
    def setUp(self, mock_openai):
        self.mock_openai_api_key = 'test_api_key'
        self.mock_assistant_id = 'test_assistant_id'
        self.service = OpenAIAssistantService(self.mock_openai_api_key, self.mock_assistant_id)
        self.mock_openai = mock_openai

    def test_create_thread(self):
        mock_thread_id = 'test_thread_id'
        self.mock_openai.OpenAI.create_beta_threads.create.return_value = {'id': mock_thread_id}
        
        thread_id = self.service.create_thread()
        
        self.mock_openai.OpenAI.create_beta_threads.create.assert_called_once()
        self.assertEqual(thread_id, mock_thread_id)

    def test_send_message(self):
        mock_thread_id = 'test_thread_id'
        mock_message = 'test_message'
        self.mock_openai.OpenAI.create_beta_messages.create.return_value = {'id': mock_message}
        message_id = self.service.send_message(mock_thread_id, mock_message)

        self.mock_openai.OpenAI.create_beta_messages.create.assert_called_once()
        self.assertEqual(message_id, mock_message)

if __name__ == '__main__':
    unittest.main()