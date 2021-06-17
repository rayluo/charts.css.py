from charts.css import (
    bar, column, line, area, wrapper,
    transpose,
    LegendRectangle, LegendSquare)


def minify(html):
    return list(filter(None, (line.strip() for line in html.split("\n"))))

def test_single_dataset_in_one_column_without_header():
    heading = "This mimics the sample of https://chartscss.org/components/data/#display-size"
    chart = column(
        [
            [40],
            [60],
            [75],
            [90],
            [100],
        ],
        value_displayer="${}K".format,
        heading=heading,
        )
    assert minify(chart) == minify("""<table class='charts-css column show-labels show-heading show-primary-axis show-data-axes'>
  <caption>{}</caption>

  <tbody>
    <tr>
      <td style="--size:calc(40/100);">
        <span class="data">$40K</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(60/100);">
        <span class="data">$60K</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(75/100);">
        <span class="data">$75K</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(90/100);">
        <span class="data">$90K</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(100/100);">
        <span class="data">$100K</span>
      </td>
    </tr>
  </tbody>
</table>""".format(heading))

def test_single_dataset_with_col_and_row_headers():
    heading = "This expands from the sample of https://chartscss.org/components/data/"
    chart = bar(
        [
            ["Employee", "Salary"],
            ["Alex", 40],
            ["Bob", 60],
            ["Charlie", 75],
            ["David", 90],
            ["Einstein", 100],
        ],
        headers_in_first_column=True,
        headers_in_first_row=True,
        value_displayer="${}K".format,
        heading=heading,
        )
    assert minify(chart) == minify("""
<table class='charts-css bar show-labels show-heading show-primary-axis show-data-axes'>
  <caption>{}</caption>
  <thead>
    <tr>
      <th scope="col">Employee</th>
      <th scope="col">Salary</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Alex</th>
      <td style="--size:calc(40/100);">
        <span class="data">$40K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Bob</th>
      <td style="--size:calc(60/100);">
        <span class="data">$60K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Charlie</th>
      <td style="--size:calc(75/100);">
        <span class="data">$75K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">David</th>
      <td style="--size:calc(90/100);">
        <span class="data">$90K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Einstein</th>
      <td style="--size:calc(100/100);">
        <span class="data">$100K</span>
      </td>
    </tr>
  </tbody>
</table>""".format(heading))

def test_multi_datasets_with_auto_legend():
    heading = "This mimics this sample https://chartscss.org/components/datasets/#datasets-colors"
    chart = column(
        [
            ["Continent", "1st year", "2nd year", "3rd year", "4th year", "5th year"],
            ["Asia", 20, 30, 40, 50, 75],
            ["Euro", 40, 60, 75, 90, {"value": 100, "tooltip": "This is <strong>a tooltip</strong>"}],
        ],
        headers_in_first_row=True,
        headers_in_first_column=True,
        legend=LegendSquare,
        value_displayer="${}K".format,
        heading=heading,
        data_spacing=20,
        datasets_spacing=4,
        )
    assert minify(chart) == minify("""
<table class='charts-css column show-labels show-heading show-primary-axis show-data-axes data-spacing-20 datasets-spacing-4 multiple'>
  <caption>This mimics this sample https://chartscss.org/components/datasets/#datasets-colors</caption>
  <thead>
    <tr>
      <th scope="col">Continent</th>
      <th scope="col">1st year</th>
      <th scope="col">2nd year</th>
      <th scope="col">3rd year</th>
      <th scope="col">4th year</th>
      <th scope="col">5th year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Asia</th>
      <td style="--size:calc(20/100);">
        <span class="data">$20K</span>
      </td>
      <td style="--size:calc(30/100);">
        <span class="data">$30K</span>
      </td>
      <td style="--size:calc(40/100);">
        <span class="data">$40K</span>
      </td>
      <td style="--size:calc(50/100);">
        <span class="data">$50K</span>
      </td>
      <td style="--size:calc(75/100);">
        <span class="data">$75K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Euro</th>
      <td style="--size:calc(40/100);">
        <span class="data">$40K</span>
      </td>
      <td style="--size:calc(60/100);">
        <span class="data">$60K</span>
      </td>
      <td style="--size:calc(75/100);">
        <span class="data">$75K</span>
      </td>
      <td style="--size:calc(90/100);">
        <span class="data">$90K</span>
      </td>
      <td style="--size:calc(100/100);">
        <span class="data">$100K</span> <span class="tooltip">This is <strong>a tooltip</strong></span>
      </td>
    </tr>
  </tbody>
</table>


<ul class='charts-css legend legend-square '><li>1st year</li><li>2nd year</li><li>3rd year</li><li>4th year</li><li>5th year</li></ul>
""")


