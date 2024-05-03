import pandas as pd
from dash import dash, html, dcc, Input, Output, State, callback, ctx

def watch_save(click_save, n, datatable, active_cell):
    trigger = ctx.triggered_id    
    if datatable:
        df_datatable = pd.DataFrame(datatable)
        df_datatable['id'] = df_datatable['id'].astype('Int64')

        if trigger == 'trigger-save-changes' and click_save is not None:
            return df_datatable.to_dict('records')
        elif trigger == "interval-component":
            if active_cell is None or df_datatable.iloc[active_cell['row']].isnull().all():
                return df_datatable.to_dict('records')
    return dash.no_update

def update_data(data, selected, current, id_datatable):
    trigger = ctx.triggered_id
    if trigger == id_datatable:
        return data
    else:
        df_datatable = pd.DataFrame(current)
        df_datatable.replace("", pd.NA, inplace=True)
        df_datatable.fillna(pd.NA, inplace=True)
        if not df_datatable.iloc[-1].isnull().all():
            df_datatable.loc[len(df_datatable)] = [pd.NA] * len(df_datatable.columns)
            return df_datatable.to_dict('records')
        if(trigger == 'trigger-remove-rows'):
            if selected:
                for index in selected:
                    del current[index]
    return current