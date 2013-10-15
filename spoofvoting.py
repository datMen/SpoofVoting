#
# UltraAdmin Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	   02110-1301	 USA

__version__ = '1.0'
__author__  = 'LouK'

import b3
import b3.events
import b3.plugin

#--------------------------------------------------------------------------------------------------
class SpoofvotingPlugin(b3.plugin.Plugin):
    _adminPlugin = None

    def startup(self):
      """\
      Initialize plugin settings
      """

   # get the admin plugin so we can register commands
      self._adminPlugin = self.console.getPlugin('admin')
      if not self._adminPlugin:
      # something is wrong, can't start without admin plugin
        self.error('Could not find admin plugin')
        return False
    
    # register our commands (you can ignore this bit)
      if 'commands' in self.config.sections():
        for cmd in self.config.options('commands'):
          level = self.config.get('commands', cmd)
          sp = cmd.split('-')
          alias = None
          if len(sp) == 2:
            cmd, alias = sp

          func = self.getCmd(cmd)
          if func:
            self._adminPlugin.registerCommand(self, cmd, level, func, alias)

      self.debug('Started')
      
    def getCmd(self, cmd):
      cmd = 'cmd_%s' % cmd
      if hasattr(self, cmd):
        func = getattr(self, cmd)
        return func

      return None
      
#--------Commands-----------------------------------------------------
    def cmd_votenextmap(self, data, client, cmd=None):
        """\
        - !votenextmap <map> vote for the next map.
        """
        if not data:
            client.message('^7Invalid or missing data, try !help votenextmap')
        else:
            defaultvote = self.console.getCvar('g_allowvote').getInt()
            match = self.console.getMapsSoundingLike(data)
            if isinstance(match, basestring):
                mapname = match
                self.console.write('g_allowvote "8"')
                self.console.write('spoof %s callvote nextmap %s' % (client.cid, mapname))
                self.console.write('g_allowvote "%s"' % defaultvote)
                if client:
                    client.message('^7Voted for ^2%s' % mapname)
            elif isinstance(match, list):
                client.message('do you mean : %s ?' % string.join(match,', '))
            else:
                client.message('^7cannot find any map like ^2%s^7.' % data)
                
    def cmd_votecycle(self, data, client, cmd=None):
        """\
        - !votecycle vote to cycle map.
        """
        if not data:
            defaultvote = self.console.getCvar('g_allowvote').getInt()
            self.console.write('g_allowvote "536870912"')
            self.console.write('spoof %s callvote cyclemap' % (client.cid))
            self.console.write('g_allowvote "%s"' % defaultvote)
            
    def cmd_votemap(self, data, client, cmd=None):
        """\
        - !votemap <map> vote to change to map.
        """
        if not data:
            client.message('^7Invalid or missing data, try !help votemap')
        else:
            defaultvote = self.console.getCvar('g_allowvote').getInt()
            match = self.console.getMapsSoundingLike(data)
            if isinstance(match, basestring):
                mapname = match
                self.console.write('g_allowvote "4"')
                self.console.write('spoof %s callvote map %s' % (client.cid, mapname))
                self.console.write('g_allowvote "%s"' % defaultvote)
                if client:
                    client.message('^7Voted for ^2%s' % mapname)
            elif isinstance(match, list):
                client.message('do you mean : %s ?' % string.join(match,', '))
            else:
                client.message('^7cannot find any map like ^2%s^7.' % data)
                
    def cmd_votekick(self, data, client, cmd=None):
        """\
        - !votekick <player> vote to kick player.
        """
        if not data:
            client.message('^7Invalid or missing data, try !help votekick')
            return
        else:
            input = self._adminPlugin.parseUserCmd(data)
    	    sclient = self._adminPlugin.findClientPrompt(input[0], client)
            if sclient:
                defaultvote = self.console.getCvar('g_allowvote').getInt()
                self.console.write('g_allowvote "16"')
                self.console.write('spoof %s callvote kick %s' % (client.cid, sclient.cid))
                self.console.write('g_allowvote "%s"' % defaultvote)
            else:
                client.message('^7Invalid or missing data, try !help votekick')
                return
            