def create_connection():

    # Import engine package
    from qe_api_client.engine import QixEngine

    # Connect to Qlik Sense Desktop engine
    url = 'ws://localhost:4848/app'
    qixe = QixEngine(url)

    return qixe


def create_sample_app(qixe):

    # Create an app
    app_name = "TestApp"
    try:
        app_id = qixe.ega.create_app(app_name)['qAppId']
    except KeyError:
        qixe.ega.delete_app(app_name)
        app_id = qixe.ega.create_app(app_name)['qAppId']

    # Open app
    opened_app = qixe.ega.open_doc(app_name)

    # Get app handle
    app_handle = qixe.get_handle(opened_app)

    # Set script
    with open('../test/test_data/ctrl00_script.qvs') as f:
        app_script = f.read()
    qixe.eaa.set_script(app_handle, app_script)

    # Reload app
    qixe.eaa.do_reload_ex(app_handle)

    # Save app
    qixe.eaa.do_save(app_handle, "TestApp")

    return app_handle


def create_sample_master_dimensions(qixe, app_handle: int):

    # Create sample master dimensions
    qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension1", dim_def="Dim1",
                                        dim_label="'Dimension 1'", dim_desc="Dimension description 1",
                                        dim_tags=["dim1", "test"])
    qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension2", dim_def="Dim2",
                                        dim_label="'Dimension 2'", dim_desc="Dimension description 2",
                                        dim_tags=["dim2", "test"])
    qixe.create_single_master_dimension(app_handle=app_handle, dim_title="Dimension3", dim_def="Dim3",
                                        dim_label="'Dimension 3'", dim_desc="Dimension description 3",
                                        dim_tags=["dim3", "test"])
    # Save app
    qixe.eaa.do_save(app_handle, "TestApp")


def create_sample_master_measures(qixe, app_handle: int):

    # Create sample master measures
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression1", mes_def="Sum(Expression1)",
                               mes_label="'Expression 1'", mes_desc="Expression description 1",
                               mes_tags=["exp1", "test"])
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression2", mes_def="Sum(Expression2)",
                               mes_label="'Expression 2'", mes_desc="Expression description 2",
                               mes_tags=["exp2", "test"])
    qixe.create_master_measure(app_handle=app_handle, mes_title="Expression3", mes_def="Sum(Expression3)",
                               mes_label="'Expression 3'", mes_desc="Expression description 3",
                               mes_tags=["exp3", "test"])
    # Save app
    qixe.eaa.do_save(app_handle, "TestApp")


def save_sample_app(qixe, app_handle: int):
    qixe.eaa.do_save(app_handle, "TestApp")


def close_connection(qixe):
    # Import engine package
    from qe_api_client.engine import QixEngine

    QixEngine.disconnect(qixe)


def delete_sample_app(qixe):
    qixe.ega.delete_app("TestApp")