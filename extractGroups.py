
import yaml
from M3uParse import M3uParse

class ExtractGroups:

    def __init__(self, fileName,groups="groups.yaml"):
        self.m3uParse = M3uParse(fileName)
        self.groups = groups
        self.exportToYaml()

    def deleteUrl(self,channel):
        _channel= dict(channel)
        del _channel['url']
        return _channel

    def exportToYaml(self):
        with open(self.groups, 'w') as file:
            mapChannels = map(self.deleteUrl, self.m3uParse.channelsInfo)
            documents= yaml.dump(list(mapChannels),file)

