import argparse
from internal.exporter_factory import ExporterFactory
from internal.writer_factory import WriterFactory


def main(source, target):
    try:
        exporter = ExporterFactory.create_exporter(source)
        writer = WriterFactory.create_writer(target)
    except ValueError as e:
        print(str(e))
        return

    exporter.export(writer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='main',
        description='Export data from a source (file or PostgreSQL) to a target (file or PostgreSQL).'
    )

    parser.add_argument(
        '--source',
        help='Specify the link for the source. provide the source path or PostgreSQL connection string.'
    )

    parser.add_argument(
        '--target',
        help='Specify the link for the target. provide the target path or PostgreSQL connection string.'
    )

    args = parser.parse_args()
    if not args.source or not args.target:
        print("Error: Both source and target must be provided.")
        parser.print_help()
    else:
        main(args.source, args.target)