import os
from constant import CONFIG
from constant import ERRORS
class MESSAGES:
    # creates and returns the header
    def get_header(self, path, file_type, code):
        header = ""
        if code == 200:
            header += self.ok_header
        elif code == 0:
            header += self.close_header
            return header
        elif code == 400:
            header += self.bad_request_header
        elif code == 404:
            header += self.not_found_header
        elif code == 501:
            header += self.not_implemented_header
        else:
            header += self.server_error_header
        header += "\r\n"
        header += "Content-Type: " + CONFIG.content_types[file_type] + "\r\n"
        size = os.path.getsize(path)
        header += "Content-Length: " + str(size) + "\r\n\r\n"
        return header

    def __init__(self, http_format):
        self.bad_request_header = http_format + " 400 Bad Request"
        self.not_found_header = http_format + " 404 Not Found"
        self.not_implemented_header = http_format + " 501 Not Implemented"
        self.server_error_header = http_format + " 500 Internal Server Error"
        self.ok_header = http_format + " 200 OK"
        self.close_header = "Connection: close" + "\n\n"
        return
