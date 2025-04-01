def list_object_def(state_name: str = "$", library_id: str = "", definition: dict = None,
                    auto_sort_by_state: dict = None, frequency_mode: str = "N", show_alternatives: bool = False,
                    initial_data_fetch: list = None, expressions: list = None,
                    direct_query_simplified_view: bool = False, show_titles: bool = True, title: str = "",
                    subtitle: str = "", footnote: str = "", disable_nav_menu: bool = False, show_details: bool = True,
                    show_details_expression: bool = False, other_total_spec: dict = None):

    if other_total_spec is None:
        other_total_spec = {}
    if expressions is None:
        expressions = []
    if initial_data_fetch is None:
        initial_data_fetch = []
    if auto_sort_by_state is None:
        auto_sort_by_state = {}
    if definition is None:
        definition = {}

    return {"qStateName": state_name, "qLibraryId": library_id, "qDef": definition,
            "qAutoSortByState": auto_sort_by_state, "qFrequencyMode": frequency_mode,
            "qShowAlternatives": show_alternatives, "qInitialDataFetch": initial_data_fetch,
            "qExpressions": expressions, "qDirectQuerySimplifiedView": direct_query_simplified_view,
            "showTitles": show_titles, "title": title, "subtitle": subtitle, "footnote": footnote,
			"disableNavMenu": disable_nav_menu, "showDetails": show_details,
            "showDetailsExpression": show_details_expression, "qOtherTotalSpec": other_total_spec}


def hypercube_def(state_name="$", nx_dims=[], nx_meas=[], nx_page=[], inter_column_sort=[0, 1, 2], suppress_zero=False,
                  suppress_missing=False):
    return {"qStateName": state_name, "qDimensions": nx_dims, "qMeasures": nx_meas,
            "qInterColumnSortOrder": inter_column_sort, "qSuppressZero": suppress_zero,
            "qSuppressMissing": suppress_missing, "qInitialDataFetch": nx_page, "qMode": 'S', "qNoOfLeftDims": -1,
            "qAlwaysFullyExpanded": False, "qMaxStackedCells": 5000, "qPopulateMissing": False,
            "qShowTotalsAbove": False, "qIndentMode": False, "qCalcCond": "", "qSortbyYValue": 0}


def nx_inline_dimension_def(grouping: str = "N", field_definitions: list = None, field_labels: list = None,
                            sort_criterias: list = None, number_presentations: list = None, reverse_sort: bool = False,
                            active_field: int = 0, label_expression: str = "", alias: str = "", auto_sort: bool = True):
    if number_presentations is None:
        number_presentations = []
    if sort_criterias is None:
        sort_criterias = []
    if field_labels is None:
        field_labels = []
    if field_definitions is None:
        field_definitions = []
    return {"qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
            "qSortCriterias": sort_criterias, "qNumberPresentations": number_presentations, "qReverseSort": reverse_sort,
            "qActiveField": active_field, "qLabelExpression": label_expression, "qAlias": alias, "autoSort": auto_sort}


def nx_inline_measure_def(definition, label="", description="", tags=[], grouping="N"):
    return {"qLabel": label, "qDescription": description, "qTags": tags, "qGrouping": grouping, "qDef":	definition}


def nx_page(left=0, top=0, width=2, height=2):
    return {"qLeft": left, "qTop": top, "qWidth": width, "qHeight": height}


def nx_info(obj_type, obj_id=""):
    """
    Retrieves the data from a specific list object in a generic object.

    Parameters:
        obj_type (str): Type of the object. This parameter is mandatory.
        obj_id (str, optional): Identifier of the object. If the chosen identifier is already in use, the engine automatically
        sets another one. If an identifier is not set, the engine automatically sets one. This parameter is optional.

    Returns:
        dict: Struct "nxInfo"
    """
    return {"qId": obj_id, "qType": obj_type}


def nx_dimension(library_id="", dim_def={}, null_suppression=False):
    return {"qLibraryId": library_id, "qDef": dim_def, "qNullSuppression": null_suppression}


def nx_measure(library_id="", mes_def={}, sort_by={}):
    return {"qLibraryId": library_id, "qDef": mes_def, "qSortBy": sort_by}


