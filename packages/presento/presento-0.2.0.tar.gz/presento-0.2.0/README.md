# Presento

A tool to programmatically build slides.

Using the excellent reveal.js library, this script helps you generate slides from Python.

You can easily create markdown slides or insert charts as HTML with Plotly.

## Install

    pip install presento

or use PDM, Poetry, etc...

# Example

```python
import plotly.express as px
from markdown import markdown

import presento

p = presento.Presentation(theme='serif')
p.add_md_slide(
    """
# title of the slide

This is a slide added directly to the presentation.

It uses markdown so it can have:
1. __formatting__
2. [links](https://en.wikipedia.org/wiki/Markdown)
3. lists

"""
)
# for the next slide we use plotly, but we need a CDN
p.add_cdn_js("https://cdn.plot.ly/plotly-latest.min.js")
fig = px.scatter(x=range(10), y=range(10))
p.add_html_slide(fig.to_html(include_plotlyjs=False, full_html=False))
p.add_columns_slide(
    [
        markdown("This is a column on the left"),
        fig.to_html(include_plotlyjs=False, full_html=False),
        # markdown("This is another column, on the right"),
    ]
)
# p.save_folder('my_slides')
p.show(port=8090)
```

In this example you can see that in addition to markdown slides you can add verbatim HTML, useful for example to add Plotly charts.

For Plotly (and pretty much every other library) you will want to use a CDN to load the JS once and reuse it across slides. This can be done with `add_cdn_js`.

The function `add_columns_slide` is an helper to generate a grid layout with the provided.

The `show()` method will start a server and open the browser for you.

The `save_folder(path)` method writes the slides to a folder, that can be statically served.

## Theming

When creating the `Presentation` object, you can pass a `theme` parameter corresponding to the name of one of the [Reveal themes](https://revealjs.com/themes/). To create your own theme you need to follow the instructions on the Reveal.js website and replace it on the generated