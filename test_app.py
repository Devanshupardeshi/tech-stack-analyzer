import unittest
from app import analyze_tech_stack
from unittest.mock import patch, MagicMock

class TestAnalyzer(unittest.TestCase):
    
    @patch('app.requests.get')
    def test_nextjs_tailwind_detection(self, mock_get):
        # Mock HTML response
        mock_response = MagicMock()
        mock_response.text = '<html><head><script src="/_next/static/chunk.js"></script></head><body class="bg-blue-500 tailwind-loaded"></body></html>'
        mock_get.return_value = mock_response
        
        result = analyze_tech_stack('fake-startup.com')
        
        self.assertEqual(result['framework'], 'Next.js (React)')
        self.assertEqual(result['styling'], 'Tailwind CSS')
        
    @patch('app.requests.get')
    def test_analytics_detection(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html><script>gtag("js", new Date());</script></html>'
        mock_get.return_value = mock_response
        
        result = analyze_tech_stack('fake-startup.com')
        self.assertIn('Google Analytics', result['analytics'])

if __name__ == '__main__':
    unittest.main()
