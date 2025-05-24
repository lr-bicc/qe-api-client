import uuid


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
    return {
        "qStateName": state_name, "qLibraryId": library_id, "qDef": definition,
        "qAutoSortByState": auto_sort_by_state, "qFrequencyMode": frequency_mode,
        "qShowAlternatives": show_alternatives, "qInitialDataFetch": initial_data_fetch,
        "qExpressions": expressions, "qDirectQuerySimplifiedView": direct_query_simplified_view,
        "showTitles": show_titles, "title": title, "subtitle": subtitle, "footnote": footnote,
		"disableNavMenu": disable_nav_menu, "showDetails": show_details,
        "showDetailsExpression": show_details_expression, "qOtherTotalSpec": other_total_spec
    }


def hypercube_def(
        state_name: str = "", dimensions: list = None, measures: list = None, inter_column_sort_order: list = None,
        suppress_zero: bool = False, suppress_missing: bool = False, initial_data_fetch: list = None,
        reduction_mode: str = "N", mode: str = "S", pseudo_dim_pos: int = -1, no_of_left_dims: int = -1,
        always_fully_expanded: bool = False, max_stacked_cells: int = 5000, populate_missing: bool = False,
        show_totals_above: bool = False, indent_mode: bool = False, calc_cond: dict = None, sort_by_y_value: int = 0,
        title: dict = None, calc_condition: dict = None, column_order: list = None, expansion_state: list = None,
        dynamic_script: list = None, context_set_expression: str = "", suppress_measure_totals: bool = False,
        column_widths: list = None
):

    if column_widths is None:
        column_widths = []
    if dynamic_script is None:
        dynamic_script = []
    if expansion_state is None:
        expansion_state = []
    if column_order is None:
        column_order = []
    if calc_condition is None:
        calc_condition = nx_calc_cond()
    if title is None:
        title = string_expr()
    if calc_cond is None:
        calc_cond = value_expr()
    if initial_data_fetch is None:
        initial_data_fetch = [nx_page()]
    if inter_column_sort_order is None:
        inter_column_sort_order = []
    if measures is None:
        measures = []
    if dimensions is None:
        dimensions = []

    return {
        "qStateName": state_name, "qDimensions": dimensions, "qMeasures": measures,
        "qInterColumnSortOrder": inter_column_sort_order, "qSuppressZero": suppress_zero,
        "qSuppressMissing": suppress_missing, "qInitialDataFetch": initial_data_fetch,
        "qReductionMode": reduction_mode, "qMode": mode, "qPseudoDimPos": pseudo_dim_pos,
        "qNoOfLeftDims": no_of_left_dims, "qAlwaysFullyExpanded": always_fully_expanded,
        "qMaxStackedCells": max_stacked_cells, "qPopulateMissing": populate_missing,
        "qShowTotalsAbove": show_totals_above, "qIndentMode": indent_mode, "qCalcCond": calc_cond,
        "qSortbyYValue": sort_by_y_value, "qTitle": title, "qCalcCondition": calc_condition,
        "qColumnOrder": column_order, "qExpansionState": expansion_state, "qDynamicScript": dynamic_script,
        "qContextSetExpression": context_set_expression, "qSuppressMeasureTotals": suppress_measure_totals,
        "columnOrder": column_order, "columnWidths": column_widths
    }


def nx_inline_dimension_def(
        grouping: str = "N", field_definitions: list = None, field_labels: list = None, sort_criterias: list = None,
        number_presentations: list = None, reverse_sort: bool = False, active_field: int = 0, label_expression: str = "",
        alias: str = "", auto_sort: bool = True, id = None, others_label: str = "Others", _text_align: dict = None
):

    if _text_align is None:
        _text_align = text_align()
    if id is None:
        id = str(uuid.uuid4())
    if number_presentations is None:
        number_presentations = []
    if sort_criterias is None:
        sort_criterias = [sort_criteria()]
    if field_labels is None:
        field_labels = []
    if field_definitions is None:
        field_definitions = []

    return {
        "qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
        "qSortCriterias": sort_criterias, "qNumberPresentations": number_presentations, "qReverseSort": reverse_sort,
        "qActiveField": active_field, "qLabelExpression": label_expression, "qAlias": alias, "autoSort": auto_sort,
        "cId": id, "othersLabel": others_label, "textAlign": _text_align
    }


