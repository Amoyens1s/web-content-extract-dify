#!/usr/bin/env python3
from dify_plugin import Plugin, DifyPluginEnv

plugin = Plugin(DifyPluginEnv())

if __name__ == '__main__':
    plugin.run()