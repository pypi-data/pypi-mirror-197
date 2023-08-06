from IPython import get_ipython
from IPython.display import display
from ipywidgets import Output

from hindsight.utils.voila import QueryParams, IS_RUNNING_VOILA, LoadingSpinner

def set_query_params(global_ref):
    if not IS_RUNNING_VOILA():
        return
        
    ipython = get_ipython()
    ipython.events.register('post_execute', QueryParams(global_ref).set_variables) #post_run_cell


def add_loading_indicator():
    if not IS_RUNNING_VOILA():
        return
    
    __header = Output()
    __header.layout.margin = '0px 0px 0px 0px'
    __header.layout.padding = '0px 0px 0px 0px'
    
    loading_container = LoadingSpinner.get_loading_indicator()
    
    with __header:
        display(loading_container)
    
    def display_loading():
        __header.layout.visibility = 'visible'

    def hide_loading():
        __header.layout.visibility = 'hidden'

    display(__header)
    
    ipython = get_ipython()
    ipython.events.register('pre_execute', display_loading)
    ipython.events.register('post_execute', hide_loading)
