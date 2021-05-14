import csv
import sys
import argparse

from charts.css import *
from charts.css import __version__


def _cell_2_float(cell):
    try:
        return float(cell)
    except:
        return cell

def main():
    supported_charts = {
        "bar": bar,
        "column": column,
        "line": line,
        "area": area,
        }
    legends = {
        "dot": Legend,
        "circle": LegendCircle,
        "ellipse": LegendEllipse,
        "square": LegendSquare,
        "rectangle": LegendRectangle,
        "rhombus": LegendRhombus,
        "line": LegendLine,
        }
    parser = argparse.ArgumentParser(
        description='Convert .csv into charts in html format.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-V", "--version", action='version',
        version='%(prog)s {ver}'.format(ver=__version__))
    parser.add_argument(
        'infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
        help="The filename of the CSV file. Default to STDIN.")
    parser.add_argument(
        'outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument(
        '--chart', nargs='?', default="column", choices=supported_charts.keys(),
        help="Chart type")
    parser.add_argument('--headers_in_first_row', action="store_true")
    parser.add_argument('--headers_in_first_column', action="store_true")
    parser.add_argument(
        '--legend', nargs='?', choices=legends.keys(), help="Legend type")
    parser.add_argument('--legend_inline', action="store_true")
    parser.add_argument('--stacked', action="store_true")
    parser.add_argument('--heading')
    parser.add_argument(
        '--secondary_axes',
        nargs='?', type=int, default=5, choices=SHOW_SECONDARY_AXES)
    parser.add_argument(
        '--data_spacing',
        nargs='?', type=int, default=20, choices=DATA_SPACING)
    parser.add_argument(
        '--datasets_spacing',
        nargs='?', type=int, default=5, choices=DATASETS_SPACING)
    parser.add_argument('--value_displayer', default="{}",
        help="A string template containing a pair of curly brackets, e.g. '${}K'")

    args = parser.parse_args()
    args.outfile.write(STYLESHEET + wrapper(supported_charts[args.chart](
        [list(map(_cell_2_float, row)) for row in csv.reader(args.infile)],
        headers_in_first_row=args.headers_in_first_row,
        headers_in_first_column=args.headers_in_first_column,
        legend=legends.get(args.legend),
        legend_inline=args.legend_inline,
        stacked=args.stacked,
        heading=args.heading,
        show_secondary_axes=args.secondary_axes,
        data_spacing=args.data_spacing,
        datasets_spacing=args.datasets_spacing,
        value_displayer=args.value_displayer.format,
        )))

if __name__ == "__main__":
    main()