def nx_inline_measure_def(
        label: str = "", description: str = "", tags: list = None, grouping="N", definition: str = "",
        num_format: dict = None, relative: bool = False, brutal_sum: bool = False, aggr_func: str = "Expr",
        accumulate: int = 0, reverse_sort: bool = False, active_expression: int = 0, expressions: list = None,
        label_expression: str = "", auto_sort: bool = True, id = None, num_format_from_template: bool = True,
        _text_align: dict = None
):

    if _text_align is None:
        _text_align = text_align()
    if id is None:
        id = str(uuid.uuid4())
    if tags is None:
        tags = []
    if expressions is None:
        expressions = []
    if num_format is None:
        num_format = {}

    return {
        "qLabel": label, "qDescription": description, "qTags": tags, "qGrouping": grouping, "qDef":	definition,
        "qNumFormat": num_format, "qRelative": relative, "qBrutalSum": brutal_sum, "qAggrFunc": aggr_func,
        "qAccumulate": accumulate, "qReverseSort": reverse_sort, "qActiveExpression": active_expression,
        "qExpressions": expressions, "qLabelExpression": label_expression, "autoSort": auto_sort, "cId": id,
        "numFormatFromTemplate": num_format_from_template, "textAlign": _text_align
    }


def nx_page(left: int = 0, top: int = 0, width: int = 50, height: int = 50):
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


def nx_dimension(
        library_id: str = "", dim_def: dict = None, null_suppression: bool = False, include_elem_value: bool = False,
        other_total_spec: dict = None, show_total: bool = False, show_all: bool = False, other_label: dict = None,
        total_label: dict = None, calc_cond: dict = None, attribute_expressions: list = None,
        attribute_dimensions: list = None, calc_condition: dict = None
):

    if calc_condition is None:
        calc_condition = nx_calc_cond()
    if attribute_dimensions is None:
        attribute_dimensions = []
    if attribute_expressions is None:
        attribute_expressions = []
    if calc_cond is None:
        calc_cond = value_expr()
    if total_label is None:
        total_label = string_expr(qv="Totals")
    if other_label is None:
        other_label = string_expr(qv="Others")
    if other_total_spec is None:
        other_total_spec = {}
    if dim_def is None:
        dim_def = {}

    return {
        "qLibraryId": library_id, "qDef": dim_def, "qNullSuppression": null_suppression,
        "qIncludeElemValue": include_elem_value, "qOtherTotalSpec": other_total_spec, "qShowTotal": show_total,
        "qShowAll": show_all, "qOtherLabel": other_label, "qTotalLabel": total_label, "qCalcCond": calc_cond,
        "qAttributeExpressions": attribute_expressions, "qAttributeDimensions": attribute_dimensions,
        "qCalcCondition": calc_condition
    }


def nx_measure(
        library_id: str = "", mes_def: dict = None, sort_by: dict = None, attribute_expressions: list = None,
        attribute_dimensions: list = None, calc_cond: dict = None, calc_condition: dict = None, trend_lines: list = None
):

    if trend_lines is None:
        trend_lines = []
    if calc_condition is None:
        calc_condition = nx_calc_cond()
    if calc_cond is None:
        calc_cond = value_expr()
    if attribute_dimensions is None:
        attribute_dimensions = []
    if attribute_expressions is None:
        attribute_expressions = []
    if sort_by is None:
        sort_by = sort_criteria()
    if mes_def is None:
        mes_def = {}

    return {
        "qLibraryId": library_id, "qDef": mes_def, "qSortBy": sort_by, "qAttributeExpressions": attribute_expressions,
        "qAttributeDimensions": attribute_dimensions, "qCalcCond": calc_cond, "qCalcCondition": calc_condition,
        "qTrendLines": trend_lines
    }


