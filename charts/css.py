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
    datasets,  # A dict of {"primary axis 1": [item0, item1, ...], ...}
               # Each item is a decimal or a dict {"text": "...", "size": 0.5, "label": "...", "color": "orange", "tooltip": "..."}
    _type: str,  # One of the supported types. Currently one of "column", "bar", "area", "line".
    *,
    thead: Optional[Tuple[str, list]] = None,  # A tuple whose first item is the table head for primary axis,
                                    # the second item has the shape same as datasets,
                                    # such as ("primary axis label", ["data label", ...]).
                                    # It is invisible on chart, but would show nice table header when css is unavailable.
    _series_upper_bound: Optional[Callable[[], int]] = None,  # https://chartscss.org/components/stacked/#simple-vs-percentage
    value_displayer=lambda value: value,
    stacked=False,  # Only applicable to bar and column charts. https://chartscss.org/components/stacked/

    starting_point=False,  # If true, the first item in (each?) series is considered as the start point

    legend: Optional[Legend] = None,  # https://chartscss.org/components/legend/

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
    show_2_secondary_axes=False,
    show_4_secondary_axes=False,
    show_6_secondary_axes=False,
    show_10_secondary_axes=False,

    # https://chartscss.org/components/spacing/
    data_spacing_5=False,
    data_spacing_20=False,
    datasets_spacing_4=False,

    # More customizing can be done by regular css: https://chartscss.org/components/wrapper/#customizing-the-chart
) -> str:
    classes = filter(None, [
        "charts-css",
        _type,
        "show-labels",  # Hardcoded, for now
        "show-heading" if heading else None,
        hide_data and "hide-data",
        "show-data-on-hover" if show_data_on_hover else None,

        # https://chartscss.org/components/datasets/#datasets-colors
        "multiple" if datasets and len(list(datasets.values())[0]) > 1 else None,

        "reverse" if reverse else None,
        "show-primary-axis",  # Hardcoded for now. That axis looks good.
        "show-data-axes",  # Hardcoded for now. That axes look good.

        "show-2-secondary-axes" if show_2_secondary_axes else None,
        "show-4-secondary-axes" if show_4_secondary_axes else None,
        "show-6-secondary-axes" if show_6_secondary_axes else None,
        "show-10-secondary-axes" if show_10_secondary_axes else None,

        "data-spacing-5" if data_spacing_5 else None,
        "data-spacing-20" if data_spacing_20 else None,
        "datasets-spacing-4" if datasets_spacing_4 else None,
        "reverse-data" if reverse_data else None,
        "reverse-datasets" if reverse_datasets else None,
        "stacked" if stacked else None,
        ])

    normalized_datasets = {}
    for label, raw_items in datasets.items():
        normalized_datasets[label] = [
            item if isinstance(item, dict) else {"value": item} for item in raw_items]
    padding = 0.2 if _type == "line" else 0  # TODO: How to choose a value fitting the current datasets?
    global_upper_bound = max(
        (sum if stacked else max)(item["value"] for item in items)
            for items in normalized_datasets.values()
        ) + padding  # Padding ensures the largest value show in line chart

    # https://chartscss.org/components/datasets/#datasets
    rows = []
    for label, items in normalized_datasets.items():
        denominator = _series_upper_bound(
            i["value"] for i in items
            ) if _series_upper_bound else global_upper_bound

        cells = ["""            <th scope="row">{}</th>""".format(label)
                # https://chartscss.org/components/labels/
            ] + ["""            <td style="--size: calc( {value} / {denominator} );">
                <span class="data">{data}</span> {tooltip}
            </td>""".format(
            #label=label,  # https://chartscss.org/components/labels/
            value=item["value"],
            denominator=denominator,
            data=item.get("data", value_displayer(item["value"])),
            tooltip='<span class="tooltip">{}</span>'.format(
                # https://chartscss.org/components/tooltips/#best-practice
                item["tooltip"]) if "tooltip" in item else "",
            ) for item in items]

        print(_type)
        cells = ["""            <th scope="row">{}</th>""".format(label)
                # https://chartscss.org/components/labels/
            ] + ["""            <td style="{start} --size: calc( {value} / {denominator} );">
                <span class="data">{data}</span> {tooltip}
            </td>""".format(
                start="--start: calc({value}/{denominator});".format(
                    value=items[i-1]["value"],
                    denominator=denominator,
                    ) if (_type in ("area", "line")) and i else "",
                value=item["value"],
                denominator=denominator,
                data=item.get("data", value_displayer(item["value"])),
                tooltip='<span class="tooltip">{}</span>'.format(
                    # https://chartscss.org/components/tooltips/#best-practice
                    item["tooltip"]) if "tooltip" in item else "",
            ) for i, item in enumerate(items)]
        rows.append("""    <tr>
{}
    </tr>""".format("\n".join(cells)))


    if starting_point:
        # https://chartscss.org/components/data/#starting-point
        pass

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
      <th scope="col">{}</th>
      {}
    </tr>
  </thead>""".format(
            thead[0],
            "\n      ".join('<th scope="col">{}</th>'.format(h) for h in thead[1]),
            ) if thead else "",
        rows="\n".join(rows),
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
        legend=legend or "",  # TODO: Shall it be customizable to put legend before or after the table?
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

def area(datasets, **kwargs) -> str:  # TODO: First value of each dataset is considered as start value
    return _chart(datasets, "area", **kwargs)

def line(datasets, **kwargs) -> str:  # TODO: First value of each dataset is considered as start value
    return _chart(datasets, "line", **kwargs)

if __name__ == "__main__":
    chart = line(  # This mimics the sample of https://chartscss.org/components/data/
        {
            "Alex": [40],
            "Bob": [60],
            "Charlie": [75],
            "David": [90],
            "Einstein": [100],
        },
        value_displayer="${}K".format,
        heading="Sample of https://chartscss.org/components/data/",
        thead=("Employee", ["Salary"]),
        )
    chart2 = line(  # This looks the same as the previous sample, but easier to write
        {
            "Salary": [40, 60, 75, 90, 100],
        },
        value_displayer="${}K".format,
        heading="Sample of https://chartscss.org/components/data/",
        thead=("Attributes", ["Alex", "Bob", "Charlie", "David", "Einstein"]),
        )
    chart3 = line(
        {
            "Asia": [20, 30, 40, 50, 75],
            "Euro": [40, 60, 75, 90, {"value": 100, "tooltip": "This is <strong>a tooltip</strong>"}],
        },
        value_displayer="${}K".format,
        data_spacing_20=True,
        datasets_spacing_4=True,
        show_6_secondary_axes=True,
        #stacked=True, #percentage=True,
        #reverse_data=True,
        #reverse_datasets=True,

        # The following options would need your own css to make them look right
        #primary_axis="Continents",
        #data_axis="Year",
        legend=LegendRectangle(["1st year", "2nd year", "3rd year", "4th year", "5th year"]),
        heading="Sample of https://chartscss.org/components/data/",
        )
    print("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/charts.css/dist/charts.min.css">
{}""".format(chart))