def test_multi_datasets_line_chart_handles_start_value():
    heading = "This mimics this sample https://chartscss.org/components/datasets/#datasets-colors"
    chart = line(
        [
            ["Year", "Progress 1", "Progress 2", "Progress 3"],
            [2000, 50, 20, 40],
            [2010, 80, 50, 10],
            [2020, 40, 30, 20],
        ],
        headers_in_first_row=True,
        headers_in_first_column=True,
        value_displayer="${}K".format,
        heading=heading,
        show_secondary_axes=4,
        )
    assert minify(chart) == minify("""
<table class='charts-css line show-labels show-heading show-primary-axis show-data-axes show-4-secondary-axes multiple'>
  <caption>This mimics this sample https://chartscss.org/components/datasets/#datasets-colors</caption>
  <thead>
    <tr>
      <th scope="col">Year</th>
      <th scope="col">Progress 1</th>
      <th scope="col">Progress 2</th>
      <th scope="col">Progress 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">2000</th>
      <td style="--start:calc(50/80.2);--size:calc(50/80.2);">
        <span class="data">$50K</span>
      </td>
      <td style="--start:calc(20/80.2);--size:calc(20/80.2);">
        <span class="data">$20K</span>
      </td>
      <td style="--start:calc(40/80.2);--size:calc(40/80.2);">
        <span class="data">$40K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">2010</th>
      <td style="--start:calc(50/80.2);--size:calc(80/80.2);">
        <span class="data">$80K</span>
      </td>
      <td style="--start:calc(20/80.2);--size:calc(50/80.2);">
        <span class="data">$50K</span>
      </td>
      <td style="--start:calc(40/80.2);--size:calc(10/80.2);">
        <span class="data">$10K</span>
      </td>
    </tr>
    <tr>
      <th scope="row">2020</th>
      <td style="--start:calc(80/80.2);--size:calc(40/80.2);">
        <span class="data">$40K</span>
      </td>
      <td style="--start:calc(50/80.2);--size:calc(30/80.2);">
        <span class="data">$30K</span>
      </td>
      <td style="--start:calc(10/80.2);--size:calc(20/80.2);">
        <span class="data">$20K</span>
      </td>
    </tr>
  </tbody>
</table>""")

def test_multi_datasets_stacked_by_value():
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
        hide_data=True,
        heading=heading,
        show_secondary_axes=5,
        data_spacing=5,
        )
    assert minify(chart) == minify("""
<table class='charts-css bar show-labels show-heading hide-data show-primary-axis show-data-axes show-5-secondary-axes data-spacing-5 stacked multiple'>
  <caption>{}</caption>
  <thead>
    <tr>
      <th scope="col">Continent</th>
      <th scope="col">#1</th>
      <th scope="col">#2</th>
      <th scope="col">#3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">America</th>
      <td style="--size:calc(50/150);">
        <span class="data">50</span>
      </td>
      <td style="--size:calc(50/150);">
        <span class="data">50</span>
      </td>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
      <td style="--size:calc(20/150);">
        <span class="data">20</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Asia</th>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Europe</th>
      <td style="--size:calc(40/150);">
        <span class="data">40</span>
      </td>
      <td style="--size:calc(25/150);">
        <span class="data">25</span>
      </td>
      <td style="--size:calc(25/150);">
        <span class="data">25</span>
      </td>
      <td style="--size:calc(30/150);">
        <span class="data">30</span>
      </td>
    </tr>
    <tr>
      <th scope="row">Africa</th>
      <td style="--size:calc(20/150);">
        <span class="data">20</span>
      </td>
      <td style="--size:calc(20/150);">
        <span class="data">20</span>
      </td>
      <td style="--size:calc(20/150);">
        <span class="data">20</span>
      </td>
      <td style="--size:calc(20/150);">
        <span class="data">20</span>
      </td>
    </tr>
  </tbody>
</table>""".format(heading))

