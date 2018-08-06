#!/usr/bin/env python

import argparse

from lib.remote_actions import PuppetBaseAction

__all__ = [
    'PuppetLookupAction'
]


class PuppetLookupAction(PuppetBaseAction):

    def run(self, config=None, explain=False, node=None,
            facts=None, environment=None, merge=None,
            knock_out_prefix=None, sort_merged_arrays=False, merge_hash_arrays=False,
            explain_options=False, default=None, type=None, compile=False,
            keys=None):
        args = ['lookup']

        if config:
            args += ['--config={}'.format(config)]
        if explain:
            args += ['--explain']
        if node:
            args += ['--node={}'.format(node)]
        if facts:
            args += ['--facts={}'.format(facts)]
        if environment:
            args += ['--environment={}'.format(environment)]
        if merge:
            args += ['--merge={}'.format(merge)]
        if knock_out_prefix:
            args += ['--knock-out-prefix={}'.format(knock_out_prefix)]
        if sort_merged_arrays:
            args += ['--sort-merged-arrays']
        if merge_hash_arrays:
            args += ['--merge-hash-arrays']
        if explain_options:
            args += ['--explain-options']
        if default:
            args += ['--default={}'.format(default)]
        if type:
            args += ['--type={}'.format(type)]
        if compile:
            args += ['--compile']

        # run one command per key
        for k in keys:
            cmd = self._get_full_command(args=args + [k])
            self._run_command(cmd=cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run puppet lookup')
    parser.add_argument('--config', required=False)
    parser.add_argument('--explain', action='store_true', default=False, required=False)
    parser.add_argument('--node', required=False)
    parser.add_argument('--facts', required=False)
    parser.add_argument('--environment', required=False)
    parser.add_argument('--merge', required=False)
    parser.add_argument('--knock_out_prefix', required=False)
    parser.add_argument('--sort_merged_arrays', action='store_true', default=False,
                        required=False)
    parser.add_argument('--merge_hash_arrays', action='store_true', default=False,
                        required=False)
    parser.add_argument('--explain_options', action='store_true', default=False,
                        required=False)
    parser.add_argument('--default', required=False)
    parser.add_argument('--type', required=False)
    parser.add_argument('--compile', action='store_true', default=False,
                        required=False)
    parser.add_argument('keys', nargs='+')

    args = vars(parser.parse_args())
    action = PuppetRunAgentAction()
    action.run(**args)
