def list_object_def(state_name="$", library_id="", field_defs=None, field_labels=None, sort_criterias=None,
                    initial_data_fetch=None):
    if initial_data_fetch is None:
        initial_data_fetch = []
    if sort_criterias is None:
        sort_criterias = []
    if field_labels is None:
        field_labels = []
    if field_defs is None:
        field_defs = []
    return {"qStateName": state_name, "qLibraryId": library_id,
            "qDef": {"qFieldDefs": field_defs, "qFieldLabels": field_labels, "qSortCriterias": sort_criterias},
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