def test_mixed_charts():
    heading = "This sample mimics https://chartscss.org/charts/mixed/#using-css-grid"
    price = area(
        [
            [40],
            [80],
            [60],
            [100],
            [30],
        ],
        hide_data=True,
        )
    trend = line(
        [
            [40],
            [60],
            [75],
            [90],
            [100],
        ],
        hide_data=True,
        )
    volume = column(
        [
            [6],
            [9],
            [10],
            [4],
            [3],
            [6],
            [9],
            [10],
            [4],
            [3],
            [6],
            [9],
            [10],
            [4],
            [3],
        ],
        hide_data=True,
        data_spacing=2,
        )
    outcome = wrapper(
        price, trend, volume,
        "<div style='grid-area:sidebar_left; writing-mode: sideways-lr;'>Stock Price</div>",
        "<div style='grid-area:sidebar_right; writing-mode: sideways-rl;'>Moving Average</div>",
        "<div style='grid-area:header'>{}</div>".format(heading),
        "<div style='grid-area:footer'>Volume</div>",
        arrangement="""
.area, .line {grid-area: main}
.column {grid-area: basement}

/* Colors */
table.area {
  --color: linear-gradient(#666, rgba(255, 255, 255, 0));
}
table.line {
  --color: #fc1;
}
table.column tr:nth-child(even) {
  --color: #e88;
}
table.column tr:nth-child(odd) {
  --color: #8c8;
}
""",
        )
    assert minify(outcome) == minify("""
<style>
#my_chart {
  display: grid;
  align-items: center;
  justify-items: center;
  background-color: #eee;

  height: calc(100vh - 1em);
  grid-template-areas:
    "header header header"
    "sidebar_left loft sidebar_right"
    "sidebar_left main sidebar_right"
    "sidebar_left basement sidebar_right"
    "footer footer footer";
  grid-template-columns: auto 1fr auto;
  grid-template-rows: auto auto 1fr auto auto;
}

.area, .line {grid-area: main}
.column {grid-area: basement}

/* Colors */
table.area {
  --color: linear-gradient(#666, rgba(255, 255, 255, 0));
}
table.line {
  --color: #fc1;
}
table.column tr:nth-child(even) {
  --color: #e88;
}
table.column tr:nth-child(odd) {
  --color: #8c8;
}
</style>
<div id="my_chart">
<table class='charts-css area show-labels hide-data show-primary-axis show-data-axes'>


  <tbody>
    <tr>
      <td style="--start:calc(40/100);--size:calc(40/100);">
        <span class="data">40</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(40/100);--size:calc(80/100);">
        <span class="data">80</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(80/100);--size:calc(60/100);">
        <span class="data">60</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(60/100);--size:calc(100/100);">
        <span class="data">100</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(100/100);--size:calc(30/100);">
        <span class="data">30</span>
      </td>
    </tr>
  </tbody>
</table>

<table class='charts-css line show-labels hide-data show-primary-axis show-data-axes'>


  <tbody>
    <tr>
      <td style="--start:calc(40/100.2);--size:calc(40/100.2);">
        <span class="data">40</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(40/100.2);--size:calc(60/100.2);">
        <span class="data">60</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(60/100.2);--size:calc(75/100.2);">
        <span class="data">75</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(75/100.2);--size:calc(90/100.2);">
        <span class="data">90</span>
      </td>
    </tr>
    <tr>
      <td style="--start:calc(90/100.2);--size:calc(100/100.2);">
        <span class="data">100</span>
      </td>
    </tr>
  </tbody>
</table>

<table class='charts-css column show-labels hide-data show-primary-axis show-data-axes data-spacing-2'>


  <tbody>
    <tr>
      <td style="--size:calc(6/10);">
        <span class="data">6</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(9/10);">
        <span class="data">9</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(10/10);">
        <span class="data">10</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(4/10);">
        <span class="data">4</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(3/10);">
        <span class="data">3</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(6/10);">
        <span class="data">6</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(9/10);">
        <span class="data">9</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(10/10);">
        <span class="data">10</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(4/10);">
        <span class="data">4</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(3/10);">
        <span class="data">3</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(6/10);">
        <span class="data">6</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(9/10);">
        <span class="data">9</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(10/10);">
        <span class="data">10</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(4/10);">
        <span class="data">4</span>
      </td>
    </tr>
    <tr>
      <td style="--size:calc(3/10);">
        <span class="data">3</span>
      </td>
    </tr>
  </tbody>
</table>

<div style='grid-area:sidebar_left; writing-mode: sideways-lr;'>Stock Price</div>
<div style='grid-area:sidebar_right; writing-mode: sideways-rl;'>Moving Average</div>
<div style='grid-area:header'>This sample mimics https://chartscss.org/charts/mixed/#using-css-grid</div>
<div style='grid-area:footer'>Volume</div>
</div>
""")

def test_transpose():
    matrix = [
        (1, 2, 3),
        (4, 5, 6),
        ]
    assert transpose(matrix) == [
        (1, 4),
        (2, 5),
        (3, 6),
        ]
    assert transpose(transpose(matrix)) == matrix
