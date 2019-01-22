import os
import random

import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class UserAgentMiddleware(object):
    def __init__(self):
        filepath = os.path.join(PROJECT_ROOT, 'crawler', 'user_agents.txt')
        self.user_agent_list = pd.read_csv(filepath, header=None, delimiter='\n').values.flatten()

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent
