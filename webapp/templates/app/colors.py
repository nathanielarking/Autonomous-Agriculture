#Dict to store palette for flask app and dashboards
palette = {
    'navbar': '#0d0f12',
    'sidebar': '#181c21',
    'background': '#1c2126',
    'text_title': '#e1f3f4',
    'text_body': '#d2eeef',
    'text_light': '#9c9c9c',
    'col0': '#252e41',
    'col1': '#303c54',
    'col2': '#36435e',
    'col3': '#1c2a45',
    'col4': '#2a3751',
    'border': '#0d0f11'
}  

#Have to predefine the table border as it doesn't allow string formatting
border_color = palette['border']

#Have to define tab styles in this file so python can import the colors
tabs_style = {
    'height': '44px'
}
tab_style = {
    'border': f'1px solid {border_color}',
    'backgroundColor': palette['col2'],
    'color': palette['text_title'],
    'padding': '6px'
}

tab_selected_style = {
    'border': f'1px solid {border_color}',
    'backgroundColor': palette['col3'],
    'color': palette['text_body'],
    'fontWeight': 'bold',
    'padding': '6px'
}

#Define custom styles for other components
picker_style = {
    'backgroundColor': palette['col4']
}
dropdown_style = {
    'backgroundColor': palette['col4'],
    'borderColor': palette['border']
}