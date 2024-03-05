import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import MLData

class APIServer(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/get_task':
            query_params = parse_qs(parsed_path.query)
            if 'new_material' in query_params and 'pages' in query_params and 'time' in query_params:
                try:
                    new_material = float(query_params['new_material'][0])
                    pages = float(query_params['pages'][0])
                    time = float(query_params['time'][0])
                    result = MLData.get_task(new_material, pages, time)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'result': str(result)}
                    self.wfile.write(json.dumps(response).encode())
                except ValueError:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing parameters. Please provide new_material, pages, and time.')
        elif parsed_path.path == '/get_score':
            query_params = parse_qs(parsed_path.query)
            if 'Q1' in query_params and 'Q2' in query_params and 'weights' in query_params:
                try:
                    Q1 = int(query_params['Q1'][0])
                    Q2 = [int(q) for q in query_params['Q2']]
                    weights = float(query_params['weights'][0])
                    result = MLData.get_score(Q1, Q2, weights)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'result': str(result)}
                    self.wfile.write(json.dumps(response).encode())
                except Exception as inst:
                    print(inst)
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Missing parameters. Please provide new_material, pages, and time.')
        elif parsed_path.path == "/get_rate":
            query_params = parse_qs(parsed_path.query)
            if 'task' in query_params and 'score' in query_params:
                try:
                    task = float(query_params['task'][0])
                    score = float(query_params['score'][0])
                    result = MLData.get_rate(task, score)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'result': str(result)}
                    self.wfile.write(json.dumps(response).encode())
                except (ValueError, TypeError):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
        elif parsed_path.path == "/get_next_interval":
            query_params = parse_qs(parsed_path.query)
            if 'weight' in query_params and 'weights' in query_params and 'rate' in query_params and 'daysLeft' in query_params:
                try:
                    weight = float(query_params['weight'][0])
                    weights = float(query_params['weights'][0])
                    rate = float(query_params['rate'][0])
                    daysLeft = float(query_params['daysLeft'][0])
                    result = MLData.get_next_interval(weight, weights, rate, daysLeft)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'result': result}
                    self.wfile.write(json.dumps(response).encode())
                except Exception as ar:
                    print(ar)
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
        elif parsed_path.path == "/get_habit":
            query_params = parse_qs(parsed_path.query)
            if 'Q3' in query_params and 'T1' in query_params and 'age' in query_params:
                try:
                    Q3 = [int(q) for q in query_params['Q3']]
                    T1 = [int(q) for q in query_params['T1']]
                    age = int(query_params['age'][0])
                    name, type, value, solution = MLData.get_habit(Q3, T1, age)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'name': name, 'type': type, 'value': value, 'solution': solution}
                    print(response)
                    self.wfile.write(json.dumps(response).encode())
                except (ValueError, TypeError):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
        elif parsed_path.path == "/get_grade":
            query_params = parse_qs(parsed_path.query)
            if 'count_task' in query_params and 'count_todos' in query_params and 'count_habits' in query_params \
                and "missed_events" in query_params and "events" in query_params and "reviewed" in query_params:
                try:
                    count_task = int(query_params['count_task'][0])
                    count_todos = int(query_params['count_todos'][0])
                    count_habits = int(query_params['count_habits'][0])
                    missed_events = int(query_params['missed_events'][0])
                    events = [int(q) for q in query_params['events']]
                    reviewed = bool(query_params['reviewed'][0])
                    result = MLData.get_grade(count_task, count_todos, count_habits, missed_events, events, reviewed)
                    response = {'result': str(result)}
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                except (ValueError, TypeError):
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Invalid parameters. Please provide valid numbers.')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Data not found"}).encode())

    def do_PUT(self):
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Data not found"}).encode())

    def do_DELETE(self):
        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Data not found"}).encode())

def run(server_class=HTTPServer, handler_class=APIServer, port=8282, address="0.0.0.0"):
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    print("Upload")
    run()
