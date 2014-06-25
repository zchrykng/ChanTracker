###
# Copyright (c) 2013, Nicolas Coevoet
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('ChanTracker', True)


ChanTracker = conf.registerPlugin('ChanTracker')

conf.registerGlobalValue(ChanTracker, 'pool',
    registry.Integer(60, """delay between two checks about mode removal, in seconds. Note, check is also based on irc activity, so removal may be delayed a bit"""))

conf.registerGlobalValue(ChanTracker, 'CAPS',
    registry.CommaSeparatedListOfStrings(['account-notify','extended-join'], """CAP asked of ircd that permits tracking username and account changes"""))

conf.registerGlobalValue(ChanTracker, 'logsSize',
    registry.PositiveInteger(60, """number of messages to keep in logs. Note, this is per nick - not per nick per channel"""))

conf.registerGlobalValue(ChanTracker, 'quietCommand',
    registry.String("CS QUIET $channel $hostmask","""command issued to quiet a user; $channel and $hostmask will be replaced at runtime"""))

conf.registerGlobalValue(ChanTracker, 'unquietCommand',
    registry.String("CS UNQUIET $channel $hostmask","""command issued to unquiet a user $channel and $hostmask will be replaced at runtime"""))

#now per channel

conf.registerChannelValue(ChanTracker, 'opCommand',
    registry.String("CS OP $channel $nick", """command used to obtain channel operator mode"""))

conf.registerChannelValue(ChanTracker, 'modesToAsk',
    registry.CommaSeparatedListOfStrings(['b','q'], """list of channel modes to sync into the bot's tracking database when it joins the channel"""))
    
conf.registerChannelValue(ChanTracker, 'modesToAskWhenOpped',
    registry.CommaSeparatedListOfStrings(['e','I'], """list of channel modes to sync into the bot's tracking database when it is opped"""))

# per channel settings
# related to ban tracking

conf.registerChannelValue(ChanTracker, 'autoExpire',
    registry.Integer(-1, """default expiration time for newly placed bans; -1 disables auto-expiration, otherwise it's in seconds"""))

# related to logChannel
    
conf.registerChannelValue(ChanTracker, 'logChannel',
    registry.String("", """where bot announces op's actions; it is highly recommended to set an appropriate operator's channel to receive the various useful messages"""))

conf.registerChannelValue(ChanTracker, 'announceOthers',
    registry.Boolean(True,"""forward messages from quieted/banned users to logChannel; used when bot stays opped and channel is +z (reduced moderation).
Messages from users flagged as bad, or when channel is under attack will not be forwarded"""))

