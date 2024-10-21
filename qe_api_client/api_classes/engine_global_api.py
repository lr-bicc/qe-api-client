import json


class EngineGlobalApi:
    """
    A class to interact with the Qlik Engine Global API using a provided socket interface.

    Attributes:
    engine_socket : object
        The socket object used to communicate with the Qlik Engine.
    """

    def __init__(self, socket):
        """
        Initializes the EngineGlobalApi with a socket object.

        Parameters:
        socket : object
            The socket object used to communicate with the Qlik Engine.
        """
        self.engine_socket = socket

    def get_doc_list(self):
        """
        Retrieves a list of documents available in the Qlik Sense environment.

        Returns:
        list of dict: An array of document objects containing details such as doc name, size, and file time.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetDocList", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']['qDocList']
        except KeyError:
            return response['error']

    def get_os_name(self):
        """
        Retrieves the operating system name where the Qlik Sense Engine is running.

        Returns:
        str: The OS name, typically "windowsNT".
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "OSName", "params": []})
        response = json.loads(
            self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']['qReturn']
        except KeyError:
            return response['error']

    def create_app(self, app_name):
        """
        Creates a new application in Qlik Sense.

        Parameters:
        app_name : str
            The name of the application to be created.

        Returns:
        dict: Information about the created app, including its ID.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateApp", "params": [app_name]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # DeleteApp Method Deletes an app from the Qlik Sense repository or from the file system. Qlik Sense Enterprise:  # NOQA
    # In addition to being removed from the repository, the app is removed from the directory as well:  # NOQA
    # <installation_directory>\Qlik\Sense\Apps The default installation directory is ProgramData. Qlik Sense Desktop:  # NOQA
    #  The app is deleted from the directory %userprofile%\Documents\Qlik\Sense\Apps. Parameters: qAppId.. Identifier  # NOQA
    #  of the app to delete. In Qlik Sense Enterprise, the identifier of the app is a GUID in the Qlik Sense  # NOQA
    # repository. In Qlik Sense Desktop, the identifier of the app is the name of the app, as defined in the apps  # NOQA
    # folder %userprofile%\Documents\Qlik\Sense\Apps. This parameter is mandatory.  # NOQA
    def delete_app(self, app_name):
        """
        Deletes an application from the Qlik Sense repository or file system.

        Parameters:
        app_name : str
            The name or identifier of the app to delete.

        Returns:
        dict: Information about the deletion result.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "DeleteApp",
                          "params": {"qAppId": app_name}})
        response = json.loads(
            self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    def open_doc(self, app_name, user_name='', password='', serial='', no_data=False):
        """
        Opens a document (app) in Qlik Sense and returns details about it.

        Parameters:
        app_name : str
            The name of the app to open.
        user_name : str, optional
            The username for authentication (default is '').
        password : str, optional
            The password for authentication (default is '').
        serial : str, optional
            The serial key for authentication (default is '').
        no_data : bool, optional
            If True, opens the app without data (default is False).

        Returns:
        dict: Information about the opened document, including handle, generic ID, and type.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "OpenDoc",
                          "params": [app_name, user_name, password, serial, no_data]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]["qReturn"]
        except KeyError:
            return response["error"]

    # returns an object with handle, generic id and type for the active app
    def get_active_doc(self):
        """
        Retrieves the currently active document in Qlik Sense.

        Returns:
        dict: Information about the active document.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetActiveDoc", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # Abort All commands
    def abort_all(self):
        """
        Aborts all ongoing commands in Qlik Sense.

        Returns:
        dict: Information about the abort result.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "AbortAll", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # Abort Specific Request
    def abort_request(self, request_id):
        """
        Aborts a specific request in Qlik Sense.

        Parameters:
        request_id : str
            The identifier of the request to abort.

        Returns:
        dict: Information about the abort result.
        """
        msg = json.dumps(
            {"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "AbortRequest", "params": {"qRequestId": request_id}})
        response = json.loads(
            self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']  # ['qReturn']
        except KeyError:
            return response["error"]

    # Configure Reload - This is done before doing a reload qCancelOnScriptError: If set to true, the script  # NOQA
    # execution is halted on error. Otherwise, the engine continues the script execution. This parameter is relevant  # NOQA
    # only if the variable ErrorMode is set to 1. qUseErrorData: If set to true, any script execution error is  # NOQA
    # returned in qErrorData by the GetProgress method. qInteractOnError: If set to true, the script execution is  # NOQA
    # halted on error and the engine is waiting for an interaction to be performed. If the result from the  # NOQA
    # interaction is 1 (qDef.qResult is 1), the engine continues the script execution otherwise the execution is  # NOQA
    # halted. This parameter is relevant only if the variable ErrorMode is set to 1 and the script is run in debug  # NOQA
    # mode (qDebug is set to true when calling the DoReload method).
    def configure_reload(self, cancel_on_error=False, use_error_data=True, interact_on_error=False):
        """
        Configures the reload settings for a Qlik Sense application.

        Parameters:
        cancel_on_error : bool, optional
            If True, the script execution is halted on error (default is False).
        use_error_data : bool, optional
            If True, any script execution error is returned in qErrorData (default is True).
        interact_on_error : bool, optional
            If True, script execution is halted on error and awaits interaction (default is False).

        Returns:
        dict: Information about the configuration result.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ConfigureReload",
                          "params": {"qCancelOnScriptError": cancel_on_error, "qUseErrorData": use_error_data,
                                     "qInteractOnError": interact_on_error}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # Copy app - This is done before doing a reload qTargetAppId (MANDATORY):  Identifier (GUID) of the app  # NOQA
    # entity in the Qlik Sense repository. The app entity must have been previously created by the repository (via  # NOQA
    # the REST API). qSrcAppId (MANDATORY): Identifier (GUID) of the source app in the Qlik Sense repository. Array  # NOQA
    # of QRS identifiers. The list of all the objects in the app to be copied must be given. This list must contain  # NOQA
    # the GUIDs of all these objects. If the list of the QRS identifiers is empty, the CopyApp method copies all  # NOQA
    # objects to the target app. Script-defined variables are automatically copied when copying an app. To be able to  # NOQA
    #  copy variables not created via script, the GUID of each variable must be provided in the list of QRS  # NOQA
    # identifiers. To get the QRS identifiers of the objects in an app, you can use the QRS API. The GET method (from  # NOQA
    #  the QRS API) returns the identifiers of the objects in the app. The following example returns the QRS  # NOQA
    # identifiers of all the objects in a specified app: GET /qrs/app/9c3f8634-6191-4a34-a114-a39102058d13 Where  # NOQA
    # 9c3f8634-6191-4a34-a114-a39102058d13 is the identifier of the app.

    # BUG - Does not work in September 2017 release
    def copy_app(self, target_app_id, src_app_id, qIds=[""]):
        """
        Copies an app in Qlik Sense from a source app ID to a target app ID.

        Parameters:
        target_app_id : str
            The identifier (GUID) of the target app.
        src_app_id : str
            The identifier (GUID) of the source app.
        qIds : list, optional
            List of object identifiers to copy. If empty, all objects are copied (default is [""]).

        Returns:
        dict: Information about the copy result.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CopyApp",
                          "params": {"qTargetAppId": target_app_id, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = json.loads(
            self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # Creates an empty session app. The following applies: The name of a session app cannot be chosen. The engine  # NOQA
    # automatically assigns a unique identifier to the session app. A session app is not persisted and cannot be  # NOQA
    # saved. Everything created during a session app is non-persisted; for example: objects, data connections.  # NOQA
    def create_session_app(self):
        """
        Creates an empty session app in Qlik Sense.

        Returns:
        dict: Information about the created session app.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateSessionApp", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

            # Return the session App Id to use for subsequent calls
            # The identifier of the session app is composed of the prefix SessionApp_ and of a GUID.  # NOQA
            # ['qReturn']

    # Create an empty session app from an Existing App The objects in the source app are copied into the session app  # NOQA
    # but contain no data. The script of the session app can be edited and reloaded. The name of a session app cannot  # NOQA
    #  be chosen. The engine automatically assigns a unique identifier to the session app. A session app is not  # NOQA
    # persisted and cannot be saved. Everything created during a session app is non-persisted; for example: objects,  # NOQA
    # data connections.
    def create_session_app_from_app(self, src_app_id):
        """
        Creates a session app in Qlik Sense from an existing app.

        Parameters:
        src_app_id : str
            The identifier (GUID) of the source app.

        Returns:
        dict: Information about the created session app.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "CreateSessionAppFromApp",
                          "params": {"qSrcAppId": src_app_id}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # ExportApp method: Exports an app from the Qlik Sense repository to the file system. !!! This operation is  # NOQA
    # possible only in Qlik Sense Enterprise. !!! Parameters: qTargetPath (MANDATORY) - Path and name of the target  # NOQA
    # app qSrcAppId (MANDATORY) - Identifier of the source app. The identifier is a GUID from the Qlik Sense  # NOQA
    # repository. qIds - Array of identifiers.. The list of all the objects in the app to be exported must be given.  # NOQA
    # This list must contain the GUIDs of all these objects.
    def export_app(self, target_path, src_app_id, qIds=[""]):
        """
        Exports an app from the Qlik Sense repository to the file system.

        This operation is available only in Qlik Sense Enterprise.

        Parameters:
            target_path (str): The path and name of the target app file to export to.
            src_app_id (str): The GUID of the source app in the Qlik Sense repository.
            qIds (list of str): An array of identifiers (GUIDs) for the objects in the app to be exported.
                                The list must contain the GUIDs of all these objects.

        Returns:
            dict: The result of the export operation. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ExportApp",
                          "params": {"qTargetPath": target_path, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response["error"]

    # ReplaceAppFromID method: Replaces an app with the objects from a source app. The list of objects in the app to  # NOQA
    # be replaced must be defined in qIds. !!! This operation is possible only in Qlik Sense Enterprise. !!!  # NOQA
    # Parameters: qTargetAppId (MANDATORY) - Identifier (GUID) of the target app. The target app is the app to be  # NOQA
    # replaced. qSrcAppId (MANDATORY) - Identifier of the source app. The identifier is a GUID from the Qlik Sense  # NOQA
    # repository. qIds - QRS identifiers (GUID) of the objects in the target app to be replaced. Only QRS-approved  # NOQA
    # GUIDs are applicable. An object that is QRS-approved, is for example an object that has been published (i.e not  # NOQA
    #  private anymore). If an object is private, it should not be included in this list.  If qIds is empty,  # NOQA
    # the engine automatically creates a list that contains all QRS-approved objects. If the array of identifiers  # NOQA
    # contains objects that are not present in the source app, the objects related to these identifiers are removed  # NOQA
    # from the target app.
    def replace_app_from_id(self, target_path, src_app_id, qIds=[""]):
        """
        Replaces an app with the objects from a source app.

        The list of objects in the app to be replaced must be defined in qIds.
        This operation is available only in Qlik Sense Enterprise.

        Parameters:
            target_app_id (str): The GUID of the target app to be replaced.
            src_app_id (str): The GUID of the source app in the Qlik Sense repository.
            qIds (list of str): An array of GUIDs for the objects in the target app to be replaced.
                                Only QRS-approved GUIDs are applicable. If qIds is empty,
                                the engine automatically creates a list containing all QRS-approved objects.
                                If the array contains objects not present in the source app,
                                those objects are removed from the target app.

        Returns:
            dict: The result of the replace operation. In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "ReplaceAppFromID",
                          "params": {"qTargetAppId": target_path, "qSrcAppId": src_app_id, "qIds": qIds}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # GetAuthenticatedUser
    # No parameters
    def get_auth_user(self):
        """
        Retrieves information about the authenticated user.

        Returns:
            dict: The result containing information about the authenticated user.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetAuthenticatedUser", "params": {}})
        response_json = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response_json["result"]
        except KeyError:
            return response_json["error"]

    # GetDatabasesFromConnectionString Lists the databases in a ODBC, OLEDB or CUSTOM data source (global level)  # NOQA
    # Parameters: qConnection (object - has several fields) qId: Identifier of the connection. Is generated by  # NOQA
    # the engine and is unique. qName (MANDATORY): Name of the connection. This parameter is mandatory and must  # NOQA
    # be set when creating or modifying a connection. qConnectionString (MANDATORY): One of: ODBC CONNECT TO [  # NOQA
    # <provider name>], OLEDB CONNECT TO [<provider name>], CUSTOM CONNECT TO [<provider name>], "<local absolut  # NOQA
    #  or relative path,UNC path >", "<URL>" Connection string. qType (MANDATORY): Type of the connection. One  # NOQA
    # of- ODBC, OLEDB, <Name of the custom connection file>, folder, internet. For ODBC, OLEDB and custom  # NOQA
    # connections, the engine checks that the connection type matches the connection string. The type is not cas  # NOQA
    #  sensitive. qUserName: Name of the user who creates the connection. This parameter is optional; it is only  # NOQA
    # used for OLEDB, ODBC and CUSTOM connections. A call to GetConnection method does not return the user name.  # NOQA
    # qPassword: Password of the user who creates the connection. This parameter is optional; it is only used fo  # NOQA
    #  OLEDB, ODBC and CUSTOM connections. A call to GetConnection method does not return the password.  # NOQA
    # qModifiedDate: Is generated by the engine. Creation date of the connection or last modification date of th  # NOQA
    #  connection. qMeta: Information about the connection. qLogOn (SSO Passthrough or not): Select which user  # NOQA
        # credentials to use to connect to the source. LOG_ON_SERVICE_USER: Disables, LOG_ON_CURRENT_USER: Enabl  # NOQA
    def list_databases_from_odbc(self, connect_name, connect_string, connect_type, user_name, password, mod_date="",
                                 meta="", sso_passthrough="LOG_ON_SERVICE_USER"):
        """
        Lists the databases available in an ODBC, OLEDB, or CUSTOM data source.

        Parameters:
            connect_name (str): Name of the connection.
            connect_string (str): Connection string (e.g., ODBC CONNECT TO [<provider name>]).
            connect_type (str): Type of the connection (ODBC, OLEDB, CUSTOM, etc.).
            user_name (str): Name of the user creating the connection.
            password (str): Password of the user creating the connection.
            mod_date (str, optional): Modification date of the connection.
            meta (str, optional): Metadata information about the connection.
            sso_passthrough (str, optional): User credentials to use (LOG_ON_SERVICE_USER, LOG_ON_CURRENT_USER).

        Returns:
            dict: A dictionary containing the list of databases.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetDatabasesFromConnectionString",
                          "params": [{"qId": "", "qName": connect_name, "qConnectionString": connect_string,
                                      "qType": connect_type, "qUserName": user_name, "qPassword": password,
                                      "qModifiedDate": mod_date, "qMeta": meta, "qLogOn": sso_passthrough}]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # IsValidConnectionString method: Checks if a connection string is valid.
    def is_valid_connect_string(self, connect_name, connect_string, connect_type, user_name, password, mod_date="",
                                meta="", sso_passthrough="LOG_ON_SERVICE_USER"):
        """
        Checks if a connection string is valid.

        Parameters:
            connect_name (str): Name of the connection.
            connect_string (str): Connection string (e.g., ODBC CONNECT TO [<provider name>]).
            connect_type (str): Type of the connection (ODBC, OLEDB, CUSTOM, etc.).
            user_name (str): Name of the user creating the connection.
            password (str): Password of the user creating the connection.
            mod_date (str, optional): Modification date of the connection.
            meta (str, optional): Metadata information about the connection.
            sso_passthrough (str, optional): User credentials to use (LOG_ON_SERVICE_USER, LOG_ON_CURRENT_USER).

        Returns:
            dict: A dictionary containing validation information.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "IsValidConnectionString",
                          "params": [{"qId": "", "qName": connect_name, "qConnectionString": connect_string,
                                      "qType": connect_type, "qUserName": user_name, "qPassword": password,
                                      "qModifiedDate": mod_date, "qMeta": meta, "qLogOn": sso_passthrough}]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']  # Returns an array of databases
        except KeyError:
            return response['error']

    # GetOdbcDsns: List all the ODBC connectors installed on the Sense server machine in Windows  # NOQA
    def get_odbc_dsns(self):
        """
        Retrieves a list of all ODBC connectors installed on the Qlik Sense server.

        Returns:
            dict: A dictionary containing the details of the ODBC connectors installed.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetOdbcDsns", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # GetOleDbProviders: Returns the list of the OLEDB providers installed on the system.  # NOQA
    def get_ole_dbs(self):
        """
        Retrieves a list of all OLEDB providers installed on the Qlik Sense server.

        Returns:
            dict: A dictionary containing the details of the OLEDB providers installed.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetOleDbProviders", "params": {}})
        response = json.loads(
            self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # GetProgress: Gives information about the progress of the DoReload and DoSave calls. Parameters: qRequestId:  # NOQA
    # Identifier of the DoReload or DoSave request or 0. Complete information is returned if the identifier of the  # NOQA
    # request is given. If the identifier is 0, less information is given. Progress messages and error messages are  # NOQA
    # returned but information like when the request started and finished is not returned.  # NOQA

    def get_progress(self, request_id):
        """
        Provides information about the progress of DoReload and DoSave calls.

        Parameters:
            request_id (int): Identifier of the DoReload or DoSave request.
                              If set to 0, only limited information is provided.

        Returns:
            dict: A dictionary containing progress messages and error messages.
                  If request_id is 0, detailed information like start and end times is not provided.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "GetProgress", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # IsDesktopMode: Indicates whether the user is working
    # in Qlik Sense Desktop.
    # No parameters
    def is_desktop_mode(self, request_id):
        """
        Checks if the user is working in Qlik Sense Desktop mode.

        Returns:
            dict: A dictionary indicating whether the user is in desktop mode.
                  In case of an error, returns the error information.
        """
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": -1, "method": "IsDesktopMode", "params": {}})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response['result']
        except KeyError:
            return response['error']

    # ## NOT IMPLEMENTED, perceived out of use case scope: ## CreateDocEx, GetBaseBNFHash, GetBaseBNF, GetBNF,  # NOQA
        # GetCustomConnectors, GetDefaultAppFolder, GetFunctions, GetInteract, GetLogicalDriveStrings,  # NOQA
        # ## GetStreamList, GetSupportedCodePages, GetUniqueID, InteractDone, IsPersonalMode (deprecated), OSVersion,  # NOQA
        #  ProductVersion (depr), QTProduct, QvVersion (depr), ## ReloadExtensionList, ReplaceAppFromID,  # NOQA
