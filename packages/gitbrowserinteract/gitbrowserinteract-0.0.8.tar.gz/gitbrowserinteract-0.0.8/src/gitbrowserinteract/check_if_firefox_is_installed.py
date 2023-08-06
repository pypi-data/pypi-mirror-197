"""Runs a bash command."""
import subprocess  # nosec

from typeguard import typechecked


@typechecked
def run_bash_command(*, bashCommand: str) -> None:
    """Runs a bash command.

    :param bashCommand: A string containing a bash command that can be executed.
    """
    # Verbose call.
    # subprocess.Popen(bashCommand, shell=True)
    # Silent call.
    # subprocess.Popen(
    # bashCommand, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    # )

    # Await completion:
    # Verbose call.
    # proc = subprocess.call(bashCommand, shell=True,stdout=subprocess.PIPE)
    # Silent call.
    # proc = subprocess.call(
    # bashCommand, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE
    # )

    # output = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
    with subprocess.Popen(  # nosec
        bashCommand, shell=True, stdout=subprocess.PIPE, bufsize=1
    ) as p:
        lines = []
        for line in iter(p.stdout.readline, b""):
            print(line)
            lines.append(line)
        p.stdout.close()
        p.wait()
        print("")

    # return output.decode("utf-8")
    return lines
