"""
Use the `AdminTask` object to run administrative commands with the `wsadmin` tool.

Administrative commands are loaded dynamically when you start the `wsadmin` tool. 

The administrative commands that are available for you to use, and what you can do 
with them, depends on the edition of the product that you use.

For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-admintask-object-using-wsadmin).

!!! Note
    All methods and descriptions were generated using the `AdminTask.help("-commands")` command.
"""

from typing import Any, Literal, Optional, Union, overload

from wsadmin_type_hints.typing_objects.object_name import ConfigurationObjectName


def WIMCheckPassword(*args, **kwargs):
	""" Validates the user/pasword in the Federated repositories user registry """
	...

def activateEdition(*args, **kwargs):
	""" Marks the state of an edition as ACTIVE. """
	...

def addActionToRule(*args, **kwargs):
	""" Use this command to add an action to a rule. """
	...

def addAdminIdToUserRegObj(*args, **kwargs):
	""" Adds the adminId to the user registry object in the security.xml file """
	...

def addCompUnit(*args, **kwargs):
	""" Add a composition unit, based on an asset or another business-level application, to a business-level application. """
	...

def addConditionalTraceRuleForIntelligentManagement(*args, **kwargs):
	""" Add conditional trace for Intelligent Management """
	...

def addDefaultAction(*args, **kwargs):
	""" Use this command to add a default action to a ruleset. """
	...

def addDisabledSessionCookie(*args, **kwargs):
	""" Adds a cookie configuration that applications will not be able to programmatically modify """
	...

def addExternalBundleRepository(*args, **kwargs):
	""" Adds an external bundle repository to the configuration.  Requires a repository name and a URL. """
	...

def addFeaturesToServer(*args, **kwargs):
	""" Add feature pack or stack product features to existing server """
	...

def addFileRegistryAccount(*args, **kwargs):
	""" Adds an account to the file registry. """
	...

def addForeignServersToDynamicCluster(*args, **kwargs):
	""" Add foreign servers to dynamic cluster """
	...

def addGroupToBusConnectorRole(*args, **kwargs):
	""" Give a group permission to connect to the bus specified. """
	...

def addGroupToDefaultRole(*args, **kwargs):
	""" Grants a group default access to all local destinations on the bus for the specified role. """
	...

def addGroupToDestinationRole(*args, **kwargs):
	""" Grants a group access to a destination for the specified destination role. """
	...

def addGroupToForeignBusRole(*args, **kwargs):
	""" Grants a group access to a foreign bus from the local bus specified for the specified destination role. """
	...

def addGroupToTopicRole(*args, **kwargs):
	""" Gives a group permission to access the topic for the specified role. """
	...

def addGroupToTopicSpaceRootRole(*args, **kwargs):
	""" Gives a group permission to access the topic space for the specified role. """
	...

def addIdMgrLDAPAttr(*args, **kwargs):
	""" Adds an LDAP attribute configuration to the LDAP repository configuration. """
	...

def addIdMgrLDAPAttrNotSupported(*args, **kwargs):
	""" Adds a configuration for a virtual member manager property not supported by a specific LDAP repository. """
	...

def addIdMgrLDAPBackupServer(*args, **kwargs):
	""" Sets up a backup LDAP server. """
	...

def addIdMgrLDAPEntityType(*args, **kwargs):
	""" Adds an LDAP entity type definition to the LDAP repository configuration. """
	...

def addIdMgrLDAPEntityTypeRDNAttr(*args, **kwargs):
	""" Adds RDN attribute configuration to an LDAP entity type configuration. """
	...

def addIdMgrLDAPExternalIdAttr(*args, **kwargs):
	""" Adds a configuration for an LDAP attribute used as an external ID. """
	...

def addIdMgrLDAPGroupDynamicMemberAttr(*args, **kwargs):
	""" Adds a dynamic member attribute configuration to an LDAP group configuration. """
	...

def addIdMgrLDAPGroupMemberAttr(*args, **kwargs):
	""" Adds a member attribute configuration to the LDAP group configuration. """
	...

def addIdMgrLDAPServer(*args, **kwargs):
	""" Adds an LDAP server to the LDAP repository configuration. """
	...

def addIdMgrPropertyToEntityTypes(*args, **kwargs):
	""" Adds a property to one or more entity types either into repositories or into the property extension repository. """
	...

def addIdMgrRealmBaseEntry(*args, **kwargs):
	""" Adds a base entry to a specified realm configuration. """
	...

def addIdMgrRepositoryBaseEntry(*args, **kwargs):
	""" Adds a base entry to the specified repository. """
	...

def addLocalRepositoryBundle(*args, **kwargs):
	""" Adds a bundle to the internal bundle repository. """
	...

def addMemberToGroup(*args, **kwargs):
	""" Adds a member (user or group) to a group. """
	...

def addMemberToManagedNodeGroup(*args, **kwargs):
	""" This command is used to add members to a group of managed nodes. (deprecated) """
	...

def addMemberToTargetGroup(*args, **kwargs):
	""" This command is used to add members to a target group. """
	...

def addMiddlewareAppWebModule(*args, **kwargs):
	""" Use this command to add a web module to a middleware application. """
	...

def addMiddlewareTarget(*args, **kwargs):
	""" Use this command to add a deployment target to a middleware application. """
	...

def addNodeGroupMember(*args, **kwargs):
	""" add node to the node group """
	...

def addOSGiExtension(*args, **kwargs):
	""" Adds an extension to the composition unit. """
	...

def addOSGiExtensions(*args, **kwargs):
	""" Adds multiple extensions to the composition unit. """
	...

def addPluginPropertyForIntelligentManagement(*args, **kwargs):
	""" Add plug-in property for Intelligent Management """
	...

def addPolicyType(*args, **kwargs):
	""" The addPolicyType command creates a policy type with default values for the specified policy set. You may indicate whether to enable or disable the added policy type. """
	...

def addProductInfo(*args, **kwargs):
	""" Add feature pack or stack product information to product info. """
	...

def addRemoteCellToIntelligentManagement(*args, **kwargs):
	""" Command to add remote cell connectors to Intelligent Management """
	...

def addResourceToAuthorizationGroup(*args, **kwargs):
	""" Add resources to an existing authorization group. """
	...

def addRoutingPolicyRoutingRule(*args, **kwargs):
	""" Use this command to add a routing rule to an existing workclass """
	...

def addRoutingRule(*args, **kwargs):
	""" Use this command to add a routing policy rule. """
	...

def addRuleToRuleset(*args, **kwargs):
	""" Use this command to add a rule to a ruleset. """
	...

def addSAMLTAISSO(*args, **kwargs):
	""" This command adds the SAML Single Sign-On (SSO) service provider (SP) to the security configuration SAML TAI. """
	...

def addSIBBootstrapMember(*args, **kwargs):
	""" Nominates a server or cluster for use as a bootstrap server. """
	...

def addSIBPermittedChain(*args, **kwargs):
	""" Adds the specified chain to the list of permitted chains for the specified bus. """
	...

def addSIBWSInboundPort(*args, **kwargs):
	""" Add an inbound port to an inbound service. """
	...

def addSIBWSOutboundPort(*args, **kwargs):
	""" Add an outbound port to an outbound service. """
	...

def addSIBusMember(*args, **kwargs):
	""" Add a member to a bus. """
	...

def addSTSProperty(*args, **kwargs):
	""" Add a configuration property under a configuration group. """
	...

def addServicePolicyRoutingRule(*args, **kwargs):
	""" Use this command to add a routing rule to an existing workclass """
	...

def addServiceRule(*args, **kwargs):
	""" Use this command to add a service policy rule. """
	...

def addSignerCertificate(*args, **kwargs):
	""" Add a signer certificates from a certificate file to a keystore. """
	...

def addSpnegoFilter(*args, **kwargs):
	""" This command adds SPNEGO Web authentication filter in the security configuration. """
	...

def addSpnegoTAIProperties(*args, **kwargs):
	""" This command adds SPNEGO TAI properties in the security configuration. """
	...

def addToAdminAuthz(*args, **kwargs):
	""" Adds the input administrative user to admin-authz.xml. """
	...

def addToPolicySetAttachment(*args, **kwargs):
	""" The addToPolicySetAttachment command adds additional resources that apply to a policy set attachment. """
	...

def addTrustedRealms(*args, **kwargs):
	""" Adds a realm or list of realms to the list of trusted realms in a security domain or in global security. """
	...

def addUserToBusConnectorRole(*args, **kwargs):
	""" Give a user permission to connect to the bus specified. """
	...

def addUserToDefaultRole(*args, **kwargs):
	""" Grants a user default access to all local destinations on the bus for the specified role. """
	...

def addUserToDestinationRole(*args, **kwargs):
	""" Grants a user access to a destination for the specified destination role. """
	...

def addUserToForeignBusRole(*args, **kwargs):
	""" Grants a user access to a foreign bus from the local bus specified for the specified destination role. """
	...

def addUserToTopicRole(*args, **kwargs):
	""" Gives a user permission to access the topic for the specified role. """
	...

def addUserToTopicSpaceRootRole(*args, **kwargs):
	""" Gives a user permission to access the topic space for the specified role. """
	...

def addWSGWTargetService(*args, **kwargs):
	""" addWSGWTargetService.description """
	...

def addWebServerRoutingRule(*args, **kwargs):
	""" Use this command to create a new routing rule. """
	...

def applyConfigProperties(*args, **kwargs):
	""" Apply configuration as specified in properties file """
	...

def applyProfileSecuritySettings(*args, **kwargs):
	""" Applies the security settings selected during install or profile creation time. """
	...

def applyWizardSettings(*args, **kwargs):
	""" Applies current Security Wizard settings from the workspace. """
	...

def assignSTSEndpointTokenType(*args, **kwargs):
	""" Assign a token type to be issued for the client to access a given endpoint. Endpoints must be unique. If the local name parameter is omitted, the default token type is assumed. """
	...

def attachServiceMap(*args, **kwargs):
	""" Use the "attachServiceMap" command to attach a service map to a local mapping service. """
	...

def autogenLTPA(*args, **kwargs):
	""" Auto-generates an LTPA password and updates the LTPA object in the security.xml. """
	...

def autogenServerId(*args, **kwargs):
	""" Auto-generates a server Id and updates the internalServerId field in the security.xml. """
	...

def backupJobManager(*args, **kwargs):
	""" Backs up the job manager database to a specified location. """
	...

def binaryAuditLogReader(*args, **kwargs):
	""" Binary Audit Log Reader Command """
	...

def canNodeJoinNodeGroup(*args, **kwargs):
	""" Check if a specified node can be added to a specified node group. """
	...

def cancelValidation(*args, **kwargs):
	""" Cancels the validation mode of an edition. """
	...

def changeClusterShortName(*args, **kwargs):
	""" A command that can be used to change the cluster's short name. """
	...

def changeFileRegistryAccountPassword(*args, **kwargs):
	""" Change the password of an account in the file registry. """
	...

def changeHostName(*args, **kwargs):
	""" Change the host name of a node """
	...

def changeKeyStorePassword(*args, **kwargs):
	""" Change the password of a keystore. This will automatically save the new password to the configuration. """
	...

def changeMultipleKeyStorePasswords(*args, **kwargs):
	""" Change all the passwords for the keystores that use the password provided, which automatically saves the new passwords to the configuration. """
	...

def changeMyPassword(*args, **kwargs):
	""" Changes the password of this logged-in user. """
	...

def changeRoutingDefaultRulesAction(*args, **kwargs):
	""" Use this command to change a rules routing policy default action. """
	...

def changeRoutingRuleAction(*args, **kwargs):
	""" Use this command to change a routing policy action for a rule. """
	...

def changeRoutingRuleExpression(*args, **kwargs):
	""" Use this command to change a routing policy rule expression. """
	...

def changeRoutingRulePriority(*args, **kwargs):
	""" Use this command to change a routing policy rule priority. """
	...

def changeRuleExpression(*args, **kwargs):
	""" Use this command to change a rule expression. """
	...

def changeRulePriority(*args, **kwargs):
	""" Use this command to change a rule prioritiy. """
	...

def changeServerGenericShortName(*args, **kwargs):
	""" A command that can be used to change the server generic short name. """
	...

def changeServerSpecificShortName(*args, **kwargs):
	""" A command that can be used to change the server specific short name. """
	...

def changeServiceDefaultRulesAction(*args, **kwargs):
	""" Use this command to change a rules service policy default action. """
	...

def changeServiceRuleAction(*args, **kwargs):
	""" Use this command to change a service policy action for a rule. """
	...

def changeServiceRuleExpression(*args, **kwargs):
	""" Use this command to change a service policy rule expression. """
	...

def changeServiceRulePriority(*args, **kwargs):
	""" Use this command to change a service policy rule priority. """
	...

def changeWebServerRoutingRuleAction(*args, **kwargs):
	""" Use this command to change the action associated with an existing routing rule. """
	...

def changeWebServerRoutingRuleExpression(*args, **kwargs):
	""" Use this command to change the expression associated with an existing routing rule. """
	...

def changeWebServerRoutingRuleOrder(*args, **kwargs):
	""" Use this command to change the order associated with an existing routing rule. """
	...

def checkDynamicClustersForNodeGroupRemoval(*args, **kwargs):
	""" Check Node Group for XD Dynamic Clusters """
	...

def checkMode(*args, **kwargs):
	""" checks the maintenance mode indicator on specified server """
	...

def checkRegistryRunAsUser(*args, **kwargs):
	""" Checks if the provided runas user is valid.  True is return if the runas user is valid and false if it is not. """
	...

def checkRegistryUserPassword(*args, **kwargs):
	""" Check if the provided user and password authenticate in the registry. """
	...

def cleanupManagedNode(*args, **kwargs):
	""" Cleanup a managed node that no longer exists """
	...

def cleanupTarget(*args, **kwargs):
	""" Cleanup a Target that no longer exists """
	...

def clearAuthCache(*args, **kwargs):
	""" Clears the auth cache for a security domain; if no security domain is specified, the auth cache for the admin security domain will be cleared """
	...

def clearIdMgrRepositoryCache(*args, **kwargs):
	""" Clears the cache of the specified repository or of all repositories. """
	...

def clearIdMgrUserFromCache(*args, **kwargs):
	""" Removes a specified user from the cache. """
	...

def cloneDynamicCluster(*args, **kwargs):
	""" Use this command to clone a dynamic cluster. """
	...

def clonePreference(*args, **kwargs):
	""" Command to clone a user preference """
	...

def compareMultipleResourceAdapters(*args, **kwargs):
	""" Compare a list of multiple resource adapters to see if they are all able to be updated with the same RAR file. """
	...

def compareNodeVersion(*args, **kwargs):
	""" Compares the version of a given node with the specified version.  Only the number of levels in the specified version number are compared.  For example, if "6.0" compared to a node version of "6.0.1.0", they will compare as equal.  The possible return values are -1, 0, and 1. They are defined as follows: 
            - `-1`: node version is less than the specified version
            - `0`: node version is equal to the specified version
            - `1`: node version is greater than the specified version
    """
	...

def compareResourceAdapterToRAR(*args, **kwargs):
	""" Compare an existing Resource Adapter to a RAR file and determine whether the RAR is compatible for updating the Resource Adapter. """
	...

def configureAdminCustomUserRegistry(*args, **kwargs):
	""" Configure a custom user registry in the administrative security configuration """
	...

def configureAdminLDAPUserRegistry(*args, **kwargs):
	""" Configure an LDAP user registry in the administrative security configuration """
	...

def configureAdminLocalOSUserRegistry(*args, **kwargs):
	""" Configures a local OS user registry in the administrative security configuration. """
	...

def configureAdminWIMUserRegistry(*args, **kwargs):
	""" Configures a Federated repositories user registry in the administrative security configuration. """
	...

def configureAppCustomUserRegistry(*args, **kwargs):
	""" Configure a custom user registry in an application security domain """
	...

def configureAppLDAPUserRegistry(*args, **kwargs):
	""" Configures an LDAP user registry in an application security domain """
	...

def configureAppLocalOSUserRegistry(*args, **kwargs):
	""" Configures a local OS user registry in an application security domain. """
	...

def configureAppWIMUserRegistry(*args, **kwargs):
	""" Configures a Federated repositories user registry in an application security domain. """
	...

def configureAuthzConfig(*args, **kwargs):
	""" Configures an external authorization provider in global security or in an application security domain. """
	...

def configureCSIInbound(*args, **kwargs):
	""" Configures the CSI inbound information in the administrative security configuration or in an application security domain. """
	...

def configureCSIOutbound(*args, **kwargs):
	""" Configures the CSI outbound information in the administrative security configuration or in an application security domain. """
	...

def configureDVIPA(*args, **kwargs):
	""" configureDVIPA.desc """
	...

def configureInterceptor(*args, **kwargs):
	""" Configures an interceptor. """
	...

def configureJAASLoginEntry(*args, **kwargs):
	""" Configures a JAAS login module entry in the administrative security configuration or in an application security domain. """
	...

def configureJaspi(*args, **kwargs):
	""" Configure the Jaspi configuration. """
	...

def configureLoginModule(*args, **kwargs):
	""" Configures a login module in the administrative security configuration or in an application security domain. """
	...

def configureRSATokenAuthorization(*args, **kwargs):
	""" Command that modifies the role propagation authorization mechanism """
	...

def configureSingleHome(*args, **kwargs):
	""" configureDVIPA.desc """
	...

def configureSingleSignon(*args, **kwargs):
	""" Configure single signon. """
	...

def configureSpnego(*args, **kwargs):
	""" This command configures SPNEGO Web Authentication in the security configuration. """
	...

def configureTAM(*args, **kwargs):
	""" This command configures embedded Tivoli Access Manager on the WebSphere Application Server node or nodes specified. """
	...

def configureTAMTAI(*args, **kwargs):
	""" This command configures the embedded Tivoli Access Manager Trust Association Interceptor with classname TAMTrustAsociationInterceptorPlus. """
	...

def configureTAMTAIPdjrte(*args, **kwargs):
	""" This command performs the tasks necessary to fully configure the Tivoli Access Manager Runtime for Java. The specific tasks run are PDJrteCfg and SvrSslCfg. """
	...

def configureTAMTAIProperties(*args, **kwargs):
	""" This command adds the custom properties to the security configuration for the embedded Tivoli Access Manager Trust Association Interceptor with classname TAMTrustAsociationInterceptorPlus. """
	...

def configureTrustAssociation(*args, **kwargs):
	""" Configures a trust association. """
	...

def configureTrustedRealms(*args, **kwargs):
	""" Configures an inbound or outbound trusted realms. """
	...

def connectSIBWSEndpointListener(*args, **kwargs):
	""" Connect an endpoint listener to a service integration bus. """
	...

def convertCertForSecurityStandard(*args, **kwargs):
	""" Converts certificates used by SSL configuration and plugins so that they comply with specified FIPS level.  Also lists certificates that cannot be converted by WebSphere. """
	...

def convertFilterRefToString(*args, **kwargs):
	""" Converts an audit specification reference to a string representation. """
	...

def convertFilterStringToRef(*args, **kwargs):
	""" Converts an audit specification event and outcome to a reference representation. """
	...

def convertSSLCertificates(*args, **kwargs):
	""" Converts SSL personal certificates to a certificate that is created with the desired signature algorithm or lists SSL personal certificates that are not created with the desired signature algorithm. """
	...

def convertSSLConfig(*args, **kwargs):
	""" Converts old style SSL configuration to new style SSL configurations.  The CONVERT_SSLCONFIGS option will look for old style SSL configuration objects and change them to look like new style SSL configuration objects.  The CONVERT_TO_DEFAULT will go through make convert the whole SSL configuration to the new centralized SSL configuration style, removing the SSL configuraiton direct referencing from the servers. """
	...

def convertSelfSignedCertificatesToChained(*args, **kwargs):
	""" Converts self-signed certificates to chained certificate in a keystore, all keystore, or the default keystores.  The new chained certificate will be signed with root certificate specified or the default root if one is not specified.  All keystores in the configuration will be searched for the self-signed certificate's signer certificate and it will be replaced with the signer of the default root certificate. """
	...

def convertServerSecurityToSecurityDomain(*args, **kwargs):
	""" Task to convert server level security configuration to a security domain configuration. """
	...

def convertToSysplexNodeGroup(*args, **kwargs):
	""" Converts to a sysplex node group """
	...

def copyBinding(*args, **kwargs):
	""" The copyBinding command creates a copy of an existing binding. """
	...

def copyIdMgrFilesForDomain(*args, **kwargs):
	""" Copies the files related to virtual member manager from the specified source domain to the specified destination domain. """
	...

def copyPolicySet(*args, **kwargs):
	""" The copyPolicySet command creates a copy of an existing policy set. The default indicator is set to false for the new policy set. You may indicate whether to transfer attachments from the existing policy set to the new policy set. """
	...

def copyResourceAdapter(*args, **kwargs):
	""" copy the specified J2C resource adapter to the specified scope. """
	...

def copySecurityDomain(*args, **kwargs):
	""" Creates a security domain by coping from another security domain. """
	...

def copySecurityDomainFromGlobalSecurity(*args, **kwargs):
	""" Creates a security domain by copy the global administrative security configuration. """
	...

def correctSIBEnginePolicy(*args, **kwargs):
	""" Ensures that a messaging engines core group policy conforms to its associated bus members messaging engine assistance policy. """
	...

def createAllActivePolicy(*args, **kwargs):
	""" Create a policy that automatically activates all group members. """
	...

def createApacheServer(*args, **kwargs):
	""" Use this command to create an Apache Server. """
	...

def createApacheServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createApplicationServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createApplicationServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createAuditEncryptionConfig(*args, **kwargs):
	""" Configures audit record encryption. """
	...

def createAuditEventFactory(*args, **kwargs):
	""" Creates an entry in the audit.xml to reference the configuration of an audit event factory implementation of the Audit Event Factory interface. """
	...

def createAuditFilter(*args, **kwargs):
	""" Creates an entry in the audit.xml to reference an Audit Specification. Enables the specification by default. """
	...

def createAuditKeyStore(*args, **kwargs):
	""" Creates a new Key Store. """
	...

def createAuditNotification(*args, **kwargs):
	""" Configures an audit notification. """
	...

def createAuditNotificationMonitor(*args, **kwargs):
	""" Configures an audit notification monitor. """
	...

def createAuditSelfSignedCertificate(*args, **kwargs):
	""" Create a new self-signed certificate and store it in a key store. """
	...

def createAuditSigningConfig(*args, **kwargs):
	""" Configures audit record signing. """
	...

def createAuthDataEntry(*args, **kwargs):
	""" Create an authentication data entry in the administrative security configuration or a in a security domain. """
	...

def createAuthorizationGroup(*args, **kwargs):
	""" Create a new authorization group. """
	...

def createBinaryEmitter(*args, **kwargs):
	""" Creates an entry in the audit.xml to reference the configuration of the Binary File Emitter implementation of the Service Provider interface. """
	...

def createCAClient(*args, **kwargs):
	""" Creates a certificate authority (CA) client configurator object. """
	...

def createCMSKeyStore(*args, **kwargs):
	""" Create a CMS KeyStore with password stash file. """
	...

def createCertificateRequest(*args, **kwargs):
	""" Create Certificate Request """
	...

def createChain(*args, **kwargs):
	""" Create a new chain of transport channels based on a chain template. """
	...

def createChainedCertificate(*args, **kwargs):
	""" Create a new chained certificate and store it in a key store. """
	...

def createCluster(*args, **kwargs):
	""" Creates a new application server cluster. """
	...

def createClusterMember(*args, **kwargs):
	""" Creates a new member of an application server cluster. """
	...

