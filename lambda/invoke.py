import sys
from subprocess import check_call


def main():
    # TODO: Handle payload
    # --payload '{"min_date": "...", "shutdown": true}'
    check_call(['aws', 'lambda', 'invoke', '--function-name', 'startNetkeibaPipeline', '/dev/null'], stdout=sys.stdout)


if __name__ == '__main__':
    main()
