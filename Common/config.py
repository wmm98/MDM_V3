import os


class Config:
    project_path = path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    xml_report_path = os.path.join(project_path, "Report", "xml")
    html_report_path = os.path.join(project_path, "Report", "html")
    environment_properties_path = os.path.join(project_path, "Report", "environment.properties")
    debug_log_path = os.path.join(project_path, "Log", "Debug", "log.log")