def createCoreGroup(*args, **kwargs):
	""" Create a new core group """
	...

def createCoreGroupAccessPoint(*args, **kwargs):
	""" This command creates a default core group access point for the specified core group and adds it to the default access point group. """
	...

def createDatasource(*args, **kwargs):
	""" Create a new Datasource to access the backend data store.  Application components use the Datasource to access connection instances to your database. A connection pool is associated with each Datasource. """
	...

def createDefaultARPWorkClass(*args, **kwargs):
	""" Creates default application routing policy work classes """
	...

def createDefaultASPWorkClass(*args, **kwargs):
	""" Creates default application service policy work classes """
	...

def createDefaultGRPWorkClass(*args, **kwargs):
	""" Creates a default generic server routing policy default work class """
	...

def createDefaultGSPWorkClass(*args, **kwargs):
	""" Creates a default generic server service policy default work class """
	...

def createDefaultSystemRPWorkClass(*args, **kwargs):
	""" Creates default system application routing policy work classes """
	...

def createDefaultSystemSPWorkClass(*args, **kwargs):
	""" Creates default system application service policy work classes """
	...

def createDescriptiveProp(*args, **kwargs):
	""" Create a descriptive property under an object. """
	...

def createDynamicCluster(*args, **kwargs):
	""" Create a new WAS dynamic cluster """
	...

def createDynamicClusterFromForeignServers(*args, **kwargs):
	""" Create a new dynamic cluster from existing foreign servers """
	...

def createDynamicClusterFromStaticCluster(*args, **kwargs):
	""" Create a new dynamic cluster from existing static cluster """
	...

def createDynamicSSLConfigSelection(*args, **kwargs):
	""" Create a Dynamic SSL configuration Selection. """
	...

def createElasticityAction(*args, **kwargs):
	""" Command to create a elasticity action """
	...

def createEmptyBLA(*args, **kwargs):
	""" Create a new business-level application with no composition units. """
	...

def createExtWasAppServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createExtWasAppServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createForeignServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createForeignServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createFullCheckpoint(*args, **kwargs):
	""" Create a full named checkpoint specified by the "checkpointName" """
	...

def createGenericServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createGenericServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createGroup(*args, **kwargs):
	""" Creates a group in the default realm. """
	...

def createHealthAction(*args, **kwargs):
	""" Command to create a health action """
	...

def createHealthPolicy(*args, **kwargs):
	""" Command to create a health policy """
	...

def createIdMgrCustomRepository(*args, **kwargs):
	""" Creates a custom repository configuration. """
	...

def createIdMgrDBRepository(*args, **kwargs):
	""" Creates a database repository configuration. """
	...

def createIdMgrFileRepository(*args, **kwargs):
	""" Creates a file repository configuration. """
	...

def createIdMgrLDAPRepository(*args, **kwargs):
	""" Creates an LDAP repository configuration object. """
	...

def createIdMgrRealm(*args, **kwargs):
	""" Creates a realm configuration. """
	...

def createIdMgrSupportedEntityType(*args, **kwargs):
	""" Creates a supported entity type configuration. """
	...

def createJ2CActivationSpec(*args, **kwargs):
	""" Create a J2C activation specification. """
	...

def createJ2CAdminObject(*args, **kwargs):
	""" Create a J2C administrative object. """
	...

def createJ2CConnectionFactory(*args, **kwargs):
	""" Create a J2C connection factory """
	...

def createJAXWSHandler(*args, **kwargs):
	""" Create a JAX-WS Handler """
	...

def createJAXWSHandlerList(*args, **kwargs):
	""" Create a JAX-WS Handler List """
	...

def createJBossServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createJBossServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createJDBCProvider(*args, **kwargs):
	""" Create a new JDBC provider that is used to connect with a relational database for data access. """
	...

def createJobSchedulerProperty(*args, **kwargs):
	""" add a custom property for job scheduler """
	...

def createKeyManager(*args, **kwargs):
	""" Create a key manager. """
	...

def createKeyReference(*args, **kwargs):
	""" Create a Key Reference for a keySet. """
	...

def createKeySet(*args, **kwargs):
	""" Create a Key Set. """
	...

def createKeySetGroup(*args, **kwargs):
	""" Create a key set group. """
	...

def createKeyStore(*args, **kwargs):
	""" Creates a new keystore. """
	...

def createKrbAuthMechanism(*args, **kwargs):
	""" The KRB5 authentication mechanism security object field in the security configuration file is created based on the user input. """
	...

def createKrbConfigFile(*args, **kwargs):
	""" This command creates a Kerberos configuration file (krb5.ini or krb5.conf). """
	...

def createLMService(*args, **kwargs):
	""" Use the "createLMService" command to create a local mapping service, to which a service map can be attached. """
	...

def createLMServiceEventPoint(*args, **kwargs):
	""" Use the "createLMServiceEventPoint" command to create a local mapping service event point, in order to generate service mapping events. """
	...

def createLibertyServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createLibertyServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createLongRunningSchedulerProperty(*args, **kwargs):
	""" (Deprecated) add a custom property for long-running scheduler. Use createJobSchedulerProperty. """
	...

def createMOfNPolicy(*args, **kwargs):
	""" Create a policy that activates the specified number of group members. """
	...

def createManagedNodeGroup(*args, **kwargs):
	""" This command is used to create a group of managed nodes. (deprecated) """
	...

def createManagementScope(*args, **kwargs):
	""" Create a management scope. """
	...

def createMigrationReport(*args, **kwargs):
	""" Scans an application to create a Liberty migration report """
	...

def createMissingSIBEnginePolicy(*args, **kwargs):
	""" Create a core group policy for a messaging engine configured for server cluster bus member with messaging engine policy assistance enabled for the "Custom" policy. """
	...

def createNoOpPolicy(*args, **kwargs):
	""" Create a policy in which no group members are automatically activated. """
	...

def createNodeGroup(*args, **kwargs):
	""" create a node group """
	...

def createNodeGroupProperty(*args, **kwargs):
	""" add a custom property for a node group """
	...

def createNonWASDynamicCluster(*args, **kwargs):
	""" Create a new non-WAS dynamic cluster """
	...

def createOAuthProvider(*args, **kwargs):
	""" Create OAuth Provider """
	...

def createODRDynamicCluster(*args, **kwargs):
	""" Create On Demand Router dynamic cluster """
	...

def createObjectCacheInstance(*args, **kwargs):
	""" Create an Object Cache Instance.  An object cache instance is a location where an applications can store, distribute, and share data. """
	...

def createOnDemandRouter(*args, **kwargs):
	""" Command that creates a server """
	...

def createOnDemandRouterTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createOneOfNPolicy(*args, **kwargs):
	""" Create a policy that keeps one member active at a time. """
	...

def createPHPDynamicCluster(*args, **kwargs):
	""" Create a new PHP dynamic cluster """
	...

def createPHPServer(*args, **kwargs):
	""" Use this command to create a PHP Server. """
	...

def createPHPServerTemplate(*args, **kwargs):
	""" Use this command to create a PHP Server template. """
	...

def createPolicySet(*args, **kwargs):
	""" The createPolicySet command creates a new policy set. Policy types are not created with the policy set. The default indicator is set to false. """
	...

def createPolicySetAttachment(*args, **kwargs):
	""" The createPolicySetAttachment command creates a new policy set attachment. """
	...

def createPropertiesFileTemplates(*args, **kwargs):
	""" Create properties file template for create/delete objects """
	...

def createProxyServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createProxyServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createRoutingPolicyWorkClass(*args, **kwargs):
	""" Use this command to create a Routing Policy Workclass """
	...

def createRoutingRules(*args, **kwargs):
	""" Use this command to create a routing policy rule list. """
	...

def createRuleset(*args, **kwargs):
	""" Use this command to create a ruleset. """
	...

def createSIBDestination(*args, **kwargs):
	""" Create bus destination. """
	...

def createSIBDestinations(*args, **kwargs):
	""" Create bus destinations. """
	...

def createSIBEngine(*args, **kwargs):
	""" Create a messaging engine. """
	...

def createSIBForeignBus(*args, **kwargs):
	""" Create a SIB foreign bus. """
	...

def createSIBJMSActivationSpec(*args, **kwargs):
	""" Create an activation specification in the SIB JMS resource adapter. """
	...

def createSIBJMSConnectionFactory(*args, **kwargs):
	""" Create a SIB JMS connection factory at the scope identified by the target object. """
	...

def createSIBJMSQueue(*args, **kwargs):
	""" Create a SIB JMS queue at the scope identified by the target object. """
	...

def createSIBJMSTopic(*args, **kwargs):
	""" Create a SIB JMS topic at the scope identified by the target object. """
	...

def createSIBLink(*args, **kwargs):
	""" Create a new SIB link. """
	...

def createSIBMQLink(*args, **kwargs):
	""" Create a new WebSphere MQ link. """
	...

def createSIBMediation(*args, **kwargs):
	""" Create a mediation. """
	...

def createSIBWMQServer(*args, **kwargs):
	""" Create a new WebSphere MQ server. """
	...

def createSIBWSEndpointListener(*args, **kwargs):
	""" Creates an endpoint listener configuration.This command is supported only in the connected mode. """
	...

def createSIBWSInboundService(*args, **kwargs):
	""" Create an inbound service. """
	...

def createSIBWSOutboundService(*args, **kwargs):
	""" Create an outbound service. """
	...

def createSIBus(*args, **kwargs):
	""" Create a bus. """
	...

def createSMFEmitter(*args, **kwargs):
	""" Creates an entry in the audit.xml to reference the configuration of an SMF Emitter implementation of the Service Provider interface. """
	...

def createSSLConfig(*args, **kwargs):
	""" Create a SSL Configuration. """
	...

def createSSLConfigGroup(*args, **kwargs):
	""" Create a SSL Configuration Group. """
	...

def createSSLConfigProperty(*args, **kwargs):
	""" Create a SSLConfig Property. """
	...

def createSecurityDomain(*args, **kwargs):
	""" Creates an empty security domain object. """
	...

def createSelfSignedCertificate(*args, **kwargs):
	""" Create a new self-signed certificate and store it in a keystore. """
	...

def createServerType(*args, **kwargs):
	""" Create a new Server Type e.g. (APPLICATION_SERVER) """
	...

def createServicePolicyWorkClass(*args, **kwargs):
	""" Use these commands to configure Service Policy Workclasses """
	...

def createServiceRules(*args, **kwargs):
	""" Use this command to create a service policy rule list. """
	...

def createServletCacheInstance(*args, **kwargs):
	""" Create a Servlet Cache Instance.  A servlet cache instance is a location where the dynamic cache can store, distribute, and share data. """
	...

def createStaticPolicy(*args, **kwargs):
	""" Create a policy that activates group members on all of the servers in the list. """
	...

def createSysplexNodeGroup(*args, **kwargs):
	""" create sysplex node group """
	...

def createSystemRoutingPolicyWorkClass(*args, **kwargs):
	""" Use this command to create a Routing Policy Workclass """
	...

def createSystemServicePolicyWorkClass(*args, **kwargs):
	""" Use this command to create a Routing Policy Workclass """
	...

def createTADataCollection(*args, **kwargs):
	""" This command scans the profile to create a Transformation Advisor data collection. """
	...

# --------------------------------------------------------------------------
@overload
def createTCPEndPoint(target_object: Literal['-interactive'], /) -> Any:
    ...

@overload
def createTCPEndPoint(target_object: ConfigurationObjectName, /) -> ConfigurationObjectName:
    ...

@overload
def createTCPEndPoint(target_object: ConfigurationObjectName, options: Union[str, list], /) -> ConfigurationObjectName:
    ...

def createTCPEndPoint(target_object: Union[Literal['-interactive'], ConfigurationObjectName], options: Union[str, list], /) -> ConfigurationObjectName: # type: ignore[misc]
    """Create a new endpoint that you can associate with a TCP inbound channel.

    - If `options` is set to a string with value `"-interactive"`, the endpoint will 
        be created in _interactive mode_.

    Args:
        target_object (ConfigurationObjectName): Parent instance of the TransportChannelService that contains the TCPInboundChannel.
        options (str | list): String containing the `-name`, `-host` and `-port` parameters (all **required**) with their values set. 
            If `options` is set to a string with value `"-interactive"`, the endpoint will be created in _interactive mode_.

    Returns:
        ConfigurationObjectName: The object name of the endpoint that was created.

    Example:
        ```pycon
        >>> target = 'cells/mybuildCell01/nodes/mybuildCellManager01/servers/dmgr|server.xml#TransportChannelService_1'
        
        # As a string...
        >>> AdminTask.createTCPEndPoint(target, '[-name Sample_End_Pt_Name -host mybuild.location.ibm.com -port 8978]')
        
        # ... or as a list...
        >>> AdminTask.createTCPEndPoint(target, ['-name', 'Sample_End_Pt_Name', '-host', 'mybuild.location.ibm.com', '-port', '8978'])
        ```
    """
    ...
# --------------------------------------------------------------------------


def createTargetGroup(*args, **kwargs):
	""" This command is used to create a group of targets. """
	...

def createTemplateFromTemplate(*args, **kwargs):
	""" Create a server template from an existing server template """
	...

def createThirdPartyEmitter(*args, **kwargs):
	""" Creates an entry in the audit.xml to reference the configuration of a Third Party Emitter implementation of the Service Provider interface. """
	...

def createTomCatServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createTomCatServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createTrustManager(*args, **kwargs):
	""" Create a trust Manager. """
	...

def createUDPEndPoint(*args, **kwargs):
	""" Create a new NamedEndPoint endpoint to associate with a UDPInboundChannel """
	...

def createUnmanagedNode(*args, **kwargs):
	""" Use this command to create an unmanaged node in a cell. """
	...

def createUser(*args, **kwargs):
	""" Creates a PersonAccount in the default realm. """
	...

def createWMQActivationSpec(*args, **kwargs):
	""" Creates a IBM MQ Activation Specification at the scope provided to the command. """
	...

def createWMQConnectionFactory(*args, **kwargs):
	""" Creates a IBM MQ Connection Factory at the scope provided to the command. """
	...

def createWMQQueue(*args, **kwargs):
	""" Creates a IBM MQ Queue at the scope provided to the command. """
	...

def createWMQTopic(*args, **kwargs):
	""" Creates a IBM MQ Topic at the scope provided to the command. """
	...

def createWSCertExpMonitor(*args, **kwargs):
	""" Create a certificate expiration monitor. """
	...

def createWSGWGatewayService(*args, **kwargs):
	""" createWSGWGatewayService.description """
	...

def createWSGWProxyService(*args, **kwargs):
	""" createWSGWProxyService.description """
	...

def createWSNAdministeredSubscriber(*args, **kwargs):
	""" Add an administered subscriber to a WS-Notification service point """
	...

def createWSNService(*args, **kwargs):
	""" Create a WS-Notification service """
	...

def createWSNServicePoint(*args, **kwargs):
	""" Create a WS-Notification service point """
	...

def createWSNTopicDocument(*args, **kwargs):
	""" Add an instance document to a WS-Notification topic namespace """
	...

def createWSNTopicNamespace(*args, **kwargs):
	""" Create a WS-Notification topic namespace """
	...

def createWSNotifier(*args, **kwargs):
	""" Create a notifier. """
	...

def createWSSchedule(*args, **kwargs):
	""" Create a schedule. """
	...

def createWasCEServer(*args, **kwargs):
	""" Use this command to create an WebSphere Community Edition Server. """
	...

def createWasCEServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createWebLogicServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createWebLogicServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def createWebModuleProxyConfig(*args, **kwargs):
	""" Create a proxy configuration for a Web module """
	...

def createWebServer(*args, **kwargs):
	""" Command that creates a server """
	...

def createWebServerByHostName(*args, **kwargs):
	""" Create Web server definition using hostname. """
	...

def createWebServerTemplate(*args, **kwargs):
	""" creates a server Template based on a server configuration """
	...

def deactivateEdition(*args, **kwargs):
	""" Marks the state of an edition as INACTIVE. """
	...

def defineJaspiProvider(*args, **kwargs):
	""" Define a new authentication provider. """
	...

def deleteAsset(*args, **kwargs):
	""" Delete an asset which was imported into the product configuration repository. """
	...

def deleteAttachmentsForPolicySet(*args, **kwargs):
	""" The deleteAttachmentsForPolicySet command removes all attachments for a specific policy set. """
	...

def deleteAuditCertificate(*args, **kwargs):
	""" Delete the personal certificate used for audit encryption from the keystore identified as the audit encryption keystore """
	...

def deleteAuditEmitterByName(*args, **kwargs):
	""" Deletes an audit emitter implementation object by unique name. """
	...

def deleteAuditEmitterByRef(*args, **kwargs):
	""" Deletes an audit emitter implementation object by reference id. """
	...

def deleteAuditEncryptionConfig(*args, **kwargs):
	""" Deletes the audit record encryption configuration. """
	...

def deleteAuditEventFactoryByName(*args, **kwargs):
	""" Deletes the audit event factory specified by the unique name. """
	...

def deleteAuditEventFactoryByRef(*args, **kwargs):
	""" Deletes the audit event factory specified by the reference id. """
	...

def deleteAuditFilter(*args, **kwargs):
	""" Deletes an audit specification entry in the audit.xml that matches the event and outcome. """
	...

def deleteAuditFilterByRef(*args, **kwargs):
	""" Deletes an audit specification entry in the audit.xml that matches the reference Id. """
	...

def deleteAuditKeyStore(*args, **kwargs):
	""" Deletes an existing Key Store. """
	...

def deleteAuditNotification(*args, **kwargs):
	""" Deletes an audit notification. """
	...

def deleteAuditNotificationMonitorByName(*args, **kwargs):
	""" Deletes an audit notification monitor specified by the unique name. """
	...

def deleteAuditNotificationMonitorByRef(*args, **kwargs):
	""" Deletes an audit notification monitor specified by the reference id. """
	...

def deleteAuditSigningConfig(*args, **kwargs):
	""" Unconfigures audit record signing. """
	...

def deleteAuthDataEntry(*args, **kwargs):
	""" Delete an authentication data entry from the administrative security configuration or a in a security domain. """
	...

def deleteAuthorizationGroup(*args, **kwargs):
	""" Delete an existing authorization group """
	...

def deleteBLA(*args, **kwargs):
	""" Delete a specified business-level application. """
	...

def deleteCAClient(*args, **kwargs):
	""" Deletes a certificate authority (CA) client configurator object. """
	...

def deleteCertificate(*args, **kwargs):
	""" Delete a personal certificate from a keystore. """
	...

def deleteCertificateRequest(*args, **kwargs):
	""" Delete an existing certificate request from a keystore. """
	...

def deleteChain(*args, **kwargs):
	""" Delete an existing chain and, optionally, the transport channels in the chain. """
	...

def deleteCheckpoint(*args, **kwargs):
	""" Delete the named checkpoint specified by the "checkpointName" """
	...

def deleteCluster(*args, **kwargs):
	""" Delete the configuration of an application server cluster. """
	...

def deleteClusterMember(*args, **kwargs):
	""" Deletes a member from an application server cluster. """
	...

def deleteCompUnit(*args, **kwargs):
	""" Delete a composition unit from a business-level application. """
	...

def deleteConfigProperties(*args, **kwargs):
	""" Delete configuration specified in properties file """
	...

def deleteCoreGroup(*args, **kwargs):
	""" Delete an existing core group. The core group must contain no servers. """
	...

def deleteCoreGroupAccessPoints(*args, **kwargs):
	""" Delete all the core group access points associated with a specified core group. """
	...

def deleteDatasource(*args, **kwargs):
	""" Delete a Datasource used to access a relational database. """
	...

def deleteDescriptiveProp(*args, **kwargs):
	""" Delete a descriptive property under an object. """
	...

def deleteDynamicCluster(*args, **kwargs):
	""" Delete a dynamic cluster from the configuration repository. """
	...

def deleteDynamicSSLConfigSelection(*args, **kwargs):
	""" Delete an existing Dynamic SSL configuration Selection. """
	...

def deleteElasticityAction(*args, **kwargs):
	""" Command to delete a elasticity action """
	...

def deleteGroup(*args, **kwargs):
	""" Deletes a group from the default realm. """
	...

def deleteHealthAction(*args, **kwargs):
	""" Command to delete a health action """
	...

def deleteHealthPolicy(*args, **kwargs):
	""" Command to delete a health policy """
	...

def deleteIdMgrDBTables(*args, **kwargs):
	""" Deletes the tables of the database in virtual member manager. """
	...

def deleteIdMgrEntryMappingRepositoryTables(*args, **kwargs):
	""" Deletes the tables of the entry mapping database in virtual member manager. """
	...

def deleteIdMgrLDAPAttr(*args, **kwargs):
	""" Deletes a LDAP attribute configuration data for a specified entity type for a specific LDAP repository. Use the name of either the LDAP attribute or virtual member manager property. """
	...

def deleteIdMgrLDAPAttrNotSupported(*args, **kwargs):
	""" Deletes the configuration for a virtual member manager property not supported by a specific LDAP repository. """
	...

def deleteIdMgrLDAPEntityType(*args, **kwargs):
	""" Deletes a LDAP entity type configuration data for a specified entity type for a specific LDAP repository. """
	...

def deleteIdMgrLDAPEntityTypeRDNAttr(*args, **kwargs):
	""" Deletes RDN attribute configuration from an LDAP entity type configuration. """
	...

def deleteIdMgrLDAPExternalIdAttr(*args, **kwargs):
	""" Deletes the configuration for an LDAP attribute used as an external ID. """
	...

def deleteIdMgrLDAPGroupConfig(*args, **kwargs):
	""" Deletes the entire LDAP group configuration. """
	...

def deleteIdMgrLDAPGroupDynamicMemberAttr(*args, **kwargs):
	""" Deletes the dynamic member attribute configuration from the LDAP group configuration. """
	...

def deleteIdMgrLDAPGroupMemberAttr(*args, **kwargs):
	""" Deletes the member attribute configuration from the LDAP group configuration. """
	...

def deleteIdMgrLDAPServer(*args, **kwargs):
	""" Deletes the primary LDAP server and configured backup servers. """
	...

def deleteIdMgrPropertyExtensionEntityData(*args, **kwargs):
	""" Deletes the property data from the property extension repository. It also deletes any entity IDs with which there is no property data associated, from the property extension repository in virtual member manager. """
	...

def deleteIdMgrPropertyExtensionRepositoryTables(*args, **kwargs):
	""" Deletes the tables of the property extension database in virtual member manager. """
	...

def deleteIdMgrRealm(*args, **kwargs):
	""" Deletes the specified realm configuration. """
	...

def deleteIdMgrRealmBaseEntry(*args, **kwargs):
	""" Deletes a base entry from a specified realm configuration. """
	...

def deleteIdMgrRealmDefaultParent(*args, **kwargs):
	""" Deletes the default parent of an entity type for a realm. If * is specified as entityTypeName, default parent mapping for all entity types is deleted. If the realm name is not specified, default realm is used. """
	...

def deleteIdMgrRepository(*args, **kwargs):
	""" Deletes the configuration of the specified repository. """
	...

def deleteIdMgrRepositoryBaseEntry(*args, **kwargs):
	""" Deletes a base entry from the specified repository. """
	...

def deleteIdMgrSupportedEntityType(*args, **kwargs):
	""" Deletes a supported entity type configuration. """
	...

def deleteJAXWSHandler(*args, **kwargs):
	""" Delete a JAX-WS Handler """
	...

def deleteJAXWSHandlerList(*args, **kwargs):
	""" Delete a JAX-WS Handler List """
	...

