import math

from qe_api_client.api_classes.engine_app_api import EngineAppApi
from qe_api_client.api_classes.engine_field_api import EngineFieldApi
from qe_api_client.api_classes.engine_generic_object_api import EngineGenericObjectApi
from qe_api_client.api_classes.engine_global_api import EngineGlobalApi
import qe_api_client.structs as structs

import pandas as pd


def getDataFrame(connection, appHandle, measures, dimensions, selections={}):
    engineGlobalApi = EngineGlobalApi(connection)
    # Define Dimensions of hypercube
    hc_inline_dim = structs.nx_inline_dimension_def(dimensions)

    # Set sorting of Dimension by Measure
    hc_mes_sort = structs.sort_criteria()

    # Define Measure of hypercube
    hc_inline_mes = structs.nx_inline_measure_def(measures)

    # Build hypercube from above definition
    hc_dim = structs.nx_dimension(hc_inline_dim)
    hc_mes = structs.nx_measure("", hc_inline_mes, hc_mes_sort)

    width = len(measures) + len(dimensions)
    height = int(math.floor(10000 / width))
    nx_page = structs.nx_page(0, 0, width, height)
    hc_def = structs.hypercube_def("$", [hc_dim], [hc_mes], [nx_page])

    engineAppApi = EngineAppApi(connection)
    hc_response = engineAppApi.create_object(appHandle, "CH01", "Chart", "qHyperCubeDef", hc_def)  # NOQA
    hc_handle = engineGlobalApi.get_handle(hc_response['qReturn'])

    engineGenericObjectApi = EngineGenericObjectApi(connection)

    engineFieldApi = EngineFieldApi(connection)

    for field in selections.keys():
        fieldHandle = engineGlobalApi.get_handle(engineAppApi.get_field(appHandle, field))  # NOQA
        values = []
        for selectedValue in selections[field]:
            values.append({'qText': selectedValue})

        engineFieldApi.select_values(fieldHandle, values)

    i = 0
    while i % height == 0:
        nx_page = structs.nx_page(0, i, width, height)
        hc_data = engineGenericObjectApi.get_hypercube_data(hc_handle, "/qHyperCubeDef", nx_page)  # NOQA
        elems = hc_data["qDataPages"][0]['qMatrix']

        df = pd.DataFrame()

        for elem in elems:
            j = 0
            for dim in dimensions:
                df.set_value(i, dim, elem[j]["qText"])
                j += 1
            for meas in measures:
                df.set_value(i, meas, elem[j]["qNum"])
                j += 1

            i += 1

    return df
