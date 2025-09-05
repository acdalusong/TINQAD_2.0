import dash
from dash import dcc,html
from dash import dash, html, dcc, Input, Output, State, dash_table
from dash import callback_context
import dash_bootstrap_components as dbc
import logging
from flask import Flask, send_from_directory
from flask import render_template, send_file, make_response, request
from weasyprint import HTML
import webbrowser
import io
import pandas as pd
from apps import dbconnect as db

from dash.exceptions import PreventUpdate

import base64
import os
from urllib.parse import urlparse, parse_qs

server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=["assets/bootstrap.css", dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

#if __name__ == '__main__':
    # app.run_server(host='10.206.100.41',port=8050)
   # webbrowser.open('http://10.206.100.41:8050/',autoraise=True)


app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.title = 'TINQAD'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# if __name__ == '__main__':
#     # Run the app on all network interfaces (10.206.100.41) on port 8050
#     app.run_server(host='10.206.100.41', port=8050)
    
#     # Optionally, open the web browser to the correct URL
#     url = 'http://10.206.100.41:8050/'
#     webbrowser.open(url, new=0, autoraise=True)

#server = Flask(__name__)
#app = dash.Dash(server=server)