def generic_object_properties(info: dict, prop_name: str, prop_def:dict = None, extends_id: str = "",
                              state_name: str = ""):
    if prop_def is None:
        prop_def = {}
    return {"qInfo": info, "qExtendsId": extends_id, prop_name: prop_def, "qStateName": state_name}


def sort_criteria(
        sort_by_state: int = 1, sort_by_frequency:int = 0, sort_by_numeric: int = 1, sort_by_ascii: int = 1,
        sort_by_load_order: int = 1, sort_by_load_expression: int = 0, expression=None, sort_by_load_greyness: int = 0
):

    if expression is None:
        expression = value_expr()

    return {
        "qSortByState": sort_by_state, "qSortByFrequency": sort_by_frequency, "qSortByNumeric": sort_by_numeric,
        "qSortByAscii": sort_by_ascii, "qSortByLoadOrder": sort_by_load_order,
        "qSortByExpression": sort_by_load_expression, "qExpression": expression,
        "qSortByGreyness": sort_by_load_greyness
    }


def value_expr(qv: str = ""):
    return {"qv": qv}


def string_expr(qv: str = ""):
    return {"qv": qv}


def nx_calc_cond(cond: dict = None, msg: dict = None):
    if msg is None:
        msg = string_expr()
    if cond is None:
        cond = value_expr()
    return {"qCond": cond, "qMsg": msg}


def field_value(text, is_numeric = False, number = 0):
    return {"qText": text, "qIsNumeric": is_numeric, "qNumber": number}


def generic_dimension_properties(nx_info: dict, nx_library_dimension_def: dict, title: str, description: str = "",
                                 tags: list = None):
    if tags is None:
        tags = []
    return {"qInfo": nx_info, "qDim": nx_library_dimension_def, "qMetaDef": {"title": title, "description": description,
                                                                             "tags": tags}}


def nx_library_dimension_def(grouping: str = "N", field_definitions: list = None, field_labels: list = None,
                             label_expression: str = "", alias: str = "", title: str = "", coloring: dict = None):
    if coloring is None:
        coloring = {}
    if field_labels is None:
        field_labels = []
    if field_definitions is None:
        field_definitions = []
    return {
        "qGrouping": grouping, "qFieldDefs": field_definitions, "qFieldLabels": field_labels,
        "qLabelExpression": label_expression, "qAlias": alias, "title": title, "coloring": coloring
    }


def nx_library_measure_def(label: str, mes_def: str, grouping: str = "N", expressions: list = None,
                           active_expression: int = 0, label_expression:str = "", num_format: dict = None,
                           coloring: dict = None):
    if coloring is None:
        coloring = {}
    if num_format is None:
        num_format = {}
    if expressions is None:
        expressions = []
    return {
        "qLabel": label, "qDef": mes_def,"qGrouping": grouping, "qExpressions": expressions,
        "qActiveExpression": active_expression, "qLabelExpression": label_expression, "qNumFormat": num_format,
        "coloring": coloring
    }


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


def sheet_list_def():
    return {
        "qType": "sheet",
        "qData": {
            "title": "/qMetaDef/title",
            "description": "/qMetaDef/description",
            "thumbnail": "/thumbnail",
            "cells": "/cells",
            "rank": "/rank",
            "columns": "/columns",
            "rows": "/rows"
        }
    }


def variable_list_def():
    return {
        "qType": "variable",
        "qShowReserved": True,
        "qShowConfig": True,
        "qData": {
            "tags": "/tags"
        }
    }


def nx_patch(op: str, path: str, value: str):
    return {"qOp": op, "qPath": path, "qValue": value}


