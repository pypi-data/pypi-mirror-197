import requests, os, json, socket
from dotenv import load_dotenv
load_dotenv()

COLOR_TYPE = {
  "ERROR": "\033[31m",
  "DEBUG": "\033[36m",
  "INFO": "\033[32m",
  "END": "\033[0m"
}

class _Logger:
    def __init__(self) -> None:
        self.host = socket.gethostname()
        self.region = os.environ.get('LOGGER_REGION', '')
        self.app_name = os.environ.get('LOGGER_APP_NAME', '')
        self.app_type = os.environ.get('LOGGER_APP_TYPE', '')
        self.DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', None)
        self.LOG_TYPE = self._parse_log_type(os.environ.get('LOG_TYPE', None))

    def _parse_log_type(self, t):
      if (
        t == 'CONSOLE'
        or t == 'DISCORD'
      ): return t
      return 'CONSOLE'

    def _send_message(self, msg, decorators, log_type):
      if self.LOG_TYPE == 'CONSOLE':
        print(
          f"\n{decorators}\033[1m[{self.region} > {self.app_type} > {self.app_name} > {self.host}]\033[0m \n{COLOR_TYPE[log_type]}\n{msg}{COLOR_TYPE['END']}\n"
        )
        return True

      if self.DISCORD_WEBHOOK is None:
        raise ValueError("DISCORD WEBHOOK missing")

      __msg__ = json.dumps({
        "content": f"**{decorators}\n[{self.region} > {self.app_type} > {self.app_name} > {self.host}]** \n```{msg}```"
      })

      __r__ = requests.post(
        self.DISCORD_WEBHOOK,
        data=__msg__,
        headers={"Content-Type": "application/json"}
      )

      return (
        __r__.status_code == 200
        or __r__.status_code == 204
      )

    def error(self, msg):
      return self._send_message(
        msg,
        "🚨️ ERROR 🚨️",
        log_type='ERROR'
      )

    def debug(self, msg):
      return self._send_message(
        msg,
        "🐞️ DEBUG 🐞️",
        log_type='DEBUG'
      )

    def info(self, msg):
      return self._send_message(
        msg,
        "✅️️ INFO ✅️️",
        log_type='INFO'
      )

logger = _Logger()