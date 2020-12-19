from extractGroups import ExtractGroups
from cloneGroups import  CloneGroups

filename="tv_channels_90108395215688_plus.m3u"

exported = "tv_channels_285576393671698.m3u"


cloner= CloneGroups(exported)

cloner.cloneGroups()