def generic_object_properties(info: dict, prop_name: str, prop_def:dict = None, extends_id: str = "",
                              state_name: str = "$"):
    if prop_def is None:
        prop_def = {}
    return {"qInfo": info, "qExtendsId": extends_id, prop_name: prop_def, "qStateName": state_name}


def sort_criteria(sort_by_state: int = 1, sort_by_frequency:int = 0, sort_by_numeric: int = 1, sort_by_ascii: int = 1,
                  sort_by_load_order: int = 1, sort_by_load_expression: int = 0, expression=None,
                  sort_by_load_greyness: int = 0):
    if expression is None:
        expression = {}
    return {"qSortByState": sort_by_state, "qSortByFrequency": sort_by_frequency, "qSortByNumeric": sort_by_numeric,
            "qSortByAscii": sort_by_ascii, "qSortByLoadOrder": sort_by_load_order,
            "qSortByExpression": sort_by_load_expression, "qExpression": expression,
            "qSortByGreyness": sort_by_load_greyness}


def value_expr(qv: str = ""):
    return {"qv": qv}


def field_value(text, is_numeric = False, number = 0):
    return {"qText": text, "qIsNumeric": is_numeric, "qNumber": number}


def generic_dimension_properties(nx_info: dict, nx_library_dimension_def: dict, title: str, description: str = "",
                                 tags: list = None):
    if tags is None:
        tags = []
    return {"qInfo": nx_info, "qDim": nx_library_dimension_def, "qMetaDef": {"title": title, "description": description,
                                                                             "tags": tags}}


def nx_library_dimension_def(grouping: str = "N", field_definitions: list = None, field_labels: list = None,
                             label_expression: str = ""):
    if field_labels is None:
        field_labels = []
    if field_definitions is None:
        field_definitions = []
    return {"qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
            "qLabelExpression": label_expression}


def nx_library_measure_def(label: str, mes_def: str, grouping: str = "N", expressions: list = None,
                           active_expression: int = 0, label_expression:str = "", num_format: dict = None):
    if num_format is None:
        num_format = {}
    if expressions is None:
        expressions = []
    return {"qLabel": label, "qDef": mes_def,"qGrouping": grouping, "qExpressions": expressions,
            "qActiveExpression": active_expression, "qLabelExpression": label_expression, "qNumFormat": num_format}


def field_attributes(type: str = "U", n_dec: int = 10, use_thou:int = 0, fmt: str = "", dec: str = "", thou: str = ""):
    return {"qType": type, "qnDec": n_dec, "qUseThou": use_thou, "qFmt": fmt, "qDec": dec, "qThou": thou}


def generic_measure_properties(nx_info: dict, nx_library_measure_def: dict, title: str, description: str = "",
                               tags: list = None):
    if tags is None:
        tags = []
    return {"qInfo": nx_info, "qMeasure": nx_library_measure_def, "qMetaDef": {"title": title,
                                                                               "description": description,
                                                                               "tags": tags}}


def do_reload_ex_params(mode=0, partial=False, debug=False, reload_id="", skip_store=False, row_limit=0):
    return {"qMode": mode, "qPartial": partial, "qDebug": debug, "qReloadId": reload_id, "qSkipStore": skip_store,
            "qRowLimit": row_limit}


def dimension_list_def():
    return {"qType": "dimension",
            "qData": {"title": "/title", "tags": "/tags", "grouping": "/qDim/qGrouping", "info": "/qDimInfos"}}


def measure_list_def():
    return {"qType": "measure", "qData": {"title": "/title", "tags": "/tags"}}


def field_list_def(show_system: bool = True, show_hidden: bool = True, show_derived_fields: bool = True,
                   show_semantic: bool = True, show_src_tables: bool = True, show_implicit: bool = True):
    return {"qShowSystem": show_system, "qShowHidden": show_hidden,	"qShowDerivedFields": show_derived_fields,
            "qShowSemantic": show_semantic, "qShowSrcTables": show_src_tables, "qShowImplicit": show_implicit}

def nx_patch(op: str, path: str, value: str):
    return {"qOp": op, "qPath": path, "qValue": value}