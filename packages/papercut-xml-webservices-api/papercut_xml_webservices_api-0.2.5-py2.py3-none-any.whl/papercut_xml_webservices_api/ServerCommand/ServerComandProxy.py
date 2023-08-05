"""Main module."""

from contextlib import contextmanager
from xmlrpc.client import ServerProxy


class ServerCommandProxy:

    """
    A proxy designed to wrap XML-RPC calls to the Application Server's XML-RPC API endpoint

    The constructor

    Parameters:

        - `host` (str): The name or IP address of the server hosting the Application Server. The server should be configured to allow XML-RPC connections from the host running this library
            - `Localhost` is generally accepted by default
        - `port` (str): The port the Application Server is listening on
            - Default is `9191`. This is the listening port for your PaperCut App server
        - `ssl` (bool): If `True`; Requests are transmitted over HTTPS. Ensure to change your port to `9192` or preferred port configured in your `server.properties` configuration file
            - default = `False`
            - [Change the Application Server ports](https://www.papercut.com/help/manuals/ng-mf/common/sys-security-options-change-ports/)
        - `verbose` (bool): Enables debugging and raw XMLRPC output for requests

    See Also:
    - [PaperCut MF/NG user manual](https://www.papercut.com/help/manuals/ng-mf/)

    """

    def __init__(self, host="localhost", port=9191, ssl=False, verbose=False):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.verbose = verbose

        if self.ssl is True:
            self.url = f"https://{self.host}:{self.port}/rpc/api/xmlrpc"
        else:
            self.url = f"http://{self.host}:{self.port}/rpc/api/xmlrpc"

        self.api = None

    @contextmanager
    def __enter__(self):
        self.api = ServerProxy(uri=self.url, verbose=self.verbose, allow_none=True).api
        return self.api

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.api.__close

    def addAdminAccessGroup(self, authToken: str, groupName: str):
        """
        Adds a group as an admin group with the default admin rights

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group

        Returns:
        """
        return self.api.addAdminAccessGroup(authToken, groupName)

    def addAdminAccessUser(self, authToken: str, userName: str):
        """
        Adds a user as administrator with the default admin rights

        Parameters:
        - `Required`
            - `userName` (str): The name of the user

        Returns:
        """
        return self.api.addAdminAccessUser(authToken, userName)

    def addNewGroup(self, authToken: str, groupName: str):
        """
        Add a new group to system's group list. The caller is responsible for ensuring that the supplied group name is valid and exists in the linked user directory source. The status of this method may be monitored with calls to getTaskStatus()

        Parameters:
        - `Required`
            - `groupName` (str): The name of the new group to add. The group should already exist in the network user directory

        Returns:
        """
        return self.api.addNewGroup(authToken, groupName)

    def addNewInternalUser(
        self,
        authToken: str,
        userName: str,
        password: str,
        fullName=None,
        email=None,
        cardId=None,
        pin=None,
    ):
        """
        Creates and sets up a new internal user account
            - The (unique) username and password are required at a minimum
            - Additional properties are optional and will be used if not blank. Properties may also be set after creation using `setUserProperty()` or `setUserProperties()`

        Parameters:
        - `Required`
            - `username` (str): A unique username. An exception is thrown if the username already exists
            - `password` (str): The user's password
        - `Optional`
            - `fullName` (str): The full name of the user
            - `email` (str): The email address of the user
            - `cardId` (str): The card/identity number of the user
            - `pin` (int): The card/id pin

        Returns:
        """
        return self.api.addNewInternalUser(
            authToken, userName, password, fullName, email, cardId, pin
        )

    def addNewSharedAccount(self, authToken: str, sharedAccountName: str):
        """
        Create a new shared account with the given name

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to create. Use a '\\\\' to denote a subaccount
                - e.g.: `'parent\sub' renameSharedAccount`

        Returns:
        """
        return self.api.addNewSharedAccount(authToken, sharedAccountName)

    def addNewUser(self, authToken: str, userName: str):
        """
        Trigger the process of adding a new user account. \\
        Assuming the user exists in the OS/Network/Domain user directory, the account will be created with the correct initial settings as defined by the rules setup in the admin interface under the Group's section. \\
        Calling this method is equivalent to triggering the "new user" event when a new user performs printing for the first time

        Parameters:
        - `Required`
            - `username` (str): The username of the user to add
        """
        return self.api.addNewUser(authToken, userName)

    def addNewUsers(self, authToken: str):
        """
        Calling this method will start a specialized user and group synchronization process optimized for tracking down adding any new users that exist in the OS/Network/Domain user directory and not in the system. \\
        - Any existing user accounts will not be modified
        - Group synchronization will only be performed if new users are actually added to the system

        Returns:
        """
        return self.api.addNewUsers(authToken)

    def addPrinterAccessGroup(
        self, authToken: str, serverName: str, printerName: str, groupName: str
    ):
        """
        Adds the group to the printer access group list

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server name
            - `printerName` (str): The name of the printer
            - `groupName` (str): name of the group that needs to be added to the list of groups that are allowed to print to this printer

        Returns:
        """
        return self.api.addPrinterAccessGroup(
            authToken, serverName, printerName, groupName
        )

    def addPrinterGroup(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        printerGroupName: str,
    ):
        """
        Add a printer to a single printer group

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The printer's name
            - `printerGroupName` (str): Name of a printer group

        Returns:
        """
        return self.api.addPrinterGroup(
            authToken, serverName, printerName, printerGroupName
        )

    def addSharedAccountAccessGroup(
        self, authToken: str, sharedAccountName: str, groupName: str
    ):
        """
        Allow the given group access to the given shared account without using a pin

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to allow access to
            - `groupName` (str): The name of the group to give access to

        Returns:
        """
        return self.api.addSharedAccountAccessGroup(
            authToken, sharedAccountName, groupName
        )

    def addSharedAccountAccessUser(
        self, authToken: str, sharedAccountName: str, userName: str
    ):
        """
        Allow the given user access to the given shared account without using a pin

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to allow access to
            - `userName` (str): The name of the user to give access to

        Returns:
        """
        return self.api.addSharedAccountAccessUser(
            authToken, sharedAccountName, userName
        )

    def addUserToGroup(self, authToken: str, userName: str, groupName: str):
        """
        Adds the user to the specified group

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
            - `groupName` (str): The name of the group

        Returns:
        """
        return self.api.addUserToGroup(authToken, userName, groupName)

    def adjustSharedAccountAccountBalance(
        self, authToken: str, accountName: str, adjustment: float, comment=None
    ):
        """
        Adjust a shared account's account balance by an adjustment amount. An adjustment bay be positive (add to the account) or negative (subtract from the account)

        Parameters:
        - `Required`
            - `accountName` (str): The full name of the shared account to adjust
            - `adjustment` (float): The adjustment amount. Positive to add credit and negative to subtract
        - `Optional`
            - `comment` (str): A user defined comment to associated with the transaction

        Returns:
        """
        return self.api.adjustSharedAccountAccountBalance(
            authToken, accountName, adjustment, comment
        )

    def adjustUserAccountBalance(
        self,
        authToken: str,
        userName: str,
        adjustment: float,
        accountName=None,
        comment=None,
    ):
        """
        Adjust a user's account balance by an adjustment amount. An adjustment may be positive (add to the user's account) or negative (subtract from the account)

        Parameters:
        - `Required`
            - `username` (str): The username account to be adjusted
            - `adjustment` (float): The adjustment amount
                - Positive to add credit and negative to subtract
        - `Optional`
            - `accountName` (str): Name of the user's personal account
                - If unused, the built-in default account is used
            - `comment` (str): A user defined comment to be associated with the transaction

        Returns:
        """
        return self.api.adjustUserAccountBalance(
            authToken, userName, adjustment, comment, accountName
        )

    def adjustUserAccountBalanceByCardNumber(
        self,
        authToken: str,
        cardNumber: int,
        adjustment: float,
        comment=None,
        accountName=None,
    ):
        """
        Adjust a user's account balance. User lookup is by card number. An adjustment may be positive (add to the user's account), or negative (subtract from the account)

        Parameters:
        - `Required`
            - `cardNumber` (int): The card number associated with the user who's account is to be adjusted
            - `adjustment` (float): The adjustment amount. Positive to add credit and negative to subtract
        - `Optional`
            - `comment` (str): A user defined comment to be associated with the transaction
            - `accountName` (str): Optional name of the user's personal account
                - If unused, the built-in default account is used

        Returns:
            - bool
                - `True` = success
                - `False` = no users found for the supplied card number
        """
        return self.api.adjustUserAccountBalanceByCardNumber(
            authToken, cardNumber, adjustment, comment, accountName
        )

    def adjustUserAccountBalanceByGroup(
        self,
        authToken: str,
        group: str,
        adjustment: float,
        accountName=None,
        comment=None,
    ):
        """
        Adjust the account balance of all users in a group by an adjustment amount. \\
        An adjustment may be positive (add to the user's account) or negative (subtract from the account)

        Parameters:
        - `Required`
            - `group` (str): The group for which all users' accounts are to be adjusted
            - `adjustment` (float): The adjustment amount. Positive to add credit and negative to subtract
        - `Optional`
            - `accountName` (str): Name of the user's personal account
                - If unused, the built-in default account is used
            - `comment` (str): A user defined comment to be associated with the transaction

        Returns:
        """
        return self.api.adjustUserAccountBalanceByGroup(
            authToken, accountName, group, adjustment, comment
        )

    def adjustUserAccountBalanceByGroupUpTo(
        self,
        authToken: str,
        accountName: str,
        adjustment: float,
        comment: str,
        group: str,
        limit=1000,
    ):
        """
        Adjust the account balance of all users in a group by an adjustment amount. \\
        An adjustment may be positive (add to the user's account) or negative (subtract from the account). \\
        Balance will not be increased beyond the given limit

        Parameters:
        - `Required`
            - `adjustment` (float): The adjustment amount
                - Positive to add credit and negative to subtract
            - `group` (str): The group for which all users' accounts are to be adjusted
        - `Optional`
            - `accountName` (str): Optional name of the user's personal account
                - If unused, the built-in default account is used
            - `comment` (str): A user defined comment to be associated with the transaction
            - `limit` (int): Only add balance up to this limit
                - default = `1000`

        Returns:
        """
        return self.api.adjustUserAccountBalanceByGroupUpTo(
            authToken, accountName, adjustment, group, comment, limit
        )

    def adjustUserAccountBalanceIfAvailable(
        self, authToken: str, userName: str, adjustment: float, comment=None
    ):
        """
        Adjust a user's account balance by an adjustment amount (if there is credit available). \\
        This can be used to perform atomic account adjustments, without need to check the user's balance first. \\
        An adjustment may be positive (add to the user's account) or negative (subtract from the account).

        Parameters:
        - `Required`
            - `username` (str): The username associated with the user who's account is to be adjusted
            - `adjustment` (float): The adjustment amount. Positive to add credit and negative to subtract
        - `Optional`
            - `comment` (str): A user defined comment to be associated with the transaction

        Returns:
            - If `True`; the adjustment was allowed. Returns false if the user didn't have enough available credit
        """
        return self.api.adjustUserAccountBalanceIfAvailable(
            authToken, userName, adjustment, comment
        )

    def adjustUserAccountBalanceIfAvailableLeaveRemaining(
        self,
        authToken: str,
        userName: str,
        adjustment: float,
        leaveRemaining,
        comment=None,
        accountName=None,
    ):
        """
        Adjust a user's account balance by an adjustment amount (if there is credit available; leave the specified amount still available in the account). \\
        This can be used to perform atomic account adjustments, without need to check the user's balance first. \\
        An adjustment may be positive (add to the user's account) or negative (subtract from the account).

        Parameters:
        - `Required`
            - `username` (str): The username associated with the user who's account is to be adjusted
            - `adjustment` (float): The adjustment amount. Positive to add credit and negative to subtract
            - `leaveRemaining` (str): The remaining available credit will remain in the account
            - `comment` (str): A user defined comment to be associated with the transaction
            - `accountName` (str): Optional name of the user's personal account
                - If unused, the built-in default account is used

        Returns:
            - `True`; the adjustment was allowed
            - `False` Not enough available credit
        """
        return self.api.adjustUserAccountBalanceIfAvailableLeaveRemaining(
            authToken,
            userName,
            adjustment,
            leaveRemaining,
            comment,
            accountName,
        )

    def applyDeviceSettings(self, authToken: str, deviceName: str):
        """
        Initiates an update to the device of any outstanding configuration changes applied via the set-printer-property or set-printer-properties commands

        Parameters:
        - `Required`
            - `deviceName` (str): The name of the device
        """
        return self.api.applyDeviceSettings(authToken, deviceName)

    def batchImportInternalUsers(
        self,
        authToken: str,
        importFile: str,
        overwriteExistingPasswords=False,
        overwriteExistingPINs=False,
        emailUserOnCreation=False,
    ):
        """
        Import the internal users contained in the given tab-delimited import file

        Parameters:
        - `Required`
            - `importFile` (str): The import file location relative to the application server
        - `Optional`
            - `overwriteExistingPasswords` (bool): Overwrite existing user password,
                - default = `False`; only update un-set passwords
            - `overwriteExistingPINs` (bool): Overwrite existing user PINs
                - default = `False`; only update un-set PINs
            - `emailUserOnCreation` (bool): Email users upon their creation
                - default = `False`

        Returns:
        """
        return self.api.batchImportInternalUsers(
            authToken,
            importFile,
            overwriteExistingPasswords,
            overwriteExistingPINs,
            emailUserOnCreation,
        )

    def batchImportPrinters(self, authToken: str, importFile: str):
        """
        Updates printers based on the details contained in the given tab-delimited import file, creating them if required

        Parameters:
        - `Required`
            - `importFile` (str): The import file location relative to the Application Server

        Returns:
        """
        return self.api.batchImportPrinters(authToken, importFile)

    def batchImportSharedAccounts(
        self,
        authToken: str,
        importFile,
        test=False,
        deleteNonExistentAccounts=False,
    ):
        """
        Import the shared accounts contained in the given tab-delimited import file

        Parameters:
        - `Required`
            - `importFile` (str): The import file location relative to the application server
            - `deleteNonExistentAccounts` (bool):
                - If `true`, accounts that do not exist in the import file but exist in the system will be deleted
                - If `false`, they will be ignored
        - `Optional`
            - `test` (bool):
                - If `true`;, perform a test only. The printed statistics will show what would have occurred if testing wasn't enabled. No accounts will be modified

        Returns:
            - Feedback regarding the sync operation
        """
        return self.api.batchImportSharedAccounts(
            authToken, importFile, test, deleteNonExistentAccounts
        )

    def batchImportUserCardIdNumbers(
        self, authToken: str, importFile, overwriteExistingPINs=False
    ):
        """
        Import the user card/ID numbers and PINs contained in the given tab-delimited import file

        Parameters:
        - `Required`
            - `importFile` (str): The import file location relative to the application server
            - `overwriteExistingPINs` (bool): If true, users with a PIN already defined will have it overwritten by the PIN in the import file, if specified. If false, the existing PIN will not be overwritten

        Returns:
        """
        return self.api.batchImportUserCardIdNumbers(
            authToken, importFile, overwriteExistingPINs
        )

    def batchImportUsers(self, authToken: str, importFile: str, createNewUsers: bool):
        """
        Import the user details contained in the given tab-delimited import file

        Parameters:
        - `Required`
            - `importFile` (str): The import file location relative to the application server
            - `createNewUsers` (str): True to create users if they don't exist; false to just update existing details

        Returns:
        """
        return self.api.batchImportUsers(authToken, importFile, createNewUsers)

    def changeInternalAdminPassword(self, authToken: str, newPassword: str):
        """
        Change the internal admin password

        Parameters:
        - `Required`
            - `newPassword` (str): The new password. Cannot be blank

        Returns:
            - True if the password was successfully changed
        """
        return self.api.changeInternalAdminPassword(authToken, newPassword)

    def clearUserAdvancedPrinterSettings(self, authToken: str, userName: str):
        """
        Clear the User's Advanced Printer Settings, settings cleared are:
            - dont-hold-jobs-in-release-station
            - dont-apply-printer-filter-rules
            - printer-cost-adjustment-rate-percent
            - dont-archive
            - auto-release-jobs

        Parameters:
        - `Required`
            - `userName` (str): The name of the user

        Returns:
        """
        return self.api.clearUserAdvancedPrinterSettings(authToken, userName)

    def createUserClientAccountsFile(self, authToken: str):
        """
        Requests that the server create the client accounts to a file. \\
        This file can be distributed to remote sites and then loaded by the client software. \\
        This call is synchronous, the request will wait until the file is written before returning. \\
        The file will be written to `[app-path]/server/data/client/client-accounts.dat`.

        | NOTE: This is only used internally so no need to make public in the public version of ServerCommandProxy

        Returns:
            - bool
                - `True` = file was written successfully
                - `False` = file write attempt failed
        """

        return self.api.createUserClientAccountsFile(authToken)

    def deleteExistingSharedAccount(self, authToken: str, sharedAccountName: str):
        """
        Delete a shared account from the system. Use this method with care. Deleting a shared account will permanently delete it from the shared account list (print history records will remain)

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to delete

        Returns:
        """
        return self.api.deleteExistingSharedAccount(authToken, sharedAccountName)

    def deleteExistingUser(self, authToken: str, userName: str, redactUserData=False):
        """
        Delete/remove an existing user from the user list. Use this method with care. Calling this will permanently delete the user account from the user list (print & transaction history records remain)

        Parameters:
        -  `Required`
            - `username` (str): The username of the user to delete
        - `Optional`
            - `redactUserData` (bool): While deleting, permanently redact user data
                - default = `False`

        Returns:
        """
        return self.api.deleteExistingUser(authToken, userName, redactUserData)

    def deletePrinter(self, authToken: str, serverName: str, printerName: str):
        """
        Delete a printer

        Parameters:
        -  `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The name of the printer to be deleted. To delete all printers on the defined server, set to the special text "[All Printers]"

        Returns:
        """
        return self.api.deletePrinter(authToken, serverName, printerName)

    def disableDeviceSnmpv3(self, authToken: str, deviceName: str):
        """
        Disable use of SNMPv3 on the device

        Parameters:
        -  `Required`
            - `deviceName` (str): The name of the device

        Returns:
        """
        return self.api.disableDeviceSnmpv3(authToken, deviceName)

    def disablePrinter(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        disableMins=int,
    ):
        """
        Disable a printer for select period of time

        Parameters:
        -  `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The printer's name
            - `disableMins` (int): The number of minutes to disable the printer
                - If `-1` the printer will be disabled until re-enabled

        Returns:
        """
        return self.api.disablePrinter(authToken, serverName, printerName, disableMins)

    def disablePrinterSnmpv3(self, authToken: str, serverName: str, printerName: str):
        """
                Disable use of SNMPv3 on the printer
        Parameters:
        -  `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer

        Returns:
        """
        return self.api.disablePrinterSnmpv3(authToken, serverName, printerName)

    def disablePrintingForUser(self, authToken: str, userName: str, disableMins: int):
        """
        Disable printing for a user

        Parameters:
        -  `Required`
            - `userName` (str): The name of the server hosting the printer
            - `disableMins` (int): The number of minutes to disable printing for

        Returns:
        """
        return self.api.disablePrintingForUser(authToken, userName, disableMins)

    def disableSharedAccount(
        self, authToken: str, sharedAccountName: str, disableMins: int
    ):
        """
        Disable shared account

        Parameters:
        -  `Required`
            - `sharedAccountName` (str): The name of the shared account
            - `disableMins` (int): The number of minutes to disable printing for

        Returns:
        """
        return self.api.disableSharedAccount(authToken, sharedAccountName, disableMins)

    def enableDeviceSnmpv3(
        self,
        authToken: str,
        authPass: str,
        authProto: str,
        context: str,
        deviceName: str,
        privPass: str,
        privProto: str,
        userName: str,
    ):
        """
        Set the SNMPv3 device config details

        Parameters:
        - `Required`
            - `authPass` (str): The authentication password
            - `authProto` (str): The authentication protocol
            - `context` (str): The context name
            - `deviceName` (str): The name of the device
            - `privPass` (str): The privacy or encryption password
            - `privProto` (str): The privacy protocol
            - `username` (str): The authentication user

        Returns:
        """
        return self.api.enableDeviceSnmpv3(
            authToken,
            authPass,
            authProto,
            context,
            deviceName,
            privPass,
            privProto,
            userName,
        )

    def enablePrinter(self, authToken: str, serverName: str, printerName: str):
        """
        Enable a printer

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The printer's name

        Returns:
        """
        return self.api.enablePrinter(authToken, serverName, printerName)

    def enablePrinterSnmpv3(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        context: str,
        userName: str,
        authPass: str,
        privPass: str,
        authProto: str,
        privProto: str,
    ):
        """
        Set the SNMPv3 printer config details

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `context` (str): The context name
            - `username` (str): The authentication user
            - `authPass` (str): The authentication password
            - `privPass` (str): The privacy or encryption password
            - `authProto` (str): The authentication protocol
            - `privProto` (str): The privacy protocol

        Returns:
        """
        return self.api.enablePrinterSnmpv3(
            authToken,
            serverName,
            printerName,
            context,
            userName,
            authPass,
            privPass,
            authProto,
            privProto,
        )

    def exportUserDataHistory(self, authToken: str, userName: str, saveLocation: str):
        """
        Export user data based on a set of predefined CSV reports (The owner of these files will be the system account running the PaperCut process)

        Parameters:
            - `username` (str): The user in question
            - `saveLocation` (str): Location to export CSV reports to. The system account running the PaperCut process must have write permissions to this location

        Returns:
        """
        return self.api.exportUserDataHistory(authToken, userName, saveLocation)

    def generateAdHocReport(
        self,
        authToken: str,
        reportType: str,
        dataParams: str,
        exportTypeExt: str,
        reportTitle: str,
        saveLocation: str,
    ):
        """
        Generates an AdHoc report

        Parameters:
        - `Required`
            - `reportType` (str): The type of report
            - `dataParams` (str): The data parameters for the report
            - `exportTypeExt` (str): The export format
            - `reportTitle` (str): The prefix of the report title
            - `saveLocation` (str): A file path of where to save the report on the server

        Returns:
           - If `True`; the operation succeeded
                - default = `False`
        """
        return self.api.generateAdHocReport(
            authToken,
            reportType,
            dataParams,
            exportTypeExt,
            reportTitle,
            saveLocation,
        )

    def generateScheduledReport(self, authToken: str, reportTitle, saveLocation: str):
        """
        Generate a specified scheduled report

        Parameters:
        - `Required`
            - `reportTitle` (str): the title of the report
            - `saveLocation` (str): the location on the server to save the report to
        """
        return self.api.generateScheduledReport(authToken, reportTitle, saveLocation)

    def getConfigValue(self, authToken: str, configName):
        """
        Get the config value from the server

        Parameters:
        - `Required`
            - `configName` (str): The name of the config value to retrieve

        Returns:
            - The config value. If the config value does not exist a blank string is returned
        """
        return self.api.getConfigValue(authToken, configName)

    def getDeviceSnmpv3(self, authToken: str, deviceName: str):
        """
        Get the SNMPv3 device config details

        Parameters:
        - `Required`
            - `deviceName` (str): The name of the device

        Returns:
            - The associated SNMPv3 printer details if there are any
        """
        return self.api.getDeviceSnmpv3(authToken, deviceName)

    def getGroupMembers(self, authToken: str, groupName: str, offset=0, limit=1000):
        """
        Retrieves a list of all users in the group

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group whose members are to be retrieved
            - `offset` (int): Where the index of the data starts
                - default is `0`
            - `limit` (int): How many items to return
                - default is `1000`

        Returns:
           - a list of user names
        """
        return self.api.getGroupMembers(authToken, groupName, offset, limit)

    def getGroupQuota(self, authToken: str, groupName: str):
        """
        Get the group quota allocation settings on a given group

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group

        Returns:
            - A Hashtable (XML-RPC Struct) containing the information in keys: QuotaAmount, QuotaPeriod, QuotaMaxAccumulation
        """
        return self.api.getGroupQuota(authToken, groupName)

    def getPrinterCostSimple(self, authToken: str, serverName: str, printerName: str):
        """
        Get the page cost if, and only if, the printer is using the Simple Charging Model

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer

        Returns:
            - The default page cost. On failure an exception is thrown
        """
        return self.api.getPrinterCostSimple(authToken, serverName, printerName)

    def getPrinterProperties(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        propertyNames=dict[str, any] | list[str],
    ):
        """
        Get multiple printer properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `Auth` (str): The authentication token
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `propertyNames` (str): The names of the properties to get

        Returns:
            - The property values (in the same order as given in propertyNames
        See Also:
            - `getPrinterProperty()`:
        """
        return self.api.getPrinterProperties(
            authToken, serverName, printerName, propertyNames
        )

    def getPrinterProperty(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        propertyName: str,
    ):
        """
        Gets a printer property

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `propertyName` (str): The name of the property
                - Valid options include:
                    - `cost-model`
                    - `custom-field-1`
                    - `custom-field-2`
                    - `custom-field-3`
                    - `custom-field-4`
                    - `custom-field-5`
                    - `custom-field-6`
                    - `disabled`
                    - `print-stats.job-count`
                    - `print-stats.page-count`
                    - `printer-id`

        Returns:
           - The value of the requested property
        """
        return self.api.getPrinterProperty(
            authToken, serverName, printerName, propertyName
        )

    def getPrinterSnmpv3(self, authToken: str, serverName: str, printerName: str):
        """
        Get the SNMPv3 printer config details

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer

        Returns:
            - The associated SNMPv3 printer details if there are any
        getDeviceSnmpv3
        """
        return self.api.getPrinterSnmpv3(authToken, serverName, printerName)

    def getSharedAccountAccountBalance(self, authToken: str, accountName: str):
        """
        The current account balance associated with a shared account

        Parameters:
        - `Required`
            - `accountName` (str): The account's full name

        Returns:
            - The shared account's account balance as float
        """
        return self.api.getSharedAccountAccountBalance(authToken, accountName)

    def getSharedAccountOverdraftMode(self, authToken: str, accountName: str):
        """
        Get the shared account's overdraft mode

        Parameters:
        - `Required`
            - `accountName` (str): The name of the shared account

        Returns:
            - the shared account's overdraft mode
                - 'individual' \\
                or
                - 'default'
        """
        return self.api.getSharedAccountOverdraftMode(authToken, accountName)

    def getSharedAccountProperties(
        self, authToken: str, sharedAccountName: str, propertyNames: str
    ):
        """
        Get multiple shared account properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The shared account name
            - `propertyNames` (str): The names of the properties to get. See #getSharedAccountProperty for valid property names

        Returns:
            - The property values (the returned response honors the original request's order as given in propertyNames)

        See Also:
            - getSharedAccountProperty()
            - setSharedAccountProperties
        """
        return self.api.getSharedAccountProperties(
            authToken, sharedAccountName, propertyNames
        )

    def getSharedAccountProperty(
        self, authToken: str, sharedAccountName: str, propertyName: str
    ):
        """
        Gets a shared account property

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account
            - `propertyName` (str): The name of the property to get
                - Valid options include:
                    - `access-groups`
                    - `access-users`
                    - `account-id`
                    - `balance`
                    - `comment-option`
                    - `disabled`
                    - `invoice-option`
                    - `notes`
                    - `overdraft-amount`
                    - `pin`
                    - `restricted.`

        Returns:
            - The value of the requested property
        See Also:
            - `setSharedAccountProperty()`:
        """
        return self.api.getSharedAccountProperty(
            authToken, sharedAccountName, propertyName
        )

    def getTaskStatus(self, authToken: str):
        """
        Return the status (completed flag and any status message text) associated with a long running task such as a sync operation started by the `performGroupSync` method

        Returns:
            - A TaskStatus object providing information about the current or latest task started via this method
        """
        return self.api.getTaskStatus(authToken)

    def getTotalUsers(self, authToken: str) -> int:
        """
        Get the count of all users in the system

        Parameters:

        Returns:
            - Sum of all user accounts
        """
        return self.api.getTotalUsers(authToken)

    def getUserAccountBalance(self, authToken: str, userName: str, accountName=None):
        """
        The a user's current account balance

        Parameters:
        - `Required`
            - `username` (str): The user's username
            - `accountName` (str): Optional name of the user's personal account. If blank, the total user balance is returned

        Returns:
            - The user's current account balance as float
        """
        return self.api.getUserAccountBalance(authToken, userName, accountName)

    def getUserGroups(self, authToken: str, userName: str):
        """
        Retrieves a list of a user's group memberships

        Parameters:
        - `Required`
            - `userName` (str): The name of the user whose group memberships are to be retrieved

        Returns:
            - a list of group names
        """

        return self.api.getUserGroups(authToken, userName)

    def getUserOverdraftMode(self, authToken: str, userName: str):
        """
        Get the user's overdraft mode

        Parameters:
        - `Required`
            - `username` (str): the username

        Returns:
           - the user's overdraft mode \\
                - 'individual' \\
                or \\
                - 'default'):
        """
        return self.api.getUserOverdraftMode(authToken, userName)

    def getUserProperties(self, authToken: str, userName: str, propertyNames: str):
        """
        Get multiple user properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
            - `propertyNames` (str): The names of the properties to get. See #getUserProperty for valid property names

        Returns:
            - The property values (in the same order as given in propertyNames
        See Also:
            - `getUserProperty()`, setUserProperties():
        """
        return self.api.getUserProperties(authToken, userName, propertyNames)

    def getUserProperty(self, authToken: str, userName: str, propertyName: str):
        """Gets a user property

            Parameters:
        - `Required`
            - `userName` - The name of the user
        - `Optional`
            - `account-selection.can-charge-personal` (bool): If `True`; The user's account selection settings allow them to charge jobs to their personal account
                - default = `False`
            - `account-selection.can-charge-shared-by-pin` (bool): If `True`; The user's account selection settings allow them to charge a shared account by PIN or code
                - default = `False`
            - `account-selection.can-charge-shared-from-list` (bool): If `True`; The user's account selection settings allow them to select a shared account to charge from a list of shared accounts
                - default = `False`
            - `account-selection.mode` (str): The user's account selection mode
                - One of the following:
                    - `AUTO_CHARGE_TO_PERSONAL_ACCOUNT`
                    - `AUTO_CHARGE_TO_SHARED`
                    - `CHARGE_TO_PERSONAL_ACCOUNT_WITH_CONFIRMATION`
                    - `SHOW_ACCOUNT_SELECTION_POPUP`
                    - `SHOW_ADVANCED_ACCOUNT_SELECTION_POPUP`
                    - `SHOW_MANAGER_MODE_POPUP`
            - `auto-release-jobs` (bool): If `True`; The user's jobs will always release on device login
                - default = `False`
            - `auto-shared-account` (str): The shared account to auto charge to
                - Will be blank if the user's account selection mode is not `AUTO_CHARGE_TO_SHARED`
            - `balance` (float): The user's balance, unformatted, e.g. "1234.56"
            - `department` (str)
            - `disabled-print` (bool): If `True`; The user's printing is disabled
                - default = `False`
            - `dont-apply-printer-filter-rules` (bool): If `True`; The user's jobs will bypass printer filter settings
                - default = `False`
            - `dont-archive` (bool): If `True`; The user's jobs will not be archived
                - default = `False`
            - `dont-hold-jobs-in-release-station` (bool): If `True`; The user's jobs will bypass all release station queues
                - default = `False`
            - `email` (str)
            - `full-name` (str)
            - `home` (str): The user's home folder (a double-quoted UNC path)
            - `internal` (bool): `True` if this is an internal user
            - `net-stats.data-mb` (str) : total 'net MB used by this user, unformatted, e.g. "1234.56"
            - `net-stats.time-hours` (str) : total 'net hours used by this user, unformatted, e.g. "1234.56"
            - `notes` (str)
            - `office` (str)
            - `other-emails` (str) : user's other emails
            - `overdraft-amount` (float): The user's individual overdraft amount, unformatted, e.g. "1234.56". Note this amount is in use only when the user account is restricted and overdraft mode is set to `individual`
            - `primary-card-number` (int)
            - `print-stats.job-count` (int): total number of print jobs from this user, unformatted, e.g. "1234"
            - `print-stats.page-count` (int): total number of pages printed by this user, unformatted, e.g. "1234"
            - `printer-cost-adjustment-rate-percent` (float) : The percentage modifier for the user's job costs, unformatted, e.g. "123.45". If the flag to enable adjustment is not set, returns -1. \\
            - `propertyName` (str): The name of the property to get. The following list of property names can also be set using `setUserProperty()`:
                    - `restricted` (bool): `True` if this user's printing is restricted, false if they are unrestricted
                    - `secondary-card-number` (str)
            - `unauthenticated` (bool): If `True`; The user is an unauthenticated user
                - default = `False`
            - `username-alias` (str) : The alias for a given user

            Returns:
              - The value of the requested property

            See also:
              - `setUserProperty()`
            """
        return self.api.getUserProperty(authToken, userName, propertyName)

    def installLicense(self, authToken: str, licenseFile):
        """
        Install a new license

        Parameters:
        - `Required`
            - `licenseFile` (str): The location of the new license file to install On failure an exception is thrown
        """

        return self.installLicense(authToken, licenseFile)

    def isGroupExists(self, authToken: str, groupName: str):
        """
        Checks if group exists or not

        Parameters:
        - `Required`
            - `groupName` (str): The group name to check

        Returns:
            - If `True`; the group exists
                - default = `False`, false if it doesn't
        """
        return self.api.isGroupExists(authToken, groupName)

    def isSharedAccountExists(self, authToken: str, accountName: str):
        """
        Test to see if a shared account exists

        Parameters:
        - `Required`
            - `accountName` (str): The name of the shared account

        Returns:
            - bool
                - `True` the shared account exists
                - `False` the shared account does not exist
        """
        return self.api.isSharedAccountExists(authToken, accountName)

    def isUserExists(self, authToken: str, userName: str):
        """
        Test to see if a user associated with "username" exists in the system

        Parameters:
        - `Required`
            - `username` (str): The username to test

        Returns:
            - If `True`; the user exists in the system
                - default = `False`, else returns false
        """
        return self.api.isUserExists(authToken, userName)

    def listPrinters(self, authToken: str, offset=0, limit=1000):
        """
        List all printers sorted by printer name. This can be used to enumerate all printers in 'pages'. When retrieving a list of all printers, the recommended page size / limit is 1000. Batching in groups of 1000 ensures efficient transfer and processing. E.g.: listPrinters(0, 1000) - returns printers 0 through 999 listPrinters(1000, 1000) - returns printers 1000 through 1999 listPrinters(2000, 1000) - returns printers 2000 through 2999

        Parameters:
        - `Required`
            - `offset` (int): The 0-index offset in the list of printers to return. I.e. 0 is the first printer, 1 is the second, etc
            - `limit` (int): The number of printers to return in this batch. Recommended: 1000

        Returns:
            - A list of printer names
        """
        return self.api.listPrinters(authToken, offset, limit)

    def listSharedAccounts(self, authToken: str, offset=0, limit=1000):
        """
        List all shared accounts (sorted by account name) starting at offset and ending at limit. This can be used to enumerate all shared accounts in 'pages'. When retrieving a list of all shared accounts, the recommended page size / limit is 1000. Batching in groups of 1000 ensures efficient transfer and processing. E.g.: listSharedAccounts(0, 1000) - returns accounts 0 through 999 listSharedAccounts(1000, 1000) - returns accounts 1000 through 1999 listSharedAccounts(2000, 1000) - returns accounts 2000 through 2999

        Parameters:
        - `Required`
            - `offset` (int): The 0-index offset in the list of accounts to return. I.e. 0 is the first account, 1 is the second, etc
            - `limit` (int): The number of account to return in this batch. Recommended: 1000

        Returns:
            - A list of shared account names
        """
        return self.api.listSharedAccounts(authToken, offset, limit)

    def listUserAccounts(self, authToken: str, offset=0, limit=1000):
        """
        List all user accounts (sorted by username) starting at offset and ending at limit. This can be used to enumerate all user accounts in 'pages'. When retrieving a list of all user accounts, the recommended page size / limit is 1000. Batching in groups of 1000 ensures efficient transfer and processing. E.g.: listUserAccounts(0, 1000) - returns users 0 through 999 listUserAccounts(1000, 1000) - returns users 1000 through 1999 listUserAccounts(2000, 1000) - returns users 2000 through 2999

        Parameters:
        - `Required`
            - `offset` (int): The 0-index offset in the list of users to return. I.e. 0 is the first user, 1 is the second, etc
            - `limit` (int): The number of users to return in this batch. Recommended: 1000

        Returns:
           - A list of user names
        """
        return self.api.listUserAccounts(authToken, offset, limit)

    def listUserGroups(self, authToken: str, offset=0, limit=1000):
        """
        List user groups. This can be used to enumerate all user groups in 'pages'. When retrieving a list of all user groups, the recommended page size / limit is 1000. Batching in groups of 1000 ensures efficient transfer and processing. E.g.: listUserGroups(0, 1000) - returns groups 0 through 999 listUserGroups(1000, 1000) - returns groups 1000 through 1999 listUserGroups(2000, 1000) - returns groups 2000 through 2999

        Parameters:
        - `Required`
            - `offset` (int): The 0-index offset in the list of groups to return. I.e. 0 is the first group, 1 is the second, etc
            - `limit` (int): The number of groups to return in this batch. Recommended: 1000

        Returns:
            - A list of group names
        """
        return self.api.listUserGroups(authToken, offset, limit)

    def listUserSharedAccounts(
        self,
        authToken: str,
        userName: str,
        offset=0,
        limit=1000,
        ignoreAccountMode=False,
    ):
        """
        List all shared accounts (sorted by account name) that the user has access to, starting at offset and listing only limit accounts. This can be used to enumerate all shared accounts in 'pages'. When retrieving a list of all shared accounts, the recommended page size / limit is 1000. Batching in groups of 1000 ensures efficient transfer and processing. E.g.: listUserSharedAccounts("user", 0, 1000) - returns accounts 0 through 999 listUserSharedAccounts("user", 1000, 1000) - returns accounts 1000 through 1999 listUserSharedAccounts("user", 2000, 1000) - returns accounts 2000 through 2999

        Parameters:
        - `Required`
            - `userName` (str): The username of the user to get the accounts for
            - `offset` (int): The 0-index offset in the list of accounts to return. I.e. 0 is the first account, 1 is the second, etc
            - `limit` (int): The number of account to return in this batch. Recommended: 1000
            - `ignoreAccountMode` (bool): If true, list accounts regardless of current shared account mode

        Returns:
            - A list of shared account names the user has access to
        """
        return self.api.listUserSharedAccounts(
            authToken, userName, offset, limit, ignoreAccountMode
        )

    def lookUpUserNameByCardNo(self, authToken: str, cardNo: str):
        """
        Looks up the user with the given user card number and returns their user name. If no match was found an empty string is returned

        Parameters:
        - `Required`
            - `cardNo` (str): The user card number to look up

        Returns:
            - The matching user name, or an empty string if there was no match
        """
        return self.api.lookUpUserNameByCardNo(authToken, cardNo)

    def lookUpUserNameByEmail(self, authToken: str, email: str):
        """
        Looks up the user with the given email and returns their user name. If no match was found an empty string is returned

        Parameters:
        - `Required`
            - `email` (str): The user email address to look up

        Returns:
            - The matching user name, or an empty string if there was no match
        """
        return self.api.lookUpUserNameByEmail(authToken, email)

    def lookUpUserNameByIDNo(self, authToken: str, idNo: int):
        """
        Looks up the user with the given user id number and returns their user name. If no match was found an empty string is returned

        Parameters:
        - `Required`
            - `idNo` (str): The user id number to look up

        Returns:
            - The matching user name, or an empty string if there was no match
        """
        return self.api.lookUpUserNameByIDNo(authToken, idNo)

    def lookUpUserNameBySecondaryUserName(self, authToken: str, secondaryUserName: str):
        """
        Looks up the user with the specified secondary user name and returns their primary user name. If no match was found an empty string is returned

        Parameters:
        - `Required`
            - `secondaryUserName` (str): The user's secondary user name to look up

        Returns:
            - The matching user name, or an empty string if there was no match
        """
        return self.api.lookUpUserNameBySecondaryUserName(authToken, secondaryUserName)

    def lookUpUsersByFullName(self, authToken: str, fullName: str):
        """
        Looks up the users with the given full name and returns their user names. If no match was found an empty list is returned

        Parameters:
        - `Required`
            - `fullName` (str): The full name to look up

        Returns:
            - A list of the matching user names, or an empty list if there was no match
        """
        return self.api.lookUpUsersByFullName(authToken, fullName)

    def performGroupSync(self, authToken: str):
        """
        Start the process of synchronizing the system's group membership with the OS/Network/Domain's group membership. \\
        The call to this method will start the synchronization process. \\
        The operation will commence and complete in the background

        Parameters:

        Returns:
        """

        return self.api.performGroupSync(authToken)

    def performOnlineBackup(self, authToken: str):
        """
        Instigate an online backup. This process is equivalent to pressing the manual backup button in the web based admin interface. \\
        The data is expected into the server/data/backups directory as a timestamped, zipped XML file \\

        Parameters:

        Returns:
        """
        return self.api.performOnlineBackup(authToken)

    def performUserAndGroupSync(self, authToken: str):
        """
        Start a full user and group synchronization. This is equivalent to pressing on the "Synchronize Now" button in the admin user interface. \\
        The behaviour of the sync process, such as deleting old users, is determined by the current system settings as defined in the admin interface. \\
            A call to this method will commence the sync process and the operation will complete in the background

        Parameters:


        """
        return self.api.performUserAndGroupSync(authToken)

    def performUserAndGroupSyncAdvanced(
        self,
        authToken: str,
        deleteNonExistentUsers=False,
        updateUserDetails=False,
    ):
        """
        An advanced version of the user and group synchronization process providing control over the sync behaviour. \\
        A call to this method will commence the sync process and the operation will complete in the background

        Parameters:
        - `Required`
            - `deleteNonExistentUsers` (bool): If set to True, old users will be deleted
            - `updateUserDetails` (bool): If set to True, user details such as full-name, email, etc. will be synced with the underlying OS/Network/Domain user directory
        """
        return self.api.performUserAndGroupSyncAdvanced(
            authToken, deleteNonExistentUsers, updateUserDetails
        )

    def processJob(self, authToken: str, jobDetails: list[str]):
        """
        Takes the details of a job and logs and charges as if it were a "real" job. \\
        Jobs processed via this method are not susceptible to filters, pop-ups, hold/release queues etc., they are only logged. \\
        See the user manual section [Importing Job Details](https://www.papercut.com/help/manuals/ng-mf/common/tools-importing-jobs/) for more information and the format of `jobDetails`

        Parameters:
        - `Required`
            - `jobDetails` (str): The job details (a comma separated list of name-value pairs with an equals sign as the name-value delimiter)
        """
        return self.api.processJob(authToken, jobDetails)

    def reapplyInitialUserSettings(self, authToken: str, userName: str):
        """
        Re-applies initial user settings on the given user. These initial settings are based on group membership

        Parameters:
        - `Required`
            - `username` (str): the username
        """
        return self.api.reapplyInitialUserSettings(authToken, userName)

    def removeAdminAccessGroup(self, authToken: str, groupName: str):
        """
        Removes a group from the list of admin groups

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group
        """
        return self.api.removeAdminAccessGroup(authToken, groupName)

    def removeAdminAccessUser(self, authToken: str, userName: str):
        """
        Removes an admin user from the list of admins

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
        """
        return self.api.removeAdminAccessUser(authToken, userName)

    def removeGroup(self, authToken: str, groupName: str):
        """
        Removes an already existing group

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group that needs to be removed. The group should already exist in PaperCut
        """
        return self.api.removeGroup(authToken, groupName)

    def removePrinterAccessGroup(
        self, authToken: str, serverName: str, printerName: str, groupName: str
    ):
        """
        Removes the group from the printer access group list

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server name
            - `printerName` (str): The name of the printer
            - `groupName` (str): group name that needs to be removed from the list of groups allowed to print to this printer
        """
        return self.api.removePrinterAccessGroup(
            authToken, serverName, printerName, groupName
        )

    def removeSharedAccountAccessGroup(
        self, authToken: str, sharedAccountName: str, groupName: str
    ):
        """
        Revoke the given group's access to the given shared account

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to revoke access to
            - `groupName` (str): The name of the group to revoke access for
        """
        return self.api.removeSharedAccountAccessGroup(
            authToken, sharedAccountName, groupName
        )

    def removeSharedAccountAccessUser(
        self, authToken: str, sharedAccountName: str, userName: str
    ):
        """
        Revoke the given user's access to the given shared account

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account to revoke access to
            - `userName` (str): The name of the user to revoke access for
        """
        return self.api.removeSharedAccountAccessUser(
            authToken, sharedAccountName, userName
        )

    def removeUserFromGroup(self, authToken: str, userName: str, groupName: str):
        """
        Removes the user from the specified group

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
            - `groupName` (str): The name of the group
        """
        return self.api.removeUserFromGroup(authToken, userName, groupName)

    def renamePrinter(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        newServerName: str,
        newPrinterName: str,
    ):
        """
        Rename a printer. This can be useful after migrating a print queue or print server (i.e. the printer retains its history and settings under the new name). Note that in some cases case sensitivity is important, so care should be taken to enter the name exactly as it appears in the OS

        Parameters:
        - `Required`
            - `serverName` (str): The existing printer's server name
            - `printerName` (str): The existing printer's queue name
            - `newServerName` (str): The new printer's server name
            - `newPrinterName` (str): The new printer's queue name
        """
        return self.api.renamePrinter(
            authToken, serverName, printerName, newServerName, newPrinterName
        )

    def renameSharedAccount(
        self,
        authToken: str,
        currentSharedAccountName: str,
        newSharedAccountName: str,
    ):
        """
        Rename an existing shared account

        Parameters:
        - `Required`
            - `currentSharedAccountName` (str): The name of the shared account to rename. Use a '\\\\' to denote a subaccount, e.g.: 'parent\\sub'
            - `newSharedAccountName` (str) - The new shared account name
        """
        return self.api.renameSharedAccount(
            authToken, currentSharedAccountName, newSharedAccountName
        )

    def renameUserAccount(self, authToken: str, currentUserName: str, newUserName: str):
        """
        Rename a user account. Useful when the user has been renamed in the domain / directory, so that usage history can be maintained for the new username. \\
        This should be performed in conjunction with a rename of the user in the domain / user directory, as all future usage and authentication will need to use the new username

        Parameters:
        - `Required`
            - `currentUserName` (str): The username of the user to rename
            - `newUserName` (str): The user's new username
        """
        return self.api.renameUserAccount(authToken, currentUserName, newUserName)

    def resetPrinterCounts(
        self, authToken: str, serverName: str, printerName: str, resetBy: str
    ):
        """
        Reset the counts (pages and job counts) associated with a printer

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The printer's name
            - `resetBy` (str): The name of the user/script/process resetting the counts
        """
        return self.api.resetPrinterCounts(authToken, serverName, printerName, resetBy)

    def resetUserCounts(self, authToken: str, userName: str, resetBy: str):
        """
        Reset the counts (pages and job counts) associated with a user account

        Parameters:
        - `Required`
            - `username` (str): The username associated with the user who's counts are to be reset
            - `resetBy` (str): The name of the user/script/process reseting the counts
        """
        return self.api.resetUserCounts(authToken, userName, resetBy)

    def runCommand(self, authToken: str, commandName: str, args: list[str]):
        """
        Runs a custom command on the server

        Parameters:
        - `Required`
            - `commandName` (str): The command name to execute
            - `args` (list[str]): The arguments to the command

        Returns:
            - The status message returned by the command
        """
        return self.api.runCommand(authToken, commandName, args)

    def saveThreadSnapshot(self, authToken: str):
        """
        Saves the server thread snapshot to the debug log

        Parameters:

        Returns:
            - If `True`; call was successful
                - default = `False`
        """
        return self.api.saveThreadSnapshot(authToken)

    def setConfigValue(self, authToken: str, configName, configValue: str):
        """
        Set the config value from the server. \\
        Take caution when updating config values. \\
        You may cause serious problems which can only be fixed by reinstallation of the application. Use the `setConfigValue` method at your own risk

        Parameters:
        - `Required`
            - `configName` (str): The name of the config value to retrieve
            - `configValue` (str): The value to set
            """
        return self.api.setConfigValue(authToken, configName, configValue)

    def setGroupQuota(
        self,
        authToken: str,
        groupName: str,
        quotaAmount: float,
        quotaMaxAccumulation: float,
        period="NONE",
    ):
        """
        Set the group quota allocation settings on a given group

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group
            - `quotaAmount` (float): The quota amount to set
            - `period` (str): The schedule period (one of either NONE, DAILY, WEEKLY or MONTHLY);
            - `quotaMaxAccumulation` (float): The maximum quota accumulation. Set to 0.0 to have no limit
        """
        return self.api.setGroupQuota(
            authToken, groupName, quotaAmount, period, quotaMaxAccumulation
        )

    def setPrinterCostSimple(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        costPerPage: float,
    ):
        """
        Method to set a simple single page cost using the Simple Charging Model

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `costPerPage` (str): The cost per page (simple charging model):
        """
        return self.api.setPrinterCostSimple(
            authToken, serverName, printerName, costPerPage
        )

    def setPrinterGroups(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        printerGroupNames: list[str],
    ):
        """
        Set the printer groups a printer belongs to, overwriting any existing group

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server hosting the printer
            - `printerName` (str): The printer's name
            - `printerGroupNames` (list): A comma separated list of printer group names. To clear all group association set to ""
        """
        return self.api.setPrinterGroups(
            authToken, serverName, printerName, printerGroupNames
        )

    def setPrinterProperties(
        self,
        authToken: str,
        serverName: str,
        printerName: str,
        propertyNamesAndValues: list[dict[str, str]],
    ):
        """
        Set multiple printer properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `propertyNamesAndValues` (list[dict[str, str]]): The list of property names and values to set. E.g. [["balance", "1.20"], ["office", "East Wing"]]

        Returns:
            - boolean
            - exception \\

        See Also:
            - `setPrinterProperty()`
        """
        return self.api.setPrinterProperties(
            authToken, serverName, printerName, propertyNamesAndValues
        )

    def setPrinterProperty(
        self,
        authToken: str,
        printerName: str,
        propertyName: str,
        serverName: str,
        propertyValue="SIMPLE",
    ):
        """
        Sets a printer property

        Parameters:
        - `Required`
            - `serverName` (str): The name of the server
            - `printerName` (str): The name of the printer
            - `propertyName` (str): The name of the property
                -  Valid options include:
                        - `cost-model`
                        - `custom-field-1`
                        - `custom-field-2`
                        - `custom-field-3`
                        - `custom-field-4`
                        - `custom-field-5`
                        - `custom-field-6`
                        - `disabled`
            - `propertyValue` (str): The value of the property to set
                - Valid property values for `cost-model` are:
                        - `SIMPLE`
                        - `AREA`
                        - `SIZE_TABLE`
                        - `SIZE_CATEGORY`
                        - `SIZE_DETAILED`
                        - `SIZE_LENGTH.`
        """
        return self.api.setPrinterProperty(
            authToken, propertyName, propertyValue, serverName, printerName
        )

    def setSharedAccountAccountBalance(
        self, authToken: str, accountName: str, balance: float, comment=None
    ):
        """
        Set the balance on a shared account to a set value. This is conducted as a transaction

        Parameters:
        - `Required`
            - `accountName` (str): The full account name of the account to be set
            - `balance` (float): The balance to set the account to
        - `Optional`
            - `comment` (str): A user defined comment to associate with the transaction. This may be a `null` string
        """
        return self.api.setSharedAccountAccountBalance(
            authToken, accountName, balance, comment
        )

    def setSharedAccountOverdraftMode(
        self, authToken: str, accountName: str, mode: str
    ):
        """
        Set the shared account's overdraft mode

        Parameters:
        - `Required`
            - `accountName` (str): The name of the shared account
            - `mode` (str): the overdraft mode to use
                - Valid values are:
                        - `individual`
                        - `default`
        """
        return self.api.setSharedAccountOverdraftMode(authToken, accountName, mode)

    def setSharedAccountProperties(
        self,
        authToken: str,
        sharedAccountName: str,
        propertyNamesAndValues: list,
    ):
        """
        Set multiple shared account properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The shared account name
            - `propertyNamesAndValues` (list): The list of property names and values to set. E.g. [["balance", "1.20"], ["invoice-option", "ALWAYS_INVOICE"]]. See #setSharedAccountProperty for valid property names
        See Also:
            - `getSharedAccountProperties`, `setSharedAccountProperty`
        """
        return self.api.setSharedAccountProperties(
            authToken, sharedAccountName, propertyNamesAndValues
        )

    def setSharedAccountProperty(
        self,
        authToken: str,
        sharedAccountName: str,
        propertyName: str,
        propertyValue: any,
    ):
        """
        Sets a shared account property

        Parameters:
        - `Required`
            - `sharedAccountName` (str): The name of the shared account
            - `propertyName` (str): The name of the property to set. See #getSharedAccountProperty for valid property names
            - `propertyValue` (any): The value of the property to set
        See Also:
            - `getSharedAccountProperty`
        """
        return self.api.setSharedAccountProperty(
            authToken, sharedAccountName, propertyName, propertyValue
        )

    def setUserAccountBalance(
        self,
        authToken: str,
        userName: str,
        balance: float,
        comment=None,
        accountName=None,
    ):
        """
        Set the balance on a user's account to a set value. This is conducted as a transaction

        Parameters:
        - `Required`
            - `username` (str): The username associated with the user who's account is to be set
            - `balance` (float): The balance to set the account to
        - `Optional`
            - `comment` (str): A user defined comment to associate with the transaction
            - `accountName` (str): Optional name of the user's personal account
                - If unused, the built-in default account is used
        """
        return self.api.setUserAccountBalance(
            authToken, userName, balance, comment, accountName
        )

    def setUserAccountBalanceByGroup(
        self,
        authToken: str,
        group: str,
        balance: float,
        comment=None,
        accountName=None,
    ):
        """
        Set the balance for each member of a group to the given value

        Parameters:
        - `Required`
            - `group` (str): The group for which all users' balance is to be set
            - `balance` (float): The value to set all users' balance to
        - `Optional`
            - `comment` (str): A user defined comment to associate with the transaction
            - `accountName` (str): Optional name of the user's personal account
                - If unused, the built-in default account is used
        """
        return self.api.setUserAccountBalanceByGroup(
            authToken, group, balance, comment, accountName
        )

    def setUserAccountSelectionAdvancedPopup(
        self,
        authToken: str,
        userName: str,
        allowPersonal=False,
        chargeToPersonalWhenSharedSelected=False,
        defaultSharedAccount=None,
    ):
        """
        Change a user's account selection setting to use the advanced account selection pop-up

        Parameters:
        - `Required`
            - `username` (str): The user's username
            - `allowPersonal` (bool): allow user to charge to personal account
            - `chargeToPersonalWhenSharedSelected` (bool): If true, charge to personal and allocate to shared account
        - `Optional`
            - `defaultSharedAccount` (str): The default shared account
        """
        return self.api.setUserAccountSelectionAdvancedPopup(
            authToken,
            userName,
            allowPersonal,
            chargeToPersonalWhenSharedSelected,
            defaultSharedAccount,
        )

    def setUserAccountSelectionAutoChargePersonal(
        self, authToken: str, userName: str, withPopupConfirmation: bool
    ):
        """
        Sets the user to auto charge to it's personal account

        Parameters:
        - `Required`
            - `username` (str): The user's username
        - `Optional`
            - `withPopupConfirmation` (bool): If a popup confirmation is to be used
                - Defaults to false

        Returns:

        """
        return self.api.setUserAccountSelectionAutoChargePersonal(
            authToken, userName, withPopupConfirmation
        )

    def setUserAccountSelectionAutoSelectSharedAccount(
        self, authToken: str, userName: str, accountName: str, chargeToPersonal
    ):
        """
        Change a user's account selection setting to automatically charge to a single shared account

        Parameters:
        - `Required`
            - `username` (str): The user's username
            - `accountName` (str): The shared account name
            - `chargeToPersonal` (bool): If true; charge to personal account and allocate to shared account

        Returns:

        """
        return self.api.setUserAccountSelectionAutoSelectSharedAccount(
            authToken, userName, accountName, chargeToPersonal
        )

    def setUserAccountSelectionStandardPopup(
        self,
        authToken: str,
        userName: str,
        allowPersonal: bool,
        allowListSelection: bool,
        allowPinCode: bool,
        allowPrintingAsOtherUser: bool,
        chargeToPersonalWhenSharedSelected: bool,
        defaultSharedAccount=None,
    ):
        """
        Change a user's account selection setting to use the standard account selection pop-up

        Parameters:
        - `Required`
            - `username` (str): The user's username
            - `allowPersonal=False` (bool): allow user to charge to personal account
            - `allowListSelection` (bool): allow user to select an account from the list of shared account
            - `allowPinCode` (bool): allow user to select a shared account using pin ode
            - `allowPrintingAsOtherUser` (bool): allow user to charge to other users
            - `chargeToPersonalWhenSharedSelected` (bool): `True` if charge to personal and allocate to shared account
            - `defaultSharedAccount` (str): The default shared account

        Returns:

        """
        return self.api.setUserAccountSelectionStandardPopup(
            authToken,
            userName,
            allowPersonal,
            allowListSelection,
            allowPinCode,
            allowPrintingAsOtherUser,
            chargeToPersonalWhenSharedSelected,
            defaultSharedAccount,
        )

    def setUserOverdraftMode(self, authToken: str, userName: str, mode: str):
        """
        Set the user's overdraft mode

        Parameters:
        - `Required`
            - `username` (str): the username
            - `mode` (str): the overdraft mode to use \\
                - `individual` \\
                or \\
                - `default`

        Returns:
        """
        return self.api.setUserOverdraftMode(authToken, userName, mode)

    def setUserProperty(
        self,
        authToken: str,
        userName: str,
        propertyName: str,
        propertyValue: str,
    ):
        """
        Sets a user property

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
            - `propertyName` (str): The name of the property to set
                - Valid options include:
                    - `balance`
                    - `primary-card-number`
                    - `secondary-card-number`
                    - `card-pin`
                    - `department`
                    - `disabled-print`
                    - `email`
                    - `full-name`
                    - `notes`
                    - `office`
                    - `password`
                    - `print-stats.job-count`
                    - `print-stats.page-count`
                    - `net-stats.data-mb`
                    - `net-stats.time-hours`
                    - `restricted`
                    - `home`
            - `propertyValue` (str): The value of the property to set
        See Also:
            - `getUserProperty`
        """
        return self.api.setUserProperty(
            authToken, userName, propertyName, propertyValue
        )

    def setUserProperties(
        self,
        authToken: str,
        userName: str,
        propertyNamesAndValues: list[dict[str, str]],
    ):
        """
        Set multiple user properties at once (to save multiple calls)

        Parameters:
        - `Required`
            - `userName` (str): The name of the user
            - `propertyNamesAndValues` (list[dict[str, str]]): The list of property names and values to set. E.g. [["balance", "1.20"], ["office", "East Wing"]]. See #setUserProperty for valid property names
        See Also:
            - `getUserProperties`, setUserProperty:
        """
        return self.api.setUserProperties(authToken, userName, propertyNamesAndValues)

    def syncGroup(self, authToken: str, groupName: str):
        """
        Syncs an existing group with the configured directory server, updates the group membership

        Parameters:
        - `Required`
            - `groupName` (str): The name of the group to sync

        Returns:
        - bool
            - `True` = successful
                - On failure an exception is thrown
        """
        return self.api.syncGroup(authToken, groupName)

    def useCard(self, authToken: str, userName: str, cardNumber):
        """
        Add the value of the a card to a user's account

        Parameters:
        - `Required`
            - `cardNumber` (int): The number of the card to use
            - `userName` (str): The username with the account to credit

        Returns:
            - A string indicating the outcome, values are:
            - `CARD_HAS_EXPIRED`
            - `CARD_IS_USED`
            - `INVALID_CARD_NUMBER`
            - `SUCCESS`
            - `UNKNOWN_USER`
        """
        return self.api.useCard(authToken, userName, cardNumber)