def object_position_size(obj_id: str, obj_type: str, col: int, row: int, colspan: int, rowspan: int, y: float, x: float,
                         width: float, height: float):
    return {
        "name": obj_id,
        "type": obj_type,
        "col": col,
        "row": row,
        "colspan": colspan,
        "rowspan": rowspan,
        "bounds": {
            "y": y,
            "x": x,
            "width": width,
            "height": height
        }
    }


def nx_attr_expr_def(expression: str = "", library_id: str = "", attribute: bool = True, num_format: dict = None,
                     label: str = "", label_expression: str = ""):
    if num_format is None:
        num_format = {}
    return {
        "qExpression": expression,
        "qLibraryId": library_id,
        "qAttribute": attribute,
        "qNumFormat": num_format,
        "qLabel": label,
        "qLabelExpression": label_expression
    }


def table_properties(
        info: dict, hypercube_def: dict, prop_def: dict = None, extends_id: str = "", state_name: str = "",
        script: str = "", _search: dict = None, show_titles: bool = True, title: str = "", subtitle: str = "",
        footnote: str = "", disable_nav_menu: bool = False, show_details: bool = False,
        show_details_expression: bool = False, _totals: dict = None, scrolling_horizontal: bool = True, scrolling_keep_first_column_in_view: bool = False,
        scrolling_keep_first_column_in_view_touch: bool = False, multiline_wrap_text_in_headers: bool = True,
        multiline_wrap_text_in_cells: bool = True
):

    if _totals is None:
        _totals = totals()
    if prop_def is None:
        prop_def = {}
    if _search is None:
        _search = search()

    return {
        "qInfo": info, "qExtendsId": extends_id, "qMetaDef": prop_def, "qStateName": state_name,
        "qHyperCubeDef": hypercube_def, "script": script, "search": _search, "showTitles": show_titles, "title": title,
        "subtitle": subtitle, "footnote": footnote, "disableNavMenu": disable_nav_menu, "showDetails": show_details,
        "showDetailsExpression": show_details_expression, "totals": _totals,
        "scrolling": {"horizontal": scrolling_horizontal, "keepFirstColumnInView": scrolling_keep_first_column_in_view, "keepFirstColumnInViewTouch": scrolling_keep_first_column_in_view_touch},
        "multiline": {"wrapTextInHeaders": multiline_wrap_text_in_headers, "wrapTextInCells": multiline_wrap_text_in_cells},
        "visualization": "table"
    }


def sn_table_properties(
        info: dict, hypercube_def: dict, prop_def: dict = None, extends_id: str = "", state_name: str = "",
        show_titles: bool = True, title: str = "", subtitle: str = "", footnote: str = "", disable_nav_menu: bool = False,
        show_details: bool = False, show_details_expression: bool = False, components: list = None, _totals: dict = None,
        use_pagination: bool = False, enable_chart_exploration: bool = False, chart_exploration: dict = None
):

    if chart_exploration is None:
        chart_exploration = {"menuVisibility": "auto"}
    if components is None:
        components = []
    if _totals is None:
        _totals = totals()
    if prop_def is None:
        prop_def = {}

    return {
        "qInfo": info, "qExtendsId": extends_id, "qMetaDef": prop_def, "qStateName": state_name,
        "qHyperCubeDef": hypercube_def, "showTitles": show_titles, "title": title, "subtitle": subtitle,
        "footnote": footnote, "disableNavMenu": disable_nav_menu, "showDetails": show_details,
        "showDetailsExpression": show_details_expression, "components": components, "totals": _totals,
        "usePagination": use_pagination, "enableChartExploration": enable_chart_exploration,
        "chartExploration": chart_exploration, "visualization": "sn-table"
    }


def pivot_table_properties(
        info: dict, hypercube_def: dict, prop_def: dict = None, extends_id: str = "", state_name: str = "",
        _search: dict = None, show_titles: bool = True, title: str = "", subtitle: str = "",
        footnote: str = "", disable_nav_menu: bool = False, show_details: bool = True,
        show_details_expression: bool = False
):

    if prop_def is None:
        prop_def = {}
    if _search is None:
        _search = search()

    return {
        "qInfo": info, "qExtendsId": extends_id, "qMetaDef": prop_def, "qStateName": state_name,
        "qHyperCubeDef": hypercube_def, "search": _search, "showTitles": show_titles, "title": title,
        "subtitle": subtitle, "footnote": footnote, "disableNavMenu": disable_nav_menu, "showDetails": show_details,
        "showDetailsExpression": show_details_expression, "visualization": "pivot-table"
    }


