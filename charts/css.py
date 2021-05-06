from typing import List, Optional, Tuple, Callable

__version__ = "0.1.0"


class Legend:  # https://chartscss.org/components/legend/
    _shape = ""
    def __init__(self, legends: List[str], inline=None):
        self._legends = legends
        self._inline = inline  # True if inline is None else inline
    def __str__(self):
        return "<ul class='charts-css legend {} {}'>{}</ul>".format(
            self._shape,
            "legend-inline" if self._inline else "",
            "".join("<li>{}</li>".format(legend) for legend in self._legends))

class LegendCircle(Legend):
    _shape = "legend-circle"

class LegendEllipse(Legend):
    _shape = "legend-ellipse"

class LegendSquare(Legend):
    _shape = "legend-square"

class LegendRectangle(Legend):
    _shape = "legend-rectangle"

class LegendRhombus(Legend):
    _shape = "legend-rhombus"

class LegendLine(Legend):
    _shape = "legend-line"


def _chart(
    rows: list,
    _type,
    *,
    headers_in_first_row=False,
    headers_in_first_column=False,
    legend: Optional[Legend] = None,  # https://chartscss.org/components/legend/

    _series_upper_bound: Optional[Callable[[], int]] = None,  # https://chartscss.org/components/stacked/#simple-vs-percentage
    value_displayer=lambda value: value,
    stacked=False,  # Only applicable to bar and column charts. https://chartscss.org/components/stacked/

    wrapper_id=None,
    heading: str = None,
    hide_data=False,
    show_data_on_hover=False,
    reverse=False,  # https://chartscss.org/components/orientation/#reverse-orientation

    # https://chartscss.org/components/reverse-order/
    reverse_data=False,
    reverse_datasets=False,

    primary_axis=None, #show_primary_axis=False,
    data_axis=None, #show_data_axis=False,
    show_secondary_axes: Optional[int] = None,

    # https://chartscss.org/components/spacing/
    data_spacing: Optional[int] = None,
    datasets_spacing: Optional[int] = None,

    # More customizing can be done by regular css: https://chartscss.org/components/wrapper/#customizing-the-chart
    # and https://chartscss.org/customization/
) -> str:
    """
    :param list datasets:
        A list containing some rows, e.g. [row1, row2, ...].

        Each row can be a list of cells, e.g. [cell1, cell2, ...].

        Each cell is usually a number,
        but it could also be a dict with the shape {"value": number, ...}.

        Such data structure can be the outcome from ``csv.reader`` or ``csv.DictReader``
        of the `standard Python csv module <https://docs.python.org/3/library/csv.html>`_.
        So you can easily read raw data from a csv and feed it into this function.
    """
    assert rows
    if not (rows and len(rows) > (1 if headers_in_first_row else 0)):
        raise ValueError("rows (excluding header row) needs to contain numeric content.")
    if show_secondary_axes and show_secondary_axes not in range(11):
        raise ValueError("show_secondary_axes should range from 0 to 10")
    if data_spacing and data_spacing not in range(21):
        raise ValueError("data_spacing should range from 0 to 20")
    if datasets_spacing and datasets_spacing not in range(21):
        raise ValueError("datasets_spacing should range from 0 to 20")

    classes = list(filter(None, [
        "charts-css",
        _type,
        "show-labels",  # Hardcoded, for now
        "show-heading" if heading else None,
        hide_data and "hide-data",
        "show-data-on-hover" if show_data_on_hover else None,
        "reverse" if reverse else None,
        "show-primary-axis",  # Hardcoded for now. That axis looks good.
        "show-data-axes",  # Hardcoded for now. That axes look good.
        "show-{}-secondary-axes".format(show_secondary_axes) if show_secondary_axes else None,
        "data-spacing-{}".format(data_spacing) if data_spacing else None,
        "datasets-spacing-{}".format(datasets_spacing) if datasets_spacing else None,
        "reverse-data" if reverse_data else None,
        "reverse-datasets" if reverse_datasets else None,
        "stacked" if stacked else None,
        ]))

    def cell2dict(raw):
        return raw if isinstance(raw, dict) else {"value": raw}
    normalized_rows = [list(  # Normalize each cell into a dict, for easier post-process.
        map(cell2dict, row)
        ) for row in rows]
    padding = 0.2 if _type == "line" else 0  # TODO: How to choose a value fitting the current datasets?

    def numeric_values_in_a_row(row):
        values = [cell["value"] for cell in row[1 if headers_in_first_column else 0:]]
        if not values:
            raise ValueError("Inputed rows should contain at least one numeric column")
        for v in values:
            if not isinstance(v, (int, float)):
                raise ValueError(
                    "Cell ({}) needs to be either a numeric value, "
                    "or declared as a row/column header.".format(repr(v)))
        return values

    first_data_row = 1 if headers_in_first_row else 0
    if len(numeric_values_in_a_row(normalized_rows[first_data_row])) > 1:
        classes.append("multiple")  # https://chartscss.org/components/datasets/#datasets-colors

    global_upper_bound = max(
        (sum if stacked else max)(numeric_values_in_a_row(row))
        for row in normalized_rows[first_data_row:]
        ) + padding  # Padding ensures the largest value show in line chart

    # https://chartscss.org/components/datasets/#datasets
    table_rows = []
    previous_row = None
    for y, row in enumerate(normalized_rows[first_data_row:]):
        denominator = _series_upper_bound(
            numeric_values_in_a_row(row)
            ) if _series_upper_bound else global_upper_bound

        cells = [(
            """      <th scope="row">{}</th>""".format(cell["value"])
            if x == 0 and headers_in_first_column else
            """      <td style="{start}--size:calc({value}/{denominator});">
        <span class="data">{data}</span> {tooltip}
      </td>""".format(
                start="--start:calc({value}/{denominator});".format(
                    value=previous_row[x]["value"] if previous_row else cell["value"],
                    denominator=denominator,
                    ) if _type in ("line", "area") else "",
                value=cell["value"],
                denominator=denominator,
                data=cell.get("data", value_displayer(cell["value"])),
                tooltip='<span class="tooltip">{}</span>'.format(
                    # https://chartscss.org/components/tooltips/#best-practice
                    cell["tooltip"]) if "tooltip" in cell else "",
                )
            ) for x, cell in enumerate(row)]
        table_rows.append("    <tr>\n{}\n    </tr>".format("\n".join(cells)))
        previous_row = row

    table = """<table class='{classes}'>
  {heading}
{thead}
  <tbody>
{rows}
  </tbody>
</table>""".format(
        classes=" ".join(classes),
        heading="<caption>{}</caption>".format(heading) if heading else "",
        thead="""  <thead>
    <tr>
      {}
    </tr>
  </thead>""".format(
            "\n      ".join('<th scope="col">{}</th>'.format(h) for h in rows[0])
            ) if headers_in_first_row else "",
        rows="\n".join(table_rows),
        )

    return """<div id='{wrapper_id}'>
{table}
{primary_axis}
{data_axis}
{legend}
</div>""".format(
        wrapper_id=wrapper_id or "my-chart",
        table=table,
        primary_axis="<div class='primary-axis'>{}</div>".format(primary_axis)
            if primary_axis else "",
        data_axis="<div class='data-axis'>{}</div>".format(data_axis)
            if data_axis else "",
        legend=LegendSquare(rows[0][first_data_row:])
            if legend is True and headers_in_first_row  # Auto legend
            else (legend or ""),  # TODO: Shall it be customizable to put legend before or after the table?
        ) if wrapper_id or legend else table


