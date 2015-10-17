from Components.Sources.Source import Source
from Components.config import config

from Screens.MessageBox import MessageBox
#DO NOT REMOVE THE FOLLOWING IMPORT, it ensures that config.sleeptimer.defaulttime is there
import Screens.SleepTimerEdit

class SleepTimer(Source):
    def __init__(self, session):
        Source.__init__(self)
        self.session = session
        self.res = ( False, 
                     config.SleepTimer.defaulttime.value,
                     config.SleepTimer.action.value,
                     "Obligatory parameters missing [cmd [set,get], time [0-999], action [standby,shutdown], enabled [True,False]" )
        
    def handleCommand(self, cmd):
        print "[WebComponents.SleepTimer].handleCommand"
        self.res = self.setSleeptimer(cmd)
        
    def setSleeptimer(self, cmd):
        print "[WebComponents.SleepTimer].setSleeptimer, cmd=%s" %cmd
        
        from Screens.Standby import inStandby
        
        if inStandby == None:            
            if cmd['cmd'] is None or cmd['cmd'] == "get":        
                if self.session.nav.SleepTimer.isActive():
                    return ( self.session.nav.SleepTimer.isActive(), 
                             self.session.nav.SleepTimer.getCurrentSleepTime(), 
                             config.SleepTimer.action.value, 
                             "Sleeptimer is enabled" ) 
                else:
                    return ( self.session.nav.SleepTimer.isActive(), 
                             config.SleepTimer.defaulttime.value, 
                             config.SleepTimer.action.value, 
                             "Sleeptimer is disabled" )
                
            elif cmd['cmd'] == "set":
                if cmd['enabled'] == 'True':
                    enabled = True
                elif cmd['enabled'] == 'False':
                    enabled = False
                else:
                   return ( self.session.nav.SleepTimer.isActive(), 
                            config.SleepTimer.defaulttime.value, 
                            config.SleepTimer.action.value, 
                            "ERROR: Obligatory parameter 'enabled' [True,False] has unspecified value '%s'" %cmd['enabled'] )  
                
                if not enabled:
                    self.session.nav.SleepTimer.clear()
                    self.session.open(MessageBox, _("The sleep timer has been disabled."), MessageBox.TYPE_INFO)
                    return ( self.session.nav.SleepTimer.isActive(),  
                             config.SleepTimer.defaulttime.value, 
                             config.SleepTimer.action.value,
                             "Sleeptimer has been disabled" )
                
                else:
                    if cmd['time'] is None :
                        return ( self.session.nav.SleepTimer.isActive(),  
                                 config.SleepTimer.defaulttime.value, 
                                 config.SleepTimer.action.value,
                                 "ERROR: Obligatory parameter 'time' [0-999] is missing" )
                        
                    elif cmd['enabled'] is None :
                        return ( self.session.nav.SleepTimer.isActive(),  
                                 config.SleepTimer.defaulttime.value, 
                                 config.SleepTimer.action.value,
                                 "Obligatory parameter 'enabled' [True,False] is missing" )
                      
                    time = int(float(cmd['time']))
                    
                    if cmd['action'] is None :
                        action = "standby"
                    else:
                        action = cmd['action']
                    
                    if time > 999:
                        time = 999        
                    elif time < 0:
                        time = 0
                    
                    if action == "shutdown":
                        config.SleepTimer.action.value = action
                    else:
                        config.SleepTimer.action.value = "standby"
                    
                    config.SleepTimer.defaulttime.setValue(time)
                    config.SleepTimer.defaulttime.save()
                    config.SleepTimer.action.save()
                    self.session.nav.SleepTimer.setSleepTime(time)
                    self.session.open(MessageBox, _("The sleep timer has been activated for %s minutes.") %time, MessageBox.TYPE_INFO)
                    
                    return ( self.session.nav.SleepTimer.isActive(),  
                             time, 
                             config.SleepTimer.action.value,
                             "Sleeptimer set to %s minutes" %time)
                        
            else:
                return ( self.session.nav.SleepTimer.isActive(),  
                         config.SleepTimer.defaulttime.value, 
                         config.SleepTimer.action.value, 
                         "ERROR: Obligatory parameter 'cmd' [get,set] has unspecified value '%s'" %cmd['cmd'] ) 
        else:
            return ( self.session.nav.SleepTimer.isActive(),  
                     config.SleepTimer.defaulttime.value, 
                     config.SleepTimer.action.value, 
                     "ERROR: Cannot set SleepTimer while device is in Standby-Mode" )
    
    def getResult(self):
        return self.res
    
    timer = property(getResult)
        