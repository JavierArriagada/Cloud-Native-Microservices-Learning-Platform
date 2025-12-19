"""
Dash Dashboard Application
Cloud-Native Microservices Learning Platform
"""
import dash
from dash import html, dcc
import plotly.graph_objects as go
import os

# =============================================================================
# APPLICATION INITIALIZATION
# =============================================================================

app = dash.Dash(
    __name__,
    title="Cloud-Native Learning Platform - Dashboard",
    update_title="Loading...",
    url_base_pathname="/dash/",
)

# Server for WSGI
server = app.server

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_sample_chart():
    """Create a sample plotly chart"""
    fig = go.Figure()

    # Sample data
    x = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    y = [4, 7, 3, 8, 6, 9]

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        name='Sample Data',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10)
    ))

    fig.update_layout(
        title='Sample Time Series',
        xaxis_title='Month',
        yaxis_title='Value',
        hovermode='x unified',
        template='plotly_white'
    )

    return fig

# =============================================================================
# LAYOUT
# =============================================================================

app.layout = html.Div([
    html.Div([
        html.H1("🚀 Cloud-Native Microservices Dashboard",
                style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Hr(),

        # Welcome section
        html.Div([
            html.H3("Welcome to the Dashboard"),
            html.P("This is a basic Dash application integrated with FastAPI backend."),
            html.P(f"Environment: {os.getenv('ENVIRONMENT', 'production')}"),
            html.P(f"API URL: {os.getenv('API_URL', 'Not configured')}"),
        ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px', 'margin': '20px 0'}),

        # Sample Chart
        html.Div([
            html.H3("Sample Chart"),
            dcc.Graph(
                id='sample-graph',
                figure=create_sample_chart()
            )
        ], style={'padding': '20px'}),

        # Status section
        html.Div([
            html.H3("System Status"),
            html.Div(id='status-display', children=[
                html.P("✅ Dashboard: Running"),
                html.P("🔄 API: Checking..."),
                html.P("🔄 Database: Checking..."),
            ])
        ], style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px'}),

    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})
])

# =============================================================================
# CALLBACKS
# =============================================================================

# TODO: Add callbacks for interactivity
# Example:
# @app.callback(
#     Output('status-display', 'children'),
#     Input('interval-component', 'n_intervals')
# )
# def update_status(n):
#     # Fetch status from API
#     return status_components


# =============================================================================
# RUN APPLICATION
# =============================================================================

if __name__ == '__main__':
    debug = os.getenv('DASH_DEBUG', 'false').lower() == 'true'
    host = os.getenv('DASH_HOST', '0.0.0.0')
    port = int(os.getenv('DASH_PORT', '8050'))

    print(f"🚀 Starting Dash application on {host}:{port}")
    print(f"🔍 Debug mode: {debug}")

    app.run_server(
        host=host,
        port=port,
        debug=debug
    )