def bar(datasets, *, stacked=False, percentage=False, **kwargs) -> str:
    return _chart(
        datasets,
        "bar", stacked=stacked, _series_upper_bound=sum if percentage else None,
        **kwargs)

def column(datasets, *, stacked=False, percentage=False, **kwargs) -> str:
    return _chart(
        datasets,
        "column", stacked=stacked, _series_upper_bound=sum if percentage else None,
        **kwargs)

def area(datasets, **kwargs) -> str:
    return _chart(datasets, "area", **kwargs)

def line(datasets, **kwargs) -> str:
    return _chart(datasets, "line", **kwargs)


if __name__ == "__main__":
    heading = "Ideal for comparing groups. This mimics this sample https://chartscss.org/components/stacked/#stacked-bars"
    chart = bar(
        [
            ["Continent", "#1", "#2", "#3"],
            ["America", 50, 50, 30, 20],
            ["Asia", 30, 30, 30, 30],
            ["Europe", 40, 25, 25, 30],
            ["Africa", 20, 20, 20, 20],
        ],
        headers_in_first_row=True,
        headers_in_first_column=True,
        stacked=True,
        #percentage=True,
        hide_data=True,  # value_displayer=lambda x: "",  # A way to hide data
        heading=heading,
        show_secondary_axes=5,
        data_spacing=5,
        )
    print("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/charts.css/dist/charts.min.css">
{}""".format(chart))

