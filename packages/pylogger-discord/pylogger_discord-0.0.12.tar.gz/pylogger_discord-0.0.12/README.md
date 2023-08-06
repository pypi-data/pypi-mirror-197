# PyLogs

> This package allows you to send notifications to a channel using a POST request

## Configuration
```bash
# Specify the vars in your .env file

DISCORD_WEBHOOK=""
LOGGER_APP_NAME=""
LOGGER_APP_TYPE=""
LOGGER_REGION="
```

## Usage
```
from pylogs import logger

logger.debug("Hello from Python")
logger.info("Hello from Python")
logger.error("Hello from Python")

```