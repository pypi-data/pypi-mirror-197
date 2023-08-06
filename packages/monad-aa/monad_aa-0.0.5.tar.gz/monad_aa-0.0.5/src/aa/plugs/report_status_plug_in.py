from collections import defaultdict

from aa.plugs.report_status_plug_point import ReportStatusPlugPoint

status_dict = {}


class ReportStatusPlugIn(ReportStatusPlugPoint):
    def __init__(self):
        pass

    @staticmethod
    def clear_all():
        global status_dict
        status_dict = defaultdict(dict)

    def save_status(self, report_id, status):
        status_dict[report_id] = status


def get_implementation():
    return ReportStatusPlugIn()
