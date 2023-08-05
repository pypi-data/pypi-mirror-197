"""The `AdminControl` object enables the manipulation of MBeans running in a WebSphere server process.

!!! Note
    Many of the `AdminControl` commands support **two different sets of
    signatures**: one that accepts and returns **strings**, and one low-level
    set that works with **JMX** (_Java Management Extensions_) objects like ObjectName and AttributeList.
    
    In most situations, the string signatures are likely to be more useful,
    but JMX-object signature versions are supplied as well.  Each of these
    JMX-object signature commands has "_jmx" appended to the command name.
    Hence there is an "invoke" command, as well as a "invoke_jmx" command.

In addition to operational commands, the AdminControl object supports some utility commands for tracing, 
reconnecting with a server, and converting data types.

For more info see the [official documentation](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=scripting-commands-admincontrol-object-using-wsadmin).
"""

from typing import Union
from wsadmin_type_hints.typing_objects.object_name import RunningObjectName, RunningObjectTemplate
from wsadmin_type_hints.typing_objects.wsadmin_types import MultilineList


def completeObjectName(template: Union[RunningObjectName, RunningObjectTemplate], /) -> RunningObjectName:
    """
    Returns a string version of an **object name** that matches the `template`.
    For example, the template might be `type=Server,*`.
    
    !!! Warning
        If there are several MBeans that match the template, **only the first match** is returned.

        If what you need is the **full list** of MBeans that match the `template`, then
            use [`AdminControl.queryNames(...)`][wsadmin_type_hints.AdminControl.queryNames].

    Args:
        template (RunningObjectName | RunningObjectTemplate): The object name (already completed or a template) to complete.

    Returns:
        object_name(RunningObjectName): The complete object name of the running MBean.

    Example:
        ```pycon
        >>> print(AdminControl.completeObjectName('node=myNode,type=Server,*'))
            WebSphere:name=myServer,process=myServer,platform=proxy,node=myNode,j2eeType=J2EEServer,version=9.0.5.14,type=Server,mbeanIdentifier=cells/myCell/nodes/myNode/servers/myServer/server.xml#Server_1,cell=myCell,spec=1.0,processType=ManagedProcess
        ```

    Question: More testing needed
        The difference between `object_name` and `template` needs to be checked, since the official documentation does not provide any info on how to use them.
    """

def getAttribute(object_name: RunningObjectName, attribute: str, /) -> str:
    """Returns value of `attribute` for the MBean described by `object_name`.

    Args:
        object_name (RunningObjectName): The object name of the MBean.
        attribute (str): The name of the attribute to retrieve.
    
    Returns:
        value(str): The attribute value.

    !!! Tip
        For a list of available attributes, use the command [`AdminConfig.attributes(...)`][wsadmin_type_hints.AdminConfig.attributes] with the correct object type.

        For example, if you are trying to request the cluster name of a server but you don't remember the attribute name:
        ```pycon
        >>> server = AdminControl.completeObjectName('type=Server,*')
        >>> print(AdminConfig.attributes("Server"))
        adjustPort Boolean
        changeGroupAfterStartup String
        changeUserAfterStartup String
        clusterName String
        [...]
        >>> print(AdminControl.getAttribute(server, "clusterName"))
        ```
        
    Example:
        ```python
        objNameString = AdminControl.completeObjectName('WebSphere:type=Server,*') 
        process_type  = AdminControl.getAttribute(objNameString, 'processType')
        
        print(process_type)
        ```
    """

def getAttribute_jmx(object_name, attribute, /):
    """Use the `getAttribute_jmx` command to return the value of the attribute for the name that you provide.

    Args:
        object_name (ObjectName): Specifies the object name of the MBean of interest.
        attribute (str): Specifies the name of the attribute to query.
    
    Example:
        ```
        import javax.management as mgmt 

        objNameString = AdminControl.completeObjectName('WebSphere:=type=Server,*') 
        objName       = mgmt.ObjectName(objNameString)
        process_type  = AdminControl.getAttribute_jmx(objName, 'processType')
        
        print(process_type)
        ```
    
    Question: Investigation needed
        This is not very clear in the documentation, so it needs more research.
    """

def getAttributes(object_name, attributes, /):
    """Returns a string listing the values of the attributes named in `attributes` for the object named by `object_name`.

    Args:
        object_name (ObjectName): Use the getAttributes command to return the attribute values for the names that you provide.
        attributes (java.lang.String[] or java.lang.Object[]): Specifies the names of the attributes to query.
    
    Example:
        
        - Using Jython with string attributes:

        ```python
        objNameString = AdminControl.completeObjectname('WebSphere:type=Server,*)
        attributes    = AdminControl.getAttributes(objNameString, '[cellName nodeName]')
        
        print(attributes)
        ```

        - Using Jython with object attributes:
        
        ```python
        objNameString = AdminControl.completeObjectname('WebSphere:type=Server,*)
        attributes    = AdminControl.getAttributes(objNameString, ['cellName', 'nodeName'])
        
        print(attributes)
        ```


    """

def getAttributes_jmx(): # undocumented
    """ """

def getCell(): # undocumented
    """ """

def getConfigId(): # undocumented
    """ """

def getDefaultDomain(): # undocumented
    """ """

def getDomainName(): # undocumented
    """ """

def getHost(): # undocumented
    """ """

def getMBeanCount(): # undocumented
    """ """

def getMBeanInfo_jmx(): # undocumented
    """ """

def getNode(): # undocumented
    """ """

def getObjectInstance(): # undocumented
    """ """

def getPort(): # undocumented
    """ """

def getPropertiesForDataSource(): # undocumented
    """ (Deprecated) """

def getType(): # undocumented
    """ """

def help(): # undocumented
    """ """

def invoke(): # undocumented
    """ """

def invoke_jmx(): # undocumented
    """ """

def isRegistered(): # undocumented
    """ """

def isRegistered_jmx(): # undocumented
    """ """

def makeObjectName(): # undocumented
    """ """

def queryMBeans(): # undocumented
    """ """

def queryNames() -> MultilineList[RunningObjectName]: # undocumented
    """
	Example:
		```pycon
		>>> print(AdminControl.queryNames('*'))
        WebSphere:cell=MyCell,name=TraceService,mbeanIdentifier=TraceService,type=TraceService,node=MyNode,process=server1
        [...]
		```
	"""
    ...

def queryNames_jmx(): # undocumented
    """ """

def reconnect(): # undocumented
    """ """

def setAttribute(): # undocumented
    """ """

def setAttribute_jmx(): # undocumented
    """ """

def setAttributes(): # undocumented
    """ """

def setAttributes_jmx(): # undocumented
    """ """

def startServer(): # undocumented
    """ """

def stopServer(): # undocumented
    """ """

def testConnection(): # undocumented
    """ """

def trace(): # undocumented
    """ """

