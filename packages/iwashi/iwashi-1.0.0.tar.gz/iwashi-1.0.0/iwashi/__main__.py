import argparse
from .visitor import Result
from .iwashi import visit
from .helper import print_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action='store_true')
    parser.add_argument('-url', type=str, required=False)
    args = parser.parse_args()
    if args.server:
        from .server import server
        server.run_server()
    else:
        result = visit(args.url)
        assert result
        print('\n' * 4)
        print_result(result)


if __name__ == "__main__":
    main()
