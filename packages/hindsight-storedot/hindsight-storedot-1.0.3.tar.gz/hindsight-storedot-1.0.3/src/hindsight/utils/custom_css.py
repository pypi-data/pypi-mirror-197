from IPython.core.display import HTML
from IPython.display import display, Javascript

def inject_css(*args):
    style = """
    <style>
    {arguments}
    </style>
    """.format(arguments=''.join(args))
    display(HTML(style))

def inject_voila_loading_css():
    return inject_css("""
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    """)

def bokeh_transparent_button():
    return inject_css("""
    .bk-root .bk-btn-default {
        border-radius: 0px;
        opacity: 0.5;
        font-weight: bolder;
     }
    """)

