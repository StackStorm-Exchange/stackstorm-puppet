#!/usr/bin/env python

import argparse
import json
import os
import sys
import six


from lib.remote_actions import PuppetBaseAction

__all__ = [
    'PuppetLookupAction'
]


class PuppetLookupAction(PuppetBaseAction):

    def run(self, env=None, cwd=None, puppet_cmd=None, settings=None, explain=False, node=None,
            facts=None, environment=None, merge=None,
            knock_out_prefix=None, sort_merged_arrays=False, merge_hash_arrays=False,
            explain_options=False, default=None, type=None, compile=False,
            render_as=None, keys=None):
        args = ['lookup']

        if settings:
            s = eval(settings)
            for k, v in six.iteritems(s):
                args += ['--{}={}'.format(k, v)]
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
        if render_as:
            args += ['--render-as={}'.format(render_as)]

        # run one command per key
        results = {}
        keys_list = eval(keys)
        for key in keys_list:
            cmd = self._get_full_command(args=(args + [key]),
                                         puppet_cmd=puppet_cmd)
            exit_code, stdout, stderr = self._run_command(cmd=cmd,
                                                          env=env,
                                                          cwd=cwd,
                                                          handle_result=False)
            success = False if exit_code else True
            if not success:
                sys.stdout.write(stdout)
                sys.stderr.write(stderr)
                exit(exit_code)

            if stdout:
                if render_as == 'json':
                    results[key] = json.loads(stdout)
                else:
                    results[key] = stdout
            if stderr:
                sys.stderr.write(stderr)

        if len(keys_list) > 1:
            sys.stdout.write(json.dumps(results))
        else:
            sys.stdout.write(json.dumps(results[keys_list[0]]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run puppet lookup')
    parser.add_argument('--puppet_cmd', required=False)
    parser.add_argument('--settings', required=False)
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
    parser.add_argument('--render_as', required=False)
    parser.add_argument('keys')

    args = vars(parser.parse_args())
    action = PuppetLookupAction()
    # inherit environment and cwd from the runner
    args['env'] = os.environ.copy()
    args['cwd'] = os.getcwd()
    action.run(**args)