def sn_pivot_table_properties(
        info: dict, hypercube_def: dict, prop_def: dict = None, extends_id: str = "", state_name: str = "",
        _search: dict = None, show_titles: bool = True, title: str = "", subtitle: str = "",
        footnote: str = "", disable_nav_menu: bool = False, show_details: bool = True,
        show_details_expression: bool = False, components: list = None, null_value_representation: dict = None
):
    if null_value_representation is None:
        null_value_representation = {"text": "-"}
    if components is None:
        components = []
    if prop_def is None:
        prop_def = {}
    if _search is None:
        _search = search()

    return {
        "qInfo": info, "qExtendsId": extends_id, "qMetaDef": prop_def, "qStateName": state_name,
        "qHyperCubeDef": hypercube_def, "search": _search, "showTitles": show_titles, "title": title,
        "subtitle": subtitle, "footnote": footnote, "disableNavMenu": disable_nav_menu, "showDetails": show_details,
        "showDetailsExpression": show_details_expression, "components": components,
        "nullValueRepresentation": null_value_representation, "visualization": "sn-pivot-table"
    }


def search(sorting: str = "auto"):
    return {"sorting": sorting}


def text_align(auto: bool = True, align: str = "left"):
    return {"auto": auto, "align": align}


def totals(totals_show: bool = True, totals_position: str = "noTotals", totals_label: str = "Totals"):
    return {"show": totals_show, "position": totals_position, "label": totals_label}


def color_map(colors: list = None, nul: dict = None, oth: dict = None, pal: str = None, single: dict = None,
              use_pal: bool = True, auto_fill: bool = True):

    if colors is None:
        colors = []

    return {
        "colors": colors,
        "nul": nul,
        "oth": oth,
        "pal": pal,
        "single": single,
        "usePal": use_pal,
        "autoFill": auto_fill
    }


def dim_coloring(change_hash: str = None, color_map_ref: str = "", has_value_colors: bool = False, base_color: dict = None):
    if base_color is None:
        base_color = {"color": "none", "index": 0}
    return {
        "changeHash": change_hash,
        "colorMapRef": color_map_ref,
        "hasValueColors": has_value_colors,
        "baseColor": base_color
    }


def mes_coloring(base_color: dict = None, _gradient: dict = None):
    coloring = {}
    if base_color is not None:
        coloring.update({"baseColor": base_color})
    if _gradient is not None:
        coloring.update({"gradient": _gradient})
    return coloring


def color_map_properties(dim_id: str, prop_def:dict = None, extends_id: str = "", state_name: str = "",
                         _color_map: dict = None):

    if _color_map is None:
        _color_map = color_map()
    if prop_def is None:
        prop_def = {}
    info = nx_info(obj_type="ColorMap", obj_id="ColorMapModel_" + dim_id)

    return {
        "qInfo": info, "qExtendsId": extends_id, "qMetaDef": prop_def, "qStateName": state_name, "colorMap": _color_map
    }


def value_color(value: str, color: str, index: int = -1):
    return {
        "value": value,
        "baseColor": {"color": color, "index": index}
    }


def color(_color: str, index: int = -1):
    return {"color": _color, "index": index}


def gradient(colors: list = None, break_types: list = None, limits: list = None, limit_type: str = "percent"):
    if colors is None:
        colors = [color(_color="#332288"), color(_color="#117733")]
    if break_types is None:
        break_types = [False]
    if limits is None:
        limits = [0.5]
    return {"colors": colors, "breakTypes": break_types, "limits": limits, "limitType": limit_type}