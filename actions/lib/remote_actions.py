import sys
import pipes
import subprocess

__all__ = [
    'PuppetBaseAction'
]


class PuppetBaseAction(object):
    PUPPET_BINARY = 'puppet'

    def _run_command(self, cmd, env=None, cwd=None, handle_result=True):
        cmd_string = ' '.join(pipes.quote(s) for s in cmd)
        sys.stderr.write('Running command "%s"\n' % (cmd_string))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   env=env,
                                   cwd=cwd)
        stdout, stderr = process.communicate()
        exit_code = process.returncode
        if handle_result:
            return self._handle_command_result(exit_code=exit_code, stdout=stdout,
                                               stderr=stderr)
        else:
            return exit_code, stdout, stderr

    def _get_full_command(self, args, puppet_cmd=None):
        if not puppet_cmd:
            puppet_cmd = self.PUPPET_BINARY
        cmd = [puppet_cmd] + args
        return cmd

    def _handle_command_result(self, exit_code, stdout, stderr):
        if exit_code == 0:
            sys.stderr.write('Command successfully finished\n')
        else:
            error = []

            if stdout:
                error.append(stdout)

            if stderr:
                error.append(stderr)

            error = '\n'.join(error)
            sys.stderr.write('Command exited with an error: %s\n' % (error))
        sys.exit(exit_code)
