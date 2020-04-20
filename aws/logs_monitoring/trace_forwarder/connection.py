from ctypes import cdll, Structure, c_char_p, c_int
import json
import os


class GO_STRING(Structure):
    _fields_ = [("p", c_char_p), ("n", c_int)]


def make_go_string(str):
    if not type(str) is bytes:
        str = str.encode("utf-8")
    return GO_STRING(str, len(str))


class TraceConnection:
    def __init__(self, root_url, api_key):
        dir = os.path.dirname(os.path.realpath(__file__))
        self.lib = cdll.LoadLibrary("{}/bin/trace-intake.so".format(dir))
        self.lib.Configure(make_go_string(root_url), make_go_string(api_key))

    def send_trace(self, trace_str, tags=""):
        had_error = (
            self.lib.ForwardTrace(make_go_string(trace_str), make_go_string(tags)) != 0
        )
        if had_error:
            raise Exception("Failed to send to trace intake")
