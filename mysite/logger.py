# import os
# from .settings import BASE_DIR

# log_level = "DEBUG"

# # List of apps
# APPS = ["taskManager"]

# # Ensure logs directory exists
# logs_dir = os.path.join(BASE_DIR, "logs")
# print(logs_dir,"----------------------------------------------------")
# os.makedirs(logs_dir, exist_ok=True)

# # Create directories for each app
# for directory in APPS:
#     dir_path = os.path.join(logs_dir, directory)
#     if not os.path.exists(dir_path):
#         os.makedirs(dir_path, exist_ok=True)
#         print(f"Log directory {dir_path} not found, creating now...")
#     else:
#         pass

# # Logging formatters
# FORMATTERS = {
#     "verbose": {
#         "format": '{"level": "%(levelname)s", "message": "%(message)s", "time": "%(asctime)s", "function": "%(funcName)s", "correlation_id": "%(correlation_id)s"}'
#     },
# }

# # Dynamic handlers and loggers
# HANDLERS = {
#     "console": {
#         "level": "INFO",
#         "class": "logging.StreamHandler",
#     },
# }
# LOGGERS = {}

# for app in APPS:
#     handler_name = f"{app}_handler"
#     log_file = os.path.join(logs_dir, app, f"{app}.log")

#     HANDLERS[handler_name] = {
#         "level": log_level,
#         "class": "logging.handlers.TimedRotatingFileHandler",
#         "filename": log_file,
#         "when": "midnight",
#         "interval": 1,
#         "backupCount": 2,
#         "formatter": "verbose",
#         "filters": ["correlation_id"],
#     }
 
#     LOGGERS[app] = {
#         "handlers": [handler_name, "console"],
#         "level": log_level,
#         "propagate": False,  # Prevents logs from being duplicated
#     }
 
# # Logging configuration
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": FORMATTERS,
#     "handlers": HANDLERS,
#     "loggers": LOGGERS,
#     "filters": {
#         "correlation_id": {"()": "django_guid.log_filters.CorrelationId"},
#     },
# }