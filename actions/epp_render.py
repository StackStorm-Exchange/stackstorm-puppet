#!/usr/bin/env python

import argparse
import json
import os
import six
import sys


from lib.remote_actions import PuppetBaseAction

__all__ = [
    'PuppetEppRenderAction'
]


class PuppetEppRenderAction(PuppetBaseAction):

    def to_puppet_dsl(self, data):
        return json.dumps(data, separators=(',', '=>'))

    def run(self, env=None, cwd=None, puppet_cmd=None, settings=None,
            render_as=None, debug_=None, verbose=None, expression=None,
            facts=None, header=None, node=None, values=None, values_file=None,
            templates=None):
        args = ['epp', 'render']

        if settings:
            s = eval(settings)
            for k, v in six.iteritems(s):
                args += ['--{}={}'.format(k, v)]
        if render_as:
            args += ['--render-as={}'.format(render_as)]
        if verbose:
            args += ['--verbose']
        if debug_:
            args += ['--debug']
        if expression:
            args += ['--e={}'.format(expression)]
        if facts:
            args += ['--facts={}'.format(facts)]
        if header is not None:
            if header:
                args += ['--header']
            else:
                args += ['--no-header']
        if node:
            args += ['--node={}'.format(node)]
        if values:
            args += ['--values'] + [self.to_puppet_dsl(eval(values))]
        if values_file:
            args += ['--values_file={}'.format(values_file)]

        # add our list of templates
        args += eval(templates)
        cmd = self._get_full_command(args=args,
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
            sys.stdout.write(stdout)
        if stderr:
            sys.stderr.write(stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run puppet epp render')
    parser.add_argument('--puppet_cmd', required=False)
    parser.add_argument('--settings', required=False)

    parser.add_argument('--render_as', required=False)
    parser.add_argument('--debug_', action='store_true', default=False, required=False)
    parser.add_argument('--verbose', action='store_true', default=False, required=False)
    parser.add_argument('--expression', required=False)
    parser.add_argument('--facts', required=False)
    parser.add_argument('--header', action='store_true', default=False, required=False)
    parser.add_argument('--node', required=False)
    parser.add_argument('--values', required=False)
    parser.add_argument('--values_file', required=False)

    parser.add_argument('templates')

    args = vars(parser.parse_args())
    action = PuppetEppRenderAction()
    # inherit environment and cwd from the runner
    args['env'] = os.environ.copy()
    args['cwd'] = os.getcwd()
    action.run(**args)
