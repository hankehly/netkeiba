import json
import os
import random
from itertools import chain

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class UserAgentMiddleware(object):
    def __init__(self):
        file_path = os.path.join(PROJECT_ROOT, 'node_modules', 'crawler-user-agents', 'crawler-user-agents.json')
        crawler_user_agents = json.load(open(file_path, 'r'))
        multi_dim_list = [item['instances'] for item in crawler_user_agents]
        self.user_agent_list = list(chain.from_iterable(multi_dim_list))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent
