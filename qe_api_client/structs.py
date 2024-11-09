def list_object_def(state_name="$", library_id="", field_defs=[], initial_data_fetch=[]):
    return {"qStateName": state_name, "qLibraryId": library_id, "qDef": field_defs,
            "qInitialDataFetch": initial_data_fetch}

def hypercube_def(state_name="$", nx_dims=[], nx_meas=[], nx_page=[], inter_column_sort=[0, 1, 2], suppress_zero=False,
                  suppress_missing=False):
    return {"qStateName": state_name, "qDimensions": nx_dims, "qMeasures": nx_meas,
            "qInterColumnSortOrder": inter_column_sort, "qSuppressZero": suppress_zero,
            "qSuppressMissing": suppress_missing, "qInitialDataFetch": nx_page, "qMode": 'S', "qNoOfLeftDims": -1,
            "qAlwaysFullyExpanded": False, "qMaxStackedCells": 5000, "qPopulateMissing": False,
            "qShowTotalsAbove": False, "qIndentMode": False, "qCalcCond": "", "qSortbyYValue": 0}

def nx_inline_dimension_def(field_definitions=[], field_labels=[], sort_criterias=[], grouping='N'):
    return {"qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
            "qSortCriterias": sort_criterias, "qReverseSort": False}

def nx_inline_measure_def(definition, label="", description="", tags=[], grouping="N"):
    return {"qLabel": label, "qDescription": description, "qTags": tags, "qGrouping": grouping, "qDef":	definition}

def nx_page(left=0, top=0, width=2, height=2):
    return {"qLeft": left, "qTop": top, "qWidth": width, "qHeight": height}

def nx_info(obj_type, obj_id=""):
    """
    Retrieves the data from a specific list object in a generic object.

    Parameters:
        obj_type (str): Type of the object. This parameter is mandatory.
        obj_id (str): Identifier of the object. If the chosen identifier is already in use, the engine automatically
        sets another one. If an identifier is not set, the engine automatically sets one. This parameter is optional.

    Returns:
        dict: Struct "nxInfo"
    """
    return {"qId": obj_id, "qType": obj_type}

def nx_dimension(library_id="", dim_def={}, null_suppression=False):
    return {"qLibraryId": library_id, "qDef": dim_def, "qNullSuppression": null_suppression}

def nx_measure(library_id="", mes_def={}, sort_by={}):
    return {"qLibraryId": library_id, "qDef": mes_def, "qSortBy": sort_by}

def generic_object_properties(info, prop_name, prop_def, extends_id="", state_name="$"):
    return {"qInfo": info, "qExtendsId": extends_id, prop_name: prop_def, "qStateName": state_name}

def sort_criteria(state=0, freq=0, numeric=0, ascii=0, load_order=1):
    return {"qSortByState": state, "qSortByFrequency": freq, "qSortByNumeric": numeric, "qSortByAscii": ascii,
            "qSortByLoadOrder": load_order, "qSortByExpression": 0, "qExpression": {"qv": ""}}

def field_value(text, is_numeric = False, number = 0):
    return {"qText": text, "qIsNumeric": is_numeric, "qNumber": number}

def generic_dimension_properties(info, lb_dim_def, dim_title):
    return {"qInfo": info, "qDim": lb_dim_def, "qMetaDef": {"title": dim_title}}

def nx_library_dimension_def(grouping="N", field_definitions=[], field_labels=[""], label_expression=""):
    return {"qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
            "qLabelExpression": label_expression}

def nx_library_measure_def(label, mes_def, grouping="N", expressions=[], active_expression=0, label_expression="",
                           num_format={}):
    return {"qLabel": label, "qDef": mes_def,"qGrouping": grouping, "qExpressions": expressions,
            "qActiveExpression": active_expression, "qLabelExpression": label_expression, "qNumFormat": num_format}

def num_format(type="U", n_dec=10, use_thou=0, fmt="", dec="", thou=""):
    return {"qType": type, "qnDec": n_dec, "qUseThou": use_thou, "qFmt": fmt, "qDec": dec, "qThou": thou}

def generic_measure_properties(info, lb_meas_def, meas_title):
    return {"qInfo": info, "qMeasure": lb_meas_def, "qMetaDef": {"title": meas_title}}

def do_reload_ex_params(mode=0, partial=False, debug=False, reload_id="", skip_store=False, row_limit=0):
    return {"qMode": mode, "qPartial": partial, "qDebug": debug, "qReloadId": reload_id, "qSkipStore": skip_store,
            "qRowLimit": row_limit}