conf.registerChannelValue(ChanTracker, 'announceWithNotice',
    registry.Boolean(False,"""use NOTICE instead of PRIVMSG to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceModes',
    registry.CommaSeparatedListOfStrings(['b','q','e','I','r','l','v','o','h','k','n','t','F','i','t'],"""announce modes listed to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceModeSync',
    registry.Boolean(False,"""announce to logChannel that synchronisation of channel modes to tracking database has completed"""))

conf.registerChannelValue(ChanTracker, 'announceKick',
    registry.Boolean(True,"""announce kick, remove, kill and kline to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceTopic',
    registry.Boolean(True,"""announce topic changes to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceEdit',
    registry.Boolean(True,"""announce tracker item description edits to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceMark',
    registry.Boolean(True,"""announce item expiration settings (marks) to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceInTimeEditAndMark',
    registry.Boolean(False,"""announce new comments (edits) and expiries (marks) to logChannel when they are created by the do, q, b, e, i commands"""))

conf.registerChannelValue(ChanTracker, 'announceMassRemoval',
    registry.Boolean(False,"""announce mass ban removals 'undo *', 'uq *', 'ub *' to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceBotEdit',
    registry.Boolean(False,"""when banning based on a channel protection trigger (such as flood prevention), announce the items comment (edit) to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceBotMark',
    registry.Boolean(False,"""when banning based on a channel protection trigger (such as flood prevention), announce the items expiry (mark) to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceNotice',
    registry.Boolean(True,"""announce channel notices to logChannel"""))

conf.registerChannelValue(ChanTracker, 'announceCtcp',
    registry.Boolean(True,"""announce channel ctcps to logChannel"""))

# others settings

conf.registerChannelValue(ChanTracker, 'doNothingAboutOwnOpStatus',
    registry.Boolean(True, """bot will never try to change his own op status"""))

conf.registerChannelValue(ChanTracker, 'keepOp',
    registry.Boolean(False, """bot stays opped"""))

conf.registerChannelValue(ChanTracker, 'kickMode',
    registry.CommaSeparatedListOfStrings(['b'], """bot will kick affected users when mode is triggered, 
    use if with caution, if an op bans *!*@*, bot will kick everyone on the channel"""))
    
conf.registerChannelValue(ChanTracker, 'kickMessage',
    registry.String("You are banned from this channel", """bot kick reason"""))

conf.registerChannelValue(ChanTracker, 'doActionAgainstAffected',
    registry.Boolean(True, """devoice, deop, dehalfop user affected by a mode change"""))
    
conf.registerChannelValue(ChanTracker, 'useChannelBansForPermanentBan',
    registry.Boolean(True, """when users join the channel, check if the match a permanent ban"""))

conf.registerChannelValue(ChanTracker, 'addKickMessageInComment',
    registry.Boolean(False, """add kick message to mode comment in tracking database"""))
    
conf.registerChannelValue(ChanTracker, 'askOpAboutMode',
    registry.Boolean(False,"""In a private message, ask the op who added a mode about the duration of the ban and a comment on why it was set"""))

conf.registerChannelValue(ChanTracker, 'checkEvade',
    registry.Boolean(True,"""bot will apply same duration and mode than the ban evaded, currently only work when someone identify to an account, and has ip computed"""))

conf.registerChannelValue(ChanTracker, 'useChanServForQuiets',
    registry.Boolean(False,"""if bot is not opped, use services for quiet / unquiets"""))

# related to channel's protection

# flood detection settings
conf.registerChannelValue(ChanTracker, 'floodPermit',
registry.Integer(-1,"""Number of messages allowed during floodLife, -1 to disable, advice 4"""))
conf.registerChannelValue(ChanTracker, 'floodLife',
registry.PositiveInteger(7,"""Duration of messages's life in flood counter, in seconds, advice 7"""))
conf.registerChannelValue(ChanTracker, 'floodMode',
registry.String('q',"""mode used by the bot when flood detection is triggered"""))
conf.registerChannelValue(ChanTracker, 'floodDuration',
registry.PositiveInteger(60,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'floodComment',
registry.String('flood detected',"""comment added on mode changes database, empty for no comment"""))

# another flood queue, for user with throttled irc client, who copy / paste long text
conf.registerChannelValue(ChanTracker, 'lowFloodPermit',
registry.Integer(-1,"""Number of messages allowed during lowFloodLife, -1 to disable, advice 5"""))
conf.registerChannelValue(ChanTracker, 'lowFloodLife',
registry.Integer(13,"""Duration of messages's life in lowFlood counter, in seconds, advice 13"""))
conf.registerChannelValue(ChanTracker, 'lowFloodMode',
registry.String('q',"""mode used by the bot when low flood detection is triggered"""))
conf.registerChannelValue(ChanTracker, 'lowFloodDuration',
registry.PositiveInteger(180,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'lowFloodComment',
registry.String('low flood detected',"""comment added on mode changes database, empty for no comment"""))

# repeat detection
conf.registerChannelValue(ChanTracker, 'repeatPermit',
registry.Integer(-1,"""Number of repeated text allowed, -1 to disable, note, first message doesn't count, 
so if you want to trigger it after 3 repeat, you must set it to 1, advice 4"""))
conf.registerChannelValue(ChanTracker, 'repeatLife',
registry.PositiveInteger(120,"""Duration of messages's life in lowFlood counter in seconds, advice 120"""))
conf.registerChannelValue(ChanTracker, 'repeatPercent',
registry.Probability(0.85,"""percent of similarity needed between previous and current message to trigger a repeat count"""))
conf.registerChannelValue(ChanTracker, 'repeatMode',
registry.String('q',"""mode used by the bot when repeat detection is triggered"""))
conf.registerChannelValue(ChanTracker, 'repeatDuration',
registry.PositiveInteger(180,"""punishment duration  in seconds"""))
conf.registerChannelValue(ChanTracker, 'repeatComment',
registry.String('repeat detected',"""comment added on mode changes database, empty for no comment"""))

# mass repeat detection
conf.registerChannelValue(ChanTracker, 'massRepeatChars',
registry.PositiveInteger(20,"""number of chars needed to enter massRepeat detection"""))
conf.registerChannelValue(ChanTracker, 'massRepeatPermit',
registry.Integer(-1,"""Number of repeated text allowed, -1 to disable, a bit different to repeat, because it doesn't track user but channel messages, 
if repeat comes from differences sources that helps, it also add a pattern that will match future repeat, 
during massRepeatDuration, note, the first two message doesn't count, 
so if you want to trigger it after 3 repeat, you must set it to 1"""))
conf.registerChannelValue(ChanTracker, 'massRepeatLife',
registry.PositiveInteger(60,"""Duration of messages's life in massRepeat counter, in seconds, advice 120"""))
conf.registerChannelValue(ChanTracker, 'massRepeatPercent',
registry.Probability(0.95,"""percentage similarity between previous and current message to trigger a repeat count"""))
conf.registerChannelValue(ChanTracker, 'massRepeatMode',
registry.String('q',"""mode used by the bot when repeat detection is triggered"""))
conf.registerChannelValue(ChanTracker, 'massRepeatDuration',
registry.PositiveInteger(180,"""punition in seconds"""))
conf.registerChannelValue(ChanTracker, 'massRepeatComment',
registry.String('mass repeat detected',"""comment added on mode changes database, empty for no comment"""))

# YES IT'S ANNOYING
conf.registerChannelValue(ChanTracker, 'capPermit',
registry.Integer(-1,"""Number of UPPERCASE messages allowed, -1 to disable, advice 3; see capPercent for definition of an UPPERCASE message"""))
conf.registerChannelValue(ChanTracker, 'capLife',
registry.PositiveInteger(120,"""Duration in seconds before messages are removed from count, advice 120"""))
conf.registerChannelValue(ChanTracker, 'capPercent',
registry.Probability(0.75,"""percentage of uppercase chars in a message to trigger a cap count"""))
conf.registerChannelValue(ChanTracker, 'capMode',
registry.String('q',"""mode used by the bot when cap is triggered"""))
conf.registerChannelValue(ChanTracker, 'capDuration',
registry.PositiveInteger(180,"""punition in seconds"""))
conf.registerChannelValue(ChanTracker, 'capComment',
registry.String('capslock detected',"""comment added on mode changes database, empty for no comment"""))

# hilight
conf.registerChannelValue(ChanTracker, 'hilightPermit',
registry.Integer(-1,"""Number of nick allowed per message, -1 to disable, advice 2 - 3, note : it don't care if it's the same nick"""))
conf.registerChannelValue(ChanTracker, 'hilightMode',
registry.String('q',"""mode used by the bot when cap is triggered"""))
conf.registerChannelValue(ChanTracker, 'hilightDuration',
registry.PositiveInteger(180,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'hilightComment',
registry.String('hilight detected',"""comment added on mode changes database, empty for no comment"""))

# channel's notices
conf.registerChannelValue(ChanTracker, 'noticePermit',
registry.Integer(-1,"""Number of messages allowed, -1 to disable, advice 0"""))
conf.registerChannelValue(ChanTracker, 'noticeLife',
registry.PositiveInteger(3,"""Duration in seconds before messages are removed from count"""))
conf.registerChannelValue(ChanTracker, 'noticeMode',
registry.String('q',"""mode used by the bot when notice is triggered"""))
conf.registerChannelValue(ChanTracker, 'noticeDuration',
registry.PositiveInteger(300,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'noticeComment',
registry.String('notice detected',"""comment added on mode changes database, empty for no comment"""))

# channel ctcps
conf.registerChannelValue(ChanTracker, 'ctcpPermit',
registry.Integer(-1,"""Number of messages allowed, -1 to disable, advice 0"""))
conf.registerChannelValue(ChanTracker, 'ctcpLife',
registry.PositiveInteger(3,"""Duration in seconds before messages are removed from count"""))
conf.registerChannelValue(ChanTracker, 'ctcpMode',
registry.String('b',"""mode used by the bot when ctcp is triggered"""))
conf.registerChannelValue(ChanTracker, 'ctcpDuration',
registry.PositiveInteger(1800,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'ctcpComment',
registry.String('ctcp detected',"""comment added on mode changes database, empty for no comment"""))

# channel join/part flood
conf.registerChannelValue(ChanTracker, 'cyclePermit',
registry.Integer(-1,"""Number of cycles allowed, -1 to disable, count part and quit"""))
conf.registerChannelValue(ChanTracker, 'cycleLife',
registry.PositiveInteger(180,"""Duration in seconds before cycles are removed from count, advice 180"""))
conf.registerChannelValue(ChanTracker, 'cycleMode',
registry.String('b',"""mode used by the bot when ctcp is triggered"""))
conf.registerChannelValue(ChanTracker, 'cycleDuration',
registry.PositiveInteger(1800,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'cycleComment',
registry.String('cycle detected',"""comment added on mode changes database, empty for no comment"""))

# channel massJoin from an host
conf.registerChannelValue(ChanTracker, 'massJoinPermit',
registry.Integer(-1,"""Number of messages allowed, -1 to disable, note, it could mixup a bit with cycle detection"""))
conf.registerChannelValue(ChanTracker, 'massJoinLife',
registry.PositiveInteger(60,"""Duration in seconds before messages are removed from count"""))
conf.registerChannelValue(ChanTracker, 'massJoinMode',
registry.String('+rq-z $~a',"""mode used by the bot when massjoin is triggered"""))
conf.registerChannelValue(ChanTracker, 'massJoinDuration',
registry.PositiveInteger(300,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'massJoinUnMode',
registry.String('-rq+z $~a',"""mode used by the bot when massJoinDuration is finished"""))

# nick changes flood
conf.registerChannelValue(ChanTracker, 'nickPermit',
registry.Integer(-1,"""Number of messages allowed, -1 to disable, advice 2"""))
conf.registerChannelValue(ChanTracker, 'nickLife',
registry.Integer(300,"""Duration in seconds before messages are removed from count, advice 300"""))
conf.registerChannelValue(ChanTracker, 'nickMode',
registry.String('q',"""mode used by the bot when nick is triggered"""))
conf.registerChannelValue(ChanTracker, 'nickDuration',
registry.PositiveInteger(300,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'nickComment',
registry.String('nick changes flood detected',"""comment added on mode changes database, empty for no comment"""))

# if you enable this, each time someone trigger other protection that will increase this queue
conf.registerChannelValue(ChanTracker, 'badPermit',
registry.Integer(-1,"""Number of bad action allowed, -1 to disable, advice 2, each time bot had to acts on a user, it increase this item"""))
conf.registerChannelValue(ChanTracker, 'badLife',
registry.Integer(600,"""Duration in seconds before item are removed from count, advice 600"""))
conf.registerChannelValue(ChanTracker, 'badMode',
registry.String('b',"""mode used by the bot when bad is triggered"""))
conf.registerChannelValue(ChanTracker, 'badDuration',
registry.PositiveInteger(86400,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'badComment',
registry.String('bad detected',"""comment added on mode changes database, empty for no comment"""))

# if you enable this, each time someone trigger bad in a channel that will increase this queue
conf.registerChannelValue(ChanTracker, 'attackPermit',
registry.Integer(-1,"""Number of bad action allowed, -1 to disable, advice 2, each time bot flags user as bad, it increase this item"""))
conf.registerChannelValue(ChanTracker, 'attackLife',
registry.Integer(600,"""Duration in seconds before item are removed from count, advice 600"""))
conf.registerChannelValue(ChanTracker, 'attackDuration',
registry.PositiveInteger(1800,"""punishment duration in seconds"""))
conf.registerChannelValue(ChanTracker, 'attackMode',
registry.String('+rq-z $~a',"""mode used by the bot when attack is triggered"""))
conf.registerChannelValue(ChanTracker, 'attackUnMode',
registry.String('-rq+z $~a',"""mode used by the bot when attackDuration is finished"""))

