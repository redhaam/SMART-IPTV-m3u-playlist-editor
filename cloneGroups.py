import yaml
from M3uParse import M3uParse

class CloneGroups:
    def __init__(self,m3uFileName,groupsFileName="groups.yaml"):
        self.groupsFileName=groupsFileName
        with open(groupsFileName) as file:
            self.channelsInfo= yaml.safe_load(file)
        self.m3uPlaylist = M3uParse(m3uFileName)

    def cloneGroups(self):
        self.m3uPlaylist.cloneGroups(self.channelsInfo)
        self.m3uPlaylist.writeM3u()
