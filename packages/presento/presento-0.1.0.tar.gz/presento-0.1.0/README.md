# Presento

A tool to programmatically build slides.

Using the excellent reveal.js library, this script helps you generate slides from Python.

You can easily create markdown slides or insert charts as HTML with Plotly.

# Example

```python
import presento
import plotly.express as px

p = presento.Presentation()
p.add_md_slide("""
# title of the slide

This is a slide added directly to the presentation.

It uses markdown so it can have:
1. __formatting__
2. [links](https://en.wikipedia.org/wiki/Markdown)
3.

""")
# for the next slide we use plotly, but we need a CDN first
p.add_cdn_js("https://cdn.plot.ly/plotly-latest.min.js")
fig = px.scatter(x=range(10), y=range(10))
p.add_html_slide(fig.to_html(include_plotlyjs=False))
# p.save_folder('my_slides')
p.show()
```

In this example you can see that in addition to markdown slides you can add verbatim HTML, useful for example to add Plotly charts.

For Plotly (and pretty much every other library) you will want to use a CDN. This can be done with `add_cdn_js`.

The `show()` method will start a server and open the browser for you.

The `save_folder(path)` method writes the slides to a folder, that can be statically served.