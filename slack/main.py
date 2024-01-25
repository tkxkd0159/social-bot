from lib import Slack, health_check

health_check()
app = Slack(token="xoxb-")  # bot token
