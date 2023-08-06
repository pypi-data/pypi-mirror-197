from IPython.core.display import HTML
from IPython.display import display, Javascript

def inject_css(*args):
    style = """
    <style>
    {arguments}
    </style>
    """.format(arguments=''.join(args))
    display(HTML(style))

def bokeh_transparent_button():
    return inject_css("""
    .bk-root .bk-btn-default {
        border-radius: 0px;
        opacity: 0.5;
        font-weight: bolder;
     }
    """)

