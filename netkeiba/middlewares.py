import os
import random

from . import settings


class UserAgentMiddleware(object):
    def __init__(self):
        filepath = os.path.join(settings.APP_DIR, 'user_agents.txt')

        with open(filepath) as f:
            self.user_agent_list = f.read().split('\n')

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent
