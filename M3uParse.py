import re

class M3uParse:
    def __init__(self, filename):
        self.filename = filename
        self.channelsInfo = []
        self.preLineInfo = '#EXTINF:-1'
        self.moviesExtensions = ["mp4", "mkv"]
        self.readM3u()

    def readM3u(self):
        self.readAllLines()
        self.parseFile()

    # Read all file lines
    def readAllLines(self):
        self.lines = [line.rstrip('\n') for line in open(self.filename)]
        self.m3uHeader = self.lines[0]
        return len(self.lines)

    def parseFile(self):
        numLines = len(self.lines)
        for n in range(numLines):
            line = self.lines[n]
            if line[0] == "#":
                self.manageLine(n)

    def parseChannel(self, line, url):
        m = re.search("tvg-name=\"(.*?)\"", line)
        name = m.group(1) if (m is not None) else ''
        m = re.search("tvg-id=\"(.*?)\"", line)
        id = m.group(1) if (m is not None) else ''
        m = re.search("tvg-logo=\"(.*?)\"", line)
        logo = m.group(1) if (m is not None) else ''
        m = re.search("group-title=\"(.*?)\"", line)
        group = m.group(1) if (m is not None) else ''
        m = re.search("[,](?!.*[,])(.*?)$", line)
        title = m.group(1) if (m is not None) else ''

        return {
            "title": title,
            "tvg-name": name,
            "tvg-ID": id,
            "tvg-logo": logo,
            "tvg-group": group,
            "url": url
        }

    def manageLine(self, n):
        lineInfo = self.lines[n]
        lineLink = self.lines[n + 1]
        if lineInfo != self.m3uHeader:
            channel = self.parseChannel(lineInfo, lineLink)
            self.channelsInfo.append(channel)

    def cloneGroups(self, groups):
        for channel in groups:
            matchedChannels = [ch for ch in self.channelsInfo if self.channelMatchs(ch, channel)]
            if matchedChannels:
                matchedChannel = next(iter(matchedChannels))
                self.copyProperties(matchedChannel, channel)

    def copyProperties(self, channel1, channel2):
        wantedProperties = ["title", "tvg-name", "tvg-ID", "tvg-logo", "tvg-group"]
        newProperties = dict((k,channel2[k]) for k in wantedProperties if channel2[k])
        channel1.update(newProperties)

    def channelMatchs(self, channel1, channel2):
        sameTitle = (channel1['title'] !='' and channel2['title'] !='') and channel1['title'].lower() == channel2['title'].lower()
        sameID = channel1['tvg-ID'].lower() == channel2['tvg-ID'].lower()
        return sameID or sameTitle

    def channelsToLines(self):
        lines = []
        for channel in self.channelsInfo:
            lines = lines + self.channelToString(channel)
        return lines

    def channelToString(self, channel):
        _channel = dict(channel)
        url = _channel.pop('url')
        title = _channel.pop('title')
        info = ' '.join([f'{key}="{_channel[key]}"' for key in _channel if _channel[key] != ''])
        lineInfo = f'{self.preLineInfo} {info}, {title}'
        return [lineInfo, url]

    def writeM3u(self):
        with open(self.filename, 'w') as file:
            file.write(self.m3uHeader + '\n')
            file.write('\n'.join(self.channelsToLines()))