def deleteJDBCProvider(*args, **kwargs):
	""" Delete a JDBC provider that is used to connect to a relational database for data access. """
	...

def deleteJob(*args, **kwargs):
	""" Deletes a previously submitted job. """
	...

def deleteKeyManager(*args, **kwargs):
	""" Delete a key manager. """
	...

def deleteKeyReference(*args, **kwargs):
	""" Delete an existing Key Reference from a keySet. """
	...

def deleteKeySet(*args, **kwargs):
	""" Delete a key set. """
	...

def deleteKeySetGroup(*args, **kwargs):
	""" Delete a key set group. """
	...

def deleteKeyStore(*args, **kwargs):
	""" Deletes an existing keystore. """
	...

def deleteKrbAuthMechanism(*args, **kwargs):
	""" The KRB5 authentication mechanism security object field in the security configuration file is deleted. """
	...

def deleteLMService(*args, **kwargs):
	""" Use the "deleteLMService" command to delete an existing local mapping service. """
	...

def deleteLMServiceEventPoint(*args, **kwargs):
	""" Use the "deleteLMServiceEventPoint" command to delete a local mapping service event point. """
	...

def deleteManagedNodeGroup(*args, **kwargs):
	""" This command is used to delete a group of managed nodes. (deprecated) """
	...

def deleteManagementScope(*args, **kwargs):
	""" Delete an existing management scope. """
	...

def deleteMemberFromManagedNodeGroup(*args, **kwargs):
	""" This command is used to delete members from a group of managed nodes. (deprecated) """
	...

def deleteMemberFromTargetGroup(*args, **kwargs):
	""" This command is used to delete members from a target group. """
	...

def deleteMigrationReport(*args, **kwargs):
	""" Deletes a Liberty migration report for an application """
	...

def deleteOAuthProvider(*args, **kwargs):
	""" Delete OAuth Provider """
	...

def deletePasswordEncryptionKey(*args, **kwargs):
	""" Deletes an AES encryption key from the keystore file. This command is disabled when the custom KeyManager class is used. """
	...

def deletePolicy(*args, **kwargs):
	""" Delete a policy that matches the provided policy name. """
	...

def deletePolicySet(*args, **kwargs):
	""" The deletePolicySet command deletes the specified policy set. If attachments exist for the policy set, the command returns a failure message. """
	...

def deletePolicySetAttachment(*args, **kwargs):
	""" The deletePolicySetAttachment command removes a policy set attachment. """
	...

def deletePolicyType(*args, **kwargs):
	""" The deletePolicyType command deletes a policy type from a policy set. """
	...

def deleteRemoteCellFromIntelligentManagement(*args, **kwargs):
	""" deleteRemoteCellFromIntellMgmtDesc """
	...

def deleteRoutingPolicyWorkClass(*args, **kwargs):
	""" Use this command to delete a Routing Policy Workclass """
	...

def deleteSAMLIdpPartner(*args, **kwargs):
	""" This command removes the SAML TAI IdP partner from the security configuration. """
	...

def deleteSAMLTAISSO(*args, **kwargs):
	""" This command removes the SAML TAI SSO from the security configuration. """
	...

def deleteSCClientCacheConfigurationCustomProperties(*args, **kwargs):
	""" Delete the Custom property """
	...

def deleteSIBDestination(*args, **kwargs):
	""" Delete bus destination. """
	...

def deleteSIBDestinations(*args, **kwargs):
	""" Delete bus destinations. """
	...

def deleteSIBEngine(*args, **kwargs):
	""" Delete the default engine or named engine from the target bus. """
	...

def deleteSIBForeignBus(*args, **kwargs):
	""" Delete a SIB foreign bus. """
	...

def deleteSIBJMSActivationSpec(*args, **kwargs):
	""" Delete given SIB JMS activation specification. """
	...

def deleteSIBJMSConnectionFactory(*args, **kwargs):
	""" Delete the supplied SIB JMS connection factory. """
	...

def deleteSIBJMSQueue(*args, **kwargs):
	""" Delete the supplied SIB JMS queue. """
	...

def deleteSIBJMSTopic(*args, **kwargs):
	""" Delete the supplied SIB JMS topic. """
	...

def deleteSIBLink(*args, **kwargs):
	""" Delete a SIB link. """
	...

def deleteSIBMQLink(*args, **kwargs):
	""" Delete an WebSphere MQ link. """
	...

def deleteSIBMQLinkReceiverChannel(*args, **kwargs):
	""" This command deletes the Receiver Channel associated with the SIB MQ Link passed in as a target object. """
	...

def deleteSIBMQLinkSenderChannel(*args, **kwargs):
	""" This command deletes the Sender Channel associated with the SIB MQ Link passed in as a target object. """
	...

def deleteSIBMediation(*args, **kwargs):
	""" Delete a mediation. """
	...

def deleteSIBWMQServer(*args, **kwargs):
	""" Delete a named WebSphere MQ server. Also, delete its membership of any buses, and cleanup all associated configuration. """
	...

def deleteSIBWSEndpointListener(*args, **kwargs):
	""" Delete an endpoint listener. """
	...

def deleteSIBWSInboundService(*args, **kwargs):
	""" Delete an inbound service. """
	...

def deleteSIBWSOutboundService(*args, **kwargs):
	""" Delete an outbound service. """
	...

def deleteSIBus(*args, **kwargs):
	""" Delete a named bus, including everything on it. """
	...

def deleteSSLConfig(*args, **kwargs):
	""" Delete an existing SSL configuration. """
	...

def deleteSSLConfigGroup(*args, **kwargs):
	""" Delete a SSLConfig group. """
	...

def deleteSSLConfigProperty(*args, **kwargs):
	""" Delete a SSLConfig Property. """
	...

def deleteSTSProperty(*args, **kwargs):
	""" Remove a configuration property under a configuration group. """
	...

def deleteSTSTokenTypeConfigurationCustomProperties(*args, **kwargs):
	""" Delete custom properties from the configuration of a token type. """
	...

def deleteSecurityDomain(*args, **kwargs):
	""" Deletes a domain object. """
	...

def deleteServer(*args, **kwargs):
	""" Delete a server configuration """
	...

def deleteServerTemplate(*args, **kwargs):
	""" A command that Deletes a Server Template """
	...

def deleteServicePolicyWorkClass(*args, **kwargs):
	""" Use this command to delete a Service Policy Workclass """
	...

def deleteSignerCertificate(*args, **kwargs):
	""" Delete a signer certificate from a keystore. """
	...

def deleteSpnegoFilter(*args, **kwargs):
	""" This command removes SPNEGO Web authentication Filter from the security configuration. If a host name is not specified, all the SPNEGO Web authentication Filters are removed. """
	...

def deleteSpnegoTAIProperties(*args, **kwargs):
	""" This command removes SPNEGO TAI properties from the security configuration. If an spnId is not specified, all the SPNEGO TAI properties are removed. """
	...

def deleteTADataCollection(*args, **kwargs):
	""" This command deletes the previously generated Transformation Advisor data collection. """
	...

def deleteTargetGroup(*args, **kwargs):
	""" This command is used to delete a group of targets. """
	...

def deleteTrustManager(*args, **kwargs):
	""" Delete a trust manager. """
	...

def deleteUser(*args, **kwargs):
	""" Deletes a PersonAccount from the default realm. """
	...

def deleteWMQActivationSpec(*args, **kwargs):
	""" Deletes the IBM MQ Activation Specification object provided to the command. """
	...

def deleteWMQConnectionFactory(*args, **kwargs):
	""" Deletes the IBM MQ Connection Factory object provided to the command. """
	...

def deleteWMQQueue(*args, **kwargs):
	""" Deletes the IBM MQ Queue object provided to the command. """
	...

def deleteWMQTopic(*args, **kwargs):
	""" Deletes the IBM MQ Topic object provided to the command. """
	...

def deleteWSCertExpMonitor(*args, **kwargs):
	""" Specifies the certificate expiration monitor name. """
	...

def deleteWSGWGatewayService(*args, **kwargs):
	""" deleteWSGWGatewayService.description """
	...

def deleteWSGWInstance(*args, **kwargs):
	""" deleteWSGWInstance.description """
	...

def deleteWSGWProxyService(*args, **kwargs):
	""" deleteWSGWProxyService.description """
	...

def deleteWSNAdministeredSubscriber(*args, **kwargs):
	""" Remove an administered subscriber from a WS-Notification service point """
	...

def deleteWSNService(*args, **kwargs):
	""" Delete a WS-Notification service """
	...

def deleteWSNServicePoint(*args, **kwargs):
	""" Delete a WS-Notification service point """
	...

def deleteWSNTopicDocument(*args, **kwargs):
	""" Remove an instance document from a WS-Notification topic namespace """
	...

def deleteWSNTopicNamespace(*args, **kwargs):
	""" Delete a WS-Notification topic namespace """
	...

def deleteWSNotifier(*args, **kwargs):
	""" Delete an existing notifier. """
	...

def deleteWSSDistributedCacheConfigCustomProperties(*args, **kwargs):
	""" Remove Web Services Security distributed cache custom properties """
	...

def deleteWSSchedule(*args, **kwargs):
	""" Delete an existing schedule. """
	...

def deleteWebModuleProxyConfig(*args, **kwargs):
	""" Delete the proxy server configuration for a Web module """
	...

def deleteWebServer(*args, **kwargs):
	""" Delete a server configuration """
	...

def deployWasCEApp(*args, **kwargs):
	""" Use this command to deploy a WAS CE application onto a server. """
	...

def detachServiceMap(*args, **kwargs):
	""" Use the "detachServiceMap" command to detach a service map from a local mapping service. """
	...

def disableAudit(*args, **kwargs):
	""" Disables Security Auditing and resets the auditEnabled field in audit.xml. """
	...

def disableAuditEncryption(*args, **kwargs):
	""" Disables audit encryption. """
	...

def disableAuditFilter(*args, **kwargs):
	""" Disables the Audit Specification. """
	...

def disableAuditSigning(*args, **kwargs):
	""" Disables audit signing. """
	...

def disableIntelligentManagement(*args, **kwargs):
	""" Command to disable Intelligent Management """
	...

def disableLMServiceEventPoint(*args, **kwargs):
	""" Use the "disableLMServiceEventPoint" command to disable a local mapping service event point, in order to stop generation of service mapping events. """
	...

def disablePasswordEncryption(*args, **kwargs):
	""" Disables the configuration of the password encryption. As a result, the values of xor or custom are used for the encryption algorithm. """
	...

def disableProvisioning(*args, **kwargs):
	""" Disable provisioning on a server. All components will be started. """
	...

def disableServerPort(*args, **kwargs):
	""" Disable all the transport chains associated with an endpoint on a server. Returns a list of all the disabled transport chains on successful execution of the command. """
	...

def disableVerboseAudit(*args, **kwargs):
	""" Disables the verbose gathering of audit data. """
	...

def disconnectSIBWSEndpointListener(*args, **kwargs):
	""" Disconnect an endpoint listener from a service integration bus. """
	...

def displayJaspiProvider(*args, **kwargs):
	""" Display configuration data for the given authentication provider(s). """
	...

def displayJaspiProviderNames(*args, **kwargs):
	""" Display the names of all authentication providers in the security configuration. """
	...

def doesCoreGroupExist(*args, **kwargs):
	""" Check to see if a core group exists. """
	...

def dpAddAppliance(*args, **kwargs):
	""" Use the dpAddAppliance command to add an appliance to the DataPower appliance manager. """
	...

def dpAddFirmwareVersion(*args, **kwargs):
	""" Use the dpAddFirmwareVersion command to add a firmware version to the DataPower appliance manager. """
	...

def dpAddManagedSet(*args, **kwargs):
	""" Use the dpAddManagedSet command to add a managed set to the DataPower appliance manager. """
	...

def dpCopyMSDomainVersion(*args, **kwargs):
	""" Use the dpCopyMSDomainVersion command to copy a DataPower appliance manager managed domain version to a new managed set. """
	...

def dpCopyMSSettingsVersion(*args, **kwargs):
	""" Use the dpCopyMSSettingsVersion command to copy a DataPower appliance manager managed settings version to a new managed set. """
	...

def dpExport(*args, **kwargs):
	""" Use the dpExport command to export the DataPower appliance manager configuration and versions. """
	...

def dpGetAllApplianceIds(*args, **kwargs):
	""" Use the dpGetAllApplianceIds command to get the IDs of each appliance in the DataPower appliance manager. """
	...

def dpGetAllDomainNames(*args, **kwargs):
	""" Use the dpGetAllDomainNames command to get the names of each of the domains on a DataPower appliance. """
	...

def dpGetAllFirmwareIds(*args, **kwargs):
	""" Use the dpGetAllFirmwareIds command to get the IDs of each DataPower appliance manager firmware in the configuration. """
	...

def dpGetAllFirmwareVersionIds(*args, **kwargs):
	""" Use the dpGetAllFirmwareVersionIds command to get the IDs of each DataPower appliance manager firmware version. """
	...

def dpGetAllMSApplianceIds(*args, **kwargs):
	""" Use the dpGetAllMSApplianceIds command to get the IDs of each appliance in a DataPower appliance manager managed set. """
	...

def dpGetAllMSDomainIds(*args, **kwargs):
	""" Use the dpGetAllMSDomainIds command to get the IDs of each domain in a DataPower appliance manager managed set. """
	...

def dpGetAllMSDomainVersionIds(*args, **kwargs):
	""" Use the dpGetAllMSDomainVersionIds command to get the IDs of each domain version in a DataPower appliance manager managed set. """
	...

def dpGetAllMSIdsUsingFirmwareVersion(*args, **kwargs):
	""" Use the dpGetAllMSIdsUsingFirmwareVersion command to get the IDs of the managed sets that use a firmware version. """
	...

def dpGetAllMSSettingsVersionIds(*args, **kwargs):
	""" Use the dpGetAllMSSettingsVersionIds command to get the IDs of each settings version in a DataPower appliance manager managed set. """
	...

def dpGetAllManagedSetIds(*args, **kwargs):
	""" Use the dpGetAllManagedSetIds command to get the IDs of each DataPower appliance manager managed set. """
	...

def dpGetAllTaskIds(*args, **kwargs):
	""" Use the dpGetAllTaskIDs command to get the IDs of each of the DataPower appliance manager tasks. """
	...

def dpGetAppliance(*args, **kwargs):
	""" Use the dpGetAppliance command to get a specific appliance in the DataPower appliance manager. """
	...

def dpGetBestFirmware(*args, **kwargs):
	""" Use the dpGetBestFirmware command to get the firmware that best matches the parameters. """
	...

def dpGetFirmware(*args, **kwargs):
	""" Use the dpGetFirmware command to get a specific DataPower appliance manager firmware. """
	...

def dpGetFirmwareVersion(*args, **kwargs):
	""" Use the dpGetFirmwareVersion command to get a specific DataPower appliance manager firmware version. """
	...

def dpGetMSDomain(*args, **kwargs):
	""" Use the dpGetMSDomain command to get a DataPower appliance manager managed domain. """
	...

def dpGetMSDomainVersion(*args, **kwargs):
	""" Use the dpGetMSDomainVersion command to get a DataPower appliance manager managed domain version. """
	...

def dpGetMSSettings(*args, **kwargs):
	""" Use the dpGetMSSettings command to get the DataPower appliance manager managed settings. """
	...

def dpGetMSSettingsVersion(*args, **kwargs):
	""" Use the dpGetMSSettingsVersion command to get a DataPower appliance manager managed settings version. """
	...

def dpGetManagedSet(*args, **kwargs):
	""" Use the dpGetManagedSet comand to get a DataPower appliance manager managed set. """
	...

def dpGetManager(*args, **kwargs):
	""" Use the dpGetManager command to get the properties of the DataPower appliance manager. """
	...

def dpGetManagerStatus(*args, **kwargs):
	""" Use the dpGetManagerStatus command to get the status of the DataPower appliance manager. """
	...

def dpGetTask(*args, **kwargs):
	""" Use the dpGetTask command to get a specific DataPower appliance manager task. """
	...

def dpImport(*args, **kwargs):
	""" Use the dpImport command to import the DataPower appliance manager configuration and versions. """
	...

def dpManageAppliance(*args, **kwargs):
	""" Use the dpManageAppliance command to add the appliance to a managed set and to start managing the appliance. """
	...

def dpManageDomain(*args, **kwargs):
	""" Use the dpManageDomain command to add the domain to a managed set, and to start managing the domain. """
	...

def dpPurgeTask(*args, **kwargs):
	""" Use the dpPurgeTask command to purge a DataPower appliance manager task. """
	...

def dpRemoveAppliance(*args, **kwargs):
	""" Use the dpRemoveAppliance command to remove an appliance from the DataPower appliance manager. """
	...

def dpRemoveFirmwareVersion(*args, **kwargs):
	""" Use the dpRemoveFirmwareVersion command to remove a firmware version from the DataPower appliance manager. """
	...

def dpRemoveMSDomainVersion(*args, **kwargs):
	""" Use the dpRemoveMSDomainVersion command to remove a managed domain version from the DataPower appliance manager. """
	...

def dpRemoveMSSettingsVersion(*args, **kwargs):
	""" Use the dpRemoveMSSettingsVersion command to remove a managed settings version from the DataPower appliance manager. """
	...

def dpRemoveManagedSet(*args, **kwargs):
	""" Use the dpRemoveManagedSet command to remove a managed set from the DataPower appliance manager. """
	...

def dpSetAppliance(*args, **kwargs):
	""" Use the dpSetAppliance command to modify an appliance in the DataPower appliance manager. """
	...

def dpSetFirmwareVersion(*args, **kwargs):
	""" Use the dpSetFirmwareVersion command to modify a DataPower appliance manager firmware version. """
	...

def dpSetMSDomain(*args, **kwargs):
	""" Use the dpSetMSDomain command to modify a DataPower appliance manager managed domain. """
	...

def dpSetMSDomainVersion(*args, **kwargs):
	""" Use the dpSetMSDomainVersion command to modify a DataPower appliance manager managed domain version. """
	...

def dpSetMSSettings(*args, **kwargs):
	""" Use the dpSetMSSettings command to modify the DataPower appliance manager managed settings. """
	...

def dpSetMSSettingsVersion(*args, **kwargs):
	""" Use the dpSetMSSettingsVersion command to modify a DataPower appliance manager managed settings version. """
	...

def dpSetManagedSet(*args, **kwargs):
	""" Use the dpSetManagedSet command to modify a DataPower appliance manager managed set. """
	...

def dpSetManager(*args, **kwargs):
	""" Use the dpSetManager command to modify the DataPower appliance manager. """
	...

def dpStopManager(*args, **kwargs):
	""" Use the dpStopManager command to stop the DataPower appliance manager. """
	...

def dpSynchManagedSet(*args, **kwargs):
	""" Use the dpSynchManagedSet command to manually synchronize a DataPower appliance manager managed set. """
	...

def dpUnmanageAppliance(*args, **kwargs):
	""" Use the dpUnmanageAppliance command to remove the appliance of interest from its managed set, and to stop managing the appliance. """
	...

def dpUnmanageDomain(*args, **kwargs):
	""" Use the dpUnmanageDomain command to remove the domain from the managed set, and to stop managing the domain. """
	...

def duplicateMembershipOfGroup(*args, **kwargs):
	""" Makes a group a member of the same groups as another group. """
	...

def duplicateMembershipOfUser(*args, **kwargs):
	""" Makes a user a member of the same groups as another user. """
	...

def editAsset(*args, **kwargs):
	""" Edit options specified when a specified asset was imported. """
	...

def editBLA(*args, **kwargs):
	""" Edit options for a specified business-level application. """
	...

def editCompUnit(*args, **kwargs):
	""" Edit options for a specified composition unit. """
	...

def editSTSProperty(*args, **kwargs):
	""" Edit a configuration property under a configuration group. """
	...

def enableAudit(*args, **kwargs):
	""" Enables Security Auditing and sets the auditEnabled field in audit.xml. """
	...

def enableAuditEncryption(*args, **kwargs):
	""" Enables audit encryption. """
	...

def enableAuditFilter(*args, **kwargs):
	""" Enables the Audit Specification. """
	...

def enableAuditSigning(*args, **kwargs):
	""" Enables audit signing. """
	...

def enableFips(*args, **kwargs):
	""" Enables and disables a specified FIPS security level. """
	...

def enableIntelligentManagement(*args, **kwargs):
	""" Command to enable Intelligent Management """
	...

def enableLMServiceEventPoint(*args, **kwargs):
	""" Use the "enableLMServiceEventPoint" command to enable a local mapping service event point, in order to generate service mapping events. """
	...

def enableOAuthTAI(*args, **kwargs):
	""" Enable OAuth TAI """
	...

def enablePasswordEncryption(*args, **kwargs):
	""" Generates and configures the key file and passwordUtil.properties file, both of which are required for AES password encryption. """
	...

def enableProvisioning(*args, **kwargs):
	""" Enable provisioning on a server. Some components will be started as they are needed. """
	...

def enableVerboseAudit(*args, **kwargs):
	""" Enables the verbose gathering of audit data. """
	...

def enableWritableKeyrings(*args, **kwargs):
	""" Modify keystore for writable SAF support.  This task is used during the migration process and will create additional writable keystore objects for the control region and servant region keyrings for SSL keystores. """
	...

def exchangeSigners(*args, **kwargs):
	""" Exchange Signer Certificates """
	...

def executeElasticityAction(*args, **kwargs):
	""" Command to execute a elasticity action """
	...

def executeHealthAction(*args, **kwargs):
	""" Command to execute a health action """
	...

def executeMiddlewareServerOperation(*args, **kwargs):
	""" Use this command to execute an operation on a middleware server """
	...

def exportAsset(*args, **kwargs):
	""" Export an asset which has been imported into the product configuration repository.  Only the asset file itself is exported.  No import options for the asset are exported. """
	...

def exportAuditCertToManagedKS(*args, **kwargs):
	""" Exports a personal certificate from a managed key to another managed key store. """
	...

def exportAuditCertificate(*args, **kwargs):
	""" Export a certificate to another KeyStore. """
	...

def exportBinding(*args, **kwargs):
	""" The exportBinding command exports a binding as an archive that can be copied onto a client environment or imported onto a server environment. """
	...

def exportCertToManagedKS(*args, **kwargs):
	""" Export a personal certificate to a managed keystore in the configuration. """
	...

def exportCertificate(*args, **kwargs):
	""" Export a certificate to another KeyStore. """
	...

def exportCompositeToDomain(*args, **kwargs):
	""" Exports composites under specified domain """
	...

def exportDeploymentManifest(*args, **kwargs):
	""" Export the deployment manifest from an EBA asset. """
	...

def exportLTPAKeys(*args, **kwargs):
	""" Exports Lightweight Third Party Authentication keys to a file. """
	...

def exportMiddlewareApp(*args, **kwargs):
	""" Use this command to export a middleware application to a directory. """
	...

def exportMiddlewareAppScript(*args, **kwargs):
	""" Use this command to export middleware application scripts to a directory. """
	...

def exportOAuthProps(*args, **kwargs):
	""" Get OAuth Configuration to edit """
	...

def exportPolicySet(*args, **kwargs):
	""" The exportPolicySet command exports a policy set as an archive that can be copied onto a client environment or imported onto a server environment. """
	...

def exportProxyProfile(*args, **kwargs):
	""" export the configuration of a wsprofile to a config archive. """
	...

def exportProxyServer(*args, **kwargs):
	""" export the configuration of a server to a config archive. """
	...

def exportSAMLSpMetadata(*args, **kwargs):
	""" This command exports the security configuration SAML TAI SP metadata to a file. """
	...

def exportSCDL(*args, **kwargs):
	""" Export the SCA SCDL """
	...

def exportServer(*args, **kwargs):
	""" export the configuration of a server to a config archive. """
	...

def exportTunnelTemplate(*args, **kwargs):
	""" Export a tunnel template and its children into a simple properties file. """
	...

def exportWSDLArtifacts(*args, **kwargs):
	""" Export WSDL and XSD documents for a specific Composition Unit """
	...

def exportWasprofile(*args, **kwargs):
	""" export the configuration of a wsprofile to a config archive. """
	...

def extractCertificate(*args, **kwargs):
	""" extract a signer certificate to a file. """
	...

def extractCertificateRequest(*args, **kwargs):
	""" Extract a certificate request to a file. """
	...

def extractConfigProperties(*args, **kwargs):
	""" Extracts configuration of the object specified by ConfigId or ConfigData parameter to a specified properies file. Either ConfigId or ConfigData parameter should be specified, but not both. ConfigId parameter should be in the form that is returned by "AdminConfig list configType". Example of ConfigId is cellName(cells/cellName|cell.xml#Cell_1). ConfigData parameter should be in the form of configType=value[:configType=value]*. Examples of configData are Deployment=appName or Node=nodeName:Server=serverName. """
	...

def extractRepositoryCheckpoint(*args, **kwargs):
	""" Extract the repository checkpoint specified by the "checkpointName" to the file specified by the "extractToFile". """
	...

def extractSignerCertificate(*args, **kwargs):
	""" Extract a signer certificate from a keystore. """
	...

def findOtherRAsToUpdate(*args, **kwargs):
	""" Find other Resource Adapters that are copies of the entered Resource Adapter.  Since an update will replace binary files, these copies of the Resource Adapter should be updated after the current Resource Adapter is updated. """
	...

def genAndReplaceCertificates(*args, **kwargs):
	""" Generates a new certificate with new specification options that replaces existing certificates as specified by the parameter configuration. """
	...

def generateKeyForKeySet(*args, **kwargs):
	""" Generate all the keys in a KeySet. """
	...

def generateKeyForKeySetGroup(*args, **kwargs):
	""" Generate new keys for all the keys within a keySet Group. """
	...

def generateSecConfigReport(*args, **kwargs):
	""" Generates the Security Configuration report. """
	...

def generateTemplates(*args, **kwargs):
	""" Generates new set of templates by combining WebSphere Application Server base product templates with feature pack and/or stack product templates """
	...

def getAccessIdFromServerId(*args, **kwargs):
	""" Returns the access ID for the registry server ID. """
	...

def getActiveSecuritySettings(*args, **kwargs):
	""" Gets the active security setting for global security or in a security domain. """
	...

def getAllCoreGroupNames(*args, **kwargs):
	""" Get the names of all core groups """
	...

def getAuditCertificate(*args, **kwargs):
	""" Get information about a personal certificate. """
	...

def getAuditEmitter(*args, **kwargs):
	""" Returns an audit emitter implementation object. """
	...

def getAuditEmitterFilters(*args, **kwargs):
	""" Returns a list of defined filters for the supplied emitter in shortened format. """
	...

def getAuditEncryptionConfig(*args, **kwargs):
	""" Returns the audit record encryption configuration. """
	...

def getAuditEventFactory(*args, **kwargs):
	""" Returns the object of the supplied event factory. """
	...

def getAuditEventFactoryClass(*args, **kwargs):
	""" Returns the class name for the supplied event factory. """
	...

def getAuditEventFactoryFilters(*args, **kwargs):
	""" Returns a list of defined filters for the supplied event factory in shortened format. """
	...

def getAuditEventFactoryName(*args, **kwargs):
	""" Returns the unique name for the supplied event factory. """
	...

def getAuditEventFactoryProvider(*args, **kwargs):
	""" Returns the configured audit service provider for the supplied event factory. """
	...

def getAuditFilter(*args, **kwargs):
	""" Returns an audit specification entry in the audit.xml that matches the reference Id. """
	...

def getAuditKeyStoreInfo(*args, **kwargs):
	""" Shows information about a particular key store. """
	...

def getAuditNotification(*args, **kwargs):
	""" Returns an audit notification. """
	...

def getAuditNotificationMonitor(*args, **kwargs):
	""" Returns the audit notification monitor specified by the reference id. """
	...

def getAuditNotificationName(*args, **kwargs):
	""" Returns the name of the configured audit notification. """
	...

def getAuditNotificationRef(*args, **kwargs):
	""" Returns the reference id of the configured audit notification. """
	...

def getAuditOutcomes(*args, **kwargs):
	""" Returns the audit outcomes defined for an event. """
	...

def getAuditPolicy(*args, **kwargs):
	""" Returns the audit policy attributes. """
	...

def getAuditSigningConfig(*args, **kwargs):
	""" Returns the audit record signing configuration. """
	...

def getAuditSystemFailureAction(*args, **kwargs):
	""" Returns the audit system failure policy. """
	...

def getAuditorId(*args, **kwargs):
	""" Gets the auditor identity defined in the audit.xml file. """
	...

def getAuthDataEntry(*args, **kwargs):
	""" Return information about an authentication data entry """
	...

def getAuthzConfigInfo(*args, **kwargs):
	""" Return information about an external JAAC authorization provider. """
	...

def getAutoCheckpointDepth(*args, **kwargs):
	""" Get the depth of the automatic checkpoints """
	...

def getAutoCheckpointEnabled(*args, **kwargs):
	""" Get the automatic checkpoints enabled attribute value """
	...

def getAvailableSDKsOnNode(*args, **kwargs):
	""" Returns a list of names for the SDKs on a given node. """
	...

def getBLAStatus(*args, **kwargs):
	""" Determine whether a business-level application or composition unit is running or stopped. """
	...

def getBinaryFileLocation(*args, **kwargs):
	""" Returns the file location of the Binary audit log. """
	...

def getBinaryFileSize(*args, **kwargs):
	""" Returns the file size of the Binary audit log. """
	...

def getBinding(*args, **kwargs):
	""" The getBinding command returns the binding configuration for a specified policy type and scope. """
	...

def getCAClient(*args, **kwargs):
	""" Gets information about a certificate authority (CA) client configurator object. """
	...

def getCSIInboundInfo(*args, **kwargs):
	""" Returns the CSI inbound information for global security or in a security domain. """
	...

def getCSIOutboundInfo(*args, **kwargs):
	""" Returns the CSI outbound information for global security or in a security domain. """
	...

def getCertificate(*args, **kwargs):
	""" Get information about a personal certificate. """
	...

def getCertificateChain(*args, **kwargs):
	""" Gets information about each certificate in a certificate chain. """
	...

def getCertificateRequest(*args, **kwargs):
	""" Get information about a certificate request """
	...

def getCheckpointLocation(*args, **kwargs):
	""" Get the directory path where the checkpoints are stored """
	...

def getClientDynamicPolicyControl(*args, **kwargs):
	""" The getClientDynamicPolicyControl command returns the WSPolicy client acquisition information for a specified application or resource. """
	...

def getConfigRepositoryLocation(*args, **kwargs):
	""" Get the directory path where the configuration repository is stored """
	...

def getContexts(*args, **kwargs):
	""" getContextDesc """
	...

def getCoreGroupNameForServer(*args, **kwargs):
	""" Get the name of the core group the server is a member of. """
	...

def getCurrentWizardSettings(*args, **kwargs):
	""" Gets current security wizard settings from the workspace. """
	...

def getDefaultBindings(*args, **kwargs):
	""" The getDefaultBindings command returns the default binding names for a specified domain or server. """
	...

