from pathlib import Path
from typing import Tuple

from pyPhases.util.Logger import classLogger
from pyPhasesRecordloader.downloader.Downloader import Downloader
from pyPhasesRecordloader.Event import Event
from pyPhasesRecordloader.NormalizeRecordSignal import NormalizeRecordSignal
from pyPhasesRecordloader.RecordSignal import RecordSignal
from pyPhasesRecordloader.util.DynamicModule import DynamicModule

from . import recordLoaders as recordManagerPath


class ParseError(Exception):
    pass


class AnnotationException(Exception):
    path = []
    name = ""

    def __init__(self, path):
        self.path = path
        self.name = path[-1]
        super().__init__(self.getMessage())


class AnnotationNotFound(AnnotationException):
    def getMessage(self):
        return "Annotation was not found in the XML file: %s" % (self.path + [self.name])


class AnnotationInvalid(AnnotationException):
    def getMessage(self):
        return "Annotation is invalid: %s" % (self.path)


class ChannelsNotPresent(Exception):
    channels = []

    def __init__(self, channels, msg=None, recordid="Unknown"):
        if msg is None:
            msg = (
                "Channels of record %s where not present: %s, you can define 'aliases' for the channelname or make the channel optional"
                % (recordid, channels)
            )
        super().__init__(msg)
        self.channels = channels


@classLogger
class RecordLoader:
    recordLoader = DynamicModule(recordManagerPath)

    recordLoaders = {
        "EDFRecrodLoader": "pyPhasesRecordloader.recordLoaders",
        "H5RecordLoader": "pyPhasesRecordloader.recordLoaders",
        "MatRecordLoader": "pyPhasesRecordloader.recordLoaders",
        "WFDBRecordLoader": "pyPhasesRecordloader.recordLoaders",
        "XMLAnnotationLoader": "pyPhasesRecordloader.recordLoaders",
    }

    def __init__(
        self,
        filePath="",
        targetSignals=None,
        targetSignalTypes=None,
        optionalSignals=None,
        combineChannels=None,
        downloadOptions=None,
    ) -> None:
        downloadOptions = downloadOptions if downloadOptions is not None else {}
        combineChannels = combineChannels if combineChannels is not None else []
        optionalSignals = optionalSignals if optionalSignals is not None else []
        targetSignalTypes = targetSignalTypes if targetSignalTypes is not None else []
        targetSignals = targetSignals if targetSignals is not None else []

        self.filePath = filePath
        self.optionalSignals = optionalSignals
        self.targetSignals = targetSignals
        self.targetSignalTypes = targetSignalTypes
        # lightOff and lightOn are in seconds !
        self.lightOff = 0
        self.lightOn = None
        self.classificationConfig = {}
        self.exportsEventArray = False
        self.firstSleep = None
        self.lastSleep = None
        self.signalTypeDict = dict(zip(self.targetSignals, self.targetSignalTypes))
        self.useDigitalSignals = False
        self.combineChannels = combineChannels
        self.downloadOptions = downloadOptions

    def registerRecordLoader(name, path):
        RecordLoader.recordLoaders[name] = path

    def delete(self, recordName):
        pass

    def exist(self, recordName):
        pass

    def setupRemoteReadOrDownload(self):
        dl = Downloader.get()
        dl.options = self.downloadOptions
        if dl.canReadRemote:
            self.filePath = dl.basePath
        elif not Path(self.filePath).exists():
            dl.downloadTo(self.filePath)

    def loadRecord(self, recordName, eventTargetFrequency=1) -> Tuple[RecordSignal, Tuple[Event]]:
        # self.downloadOnDemand(recordName)
        signal = self.getSignal(recordName)
        eventList = self.getEventList(recordName, targetFrequency=eventTargetFrequency)

        NormalizeRecordSignal().combine(signal, self.combineChannels)

        return signal, eventList

    def getSignal(self, recordName) -> RecordSignal:
        pass

    def loadAnnotation(self, recordName):
        pass

    def getEventList(self, recordName, targetFrequency=1):
        pass

    def existAnnotation(self, recordId):
        """Check if an annotation exist for a given recordId.

        Returns:
            boolean: annotation exist
        """
        return False

    def updateFrequencyForEventList(self, eventList, targetFrequency):
        [e.updateFrequency(targetFrequency) for e in eventList]
        return eventList

    @staticmethod
    def get() -> "RecordLoader":
        packageName = RecordLoader.recordLoaders[RecordLoader.recordLoader.moduleName]
        return RecordLoader.recordLoader.get(packageName)

    def getRecordList(self):
        downloader = Downloader.get()

        return downloader.getRecordList()

    # def fillRecordFromPSGSignal(self, record: Record, psgSignal: PSGSignal):

    #     record.recordName = psgSignal.recordId

    #     for signal in psgSignal.signals:
    #         signal.typeStr = self.getSignalTypeStrFromDict(signal.name)
    #     psgSignal.checkPSGQuality()

    #     for signal in psgSignal.signals:
    #         channel = Channel()
    #         recordChannel = RecordChannel()

    #         channel.name = signal.name
    #         channel.dimension = signal.dimension
    #         channel.min = signal.physicalMin
    #         channel.max = signal.physicalMax
    #         recordChannel.transducer = signal.transducer
    #         recordChannel.frequency = signal.frequency
    #         recordChannel.prefilter = signal.prefilter
    #         recordChannel.quality = signal.quality

    #         recordChannel.Channel = channel
    #         record.recordChannels.append(recordChannel)
    #     return record

    def getSignalTypeStrFromDict(self, signalName):
        if self.signalTypeDict == {}:
            self.signalTypeDict = dict(zip(self.targetSignals, self.targetSignalTypes))
        if signalName in self.signalTypeDict:
            signalTypeStr = self.signalTypeDict[signalName]
        else:
            self.logError("Signal '%s' had no type when initilizing the RecordLoader" % str(signalName))
            signalTypeStr = "unknown"
        return signalTypeStr

    def groupBy(self, group, recordIds):
        if group is not None:
            raise Exception("groupBy is not implemented by this RecordLoader, can't group by '%s'" % group)
        return {recordId: [recordId] for recordId in recordIds}
