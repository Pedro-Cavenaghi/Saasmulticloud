from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self, status_code):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self._send_cors_headers(204)
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8')) if post_data else {}

            initial = float(body.get('initial', 0))
            monthly = float(body.get('monthly', 0))
            annual_rate = float(body.get('annualRate', 0.1))
            months = int(body.get('months', 60))

            if initial < 0 or monthly < 0 or months < 1:
                self.send_json(400, {'error': 'Parâmetros inválidos.'})
                return

            monthly_rate = (1 + annual_rate) ** (1 / 12) - 1
            balance = initial
            for _ in range(months):
                balance = balance * (1 + monthly_rate) + monthly

            invested = initial + (monthly * months)
            profit = balance - invested

            self.send_json(200, {
                'balance': round(balance, 2),
                'invested': round(invested, 2),
                'profit': round(profit, 2),
            })

        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, status_code, payload):
        response_data = json.dumps(payload).encode('utf-8')
        self._send_cors_headers(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_data)))
        self.end_headers()
        self.wfile.write(response_data)