def getDefaultContextService(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultContextService. """
	...

def getDefaultCoreGroupName(*args, **kwargs):
	""" Get the name of the default core group """
	...

def getDefaultDataSource(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultDataSource. """
	...

def getDefaultJMSConnectionFactory(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultJMSConnectionFactory. """
	...

def getDefaultManagedExecutor(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultManagedExecutorService. """
	...

def getDefaultManagedScheduledExecutor(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultManagedScheduledExecutorService. """
	...

def getDefaultManagedThreadFactory(*args, **kwargs):
	""" Get the JNDI name that is bound to java:comp/DefaultManagedThreadFactory. """
	...

def getDescriptiveProp(*args, **kwargs):
	""" Get information about a descriptive property under an object. """
	...

def getDistributedCacheProperty(*args, **kwargs):
	""" queryDistrbitedConfigCmdDesc """
	...

def getDmgrProperties(*args, **kwargs):
	""" Returns the properties of the deployment manager """
	...

def getDynamicClusterIsolationProperties(*args, **kwargs):
	""" Display Dynamic Cluster isolation properties """
	...

def getDynamicClusterMaxInstances(*args, **kwargs):
	""" Get dynamic cluster maximum number of cluster instances """
	...

def getDynamicClusterMaxNodes(*args, **kwargs):
	""" Get dynamic cluster maximum number of cluster nodes """
	...

def getDynamicClusterMembers(*args, **kwargs):
	""" Get members of specified dynamic cluster and node name.  If node name is not specified, all members of the dynamic cluster are returned. """
	...

def getDynamicClusterMembershipPolicy(*args, **kwargs):
	""" Get dynamic cluster membership policy """
	...

def getDynamicClusterMinInstances(*args, **kwargs):
	""" Get dynamic cluster minimum number of cluster instances """
	...

def getDynamicClusterMinNodes(*args, **kwargs):
	""" Get dynamic cluster minimum number of cluster nodes """
	...

def getDynamicClusterOperationalMode(*args, **kwargs):
	""" Get dynamic cluster operational mode """
	...

def getDynamicClusterServerIndexTemplateId(*args, **kwargs):
	""" Get the configuration ID of the specified dynamic cluster's ServerIndex template object. """
	...

def getDynamicClusterServerType(*args, **kwargs):
	""" Get dynamic cluster server type """
	...

def getDynamicClusterVerticalInstances(*args, **kwargs):
	""" Get dynamic cluster vertical stacking of instances on node """
	...

def getDynamicSSLConfigSelection(*args, **kwargs):
	""" Get information about a Dynamic SSL configuration selection. """
	...

def getEditionState(*args, **kwargs):
	""" Provides the state of an application edition. """
	...

def getEmailList(*args, **kwargs):
	""" Returns the notification email list for the configured audit notification. """
	...

def getEmitterClass(*args, **kwargs):
	""" Returns the class name associated with the supplied emitter reference. """
	...

def getEmitterUniqueId(*args, **kwargs):
	""" Returns the unique ID associated with the supplied emitter reference. """
	...

def getEncryptionKeyStore(*args, **kwargs):
	""" Returns the keystore containing the certificate used to encrypt the audit records. """
	...

def getEventFormatterClass(*args, **kwargs):
	""" Returns the class name of the event formatter associated with the audit service provider reference. """
	...

def getFipsInfo(*args, **kwargs):
	""" Returns information about the FIPS settings in the current WebSphere configuration.  It will print out whether the FIPS is enabled or not and if it is, then what level FIPS setting is enabled. If suite B is enabled, the level of suite B is also returned. """
	...

def getGroup(*args, **kwargs):
	""" Retrieves the attributes of a group. """
	...

def getIdMgrDefaultRealm(*args, **kwargs):
	""" Returns the name of the default realm. """
	...

def getIdMgrEntityTypeSchema(*args, **kwargs):
	""" Retrieves the schema of an entity type. If repository ID is not specified then it returns the default entity type schema supported by virtual member manager. If entity type names are not specified then it retrieves the entity type schema for all the entity types. """
	...

def getIdMgrLDAPAttrCache(*args, **kwargs):
	""" Returns the LDAP attribute cache configuration. """
	...

def getIdMgrLDAPContextPool(*args, **kwargs):
	""" Returns LDAP context pool configuration. """
	...

def getIdMgrLDAPEntityType(*args, **kwargs):
	""" Returns the LDAP entity type configuration data for the specified entity type in the LDAP repository. """
	...

def getIdMgrLDAPEntityTypeRDNAttr(*args, **kwargs):
	""" Returns the RDN attributes configuration of an LDAP entity type configuration. """
	...

def getIdMgrLDAPGroupConfig(*args, **kwargs):
	""" Returns the LDAP group configuration parameters. """
	...

def getIdMgrLDAPGroupDynamicMemberAttrs(*args, **kwargs):
	""" Returns the dynamic member attribute configuration from the LDAP group configuration. """
	...

def getIdMgrLDAPGroupMemberAttrs(*args, **kwargs):
	""" Returns the member attribute configuration from the LDAP group configuration. """
	...

def getIdMgrLDAPSearchResultCache(*args, **kwargs):
	""" Returns the LDAP search result cache configuration. """
	...

def getIdMgrLDAPServer(*args, **kwargs):
	""" Returns all the configured LDAP servers and their configurations. """
	...

def getIdMgrPropertySchema(*args, **kwargs):
	""" Retrieves the property schema of an entity type. If repository ID is not specified then it returns the default property schema supported by virtual member manager. If propertyNames is not specified it returns schema of all the properties. If entity type is not specified then it retrieves the property schema for all entity types. If propertyNames is specified then entityTypeName must be specified. """
	...

def getIdMgrRealm(*args, **kwargs):
	""" Returns the specified realm configuration. """
	...

def getIdMgrRepositoriesForRealm(*args, **kwargs):
	""" Returns repository specific details for the repositories configuration for the specified realm. """
	...

def getIdMgrRepository(*args, **kwargs):
	""" Returns the configuration of the specified repository. """
	...

def getIdMgrSupportedDataTypes(*args, **kwargs):
	""" Retrieves the supported data types. If repository ID is not specified then it returns the default data types supported by virtual member manager. """
	...

def getIdMgrSupportedEntityType(*args, **kwargs):
	""" Returns the configuration of the specified supported entity type. """
	...

def getInheritedSSLConfig(*args, **kwargs):
	""" Returns a string containing the alias of the SSL Configuration and the certificate alias for the specified scope. """
	...

def getJAASLoginEntryInfo(*args, **kwargs):
	""" Get information about a JAAS login entry. """
	...

def getJVMMode(*args, **kwargs):
	""" Get the current JVM mode. The command will return either 31-bit or 64-bit. """
	...

def getJaspiInfo(*args, **kwargs):
	""" Display information about the Jaspi configuration. """
	...

def getJavaHome(*args, **kwargs):
	""" Get the Java Home path. """
	...

def getJobTargetHistory(*args, **kwargs):
	""" This command is used to get the job target history for a job. """
	...

def getJobTargetStatus(*args, **kwargs):
	""" This command is used to get the latest job target status for a job. """
	...

def getJobTargets(*args, **kwargs):
	""" This command is used to get targets for a job.  The targets for the job may have been unregistered, or deleted. """
	...

def getJobTypeMetadata(*args, **kwargs):
	""" This command is used to get the metadata associated with a jobType. """
	...

def getJobTypes(*args, **kwargs):
	""" This command is used to get the supported job types for a managed node. """
	...

def getKeyManager(*args, **kwargs):
	""" Get information about a key manager. """
	...

def getKeyReference(*args, **kwargs):
	""" Get information about a Key Reference in a particular keySet. """
	...

def getKeySet(*args, **kwargs):
	""" Get information about a key set. """
	...

def getKeySetGroup(*args, **kwargs):
	""" Get information about a key set group. """
	...

def getKeyStoreInfo(*args, **kwargs):
	""" Returns information about a particular keystore. """
	...

def getLTPATimeout(*args, **kwargs):
	""" Return the LTPA authentication mechanism timeout from global security or a security domain. """
	...

def getManagedNodeConnectorProperties(*args, **kwargs):
	""" Get connector properties for the managed node """
	...

def getManagedNodeGroupInfo(*args, **kwargs):
	""" Information regarding a group of managed nodes. (deprecated) """
	...

def getManagedNodeGroupMembers(*args, **kwargs):
	""" This command is used to list members of a group of managed nodes. (deprecated) """
	...

def getManagedNodeKeys(*args, **kwargs):
	""" Get properties keys associated with a specific managed node. (deprecated) """
	...

def getManagedNodeProperties(*args, **kwargs):
	""" Get properties associated with a specific managed node. (deprecated) """
	...

def getManagedResourceProperties(*args, **kwargs):
	""" Get properties associated with a specific managed resource. """
	...

def getManagedResourcePropertyKeys(*args, **kwargs):
	""" Get property keys associated with an specific managed resource. """
	...

def getManagedResourceTypes(*args, **kwargs):
	""" Retrieves managed resource types. """
	...

def getManagementScope(*args, **kwargs):
	""" Get information about a management scope. """
	...

def getMaxNumBinaryLogs(*args, **kwargs):
	""" Returns the configured maximum number of Binary audit logs. """
	...

def getMembersOfGroup(*args, **kwargs):
	""" Retrieves the members of a group. """
	...

def getMembershipOfGroup(*args, **kwargs):
	""" Retrieves the groups in which a group is a member. """
	...

def getMembershipOfUser(*args, **kwargs):
	""" Get the groups in which a PersonAccount is a member. """
	...

def getMetadataProperties(*args, **kwargs):
	""" Returns all managed object metadata properties for a given node. """
	...

def getMetadataProperty(*args, **kwargs):
	""" Returns the specified managed object metadata property for agiven node. """
	...

def getMiddlewareServerType(*args, **kwargs):
	""" Use this command to show the server type of a middleware server """
	...

def getMigrationOptions(*args, **kwargs):
	""" Returns the default migration scan options used by the createMigrationReport command """
	...

def getMigrationReport(*args, **kwargs):
	""" Returns the absolute path for an application's Liberty migration report """
	...

def getMigrationSummary(*args, **kwargs):
	""" Returns a summary of a Liberty migration report for an application """
	...

def getNamedTCPEndPoint(*args, **kwargs):
	""" Returns the port associated with the specified bridge interface.  This is the port specified on the TCP inbound channel of transport channel chain for the specified bridge interface. """
	...

def getNewRAObjectProperties(*args, **kwargs):
	""" Returns a string containing all of the property values and step inputs for the updateRAR command. """
	...

def getNodeBaseProductVersion(*args, **kwargs):
	""" Returns the base version for a node, for example, "6.0.0.0". """
	...

def getNodeDefaultSDK(*args, **kwargs):
	""" Query the node's default SDK name and location """
	...

def getNodeMajorVersion(*args, **kwargs):
	""" Returns the major version for a node, for example, "6" for v6.0.0.0. """
	...

def getNodeMinorVersion(*args, **kwargs):
	""" Returns the minor version for a node, for example, "0.0.0" for v6.0.0.0. """
	...

def getNodePlatformOS(*args, **kwargs):
	""" Returns the operating system platform for a given node. """
	...

def getNodeSysplexName(*args, **kwargs):
	""" Returns the operating system platform for a given node.  This valueapplies only to nodes running on the z/OS operating system. """
	...

def getOSGiApplicationDeployedObject(*args, **kwargs):
	""" Returns the deployedObject that represents the configuration of the OSGi application given the name of its composition unit. """
	...

def getOverallJobStatus(*args, **kwargs):
	""" This command is used to get overall status of a job. """
	...

def getPolicySet(*args, **kwargs):
	""" The getPolicySet command returns general attributes, such as description and default indicator, for the specified policy set. """
	...

def getPolicySetAttachments(*args, **kwargs):
	""" The getPolicySetAttachments command lists the properties for all attachments configured for a specified application or for the trust service. """
	...

def getPolicyType(*args, **kwargs):
	""" The getPolicyType command returns the attributes for a specified policy. """
	...

def getPolicyTypeAttribute(*args, **kwargs):
	""" The getPolicyTypeAttribute command returns the value for the specified policy attribute. """
	...

def getPreferences(*args, **kwargs):
	""" Command to get user preferences """
	...

def getProfileKey(*args, **kwargs):
	""" Get the profile key """
	...

def getProviderPolicySharingInfo(*args, **kwargs):
	""" The getProviderPolicySharingInfo command returns the WSPolicy provider sharing information for a specified application or resource. """
	...

def getRSATokenAuthorization(*args, **kwargs):
	""" Returns information in the admin RSA token authorization mechanism object. """
	...

def getRequiredBindingVersion(*args, **kwargs):
	""" The getRequiredBindingVersion command returns the binding version that is required for a specified asset. """
	...

def getRuntimeRegistrationProperties(*args, **kwargs):
	""" Get certain runtime properties pertaining to a device and its registered job manager """
	...

def getSDKPropertiesOnNode(*args, **kwargs):
	""" Returns properties for the SDKs. If the SDK name is not given, all properties for all avaiable SDKs are returned.  If the SDK attributes are specified, only properties for given SDK attributes are returned. """
	...

def getSDKVersion(*args, **kwargs):
	""" Query the SDK version number in use """
	...

def getSSLConfig(*args, **kwargs):
	""" Get information about a particular SSL configuration. """
	...

def getSSLConfigGroup(*args, **kwargs):
	""" Get information about a SSL configuration group. """
	...

def getSSLConfigProperties(*args, **kwargs):
	""" Get SSL Configuration Properties """
	...

def getSecurityDomainForResource(*args, **kwargs):
	""" Returns the security domain that a particular scope belongs to. """
	...

def getSendEmail(*args, **kwargs):
	""" Returns the state of the sendEmail audit notification. """
	...

def getServerSDK(*args, **kwargs):
	""" Query the server's SDK name and location """
	...

def getServerSecurityLevel(*args, **kwargs):
	""" Get the current security level of the secure proxy server. """
	...

def getServerType(*args, **kwargs):
	""" returns the server type of the specified server. """
	...

def getSignerCertificate(*args, **kwargs):
	""" Get information about a signer Certificate. """
	...

def getSingleSignon(*args, **kwargs):
	""" Returns information about the single signon settings for global security. """
	...

def getSupportedAuditEvents(*args, **kwargs):
	""" Returns all supported audit events. """
	...

def getSupportedAuditOutcomes(*args, **kwargs):
	""" Returns all supported audit outcomes. """
	...

def getTADataCollectionSummary(*args, **kwargs):
	""" This command returns a summary of the Transformation Advisor data collection status. """
	...

# --------------------------------------------------------------------------
@overload
def getTCPEndPoint(options: Literal['-interactive'], /) -> Any:
    ...

@overload
def getTCPEndPoint(target_object: ConfigurationObjectName, /) -> ConfigurationObjectName:
    ...

@overload
def getTCPEndPoint(target_object: ConfigurationObjectName, options: Union[str, list], /) -> ConfigurationObjectName:
    ...

def getTCPEndPoint(target_object: ConfigurationObjectName, options: Union[str, list], /) -> ConfigurationObjectName: # type: ignore[misc]
    """Get the NamedEndPoint associated with either a TCPInboundChannel, or a chain that contains a TCPInboundChannel.

    - If `target_object` is set to a string with value `"-interactive"`, the endpoint will 
        be retrieved in _interactive mode_.

    Args:
        target_object (ConfigurationObjectName | Literal['-interactive']): The TCPInboundChannel, or containing chain, instance that is associated with a NamedEndPoint. 

    Returns:
        ConfigurationObjectName: The object name of an existing named end point that is associated with the TCP inbound channel instance or a channel chain.
    
    Example:
        ```pycon
        >>> target = 'TCP_1(cells/mybuildCell01/nodes/mybuildCellManager01/servers/dmgr|server.xml#TCPInboundChannel_1)'
        >>> AdminTask.getTCPEndPoint(target)
        ```
    """
    ...
# --------------------------------------------------------------------------

def getTargetGroupInfo(*args, **kwargs):
	""" Information regarding a group of Targets. """
	...

def getTargetGroupMembers(*args, **kwargs):
	""" This command is used to list members of a target group. """
	...

def getTargetKeys(*args, **kwargs):
	""" Get properties keys associated with a specific Target. """
	...

def getTargetProperties(*args, **kwargs):
	""" Get properties associated with a specific Target. """
	...

def getTrustAssociationInfo(*args, **kwargs):
	""" Get information about a trust association. """
	...

def getTrustManager(*args, **kwargs):
	""" Get information about a trust manager. """
	...

def getUDPEndPoint(*args, **kwargs):
	""" Get the NamedEndPoint endpoint that is associated with either a UDPInboundChannel, or a chain that contains a UDPInboundChannel """
	...

def getUnusedSDKsOnNode(*args, **kwargs):
	""" Query unused SDKs on the node """
	...

def getUser(*args, **kwargs):
	""" Retrieves the attributes of a PersonAccount. """
	...

def getUserRegistryInfo(*args, **kwargs):
	""" Returns information about a user registry from the administrative security configuration or an application security domain. """
	...

def getWSCertExpMonitor(*args, **kwargs):
	""" Get information about a certificate expiration monitor. """
	...

def getWSN_SIBWSInboundPort(*args, **kwargs):
    """ Retrieve one of the service integration bus inbound ports from a WS-Notification service point. """
    ...

def getWSN_SIBWSInboundService(*args, **kwargs):
    """ Retrieve one of the service integration bus inbound services from a WS-Notification service. """
    ...

def getWSNotifier(*args, **kwargs):
	""" Get information about a notifier. """
	...

def getWSSchedule(*args, **kwargs):
	""" Get schedule information. """
	...

def getWebService(*args, **kwargs):
	""" Gets the attributes for a Web service in an enterprise application. """
	...

def healthRestartAction(*args, **kwargs):
	""" restarts the sick server """
	...

# --------------------------------------------------------------------------
def help(search_query: str = "", /) -> str:
    """The number of admin commands varies and depends on your WebSphere
    install. Use the following help commands to obtain a list of supported
    commands and their parameters:

    - `AdminTask.help("-commands")`                  list all the admin commands
    - `AdminTask.help("-commands <pattern>")`        list admin commands matching with wildcard "pattern"
    - `AdminTask.help("-commandGroups")`             list all the admin command groups
    - `AdminTask.help("-commandGroups <pattern>")`   list admin command groups matching with wildcard "pattern"
    - `AdminTask.help("commandName")`                display detailed information for the specified command
    - `AdminTask.help("commandName stepName")`       display detailed information for the specified step belonging to the specified command
    - `AdminTask.help("commandGroupName")`           display detailed information for the specified command group


    Args:
        search_query (str, optional): Pass a query to filter the desired results. Defaults to "".

    Returns:
        str: The detailed help string
    
    Example:
        ```pycon
        >>> print (AdminTask.help("createTCPEndPoint"))
        WASX8006I: Detailed help for command: createTCPEndPoint
        Description: Create a new NamedEndPoint that can be associated with a TCPInboundChannel
        [...]
        ```
    """
    ...
# --------------------------------------------------------------------------

def importApplicationsFromWasprofile(*args, **kwargs):
	""" Import the applications from a configuration archive file to a sepcified application server target. """
	...

def importAsset(*args, **kwargs):
	""" Import an application file into the product configuration repository as an asset. """
	...

def importAuditCertFromManagedKS(*args, **kwargs):
	""" Imports a personal certificate from another managed key store. """
	...

def importAuditCertificate(*args, **kwargs):
	""" Import a Certificate from another keyStore to this KeyStore. """
	...

def importBinding(*args, **kwargs):
	""" The importBinding command imports a binding from a compressed archive onto a server environment. """
	...

def importCertFromManagedKS(*args, **kwargs):
	""" Import a personal certificate from managed keystore in the configuration. """
	...

def importCertificate(*args, **kwargs):
	""" port a Certificate from another keystore to this keystore. """
	...

def importDeploymentManifest(*args, **kwargs):
	""" Import the deployment manifest into the EBA asset. If the deployment manifest is resolved successfully, it will replace the existing deployment manifest in the asset. """
	...

def importEncryptionCertificate(*args, **kwargs):
	""" Import a Certificate from another keyStore to this KeyStore. """
	...

def importLTPAKeys(*args, **kwargs):
	""" Imports Lightweight Third Party Authentication keys into the configuration. """
	...

def importOAuthProps(*args, **kwargs):
	""" Import OAuth Configuration After Export """
	...

def importPolicySet(*args, **kwargs):
	""" The importPolicySet command imports a policy set from a compressed archive onto a server environment. """
	...

def importProxyProfile(*args, **kwargs):
	""" Import a Secure Proxy Profile into this cell. """
	...

def importProxyServer(*args, **kwargs):
	""" Import a Secure Proxy Server into a given Secure Proxy node. """
	...

def importSAMLIdpMetadata(*args, **kwargs):
	""" This command imports SAML IdP metadata to the security configuration SAML TAI. """
	...

def importServer(*args, **kwargs):
	""" Import a server configuration from a configuration archive. This command creates a new server based on the server configuration defined in the archive. """
	...

def importTunnelTemplate(*args, **kwargs):
	""" Import a tunnel template and its children into the cell-scoped config. """
	...

def importWasprofile(*args, **kwargs):
	""" Import the configuration of a wasprofile profile from a configuration archive. This command overwrites the configuration of the current wasprofile configuration. """
	...

def inspectServiceMapLibrary(*args, **kwargs):
	""" Use the "inspectServiceMapLibrary" command to display details about the service maps within a service map library. """
	...

def installPHPApp(*args, **kwargs):
	""" Use this command to install a PHP application. """
	...

def installResourceAdapter(*args, **kwargs):
	""" Install a J2C resource adapter """
	...

def installServiceMap(*args, **kwargs):
	""" Use the "installServiceMap" command to install a service map in a service map library. """
	...

def installWasCEApp(*args, **kwargs):
	""" Use this command to install a WAS CE application. """
	...

def isAdminLockedOut(*args, **kwargs):
	""" Checks to make sure that at least one admin user in the admin-authz.xml file exists in the input user registry. """
	...

def isAppSecurityEnabled(*args, **kwargs):
	""" Returns the current Application Security setting of true or false. """
	...

def isAuditEnabled(*args, **kwargs):
	""" Returns the state of Security Auditing. """
	...

def isAuditEncryptionEnabled(*args, **kwargs):
	""" Returns the state of audit encryption. """
	...

def isAuditFilterEnabled(*args, **kwargs):
	""" Determination of enablement state of an Audit Specification. """
	...

def isAuditNotificationEnabled(*args, **kwargs):
	""" Returns the enabled state of the audit notification policy. """
	...

def isAuditSigningEnabled(*args, **kwargs):
	""" Returns the state of audit signing. """
	...

def isEditionExists(*args, **kwargs):
	""" Use this command to check if the specified edition exists for the particular application. """
	...

def isEventEnabled(*args, **kwargs):
	""" Returns a Boolean indicating if the event has at least one audit outcome for which it has been enabled. """
	...

def isFederated(*args, **kwargs):
	""" Check if the server is a standalone server or the node of the given server is federated with a deployment manager. Returns "true" if the node of the server is federated, "false" otherwise. """
	...

def isGlobalSecurityEnabled(*args, **kwargs):
	""" Returns the current administrative security setting of true or false. """
	...

def isIdMgrUseGlobalSchemaForModel(*args, **kwargs):
	""" Returns a boolean to indicate whether the global schema option is enabled for the data model in a multiple security domain environment. """
	...

def isInheritDefaultsForDestination(*args, **kwargs):
	""" The command will return "true" if the destination specified inherits the default security permissions. """
	...

def isInheritReceiverForTopic(*args, **kwargs):
	""" Shows the inherit receiver defaults for a topic in a given topic space.  Returns "true" if the topic inherits from receiver default values. """
	...

def isInheritSenderForTopic(*args, **kwargs):
	""" Shows the inherit sender defaults for a topic for a specified topic space.  Returns "true" if the topic inherits from sender default values. """
	...

def isJACCEnabled(*args, **kwargs):
	""" Checks if the current run time is JACC enabled in the global security domain. """
	...

def isNodeZOS(*args, **kwargs):
	""" Determines whether or not a given node is a z/OS node. Returns "true" if node operating system is Z/OS, "false" otherwise. """
	...

def isPollingJobManager(*args, **kwargs):
	""" Query whether a managed node is periodically polling a JobManager """
	...

def isSAFVersionValidForIdentityMapping(*args, **kwargs):
	""" Returns a Boolean indicating if the version of the SAF product supports distributed identity mapping. """
	...

def isSendEmailEnabled(*args, **kwargs):
	""" Returns the enabled state of sending audit notification emails. """
	...

def isSingleSecurityDomain(*args, **kwargs):
	""" Checks if the current run time is a single security domain. """
	...

def isVerboseAuditEnabled(*args, **kwargs):
	""" Returns the state of verbose gathering of audit data. """
	...

def ldapSearch(*args, **kwargs):
	""" Performs ldapsearch according to search criteria from input parameter """
	...

def listAdminObjectInterfaces(*args, **kwargs):
	""" List all of the defined administrative object interfaces on the specified J2C resource adapter. """
	...

def listAllDestinationsWithRoles(*args, **kwargs):
	""" Lists all destinations which have roles defined on them. """
	...

def listAllForeignBusesWithRoles(*args, **kwargs):
	""" Lists all foreign buses which have roles defined on them for the specified bus. """
	...

def listAllRolesForGroup(*args, **kwargs):
	""" Lists all the roles defined for a specified group. """
	...

def listAllRolesForUser(*args, **kwargs):
	""" Lists all the roles defined for a specified user. """
	...

def listAllSIBBootstrapMembers(*args, **kwargs):
	""" Lists all the servers or clusters that can be used for bootstrap into the specified bus. """
	...

def listAllTopicsWithRoles(*args, **kwargs):
	""" Lists all the topics with roles defined for the specified topic space. """
	...

def listApplicationPorts(*args, **kwargs):
	""" Displays a list of ports that is used to access the specified application, including the node name, server name, named endpoint, and host and port values. """
	...

def listAssets(*args, **kwargs):
	""" List assets which have been imported into the product configuration repository. """
	...

def listAssetsAttachedToPolicySet(*args, **kwargs):
	""" The listAssetsAttachedToPolicySet command lists the assets to which a specific policy set is attached. """
	...

def listAttachmentsForPolicySet(*args, **kwargs):
	""" The listAttachmentsForPolicySet command lists the applications to which a specific policy set is attached. """
	...

def listAuditAuthorizationGroupsForGroupID(*args, **kwargs):
	""" list all the AuthorizationGroups that a given group has access to """
	...

def listAuditAuthorizationGroupsForUserID(*args, **kwargs):
	""" list all the AuthorizationGroups that a given user has access to. """
	...

def listAuditEmitters(*args, **kwargs):
	""" Lists all the audit emitter implementation objects. """
	...

def listAuditEncryptionKeyStores(*args, **kwargs):
	""" Lists the audit record encryption keystores. """
	...

def listAuditEventFactories(*args, **kwargs):
	""" Returns a list of the defined audit event factory implementations. """
	...

def listAuditFilters(*args, **kwargs):
	""" Retrieves a list of all the audit specifications defined in the audit.xml. """
	...

def listAuditFiltersByEvent(*args, **kwargs):
	""" Returns a list of event and outcome types of the defined Audit Filters. """
	...

def listAuditFiltersByRef(*args, **kwargs):
	""" Returns the references to the defined Audit Filters. """
	...

def listAuditGroupIDsOfAuthorizationGroup(*args, **kwargs):
	""" list all the group IDs in an AuthorizationGroups """
	...

def listAuditKeyStores(*args, **kwargs):
	""" Lists Audit keystores """
	...

def listAuditNotificationMonitors(*args, **kwargs):
	""" Lists the audit notification monitors. """
	...

def listAuditNotifications(*args, **kwargs):
	""" Lists the audit notifications. """
	...

def listAuditResourcesForGroupID(*args, **kwargs):
	""" List all the objects that a given group has access to. """
	...

def listAuditResourcesForUserID(*args, **kwargs):
	""" List all the objects that a given user has access to. """
	...

def listAuditUserIDsOfAuthorizationGroup(*args, **kwargs):
	""" list all the users IDs in an AuthorizationGroups """
	...

def listAuthDataEntries(*args, **kwargs):
	""" List authentication data entries in the administrative security configuration or a in a security domain. """
	...

def listAuthorizationGroups(*args, **kwargs):
	""" List existing Authorization Groups. """
	...

def listAuthorizationGroupsForGroupID(*args, **kwargs):
	""" list all the AuthorizationGroups that a given group has access to """
	...

def listAuthorizationGroupsForUserID(*args, **kwargs):
	""" list all the AuthorizationGroups that a given user has access to. """
	...

def listAuthorizationGroupsOfResource(*args, **kwargs):
	""" Get the authorization groups of a given Resource. """
	...

def listAvailableOSGiExtensions(*args, **kwargs):
	""" Shows the possible extensions available to be attached to the composition unit. """
	...

def listBLAs(*args, **kwargs):
	""" List business-level applications in the cell. """
	...

def listCAClients(*args, **kwargs):
	""" Lists certificate authority (CA) client configurator objects. """
	...

def listCertAliases(*args, **kwargs):
	""" Lists the certificate aliases. """
	...

def listCertStatusForSecurityStandard(*args, **kwargs):
	""" Returns all the certificate used by SSL configuraiton and plugins. States if they comply with the requested security level. """
	...

def listCertificateRequests(*args, **kwargs):
	""" The list of certificate request in a keystore. """
	...

def listChainTemplates(*args, **kwargs):
	""" Displays a list of templates that can be used to create chains in this configuration. All templates have a certain type of transport channel as the last transport channel in the chain. """
	...

def listChains(*args, **kwargs):
	""" List all chains configured under a particular instance of TransportChannelService. """
	...

def listCheckpointDocuments(*args, **kwargs):
	""" List the existing checkpoint documents specified by the "checkpointName" """
	...

def listCheckpoints(*args, **kwargs):
	""" List the existing checkpoints """
	...

def listClusterMemberTemplates(*args, **kwargs):
	""" No description available """
	...

def listCompUnits(*args, **kwargs):
	""" List composition units belonging to a specified business-level application. """
	...

def listConnectionFactoryInterfaces(*args, **kwargs):
	""" List all of the defined connection factory interfaces on the specified J2C resource adapter. """
	...

def listControlOps(*args, **kwargs):
	""" Lists control operations defined for a business-level application and its composition units. """
	...

def listCoreGroupServers(*args, **kwargs):
	""" Returns a list of core group servers. """
	...

def listCoreGroups(*args, **kwargs):
	""" Return a collection of core groups that are related to the specified core group. """
	...

def listDatasources(*args, **kwargs):
	""" List the datasources that are contained in the specified scope. """
	...

def listDescriptiveProps(*args, **kwargs):
	""" List descriptive properties under an object. """
	...

def listDisabledSessionCookie(*args, **kwargs):
	""" Lists the sets of cookie configurations that will not be able to be programmatically modified """
	...

def listDynamicClusterIsolationGroupMembers(*args, **kwargs):
	""" List Dynamic Cluster isolation group members """
	...

def listDynamicClusterIsolationGroups(*args, **kwargs):
	""" List Dynamic Cluster isolation groups """
	...

def listDynamicClusters(*args, **kwargs):
	""" List all dynamic clusters in the cell """
	...

def listDynamicSSLConfigSelections(*args, **kwargs):
	""" List all Dynamic SSL configuration selections. """
	...

def listEditions(*args, **kwargs):
	""" Use this command to list all the editions for a particular application. """
	...

def listElasticityActions(*args, **kwargs):
	""" Command to list all elasticity actions """
	...

def listEligibleBridgeInterfaces(*args, **kwargs):
	""" Returns a collection of node, server and transport channel chain combinations that are eligible to become bridge interfaces for the specified core group access point. """
	...

def listExternalBundleRepositories(*args, **kwargs):
	""" Lists the external bundle repositories in the configuration. """
	...

def listForeignServerTypes(*args, **kwargs):
	""" Use this command to show all of the middleware server types """
	...

def listGroupIDsOfAuthorizationGroup(*args, **kwargs):
	""" list all the group IDs in an AuthorizationGroup """
	...

def listGroupsForNamingRoles(*args, **kwargs):
	""" List the groups and special subjects from all naming roles. """
	...

def listGroupsInBusConnectorRole(*args, **kwargs):
	""" List the groups in the bus connector role """
	...

def listGroupsInDefaultRole(*args, **kwargs):
	""" List the groups in the default role. """
	...

def listGroupsInDestinationRole(*args, **kwargs):
	""" List the groups in the specified role in the destination security space role for the given destination. """
	...

def listGroupsInForeignBusRole(*args, **kwargs):
	""" List the groups in the specified role in the foreign bus security space role for the given bus. """
	...

def listGroupsInTopicRole(*args, **kwargs):
	""" Lists the groups in the specified topic role for the specified topic space. """
	...

def listGroupsInTopicSpaceRootRole(*args, **kwargs):
	""" Lists the groups in the specified topic space role for the specified topic space. """
	...

def listHealthActions(*args, **kwargs):
	""" Command to list all health actions """
	...

def listHealthPolicies(*args, **kwargs):
	""" Command to list all health policies """
	...

def listIdMgrCustomProperties(*args, **kwargs):
	""" Returns custom properties of specified repository configuration. """
	...

def listIdMgrGroupsForRoles(*args, **kwargs):
	""" Lists the uniqueName of groups for each role. """
	...

def listIdMgrLDAPAttrs(*args, **kwargs):
	""" Lists the name of all configured attributes for the specified LDAP repository. """
	...

def listIdMgrLDAPAttrsNotSupported(*args, **kwargs):
	""" Lists the details of all virtual member manager properties not supported by the specified LDAP repository. """
	...

def listIdMgrLDAPBackupServers(*args, **kwargs):
	""" Lists the backup LDAP servers. """
	...

def listIdMgrLDAPEntityTypes(*args, **kwargs):
	""" Lists the name of all configured entity types for the specified LDAP repository. """
	...

def listIdMgrLDAPExternalIdAttrs(*args, **kwargs):
	""" Lists the details of all LDAP attributes used as an external ID. """
	...

def listIdMgrLDAPServers(*args, **kwargs):
	""" Lists all the configured primary LDAP servers. """
	...

def listIdMgrPropertyExtensions(*args, **kwargs):
	""" Lists the properties that have been extended for one or more entity types. """
	...

def listIdMgrRealmBaseEntries(*args, **kwargs):
	""" Lists all base entries of the specified realm. """
	...

def listIdMgrRealmDefaultParents(*args, **kwargs):
	""" Lists the mapping of default parent uniqueName for all entity types in a specified realm. If realm name is not specified, default realm is used. """
	...

def listIdMgrRealmURAttrMappings(*args, **kwargs):
	""" Returns mappings between user and group attributes of user registry to virtual member manager properties for a realm. """
	...

def listIdMgrRealms(*args, **kwargs):
	""" Lists the name of configured realms. """
	...

def listIdMgrRepositories(*args, **kwargs):
	""" Lists names, types, and hostnames of all the configured repositories. """
	...

def listIdMgrRepositoryBaseEntries(*args, **kwargs):
	""" Returns base entries for a specified repository. """
	...

def listIdMgrSupportedDBTypes(*args, **kwargs):
	""" Returns a list of supported database types. """
	...

def listIdMgrSupportedEntityTypes(*args, **kwargs):
	""" Lists all the configured supported entity types. """
	...

def listIdMgrSupportedLDAPServerTypes(*args, **kwargs):
	""" Returns list of supported LDAP server types. """
	...

def listIdMgrSupportedMessageDigestAlgorithms(*args, **kwargs):
	""" Returns a list of supported message digest algorithms. """
	...

def listIdMgrUsersForRoles(*args, **kwargs):
	""" Lists the uniqueName of users for each role. """
	...

def listInheritDefaultsForDestination(*args, **kwargs):
	""" List inherit defaults for destination (deprecated - use isInheritDefaultsForDestination instead) """
	...

def listInheritReceiverForTopic(*args, **kwargs):
	""" List Inherit Receiver For topic (deprecated - use isInheritReceiverForTopic instead) """
	...

def listInheritSenderForTopic(*args, **kwargs):
	""" List Inherit Sender For topic (deprecated - use isInheritSenderForTopic instead) """
	...

def listInterceptors(*args, **kwargs):
	""" List interceptors from the global security configuration or from a security domain. """
	...

def listJ2CActivationSpecs(*args, **kwargs):
	""" List the J2C activation specifications that have a specified message listener type defined in the specified J2C resource adapter. """
	...

def listJ2CAdminObjects(*args, **kwargs):
	""" List the J2C administrative objects that have a specified administrative object interface defined in the specified J2C resource adapter. """
	...

def listJ2CConnectionFactories(*args, **kwargs):
	""" List J2C connection factories that have a specified connection factory interface defined in the specified J2C resource adapter. """
	...

def listJAASLoginEntries(*args, **kwargs):
	""" List JAAS login entries from the administrative security configuration or from an application security domain. """
	...

def listJAXWSHandlerLists(*args, **kwargs):
	""" List the JAX-WS Handler Lists at a given cell scope """
	...

def listJAXWSHandlers(*args, **kwargs):
	""" List the JAX-WS Handlers at a given cell scope """
	...

def listJDBCProviders(*args, **kwargs):
	""" List the JDBC providers that are contained in the specified scope. """
	...

def listJSFImplementation(*args, **kwargs):
	""" Lists the JavaServer Faces implementation used by the WebSphere runtime for an application """
	...

def listJSFImplementations(*args, **kwargs):
	""" Lists the JavaServer Faces implementations allowed by the WebSphere runtime for an application """
	...

def listJobManagers(*args, **kwargs):
	""" List all JobManagers which a given managed node is registered with """
	...

def listJobSchedulerProperties(*args, **kwargs):
	""" list properties of the job scheduler """
	...

def listKeyFileAliases(*args, **kwargs):
	""" List personal certificate aliases in a keystore file """
	...

def listKeyManagers(*args, **kwargs):
	""" List key managers within a give scope. """
	...

def listKeyReferences(*args, **kwargs):
	""" Lists key references for the keys in a keySet. """
	...

def listKeySetGroups(*args, **kwargs):
	""" List key set groups within a scope. """
	...

def listKeySets(*args, **kwargs):
	""" List key sets within a scope. """
	...

def listKeySizes(*args, **kwargs):
	""" Displays a list of certificate key sizes. """
	...

def listKeyStoreTypes(*args, **kwargs):
	""" List the supported keystore types. """
	...

def listKeyStoreUsages(*args, **kwargs):
	""" Returns a list of valid keystore usage types.  A usage is a way to identify how the keystore is intended to be used. """
	...

def listKeyStores(*args, **kwargs):
	""" List keystore objects in a particular scope. """
	...

def listKrbAuthMechanism(*args, **kwargs):
	""" The KRB5 authentication mechanism security object field in the security configuration file is displayed. """
	...

def listLMServices(*args, **kwargs):
	""" Use the "listLMServices" command to list the created local mapping services. """
	...

def listLocalRepositoryBundles(*args, **kwargs):
	""" Lists all bundles in the internal bundle repository. """
	...

def listLoginConfigs(*args, **kwargs):
	""" Lists the login module configuration aliases. """
	...

def listLoginModules(*args, **kwargs):
	""" List all login modules for a JAAS login entry. """
	...

def listLongRunningSchedulerProperties(*args, **kwargs):
	""" (Deprecated) list properties of the long-running scheduler. Use listJobSchedulerProperties. """
	...

def listManagedNodes(*args, **kwargs):
	""" Use this command to list all registered managed nodes in the admin agent, or to list all federated nodes in the deployment manager. """
	...

def listManagementScopeOptions(*args, **kwargs):
	""" Returns a list of all cell, node, server, cluster, and nodegroups management scopes in the configuration. """
	...

def listManagementScopes(*args, **kwargs):
	""" List all management scopes. """
	...

def listMessageListenerTypes(*args, **kwargs):
	""" List all of the defined message listener types on the specified J2C resource adapter. """
	...

def listMiddlewareAppEditions(*args, **kwargs):
	""" Use this command to list all editions for a middleware application. """
	...

def listMiddlewareAppWebModules(*args, **kwargs):
	""" Use this command to list the web modules for a middleware application. """
	...

def listMiddlewareApps(*args, **kwargs):
	""" Use this command to list all middleware applications. """
	...

def listMiddlewareDescriptorVersions(*args, **kwargs):
	""" Use this command to list which versions have specific information provided in the middleware descriptor. """
	...

def listMiddlewareDescriptors(*args, **kwargs):
	""" Use this command to list the names of all installed middleware descriptors """
	...

def listMiddlewareServerTypes(*args, **kwargs):
	""" Use this command to show all of the middleware server types """
	...

def listMiddlewareServers(*args, **kwargs):
	""" Use this command to show all of the servers of the specified server type.  If no server type is specified, then all servers are shown """
	...

def listMiddlewareTargets(*args, **kwargs):
	""" Use this command to list the deployment targets for a middleware application. """
	...

def listNodeGroupProperties(*args, **kwargs):
	""" list properties of a node group """
	...

def listNodeGroups(*args, **kwargs):
	""" list node groups containing given node, or list all node groups if no target node is given """
	...

def listNodes(*args, **kwargs):
	""" list all the nodes in the cell or on a specified nodeGroup. """
	...

def listOSGiExtensions(*args, **kwargs):
	""" Shows the current extensions attached to the composition unit. """
	...

def listPHPServers(*args, **kwargs):
	""" Use this command to list PHP Servers. """
	...

def listPasswordEncryptionKeys(*args, **kwargs):
	""" Displays the list of key alias names and the current encryption key in the specified keystore file. The first item in the list is the current encryption key. """
	...

def listPersonalCertificates(*args, **kwargs):
	""" The list of personal certificates in a given keystore. """
	...

def listPolicySets(*args, **kwargs):
	""" The listPolicySets command returns a list of all existing policy sets. """
	...

def listPolicyTypes(*args, **kwargs):
	""" The listPolicyTypes command returns a list of the names of the policies configured in the system, in a policy set, or in a binding. """
	...

def listPureQueryBindFiles(*args, **kwargs):
	""" List the pureQuery bind files in an installed application. """
	...

def listRegistryGroups(*args, **kwargs):
	""" Returns a list of groups in a security realm, security domain, or resource. """
	...

def listRegistryUsers(*args, **kwargs):
	""" Returns a list of users in the specified security realm, security domain, or resource. """
	...

def listRemoteCellsFromIntelligentManagement(*args, **kwargs):
	""" Command to list remote cells from Intelligent Management """
	...

def listReplicationDomainReferences(*args, **kwargs):
	""" List search object that participates in a specific data replication domain.  An object participates in a data replication domain if the object references the provided data replication domain name.  The command returns the objects that reference the data replication domain name regardless of whether replication is enabled or disabled for that object. """
	...

def listResourcesForGroupID(*args, **kwargs):
	""" List all the objects that a given group has access to. """
	...

def listResourcesForUserID(*args, **kwargs):
	""" List all the objects that a given user has access to. """
	...

def listResourcesInSecurityDomain(*args, **kwargs):
	""" List all resources mapped to the specified security domain. """
	...

def listResourcesOfAuthorizationGroup(*args, **kwargs):
	""" List all the resources within the given Authorization Group. """
	...

def listRoutingRules(*args, **kwargs):
	""" Use this command to list routing policy rules. """
	...

def listRuleset(*args, **kwargs):
	""" Use this command to list a ruleset. """
	...

def listSAMLIssuerConfig(*args, **kwargs):
	""" List SAML Issuer Configuration data """
	...

def listSIBDestinations(*args, **kwargs):
	""" List destinations belonging to a bus. """
	...

def listSIBEngines(*args, **kwargs):
	""" List messaging engines. """
	...

def listSIBForeignBuses(*args, **kwargs):
	""" List the SIB foreign buses. """
	...

def listSIBJMSActivationSpecs(*args, **kwargs):
	""" List activation specifications on the SIB JMS resource adapter in given scope. """
	...

def listSIBJMSConnectionFactories(*args, **kwargs):
	""" List all SIB JMS connection factories of the specified type at the specified scope. """
	...

def listSIBJMSQueues(*args, **kwargs):
	""" List all SIB JMS queues at the specified scope. """
	...

def listSIBJMSTopics(*args, **kwargs):
	""" List all SIB JMS topics at the specified scope. """
	...

def listSIBLinks(*args, **kwargs):
	""" List the SIB links. """
	...

def listSIBMQLinks(*args, **kwargs):
	""" List the WebSphere MQ links. """
	...

def listSIBMediations(*args, **kwargs):
	""" List the mediations on a bus. """
	...

def listSIBNominatedBootstrapMembers(*args, **kwargs):
	""" Lists all the servers or clusters that have been nominated for bootstrap into the specified bus. """
	...

def listSIBPermittedChains(*args, **kwargs):
	""" Lists the permitted chains for the specified bus. """
	...

def listSIBWMQServerBusMembers(*args, **kwargs):
	""" List all WebSphere MQ servers. """
	...

def listSIBWMQServers(*args, **kwargs):
	""" List all WebSphere MQ servers. """
	...

def listSIBusMembers(*args, **kwargs):
	""" List the members on a bus. """
	...

def listSIBuses(*args, **kwargs):
	""" List all buses in the cell. """
	...

def listSSLCiphers(*args, **kwargs):
	""" List of ciphers. """
	...

def listSSLConfigGroups(*args, **kwargs):
	""" List all SSL configuration groups. """
	...

def listSSLConfigProperties(*args, **kwargs):
	""" List the properties for a given SSL configuration. """
	...

def listSSLConfigs(*args, **kwargs):
	""" List SSL configurations for a specific management scope. """
	...

def listSSLProtocolTypes(*args, **kwargs):
	""" Lists the SSL protocols valid for the current FIPS configuration. If FIPS is not enabled, then the full list of valid SSL protocols are returned. """
	...

def listSSLRepertoires(*args, **kwargs):
	""" List all SSLConfig instances that can be associated with an SSLInboundChannel """
	...

def listSTSAssignedEndpoints(*args, **kwargs):
	""" Query the STS for a list of assigned endpoints. """
	...

def listSTSConfigurationProperties(*args, **kwargs):
	""" List the configuration properties under a configuration group. """
	...

def listSTSConfiguredTokenTypes(*args, **kwargs):
	""" Query the STS for a list of configured token types. """
	...

def listSTSEndpointTokenTypes(*args, **kwargs):
	""" List assigned token types for an endpoint. """
	...

def listSTSProperties(*args, **kwargs):
	""" List the configuration properties under a configuration group. """
	...

def listSecurityDomains(*args, **kwargs):
	""" Lists all security domains. """
	...

def listSecurityDomainsForResources(*args, **kwargs):
	""" Returns a list of resources and their associated domain for each resource provided. """
	...

def listSecurityRealms(*args, **kwargs):
	""" List all security realms in the configuration from global security and the security domains. """
	...

def listServerPorts(*args, **kwargs):
	""" Displays a list of ports that is used by a particular server, including the node name, server name, named endpoint, and host and port values. """
	...

def listServerTemplates(*args, **kwargs):
	""" Lists the available Server Templates """
	...

def listServerTypes(*args, **kwargs):
	""" Lists the available serverTypes that have a template. """
	...

def listServers(*args, **kwargs):
	""" list servers of specified server type and node name. If node name is not specified, whole cell will be searched. If the server type is not specified servers of all types are returned. """
	...

def listServiceMaps(*args, **kwargs):
	""" Use the "listServiceMaps" command to list the installed service maps. """
	...

def listServiceRules(*args, **kwargs):
	""" Use this command to list service policy rules. """
	...

def listServices(*args, **kwargs):
	""" Lists the services based on a generic query properties. It provides more generic query functions than listWebServices, listWebServiceEndpoints, listWebServiceOperations, and getWebService commands. """
	...

def listSignatureAlgorithms(*args, **kwargs):
	""" List signature algorithms available for the current FIPS configuration. If FIPS is not enabled, then the full list of valid Signature Algorithms are returned. """
	...

def listSignerCertificates(*args, **kwargs):
	""" The list of signer certificates in a keystore. """
	...

def listSqljProfiles(*args, **kwargs):
	""" List the serialized SQLJ profiles that are in an installed application. """
	...

def listSupportedJPASpecifications(*args, **kwargs):
	""" Lists JPA Specification levels supported by this version of WebSphere. """
	...

def listSupportedJaxrsProviders(*args, **kwargs):
	""" Lists JAXRS Providers supported by this version of WebSphere. """
	...

def listSupportedPolicySets(*args, **kwargs):
	""" listSupportedPolicySetsCmdDesc """
	...

def listTAMSettings(*args, **kwargs):
	""" This command lists the current embedded Tivoli Access Manager configuration settings. """
	...

def listTCPEndPoints(*args, **kwargs):
	""" Lists all NamedEndPoints that can be associated with a TCPInboundChannel """
	...

def listTCPThreadPools(*args, **kwargs):
	""" Lists all ThreadPools that can be associated with a TCPInboundChannel or TCPOutboundChannel """
	...

def listTraceRulesForIntelligentManagement(*args, **kwargs):
	""" List trace rules for Intelligent Management """
	...

def listTrustManagers(*args, **kwargs):
	""" List trust managers. """
	...

def listTrustedRealms(*args, **kwargs):
	""" List trusted realms trusted by a security realm, resource, or security domain. """
	...

def listUDPEndPoints(*args, **kwargs):
	""" Lists all the NamedEndPoints endpoints that can be associated with a UDPInboundChannel """
	...

def listUnmanagedNodes(*args, **kwargs):
	""" Use this command to list all unmanaged nodes in the cell. """
	...

def listUserIDsOfAuthorizationGroup(*args, **kwargs):
	""" list all the users IDs in an AuthorizationGroup """
	...

def listUsersForNamingRoles(*args, **kwargs):
	""" List the users from all naming roles. """
	...

def listUsersInBusConnectorRole(*args, **kwargs):
	""" List the users in the Bus Connector Role """
	...

def listUsersInDefaultRole(*args, **kwargs):
	""" List the users in a default role. """
	...

def listUsersInDestinationRole(*args, **kwargs):
	""" List the users in the specified role in the destination security space role for the given destination. """
	...

def listUsersInForeignBusRole(*args, **kwargs):
	""" List the users in the specified role in the foreign bus security space role for the given bus. """
	...

def listUsersInTopicRole(*args, **kwargs):
	""" Lists the users in the specified topic role for the specified topic space. """
	...

def listUsersInTopicSpaceRootRole(*args, **kwargs):
	""" Lists the users in the specified topic space role for the specified topic space. """
	...

def listWASServerTypes(*args, **kwargs):
	""" Use this command to show all of the middleware server types """
	...

def listWMQActivationSpecs(*args, **kwargs):
	""" Lists the IBM MQ Activation Specification defined at the scope provided to the command. """
	...

def listWMQConnectionFactories(*args, **kwargs):
	""" Lists the IBM MQ Connection Factories defined at the scope provided to the command. """
	...

def listWMQQueues(*args, **kwargs):
	""" Lists the IBM MQ Queues defined at the scope provided to the command. """
	...

def listWMQTopics(*args, **kwargs):
	""" Lists the IBM MQ Topics defined at the scope provided to the command. """
	...

def listWSCertExpMonitor(*args, **kwargs):
	""" List all certificate expiration monitors. """
	...

def listWSNAdministeredSubscribers(*args, **kwargs):
	""" Lists all the WSNAdministeredSubscriber objects in the configuration of the target WSNServicePoint that match the specified input parameters. """
	...

def listWSNServicePoints(*args, **kwargs):
	""" Lists all the WSNServicePoint objects in the configuration of the target WSNService that match the specified input parameters. """
	...

def listWSNServices(*args, **kwargs):
	""" Lists all the WSNService objects in the configuration that match the specified input parameters. """
	...

def listWSNTopicDocuments(*args, **kwargs):
	""" Lists all the WSNTopicDocument objects in the configuration of the target WSNTopicNamespace that match the specified input parameters. """
	...

def listWSNTopicNamespaces(*args, **kwargs):
	""" Lists all the WSNTopicNamespace objects in the configuration of the target WSNService that match the specified input parameters. """
	...

def listWSNotifiers(*args, **kwargs):
	""" List all notifiers. """
	...

def listWSSchedules(*args, **kwargs):
	""" List all schedules. """
	...

def listWebServerRoutingRules(*args, **kwargs):
	""" Use this command to list routing rules and their associated properties. """
	...

def listWebServiceEndpoints(*args, **kwargs):
	""" Lists the Web service endpoints that are port names defined in a Web service in an enterprise application. """
	...

def listWebServiceOperations(*args, **kwargs):
	""" Lists the Web service operations defined in a logical endpoint. """
	...

def listWebServices(*args, **kwargs):
	""" Lists the deployed Web services in enterprise applications. If there is no application name supplied, then all the Web services in the enterprise applications will are be listed. """
	...

def makeNonSystemTemplate(*args, **kwargs):
	""" makeNonSystemTemplate """
	...

def manageWMQ(*args, **kwargs):
	""" Provides the ability to manage the settings associated with the IBM MQ resource adapter installed at a particular scope. """
	...

def mapAuditGroupIDsOfAuthorizationGroup(*args, **kwargs):
	""" Maps the special subjects to actual users in the registry. """
	...

def mapGroupsToAdminRole(*args, **kwargs):
	""" Map groupids to one or more admin role in the authorization group. """
	...

def mapGroupsToAuditRole(*args, **kwargs):
	""" Map groupids to one or more audit role in the authorization group. """
	...

def mapGroupsToNamingRole(*args, **kwargs):
	""" Map groups or special subjects or both to the naming roles """
	...

def mapIdMgrGroupToRole(*args, **kwargs):
	""" Maps the group to the specified role of virtual member manager. """
	...

def mapIdMgrUserToRole(*args, **kwargs):
	""" Maps the user to the specified role of virtual member manager. """
	...

def mapResourceToSecurityDomain(*args, **kwargs):
	""" Map a resource to a security domain. """
	...

def mapUsersToAdminRole(*args, **kwargs):
	""" Map userids to one or more admin role in the authorization group. """
	...

def mapUsersToAuditRole(*args, **kwargs):
	""" Map userids to one or more audit role in the authorization group. """
	...

def mapUsersToNamingRole(*args, **kwargs):
	""" Map users to the naming roles """
	...

def mediateSIBDestination(*args, **kwargs):
	""" Mediate a destination. """
	...

def migrateServerMEtoCluster(*args, **kwargs):
	""" This command will migrate a server messaging engine to a cluster messaging engine. It will not modify the messaging engine message store. Please ensure that the message store is suitable for the new clustered environment. If it is not, the migrated engine must be re-configured with a suitable message store before it is started, or the engine may fail to start. """
	...

def migrateWMQMLP(*args, **kwargs):
	""" Migrates a IBM MQ message listener port definition to an activation specification definition. """
	...

def modifyAuditEmitter(*args, **kwargs):
	""" Modifies an audit service provider implementation in the audit.xml file """
	...

def modifyAuditEncryptionConfig(*args, **kwargs):
	""" Modifies the audit record encryption configuration. """
	...

def modifyAuditEventFactory(*args, **kwargs):
	""" Modifies an entry in the audit.xml to reference the configuration of an audit event factory implementation of the Audit Event Factory interface. """
	...

def modifyAuditFilter(*args, **kwargs):
	""" Modifies an audit specification entry in the audit.xml that matches the reference Id. """
	...

def modifyAuditKeyStore(*args, **kwargs):
	""" Modifies a Keystore object. """
	...

def modifyAuditNotification(*args, **kwargs):
	""" Modifies an audit notification. """
	...

def modifyAuditNotificationMonitor(*args, **kwargs):
	""" Modifies the audit notification monitor specified by the reference id. """
	...

def modifyAuditPolicy(*args, **kwargs):
	""" Modifies the audit policy attributes. """
	...

def modifyAuditSigningConfig(*args, **kwargs):
	""" Modifies the audit record signing configuration. """
	...

def modifyAuthDataEntry(*args, **kwargs):
	""" Modify an authentication data entry """
	...

def modifyCAClient(*args, **kwargs):
	""" Modifies a certificate authority (CA) client configurator object. """
	...

def modifyDescriptiveProp(*args, **kwargs):
	""" Modify a descriptive property under an object. """
	...

def modifyDisabledSessionCookie(*args, **kwargs):
	""" Modifies an existing cookie configuration """
	...

def modifyDynamicClusterIsolationProperties(*args, **kwargs):
	""" Modify Dynamic Cluster isolation properties """
	...

def modifyElasticityAction(*args, **kwargs):
	""" Command to modify a elasticity action """
	...

def modifyExternalBundleRepository(*args, **kwargs):
	""" Modifies the named external bundle repository with the given parameters. Unspecified parameters keep their existing values. To remove an existing value, specify an empty string for the parameter. """
	...

def modifyForeignServerProperty(*args, **kwargs):
	""" Use this command to modify a property on a middleware server """
	...

def modifyHealthAction(*args, **kwargs):
	""" Command to modify a health action """
	...

def modifyHealthPolicy(*args, **kwargs):
	""" Command to modify a health policy """
	...

def modifyIntelligentManagement(*args, **kwargs):
	""" Command to modify Intelligent Management properties """
	...

def modifyIntelligentManagementConnectorCluster(*args, **kwargs):
	""" Command to modify properties of ConnectorCluster """
	...

def modifyJAXWSHandler(*args, **kwargs):
	""" Modify a JAX-WS Handler """
	...

def modifyJAXWSHandlerList(*args, **kwargs):
	""" Modify a JAX-WS Handler List """
	...

def modifyJPASpecLevel(*args, **kwargs):
	""" Changes the active JPA specification level for a Server or ServerCluster.The operation requires either an ObjectName referencing the target object, or parameters identifying the target node and server.  The specLevel parameter must always be specified. """
	...

def modifyJSFImplementation(*args, **kwargs):
	""" Modifies the JavaServer Faces implementation used by the WebSphere runtime for an application """
	...

def modifyJaspiProvider(*args, **kwargs):
	""" Modify configuration data for a given authentication provider. """
	...

def modifyJaxrsProvider(*args, **kwargs):
	""" Changes the active JAXRS Provider for a Server or ServerCluster.The operation requires either an ObjectName referencing the target object, or parameters identifying the target node and server.  The Provider parameter must always be specified. """
	...

def modifyJobSchedulerAttribute(*args, **kwargs):
	""" modify a job scheduler attribute """
	...

def modifyJobSchedulerProperty(*args, **kwargs):
	""" modify the property of the job scheduler """
	...

def modifyKeyManager(*args, **kwargs):
	""" Modify a key manager. """
	...

def modifyKeySet(*args, **kwargs):
	""" Modify a Key Sets attributes. """
	...

def modifyKeySetGroup(*args, **kwargs):
	""" Modify the a key set group. """
	...

def modifyKeyStore(*args, **kwargs):
	""" Modifies a Keystore object. """
	...

def modifyKrbAuthMechanism(*args, **kwargs):
	""" The KRB5 authentication mechanism security object field in the security configuration file is modified based on the user input. """
	...

def modifyLongRunningSchedulerAttribute(*args, **kwargs):
	""" (Deprecated) modify a long-running scheduler attribute. Use modifyJobSchedulerAttribute. """
	...

def modifyLongRunningSchedulerProperty(*args, **kwargs):
	""" (Deprecated) modify the property of the long-running scheduler. Use modifyJobSchedulerProperty. """
	...

def modifyManagedNodeGroupInfo(*args, **kwargs):
	""" Update information for a group of managed nodes. (deprecated) """
	...

def modifyManagedNodeProperties(*args, **kwargs):
	""" Modify properties associated with a specific managed node. (deprecated) """
	...

def modifyMiddlewareAppWebModule(*args, **kwargs):
	""" Use this command to modify the web module of a middleware application. """
	...

def modifyMiddlewareDescriptorDiscoveryInterval(*args, **kwargs):
	""" Use this command to modify the discovery interval of the specified middleware descriptor """
	...

def modifyMiddlewareDescriptorProperty(*args, **kwargs):
	""" Use this command to modify a property of a specific version of the middleware platform that the descriptor represents.  If no version is specified, the "default" version will be updated. """
	...

def modifyNodeGroup(*args, **kwargs):
	""" modify a node group configuration """
	...

def modifyNodeGroupProperty(*args, **kwargs):
	""" modify the property of a node group """
	...

def modifyPHPApp(*args, **kwargs):
	""" Use this command to modify a PHP application. """
	...

def modifyPasswordEncryption(*args, **kwargs):
	""" Modifies the configuration of the password encryption. Note that the original value is unchanged unless the value is set by the parameter. To change the value to the default, use a blank string (""). """
	...

def modifyPolicy(*args, **kwargs):
	""" Modify a policy that matches the provided policy name. """
	...

def modifyRemoteCellForIntelligentManagement(*args, **kwargs):
	""" Command to modify remote cell connectors for Intelligent Management """
	...

def modifySIBDestination(*args, **kwargs):
	""" Modify bus destination. """
	...

def modifySIBEngine(*args, **kwargs):
	""" Modify a messaging engine. """
	...

def modifySIBForeignBus(*args, **kwargs):
	""" Modify a SIB foreign bus. """
	...

def modifySIBJMSActivationSpec(*args, **kwargs):
	""" Modify the attributes of the given SIB JMS activation specification. """
	...

def modifySIBJMSConnectionFactory(*args, **kwargs):
	""" Modify the attributes of the supplied SIB JMS connection factory using the supplied attribute values. """
	...

def modifySIBJMSQueue(*args, **kwargs):
	""" Modify the attributes of the supplied SIB JMS queue using the supplied attribute values. """
	...

def modifySIBJMSTopic(*args, **kwargs):
	""" Modify the attributes of the supplied SIB JMS topic using the supplied attribute values. """
	...

def modifySIBLink(*args, **kwargs):
	""" Modify an existing SIB link. """
	...

def modifySIBMQLink(*args, **kwargs):
	""" Modify an existing WebSphere MQ link. """
	...

def modifySIBMediation(*args, **kwargs):
	""" Modify a mediation. """
	...

def modifySIBWMQServer(*args, **kwargs):
	""" Modify a named WebSphere MQ server's attributes. """
	...

def modifySIBWMQServerBusMember(*args, **kwargs):
	""" Modify a named WebSphere MQ server bus member. """
	...

def modifySIBus(*args, **kwargs):
	""" Modify a bus. """
	...

def modifySIBusMemberPolicy(*args, **kwargs):
	""" Modify a cluster bus members messaging engine policy assistance settings. """
	...

def modifySSLConfig(*args, **kwargs):
	""" Modify a SSL configuration. """
	...

def modifySSLConfigGroup(*args, **kwargs):
	""" Modify a SSL configuration group. """
	...

def modifySecurityDomain(*args, **kwargs):
	""" Modifies a security domain's description. """
	...

def modifyServerPort(*args, **kwargs):
	""" Modifies the host or port of the named endpoint that is used by the specified server. """
	...

def modifySpnegoFilter(*args, **kwargs):
	""" This command modifies SPNEGO Web authentication Filter attributes in the security configuration. """
	...

def modifySpnegoTAIProperties(*args, **kwargs):
	""" This command modifies SPNEGO TAI properties in the security configuration. """
	...

def modifyTAM(*args, **kwargs):
	""" This command modifies the configuration for embedded Tivoli Access Manager on the WebSphere Application Server node or nodes specified. """
	...

def modifyTargetGroupInfo(*args, **kwargs):
	""" Update information for a group of Targets. """
	...

def modifyTargetProperties(*args, **kwargs):
	""" Modify properties associated with a specific Target. """
	...

def modifyTrustManager(*args, **kwargs):
	""" Modify a trust manager. """
	...

def modifyUnmanagedWebApp(*args, **kwargs):
	""" Use this command to modify an unmanaged web application. """
	...

def modifyWMQActivationSpec(*args, **kwargs):
	""" Modifies the properties of the IBM MQ Activation Specification provided to the command. """
	...

def modifyWMQConnectionFactory(*args, **kwargs):
	""" Modifies the properties of the IBM MQ Connection Factory provided to the command. """
	...

def modifyWMQQueue(*args, **kwargs):
	""" Modifies the properties of the IBM MQ Queue provided to the command. """
	...

def modifyWMQTopic(*args, **kwargs):
	""" Modifies the properties of the IBM MQ Topic provided to the command. """
	...

def modifyWSCertExpMonitor(*args, **kwargs):
	""" Modify a certificate expiration monitor. """
	...

def modifyWSNotifier(*args, **kwargs):
	""" Modify a notifier. """
	...

def modifyWSSchedule(*args, **kwargs):
	""" Modify a schedule. """
	...

def modifyWasCEApp(*args, **kwargs):
	""" Use this command to modify a WAS CE application. """
	...

def moveClusterToCoreGroup(*args, **kwargs):
	""" Move all servers in a cluster from one core group to another. """
	...

def moveServerToCoreGroup(*args, **kwargs):
	""" Move a server from one core group to another. """
	...

def populateUniqueNames(*args, **kwargs):
	""" Attempt to populate any missing unique name entries in the authorization model for the specified bus using its user repository. """
	...

def prepareKeysForCellProfile(*args, **kwargs):
	""" Prepare keys and keystores for Cell profile creation. """
	...

def prepareKeysForSingleProfile(*args, **kwargs):
	""" Prepare keys and keystores for a profile creation. """
	...

def processPureQueryBindFiles(*args, **kwargs):
	""" Process the pureQuery bind files that are in an installed application.  Bind static SQL packages in a database.  Refer to the information center documentation for the pureQuery bind utility. """
	...

def processSqljProfiles(*args, **kwargs):
	""" Process the serialized SQLJ profiles that are in an installed application.  Customize the profiles with information for run time and bind static SQL packages in a database.  Refer to the DB2 information center documentation for the commands db2sqljcustomize and db2sqljbind. """
	...

def propagatePolicyToJACCProvider(*args, **kwargs):
	""" Propagate the security policies of the applications to the JACC provider. """
	...

def publishSIBWSInboundService(*args, **kwargs):
	""" Publish an inbound service to a UDDI registry. """
	...

def purgeUserFromAuthCache(*args, **kwargs):
	""" Purges a user from the auth cache for a security domain; if no security domain is specified, the user will be purged from the admin security domain """
	...

def queryCACertificate(*args, **kwargs):
	""" Queries a certificate authority (CA) to see if a certificate is complete. """
	...

def queryJobs(*args, **kwargs):
	""" Query for previously submitted jobs. """
	...

def queryManagedNodeGroups(*args, **kwargs):
	""" This command is used to query groups of Managed Nodes. (deprecated) """
	...

def queryManagedNodes(*args, **kwargs):
	""" Queries for all the managed nodes registered with the job manager. (deprecated) """
	...

def queryManagedResources(*args, **kwargs):
	""" Queries for all managed resources. """
	...

def querySCClientCacheConfiguration(*args, **kwargs):
	""" List the SC cache configuration """
	...

def querySCClientCacheCustomConfiguration(*args, **kwargs):
	""" List the SC custom properties """
	...

def querySTSDefaultTokenType(*args, **kwargs):
	""" Query the STS for the default token type. """
	...

def querySTSTokenTypeConfigurationCustomProperties(*args, **kwargs):
	""" Query the STS for the values of the custom properties for a given token type. """
	...

def querySTSTokenTypeConfigurationDefaultProperties(*args, **kwargs):
	""" Query the STS for the values of the default properties for a given token type. """
	...

def queryServerAvailability(*args, **kwargs):
	""" checks the UCF server availability indicator on specified server """
	...

def queryTargetGroups(*args, **kwargs):
	""" This command is used to query groups of targets. """
	...

def queryTargets(*args, **kwargs):
	""" Queries for all the Targets registered with the job manager. """
	...

def queryWSSDistributedCacheConfig(*args, **kwargs):
	""" List the Web Services Security distributed cache configuration properties """
	...

def queryWSSDistributedCacheCustomConfig(*args, **kwargs):
	""" List Web Services Security distributed cache configuration custom properties """
	...

def receiveCertificate(*args, **kwargs):
	""" Receive a certificate from a file. """
	...

def reconfigureTAM(*args, **kwargs):
	""" This command configures embedded Tivoli Access Manager on the WebSphere Application Server node or nodes specified. """
	...

def recoverMEConfig(*args, **kwargs):
	""" Use this command if there is no configuration data of crashed ME and user needs to recover persistent SBus ME data from message store. """
	...

def refreshCellForIntelligentManagement(*args, **kwargs):
	""" Command to refresh cell connectors for Intelligent Management """
	...

def refreshSIBWSInboundServiceWSDL(*args, **kwargs):
	""" Refresh the WSDL definition for an inbound service. """
	...

def refreshSIBWSOutboundServiceWSDL(*args, **kwargs):
	""" Refresh the WSDL definition for an outbound service. """
	...

def refreshSTS(*args, **kwargs):
	""" Reload the STS configuration dynamically. """
	...

def regenPasswordEncryptionKey(*args, **kwargs):
	""" Generates a new AES password encryption key, sets it as the current key for the encryption, and then updates the passwords with the new key. This command is disabled when the custom KeyManager class is used. """
	...

def registerApp(*args, **kwargs):
	""" Use this command to register a middleware application already installed on a server. """
	...

def registerHost(*args, **kwargs):
	""" Registers a host with the job manager. """
	...

def registerWithJobManager(*args, **kwargs):
	""" Register a managed node with a JobManager """
	...

def removeActionFromRule(*args, **kwargs):
	""" Use this command to remove an action from a rule. """
	...

def removeAutomaticEJBTimers(*args, **kwargs):
	""" This command removes automatically created persistent EJBTimers for a specific application or module on a specific server.  Refer to the product InfoCenter for scenarios where this command might be used. """
	...

def removeConditionalTraceRuleForIntelligentManagement(*args, **kwargs):
	""" Remove conditional trace for Intelligent Management """
	...

def removeCoreGroupBridgeInterface(*args, **kwargs):
	""" Delete bridge interfaces associated with a specified core group, node and server. """
	...

def removeDefaultAction(*args, **kwargs):
	""" Use this command to remove a default action from a ruleset. """
	...

def removeDefaultRoles(*args, **kwargs):
	""" Remove all default roles """
	...

def removeDestinationRoles(*args, **kwargs):
	""" Removes all destination roles defined for the specified destination in the specified bus. """
	...

def removeDisabledSessionCookie(*args, **kwargs):
	""" Removes a cookie configuration so that applications will be able to programmatically modify """
	...

def removeExternalBundleRepository(*args, **kwargs):
	""" Removes the named external bundle repository from the configuration. """
	...

def removeFeaturesFromServer(*args, **kwargs):
	""" Remove feature pack or stack product features from existing server """
	...

def removeForeignBusRoles(*args, **kwargs):
	""" Remove all foreign bus roles defined for the specified bus """
	...

def removeForeignServersFromDynamicCluster(*args, **kwargs):
	""" Remove foreign servers from dynamic cluster """
	...

def removeFromPolicySetAttachment(*args, **kwargs):
	""" The removeFromPolicySetAttachment command removes resources that apply to a policy set attachment. """
	...

def removeGroupFromAllRoles(*args, **kwargs):
	""" Removes a group from all roles defined. """
	...

def removeGroupFromBusConnectorRole(*args, **kwargs):
	""" Remove a group's permission to connect to the specified bus. """
	...

def removeGroupFromDefaultRole(*args, **kwargs):
	""" Removes a group from the specified role in the default security space role. """
	...

def removeGroupFromDestinationRole(*args, **kwargs):
	""" Removes a group from the specified destination role for the specified destination. """
	...

def removeGroupFromForeignBusRole(*args, **kwargs):
	""" Removes a group from the specified foreign bus role for the bus specified """
	...

def removeGroupFromTopicRole(*args, **kwargs):
	""" Removes a groups permission to access the topic for the specified role. """
	...

def removeGroupFromTopicSpaceRootRole(*args, **kwargs):
	""" Removes a groups permission to access the topic space for the specified role. """
	...

def removeGroupsFromAdminRole(*args, **kwargs):
	""" Remove groupids from one or more admin role in the AuthorizationGroup. """
	...

def removeGroupsFromAuditRole(*args, **kwargs):
	""" Remove groupids from one or more audit role in the AuthorizationGroup. """
	...

def removeGroupsFromNamingRole(*args, **kwargs):
	""" Remove groups or special subjects or both from a naming role """
	...

def removeIdMgrGroupsFromRole(*args, **kwargs):
	""" Removes the groups from the specified virtual member manager role. If value for groupId parameter is specified as "*" all groups mapped for the role are removed. """
	...

def removeIdMgrLDAPBackupServer(*args, **kwargs):
	""" Removes a backup LDAP server. """
	...

def removeIdMgrUsersFromRole(*args, **kwargs):
	""" Removes the users from the specified virtual member manager role. If value for userId parameter is specified as "*" all users mapped for the role are removed. """
	...

def removeJaspiProvider(*args, **kwargs):
	""" Remove the given authentication provider(s) from the security configuration. """
	...

def removeJobSchedulerProperty(*args, **kwargs):
	""" remove a property from the job scheduler """
	...

def removeLocalRepositoryBundle(*args, **kwargs):
	""" Removes a bundle from the internal bundle repository. """
	...

def removeLocalRepositoryBundles(*args, **kwargs):
	""" Removes one or more bundles from the internal bundle repository in a single operation. """
	...

def removeLongRunningSchedulerProperty(*args, **kwargs):
	""" (Deprecated) remove a property from the long-running scheduler. Use removeJobSchedulerProperty. """
	...

def removeMemberFromGroup(*args, **kwargs):
	""" Removes a member (user or group) from a group. """
	...

def removeMiddlewareAppWebModule(*args, **kwargs):
	""" Use this command to remove a web module from a middleware application. """
	...

def removeMiddlewareTarget(*args, **kwargs):
	""" Use this command to remove a deployment target from a middleware application. """
	...

def removeNodeFromNodeGroups(*args, **kwargs):
	""" remove a given node from node groups """
	...

def removeNodeGroup(*args, **kwargs):
	""" remove a node group from the configuration. """
	...

def removeNodeGroupMember(*args, **kwargs):
	""" remove a member from the node group. """
	...

def removeNodeGroupProperty(*args, **kwargs):
	""" remove a property from a node group """
	...

def removeOSGiExtension(*args, **kwargs):
	""" Removes an extension from the composition unit. """
	...

def removeOSGiExtensions(*args, **kwargs):
	""" Removes multiple extensions from the composition unit. """
	...

def removePluginPropertyForIntelligentManagement(*args, **kwargs):
	""" Remove plug-in property for Intelligent Management """
	...

def removeProductInfo(*args, **kwargs):
	""" Remove feature pack or stack product information from product info. """
	...

def removeResourceFromAuthorizationGroup(*args, **kwargs):
	""" Remove resources from an existing authorization group. """
	...

def removeResourceFromSecurityDomain(*args, **kwargs):
	""" Remove a resource from a security domain. """
	...

def removeRoutingPolicyRoutingRule(*args, **kwargs):
	""" Use this command to remove a routing rule from an existing workclass """
	...

def removeRoutingRule(*args, **kwargs):
	""" Use this command to remove a routing policy rule. """
	...

def removeRuleFromRuleset(*args, **kwargs):
	""" Use this command to remove a rule from a ruleset. """
	...

def removeSIBBootstrapMember(*args, **kwargs):
	""" Removes a nominated bootstrap server or cluster from the list of nominated bootstrap members for the bus. """
	...

def removeSIBPermittedChain(*args, **kwargs):
	""" Removes the specified chain from the list of permitted chains for the specified bus. """
	...

def removeSIBWSInboundPort(*args, **kwargs):
	""" Remove an inbound port. """
	...

def removeSIBWSOutboundPort(*args, **kwargs):
	""" Remove an outbound port. """
	...

def removeSIBusMember(*args, **kwargs):
	""" Remove a member from a bus. """
	...

def removeServicePolicyRoutingRule(*args, **kwargs):
	""" Use this command to remove a routing rule from an existing workclass """
	...

def removeServiceRule(*args, **kwargs):
	""" Use this command to remove a service policy rule. """
	...

def removeTemplates(*args, **kwargs):
	""" Removes set of templates that are not required anymore when a feature pack or stack product is removed. """
	...

def removeTrustedRealms(*args, **kwargs):
	""" Remove realms from the trusted realm list """
	...

def removeUnmanagedNode(*args, **kwargs):
	""" Use this command to remove an unmanaged node from a cell. """
	...

def removeUserFromAllRoles(*args, **kwargs):
	""" Removes a user from all roles defined. """
	...

def removeUserFromBusConnectorRole(*args, **kwargs):
	""" Remove a user's permission to connect to the specified bus. """
	...

def removeUserFromDefaultRole(*args, **kwargs):
	""" Removes a user from the specified role in the default security space role. """
	...

def removeUserFromDestinationRole(*args, **kwargs):
	""" Removes a user from the specified destination role for the specified destination. """
	...

def removeUserFromForeignBusRole(*args, **kwargs):
	""" Removes a user from the specified foreign bus role for the bus specified """
	...

def removeUserFromTopicRole(*args, **kwargs):
	""" Removes a users permission to access the topic for the specified role. """
	...

def removeUserFromTopicSpaceRootRole(*args, **kwargs):
	""" Removes a users permission to access the topic space for the specified role. """
	...

def removeUsersFromAdminRole(*args, **kwargs):
	""" Remove userids from one or more admin role in the AuthorizationGroup. """
	...

def removeUsersFromAuditRole(*args, **kwargs):
	""" Remove userids from one or more audit role in the AuthorizationGroup. """
	...

def removeUsersFromNamingRole(*args, **kwargs):
	""" Remove users from a naming role. """
	...

def removeVariable(*args, **kwargs):
	""" Remove a variable definition from the system. A variable is a configuration property that can be used to provide a parameter for some values in the system. """
	...

def removeWSGWTargetService(*args, **kwargs):
	""" removeWSGWTargetService.description """
	...

def removeWebServerRoutingRule(*args, **kwargs):
	""" Use this command to remove an existing routing rule. """
	...

def renameCell(*args, **kwargs):
	""" Change the name of the cell.  This command can only run in local mode i.e.with wsadmin conntype NONE.1. Backing up your node configuration with the backupConfig tool fromprofile_root/bin directory is recommended before you change the cell name forthat node using the renameCell command.  If you are not satisfied with theresults of the renameCell command and if the renameCell command executionfailed unexpectedly, you use the restoreConfig tool to restore your backupconfiguration.2. Back up profile_root/bin/setupCmdLine script file. The command updates thecell name in this file with the new cell name as well, but is unable to changeit back if a user decides to discard the configuration change resulting fromthis command execution. If you decide to do so, you will need to restore thefile after you discard the configuration change; otherwise, you won't be ableto start a server in this profile. """
	...

def renameIdMgrRealm(*args, **kwargs):
	""" Renames the specified realm configuration. """
	...

def renameNode(*args, **kwargs):
	""" renameNode """
	...

def renewAuditCertificate(*args, **kwargs):
	""" The task will renew a certificate as a self-signed based off the previous certificates attributes such as the common name, key size and validity. """
	...

def renewCertificate(*args, **kwargs):
	""" Renew a Certificate with a newly generated certificate. """
	...

def replaceCertificate(*args, **kwargs):
	""" Replace a Certificate with a different certificate. """
	...

def reportConfigInconsistencies(*args, **kwargs):
	""" Checks the configuation repository and reports any structural inconsistencies """
	...

def reportConfiguredPorts(*args, **kwargs):
	""" Generates a report of the ports configured in the cell """
	...

def republishEDMessages(*args, **kwargs):
	""" Use the command to republish messages from the exception destination to the original destination. The messages are picked based on the criteria provided in the command execution. """
	...

def requestCACertificate(*args, **kwargs):
	""" Sends a request to a certificate authority to create a certificate authority (CA) personal certificate. """
	...

def resetAuditSystemFailureAction(*args, **kwargs):
	""" Resets the audit system failure policy to the default, NOWARN. """
	...

def resetIdMgrConfig(*args, **kwargs):
	""" Reloads the virtual member manager configuration from the virtual member manager configuration file. """
	...

def restoreCheckpoint(*args, **kwargs):
	""" Restore the named checkpoint specified by the "checkpointName" """
	...

def resumeJob(*args, **kwargs):
	""" Resumes a previously submitted job. """
	...

def retrieveSignerFromPort(*args, **kwargs):
	""" Retrieve a signer certificate from a port and add it to the KeyStore. """
	...

def retrieveSignerInfoFromPort(*args, **kwargs):
	""" Retrieve signer information from a port. """
	...

def revokeCACertificate(*args, **kwargs):
	""" Sends a request to a certificate authority (CA) to revoke the certificate. """
	...

def rolloutEdition(*args, **kwargs):
	""" Roll-out an edition. """
	...

def searchGroups(*args, **kwargs):
	""" Searches groups. """
	...

def searchUsers(*args, **kwargs):
	""" Searches PersonAccounts. """
	...

def setActiveAuthMechanism(*args, **kwargs):
	""" This command sets the active authentication mechanism attribute in the security configuration. """
	...

def setAdminActiveSecuritySettings(*args, **kwargs):
	""" Sets the security attributes on the global administrative security configuration. """
	...

def setAdminProtocol(*args, **kwargs):
	""" Allows the user to set Administrative Protocol for a server or cell """
	...

def setAdminProtocolEnabled(*args, **kwargs):
	""" Sets an Admin Protocol enabled for a server or cell """
	...

def setAppActiveSecuritySettings(*args, **kwargs):
	""" Sets the application level security active settings. """
	...

def setAuditEmitterFilters(*args, **kwargs):
	""" Sets a list of references to defined filters for the supplied audit service provider. """
	...

def setAuditEventFactoryFilters(*args, **kwargs):
	""" Sets a list of references to defined filters for the supplied event factory. """
	...

def setAuditSystemFailureAction(*args, **kwargs):
	""" Returns the state of Security Auditing. """
	...

def setAuditorId(*args, **kwargs):
	""" Sets the auditor identity in the audit.xml file. """
	...

def setAuditorPwd(*args, **kwargs):
	""" Sets the auditor password in the audit.xml file. """
	...

def setAutoCheckpointDepth(*args, **kwargs):
	""" Set the automatic checkpoints depth value """
	...

def setAutoCheckpointEnabled(*args, **kwargs):
	""" Enable or disable the automatic checkpoints """
	...

def setBinding(*args, **kwargs):
	""" The setBinding command updates the binding configuration for a specified policy type and scope. Use this command to add a server-specific binding, update an attachment to use a custom binding, edit binding attributes, or remove a binding. """
	...

def setCheckpointLocation(*args, **kwargs):
	""" Set the directory path where the checkpoints are stored """
	...

def setClientDynamicPolicyControl(*args, **kwargs):
	""" The setClientDynamicPolicyControl command sets the WSPolicy client acquisition information for a specified resource within an application. """
	...

def setCompUnitTargetAutoStart(*args, **kwargs):
	""" Enable or disable "autostart" """
	...

def setDefaultBindings(*args, **kwargs):
	""" The setDefaultBindings command updates the default binding names for a specified domain or server. """
	...

def setDefaultContextService(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultContextService. """
	...

def setDefaultDataSource(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultDataSource. """
	...

def setDefaultJMSConnectionFactory(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultJMSConnectionFactory. """
	...

def setDefaultManagedExecutor(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultManagedExecutorService. """
	...

def setDefaultManagedScheduledExecutor(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultManagedScheduledExecutorService. """
	...

def setDefaultManagedThreadFactory(*args, **kwargs):
	""" Set the JNDI name that is bound to java:comp/DefaultManagedThreadFactory. """
	...

def setDefaultSIBWSOutboundPort(*args, **kwargs):
	""" Set the default outbound port for an outbound service. """
	...

def setDefaultTraceRuleForIntelligentManagement(*args, **kwargs):
	""" Set default trace for Intelligent Management """
	...

def setDynamicClusterMaxInstances(*args, **kwargs):
	""" Set dynamic cluster maximum number of cluster instances """
	...

def setDynamicClusterMaxNodes(*args, **kwargs):
	""" Set dynamic cluster maximum number of cluster nodes """
	...

def setDynamicClusterMembershipPolicy(*args, **kwargs):
	""" Set dynamic cluster membership policy """
	...

def setDynamicClusterMinInstances(*args, **kwargs):
	""" Set dynamic cluster minimum number of cluster instances """
	...

def setDynamicClusterMinNodes(*args, **kwargs):
	""" Set dynamic cluster minimum number of cluster nodes """
	...

def setDynamicClusterOperationalMode(*args, **kwargs):
	""" Set dynamic cluster operational mode """
	...

def setDynamicClusterVerticalInstances(*args, **kwargs):
	""" Set dynamic cluster vertical stacking of instances on node """
	...

def setEmailList(*args, **kwargs):
	""" Sets the notification email list for the configured audit notification. """
	...

def setGenericJVMArguments(*args, **kwargs):
	""" Set Java virtual machine (JVM) Generic JVM Arguments Size """
	...

def setGlobalSecurity(*args, **kwargs):
	""" The administrative security field in the security.xml file is updated based on the user input of true or false. """
	...

def setIdMgrCustomProperty(*args, **kwargs):
	""" Sets/adds/deletes custom property to a repository configuration. If value is not specified or an empty string then the property will be deleted from the repository configuration. If name does not exist then it will be added, if a value is specified. If name is "*" then all the custom properties will be deleted. """
	...

def setIdMgrDefaultRealm(*args, **kwargs):
	""" Sets the name of the default realm. """
	...

def setIdMgrEntryMappingRepository(*args, **kwargs):
	""" Sets or updates an entry mapping repository configuration. """
	...

def setIdMgrLDAPAttrCache(*args, **kwargs):
	""" Sets up the LDAP attribute cache configuration. """
	...

def setIdMgrLDAPContextPool(*args, **kwargs):
	""" Sets up the LDAP context pool configuration. """
	...

def setIdMgrLDAPGroupConfig(*args, **kwargs):
	""" Sets up the LDAP group configuration. """
	...

def setIdMgrLDAPSearchResultCache(*args, **kwargs):
	""" Sets up the LDAP search result cache configuration. """
	...

def setIdMgrPropertyExtensionRepository(*args, **kwargs):
	""" Sets or updates the property mapping repository configuration. """
	...

def setIdMgrRealmDefaultParent(*args, **kwargs):
	""" Sets the default parent of an entity type in a specified realm. If mapping does not exist it is added, else the mapping is updated. If realm name is not specified, default realm is used. """
	...

def setIdMgrRealmURAttrMapping(*args, **kwargs):
	""" Sets the user registry user or group attribute mapping for a realm. """
	...

def setIdMgrUseGlobalSchemaForModel(*args, **kwargs):
	""" Sets the global schema option for the data model in a multiple security domain environment, where global schema refers to the schema of the admin domain. """
	...

def setInheritDefaultsForDestination(*args, **kwargs):
	""" Allows the override for inheritance for an individual destination.  Setting the "inherit" value to true will allow the destination to inherit from the default values. """
	...

def setInheritReceiverForTopic(*args, **kwargs):
	""" Allows the override for receiver inheritance for an individual topic on a specified topic space.  Setting the "inherit" value to true will allow the topic to inherit from the default values. """
	...

def setInheritSenderForTopic(*args, **kwargs):
	""" Allows the override for sender inheritance for an individual topic on a specified topic space.  Setting the "inherit" value to true will allow the topic to inherit from the default values. """
	...

def setJVMDebugMode(*args, **kwargs):
	""" Set Java virtual machine (JVM) Debug Mode """
	...

def setJVMInitialHeapSize(*args, **kwargs):
	""" Set Java virtual machine (JVM) Initial Heap Size """
	...

def setJVMMaxHeapSize(*args, **kwargs):
	""" Set Java virtual machine (JVM) Maximum Heap Size """
	...

def setJVMMode(*args, **kwargs):
	""" Set the JVM mode to either 64-bit or 31-bit for a release prior to V9. Starting from V9, only 64-bit is supported. """
	...

def setJVMProperties(*args, **kwargs):
	""" Set Java virtual machine (JVM) configuration for the application server. """
	...

def setJVMSystemProperties(*args, **kwargs):
	""" set Java virtual machine (JVM) system property for the application server's process. """
	...

def setLTPATimeout(*args, **kwargs):
	""" Set the LTPA authentication mechanism timeout from global security or an application security domain. """
	...

def setMaintenanceMode(*args, **kwargs):
	""" sets maintenance mode indicator on specified server """
	...

def setNodeDefaultSDK(*args, **kwargs):
	""" Set the default SDK by name or by location for the node """
	...

def setPolicyType(*args, **kwargs):
	""" The setPolicyType command updates the attributes of a specified policy. """
	...

def setPolicyTypeAttribute(*args, **kwargs):
	""" The setPolicyTypeAttribute command sets an attribute for a specific policy. """
	...

def setPreference(*args, **kwargs):
	""" Command to set a user preference """
	...

def setProcessDefinition(*args, **kwargs):
	""" Set the process definition of an application server. """
	...

def setProviderPolicySharingInfo(*args, **kwargs):
	""" The setProviderPolicySharingInfo command sets the WSPolicy provider sharing information for a specified resource within an application. """
	...

def setResourceProperty(*args, **kwargs):
	""" This command sets the value of a specified property defined on a resource provider such as JDBCProvider or a connection factory such as DataSource or JMSConnectionFactory. If the property with specified key is defined already, then this command overrides the value. If none property with specified key is defined yet, then this command will add the property with specified key and value. """
	...

def setRuntimeRegistrationProperties(*args, **kwargs):
	""" Set certain runtime properties for devices and job managers. Caution: a null ID implies each and everyone """
	...

def setSAMLIssuerConfigInBinding(*args, **kwargs):
	""" Set SAML Issuer Configuration in the specified bindings as custom properties """
	...

def setSendEmail(*args, **kwargs):
	""" Sets the option to send an audit notification email. """
	...

def setServerInstance(*args, **kwargs):
	""" Set Server Instance configuration. This command only applies to the z/OS platform. """
	...

def setServerSDK(*args, **kwargs):
	""" Set server SDK by name or by location """
	...

def setServerSecurityLevel(*args, **kwargs):
	""" Configure the security level for a secure proxy or management server. """
	...

def setTemplateProperty(*args, **kwargs):
	""" Set a property in server template's metadata. Use this command with caution. Changing a template metadata property incorrectly will result in new server creation failure. """
	...

def setTraceSpecification(*args, **kwargs):
	""" Set the trace specification for the server. If the server is running new trace specification takes effect immediately. This command also saves the trace specification in configuration. """
	...

def setUseRegistryServerId(*args, **kwargs):
	""" The useRegistryServerId security field in userRegistry object in the security.xml file is updated based on the user input of true or false. """
	...

def setVariable(*args, **kwargs):
	""" Set the value for a variable. A variable is a configuration property that can be used to provide a parameter for some values in the system. """
	...

def setWebServerRoutingRulesProperty(*args, **kwargs):
	""" Use this command to set properties associated with routing rules. """
	...

def setupIdMgrDBTables(*args, **kwargs):
	""" Creates and populates tables for database in virtual member manager. """
	...

def setupIdMgrEntryMappingRepositoryTables(*args, **kwargs):
	""" Creates and populates tables for entry mapping database in virtual member manager. """
	...

def setupIdMgrPropertyExtensionRepositoryTables(*args, **kwargs):
	""" Creates and populates tables for a property extension database in virtual member manager. """
	...

def showAuditLogEncryptionInfo(*args, **kwargs):
	""" Displays information about the keystore used during Audit Record encryption """
	...

def showExternalBundleRepository(*args, **kwargs):
	""" Shows the configured parameters of the named external bundle repository. """
	...

def showIdMgrConfig(*args, **kwargs):
	""" Shows the current configuration with unsaved changes. """
	...

def showJAXWSHandler(*args, **kwargs):
	""" Show the attributes of a JAX-WS Handler """
	...

def showJAXWSHandlerList(*args, **kwargs):
	""" Show the attributes of a JAX-WS Handler List """
	...

def showJPASpecLevel(*args, **kwargs):
	""" Displays the active JPA specification level for a Server or ServerCluster.The operation requires either an ObjectName referencing the target object, or parameters identifying the target node and server. """
	...

def showJVMProperties(*args, **kwargs):
	""" List Java virtual machine (JVM) configuration for the application server's process. """
	...

def showJVMSystemProperties(*args, **kwargs):
	""" Show Java virtual machine (JVM) system properties for the application server.'s process. """
	...

def showJaxrsProvider(*args, **kwargs):
	""" Displays the active JAXRS Provider for a Server or ServerCluster.The operation requires either an ObjectName referencing the target object, or parameters identifying the target node and server. """
	...

def showJobSchedulerAttributes(*args, **kwargs):
	""" list all job scheduler attributes """
	...

def showLMService(*args, **kwargs):
	""" Use the "showLMService" command to show the attributes of a local mapping service. """
	...

def showLocalRepositoryBundle(*args, **kwargs):
	""" Shows the information about a bundle in the internal bundle repository. """
	...

def showLongRunningSchedulerAttributes(*args, **kwargs):
	""" (Deprecated) list all long-running scheduler attributes. Use showJobSchedulerAttributes. """
	...

def showMiddlewareApp(*args, **kwargs):
	""" Use this command to show the attributes of a middleware application. """
	...

def showMiddlewareDescriptorInformation(*args, **kwargs):
	""" Use this command to display the contents of the specified middleware descriptor """
	...

def showMiddlewareServerInfo(*args, **kwargs):
	""" Use this command to show information on the middleware server """
	...

def showProcessDefinition(*args, **kwargs):
	""" Show the process definition of the server """
	...

def showResourceProperties(*args, **kwargs):
	""" This command list all the property values defined on a resource provider such as JDBCProvider or a connection factory such as DataSource or JMSConnectionFactory. """
	...

def showSAMLIdpPartner(*args, **kwargs):
	""" This command displays the SAML TAI IdP partner in the security configuration. If an idpId is not specified, all the SAML TAI IdP partners are displayed. """
	...

def showSAMLTAISSO(*args, **kwargs):
	""" This command displays the SAML TAI SSO in the security configuration. If an ssoId is not specified, all the SAML TAI SSO service providers are displayed. """
	...

def showSIBDestination(*args, **kwargs):
	""" Show a bus destination's attributes. """
	...

def showSIBEngine(*args, **kwargs):
	""" Show a messaging engine's attributes. """
	...

def showSIBForeignBus(*args, **kwargs):
	""" Show detail for a SIB foreign bus. """
	...

def showSIBJMSActivationSpec(*args, **kwargs):
	""" Show the attributes of target SIB JMS activation specification. """
	...

def showSIBJMSConnectionFactory(*args, **kwargs):
	""" Return a list containing the SIB JMS connection factory's attribute names and values. """
	...

def showSIBJMSQueue(*args, **kwargs):
	""" Return a list containing the SIB JMS queue's attribute names and values. """
	...

def showSIBJMSTopic(*args, **kwargs):
	""" Return a list containing the SIB JMS topic's attribute names and values. """
	...

def showSIBLink(*args, **kwargs):
	""" Show detail for a SIB link. """
	...

def showSIBMQLink(*args, **kwargs):
	""" Show detail for a WebSphere MQ link. """
	...

def showSIBMediation(*args, **kwargs):
	""" Show the attributes of a mediation. """
	...

def showSIBWMQServer(*args, **kwargs):
	""" Display a named WebSphere MQ server's attributes. """
	...

def showSIBWMQServerBusMember(*args, **kwargs):
	""" Display a named WebSphere MQ server bus members attributes. """
	...

def showSIBus(*args, **kwargs):
	""" Show the attributes of a bus. """
	...

def showSIBusMember(*args, **kwargs):
	""" Show a member from a bus. """
	...

def showServerInfo(*args, **kwargs):
	""" show detailed information of a specified server. """
	...

def showServerInstance(*args, **kwargs):
	""" Show Server Instance configuration. This command only applies to the z/OS platform. """
	...

def showServerTypeInfo(*args, **kwargs):
	""" Show server type information. """
	...

def showServiceMap(*args, **kwargs):
	""" Use the "showServiceMap" command to show the attributes of a service map. """
	...

def showSpnego(*args, **kwargs):
	""" This command displays the SPNEGO Web authentication in the security configuration. """
	...

def showSpnegoFilter(*args, **kwargs):
	""" This command displays the SPNEGO Web authentication Filter in the security configuration. If a host name is not specified, all the SPNEGO Web authentication Filters are displayed. """
	...

def showSpnegoTAIProperties(*args, **kwargs):
	""" This command displays the SPNEGO TAI properties in the security configuration. If an spnId is not specified, all the SPNEGO TAI properties are displayed. """
	...

def showTemplateInfo(*args, **kwargs):
	""" A command that displays all the Metadata about a given template. """
	...

def showVariables(*args, **kwargs):
	""" List variable values under a scope. """
	...

def showWMQ(*args, **kwargs):
	""" Shows all IBM MQ resource adapter and IBM MQ messaging provider settings which can be set by the manageWMQ command. """
	...

def showWMQActivationSpec(*args, **kwargs):
	""" Shows the attributes of the IBM MQ Activation Specification provided to the command. """
	...

def showWMQConnectionFactory(*args, **kwargs):
	""" Shows the attributes of the IBM MQ Connection Factory provided to the command. """
	...

def showWMQQueue(*args, **kwargs):
	""" Shows the attributes of the IBM MQ Queue provided to the command. """
	...

def showWMQTopic(*args, **kwargs):
	""" Shows the attributes of the IBM MQ Topic provided to the command. """
	...

def showWSNAdministeredSubscriber(*args, **kwargs):
	""" Show the properties of a WSNAdministeredSubscriber object in a human readable form. """
	...

def showWSNService(*args, **kwargs):
	""" Show the properties of a WSNService object in a human readable form. """
	...

def showWSNServicePoint(*args, **kwargs):
	""" Show the properties of a WSNServicePoint object in a human readable form. """
	...

def showWSNTopicDocument(*args, **kwargs):
	""" Show the properties of a WSNTopicDocument in a human readable form. """
	...

def showWSNTopicNamespace(*args, **kwargs):
	""" Show the properties of a WSNTopicNamespace object in a human readable form. """
	...

def startBLA(*args, **kwargs):
	""" Start all composition units of a specified business-level application. """
	...

def startCertificateExpMonitor(*args, **kwargs):
	""" Start the Certificate Expiration Monitor. """
	...

def startLMService(*args, **kwargs):
	""" Use the "startLMService" command to start a stopped local mapping service. """
	...

def startMiddlewareServer(*args, **kwargs):
	""" Use this command to start a middleware server """
	...

def startPollingJobManager(*args, **kwargs):
	""" Start a managed node's polling against a JobManager, possibly after a certain delay """
	...

def startWasCEApp(*args, **kwargs):
	""" Use this command to start a WAS CE application. """
	...

def stopBLA(*args, **kwargs):
	""" Stop all composition units of a specified business-level application. """
	...

def stopLMService(*args, **kwargs):
	""" Use the "stopLMService" command to stop a started local mapping service. """
	...

def stopMiddlewareServer(*args, **kwargs):
	""" Use this command to stop a middleware server """
	...

def stopPollingJobManager(*args, **kwargs):
	""" Stop a managed node's polling against a JobManager """
	...

def stopWasCEApp(*args, **kwargs):
	""" Use this command to stop a WAS CE application. """
	...

def submitJob(*args, **kwargs):
	""" Submits a new job for execution. """
	...

def suspendJob(*args, **kwargs):
	""" Suspends a previously submitted job. """
	...

def testDynamicClusterMembershipPolicy(*args, **kwargs):
	""" Test the dynamic cluster membership policy to see what nodes will be returned """
	...

def transferAttachmentsForPolicySet(*args, **kwargs):
	""" The transferAttachmentsForPolicySet command transfers all attachments from one policy set to another policy set. """
	...

def unassignSTSEndpointTokenType(*args, **kwargs):
	""" Disassociate an endpoint from its token type. """
	...

def unconfigureAuthzConfig(*args, **kwargs):
	""" Removes the external JAAC authorization provider """
	...

def unconfigureCSIInbound(*args, **kwargs):
	""" Removes CSI inbound information from an application security domain. """
	...

def unconfigureCSIOutbound(*args, **kwargs):
	""" Removes CSI outbound information from an application security domain. """
	...

def unconfigureInterceptor(*args, **kwargs):
	""" Removes an interceptor from global security configuration or from a security domain. """
	...

def unconfigureJAASLogin(*args, **kwargs):
	""" Unconfigures a JAAS login in an application security domain.  This removes the JAAS login object and all it's entries. """
	...

def unconfigureJAASLoginEntry(*args, **kwargs):
	""" Unconfigures a JAAS login entry in the administrative security configuration or in an application security domain.  Note: note all JAAS login entries can be removed. """
	...

def unconfigureJaspi(*args, **kwargs):
	""" Removes the Jaspi configuration from a security domain. """
	...

def unconfigureLoginModule(*args, **kwargs):
	""" Unconfigures a login module from a login entry in the administrative security configuration or in an application security domain. """
	...

def unconfigureSpnego(*args, **kwargs):
	""" This command unconfigures SPNEGO Web authentication in the security configuration. """
	...

def unconfigureTAM(*args, **kwargs):
	""" This command unconfigures embedded Tivoli Access Manager on the WebSphere Application Server node or nodes specified. """
	...

def unconfigureTAMTAI(*args, **kwargs):
	""" This command unconfigures the embedded Tivoli Access Manager Trust Association Interceptor with classname TAMTrustAsociationInterceptorPlus. This task does not include removing any custom properties from the security configuration """
	...

def unconfigureTAMTAIPdjrte(*args, **kwargs):
	""" This command performs the tasks necessary to unconfigure the Tivoli Access Manager Runtime for Java. The specific tasks run are PDJrteCfg and SvrSslCfg. """
	...

def unconfigureTAMTAIProperties(*args, **kwargs):
	""" This command removes the custom properties from the security configuration for the embedded Tivoli Access Manager Trust Association Interceptor with classname TAMTrustAsociationInterceptorPlus. """
	...

def unconfigureTrustAssociation(*args, **kwargs):
	""" Removes the trust association object from a security domain. """
	...

def unconfigureTrustedRealms(*args, **kwargs):
	""" Unconfigures an inbound or outbound trusted realms by removing the realm object from the configuration. """
	...

def unconfigureUserRegistry(*args, **kwargs):
	""" Unconfigure a user registry in the administrative security configuration or an application security domain. """
	...

def undeployWasCEApp(*args, **kwargs):
	""" Use this command to undeploy a WAS CE application from a server. """
	...

def uninstallMiddlewareApp(*args, **kwargs):
	""" Use this command to uninstall a middleware application. """
	...

def uninstallServiceMap(*args, **kwargs):
	""" Use the "uninstallServiceMap" command to uninstall a service map. """
	...

def unmediateSIBDestination(*args, **kwargs):
	""" Mediate a destination. """
	...

def unpublishSIBWSInboundService(*args, **kwargs):
	""" Unpublish an inbound service from a UDDI registry. """
	...

def unregisterApp(*args, **kwargs):
	""" Use this command to unregister a middleware application. """
	...

def unregisterHost(*args, **kwargs):
	""" Unregister a host from the job manager. """
	...

def unregisterWithJobManager(*args, **kwargs):
	""" Unregister a managed node from a JobManager """
	...

def unsetAppActiveSecuritySettings(*args, **kwargs):
	""" Unsets active security settings on a security domain.  The attribute is removed from the security domain configuration. """
	...

def unsetMaintenanceMode(*args, **kwargs):
	""" unsets maintenance mode indicator on specified server """
	...

def updateARSConfig(*args, **kwargs):
	""" Updates the installation/deployment of the Asynchronous Response Servlet which is used when JAX-WS client applications use the JAX-WS asynchronous API """
	...

def updateAppOnCluster(*args, **kwargs):
	""" Updates all cluster members about the application config changes. """
	...

def updateAsset(*args, **kwargs):
	""" Update an imported asset file. """
	...

def updateCluster(*args, **kwargs):
	""" Updates the configuration of an application server cluster. """
	...

def updateClusterMemberWeights(*args, **kwargs):
	""" Updates the weights of the specified cluster members. """
	...

def updateDistributedCacheProperty(*args, **kwargs):
	""" updateSeveralWSSDistributedCacheConfigCmdDesc """
	...

def updateGroup(*args, **kwargs):
	""" Updates the attributes of a group. """
	...

def updateIdMgrDBRepository(*args, **kwargs):
	""" Updates a database repository configuration. """
	...

def updateIdMgrFileRepository(*args, **kwargs):
	""" Updates a file repository configuration. """
	...

def updateIdMgrLDAPAttrCache(*args, **kwargs):
	""" Updates the LDAP attribute cache configuration. """
	...

def updateIdMgrLDAPBindInfo(*args, **kwargs):
	""" Dynamically updates the LDAP server bind information. If bindDN is specified bindPassword must be specified. If only id is specified then LDAP server information is refreshed. """
	...

def updateIdMgrLDAPContextPool(*args, **kwargs):
	""" Updates the LDAP context pool configuration. """
	...

def updateIdMgrLDAPEntityType(*args, **kwargs):
	""" Updates an existing LDAP entity type definition to an LDAP repository configuration. This command can be used to add more values to multivalued parameters. """
	...

def updateIdMgrLDAPGroupDynamicMemberAttr(*args, **kwargs):
	""" Updates a dynamic member attribute configuration of an LDAP group configuration. """
	...

def updateIdMgrLDAPGroupMemberAttr(*args, **kwargs):
	""" Updates a member attribute configuration of an LDAP group configuration. """
	...

def updateIdMgrLDAPRepository(*args, **kwargs):
	""" Updates an LDAP repository configuration. """
	...

def updateIdMgrLDAPSearchResultCache(*args, **kwargs):
	""" Updates the LDAP search result cache configuration. """
	...

def updateIdMgrLDAPServer(*args, **kwargs):
	""" Updates an LDAP server configuration of the LDAP repository configuration. """
	...

def updateIdMgrRealm(*args, **kwargs):
	""" Updates the configuration of the specified realm. """
	...

def updateIdMgrRepository(*args, **kwargs):
	""" Updates the configuration of the specified repository. To add multiple values to a multivalued parameter, call this command repeatedly. """
	...

def updateIdMgrRepositoryBaseEntry(*args, **kwargs):
	""" Updates a base entry for the specified repository. """
	...

def updateIdMgrSupportedEntityType(*args, **kwargs):
	""" Updates a supported entity type configuration. """
	...

def updateLMService(*args, **kwargs):
	""" Use the "updateLMService" command to update details about an existing local mapping service. """
	...

def updatePolicySet(*args, **kwargs):
	""" The updatePolicySet command enables you to input an attribute list to update the policy set. You can use this command to update all attributes for the policy set, or a subset of attributes. """
	...

def updatePolicySetAttachment(*args, **kwargs):
	""" The updatePolicySetAttachment command updates the resources that apply to a policy set attachment. """
	...

def updateRAR(*args, **kwargs):
	""" Update an existing resource adapter with the supplied RAR file and configure any new properties that exist on deployed objects within the resource adapter to be updated. 
    
    Before using the updateRAR command, use the compareResourceAdapterToRAR command to verify the RAR is compatible for upgrading the resource adapter, and use the findOtherRAsToUpdate command to determine the set of resources adapters that need be updated using the supplied RAR.
    """
	...

def updateSAMLIssuerConfig(*args, **kwargs):
	""" Update SAML Issuer Configuration data """
	...

def updateSCClientCacheConfiguration(*args, **kwargs):
	""" Update the SC cache configuration """
	...

def updateSCClientCacheCustomConfiguration(*args, **kwargs):
	""" Update the SC custom config """
	...

def updateSTSEndpointTokenType(*args, **kwargs):
	""" Update the assigned token type for an endpoint. If the local name parameter is omitted, the default token type is assumed. """
	...

def updateSTSTokenTypeConfiguration(*args, **kwargs):
	""" Update the configuration for an existing token type. Token type URIs must be unique. """
	...

def updateUser(*args, **kwargs):
	""" Updates the attributes of a user. """
	...

def updateWSSDistributedCacheConfig(*args, **kwargs):
	""" Update Web Services Security Distrubuted Cache configuration properties """
	...

def updateWSSDistributedCacheCustomConfig(*args, **kwargs):
	""" Update Web Services Security distributed cache configuration custom properties """
	...

def upgradeBindings(*args, **kwargs):
	""" The upgradeBindings command upgrades bindings of an older version to the current version. """
	...

def validateAdminName(*args, **kwargs):
	""" Validates the existence of the administrator name in the input user registry. """
	...

def validateConfigProperties(*args, **kwargs):
	""" Validate configuration properties in properites file """
	...

def validateEdition(*args, **kwargs):
	""" Prepares an edition for VALIDATION. """
	...

def validateKrbConfig(*args, **kwargs):
	""" Validates the Kerberos configuration data either in the global security configuration file security.xml or specified as an input parameters. """
	...

def validateLDAPConnection(*args, **kwargs):
	""" Validates the connection to the specified LDAP server. """
	...

def validatePolicySet(*args, **kwargs):
	""" The validatePolicySet command validates the policies in the policy set. """
	...

def validateSpnegoConfig(*args, **kwargs):
	""" Validates the SPNEGO Web authentication configuration. """
	...

def viewAsset(*args, **kwargs):
	""" View options for a specified asset. """
	...

def viewBLA(*args, **kwargs):
	""" View options for a specified business-level application. """
	...

def viewCompUnit(*args, **kwargs):
	""" View options for specified a composition unit of a business-level application. """
	...

