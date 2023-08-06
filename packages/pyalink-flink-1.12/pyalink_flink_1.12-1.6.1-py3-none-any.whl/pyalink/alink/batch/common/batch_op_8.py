# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class ProphetTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.ProphetTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ProphetTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)



class PyFileScalarFnBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.PyFileScalarFnBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyFileScalarFnBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassName(self, val):
        return self._add_param('className', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setResultType(self, val):
        return self._add_param('resultType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserFilePaths(self, val):
        return self._add_param('userFilePaths', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class PyFileTableFnBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.PyFileTableFnBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyFileTableFnBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassName(self, val):
        return self._add_param('className', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setResultTypes(self, val):
        return self._add_param('resultTypes', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserFilePaths(self, val):
        return self._add_param('userFilePaths', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class PyScalarFnBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.PyScalarFnBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyScalarFnBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setResultType(self, val):
        return self._add_param('resultType', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class PySqlCmdBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.PySqlCmdBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PySqlCmdBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCommand(self, val):
        return self._add_param('command', val)



class PyTableFnBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.PyTableFnBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PyTableFnBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClassObject(self, val):
        return self._add_param('classObject', val)

    def setClassObjectType(self, val):
        return self._add_param('classObjectType', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setResultTypes(self, val):
        return self._add_param('resultTypes', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setPythonEnvFilePath(self, val):
        return self._add_param('pythonEnvFilePath', val)

    def setPythonVersion(self, val):
        return self._add_param('pythonVersion', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.QuantileBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileBatchOp, self).__init__(*args, **kwargs)
        pass

    def setQuantileNum(self, val):
        return self._add_param('quantileNum', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setRoundMode(self, val):
        return self._add_param('roundMode', val)



class QuantileDiscretizerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.QuantileDiscretizerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class QuantileDiscretizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.QuantileDiscretizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class QuantileDiscretizerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.QuantileDiscretizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)



class RandomForestEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.RandomForestEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestEncoderTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.RandomForestModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class RandomForestPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.RandomForestPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.RandomForestRegEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegEncoderTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RandomForestRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class RandomForestRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RandomForestRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RandomForestRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RandomForestRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomForestTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.RandomForestTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RandomTableSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.RandomTableSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomTableSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setNumCols(self, val):
        return self._add_param('numCols', val)

    def setNumRows(self, val):
        return self._add_param('numRows', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputColConfs(self, val):
        return self._add_param('outputColConfs', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)



class RandomVectorSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.RandomVectorSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomVectorSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setNumRows(self, val):
        return self._add_param('numRows', val)

    def setSize(self, val):
        return self._add_param('size', val)

    def setSparsity(self, val):
        return self._add_param('sparsity', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)



class RandomWalkBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.RandomWalkBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomWalkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSourceCol(self, val):
        return self._add_param('sourceCol', val)

    def setTargetCol(self, val):
        return self._add_param('targetCol', val)

    def setWalkLength(self, val):
        return self._add_param('walkLength', val)

    def setWalkNum(self, val):
        return self._add_param('walkNum', val)

    def setDelimiter(self, val):
        return self._add_param('delimiter', val)

    def setIsToUndigraph(self, val):
        return self._add_param('isToUndigraph', val)

    def setIsWeightedSampling(self, val):
        return self._add_param('isWeightedSampling', val)

    def setSamplingMethod(self, val):
        return self._add_param('samplingMethod', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class RankingListBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.statistics.RankingListBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RankingListBatchOp, self).__init__(*args, **kwargs)
        pass

    def setObjectCol(self, val):
        return self._add_param('objectCol', val)

    def setAddedCols(self, val):
        return self._add_param('addedCols', val)

    def setAddedStatTypes(self, val):
        return self._add_param('addedStatTypes', val)

    def setGroupCol(self, val):
        return self._add_param('groupCol', val)

    def setGroupValues(self, val):
        return self._add_param('groupValues', val)

    def setIsDescending(self, val):
        return self._add_param('isDescending', val)

    def setStatCol(self, val):
        return self._add_param('statCol', val)

    def setStatType(self, val):
        return self._add_param('statType', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class ReadAudioToTensorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.audio.ReadAudioToTensorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadAudioToTensorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setSampleRate(self, val):
        return self._add_param('sampleRate', val)

    def setChannelFirst(self, val):
        return self._add_param('channelFirst', val)

    def setDuration(self, val):
        return self._add_param('duration', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOffset(self, val):
        return self._add_param('offset', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ReadImageToTensorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.image.ReadImageToTensorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ReadImageToTensorBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRelativeFilePathCol(self, val):
        return self._add_param('relativeFilePathCol', val)

    def setRootFilePath(self, val):
        return self._add_param('rootFilePath', val)

    def setChannelFirst(self, val):
        return self._add_param('channelFirst', val)

    def setImageHeight(self, val):
        return self._add_param('imageHeight', val)

    def setImageWidth(self, val):
        return self._add_param('imageWidth', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class RebalanceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.RebalanceBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RebalanceBatchOp, self).__init__(*args, **kwargs)
        pass



class RecommendationRankingBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.RecommendationRankingBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RecommendationRankingBatchOp, self).__init__(*args, **kwargs)
        pass

    def setMTableCol(self, val):
        return self._add_param('mTableCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setRankingCol(self, val):
        return self._add_param('rankingCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setTopN(self, val):
        return self._add_param('topN', val)



class RedisRowSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.RedisRowSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisRowSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCols(self, val):
        return self._add_param('keyCols', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCols(self, val):
        return self._add_param('valueCols', val)



class RedisStringSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.RedisStringSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RedisStringSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPluginVersion(self, val):
        return self._add_param('pluginVersion', val)

    def setClusterMode(self, val):
        return self._add_param('clusterMode', val)

    def setDatabaseIndex(self, val):
        return self._add_param('databaseIndex', val)

    def setKeyCol(self, val):
        return self._add_param('keyCol', val)

    def setPipelineSize(self, val):
        return self._add_param('pipelineSize', val)

    def setRedisIPs(self, val):
        return self._add_param('redisIPs', val)

    def setRedisPassword(self, val):
        return self._add_param('redisPassword', val)

    def setTimeout(self, val):
        return self._add_param('timeout', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)



class RegexTokenizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.RegexTokenizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setGaps(self, val):
        return self._add_param('gaps', val)

    def setMinTokenLength(self, val):
        return self._add_param('minTokenLength', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPattern(self, val):
        return self._add_param('pattern', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setToLowerCase(self, val):
        return self._add_param('toLowerCase', val)



class RegressionSelectorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.RegressionSelectorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegressionSelectorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class RegressionSelectorTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.RegressionSelectorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegressionSelectorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setAlphaEntry(self, val):
        return self._add_param('alphaEntry', val)

    def setAlphaStay(self, val):
        return self._add_param('alphaStay', val)

    def setForceSelectedCols(self, val):
        return self._add_param('forceSelectedCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)



class RidgeRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RidgeRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class RidgeRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RidgeRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class RidgeRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.RidgeRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class RightOuterJoinBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.RightOuterJoinBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RightOuterJoinBatchOp, self).__init__(*args, **kwargs)
        pass

    def setJoinPredicate(self, val):
        return self._add_param('joinPredicate', val)

    def setSelectClause(self, val):
        return self._add_param('selectClause', val)

    def setType(self, val):
        return self._add_param('type', val)



class SHEsdOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.outlier.SHEsdOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SHEsdOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFrequency(self, val):
        return self._add_param('frequency', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMaxSampleNumPerGroup(self, val):
        return self._add_param('maxSampleNumPerGroup', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setShesdAlpha(self, val):
        return self._add_param('shesdAlpha', val)



class SampleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.SampleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SampleBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRatio(self, val):
        return self._add_param('ratio', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class SampleWithSizeBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.SampleWithSizeBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SampleWithSizeBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSize(self, val):
        return self._add_param('size', val)

    def setWithReplacement(self, val):
        return self._add_param('withReplacement', val)



class ScorecardModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.finance.ScorecardModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ScorecardModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class ScorecardPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.ScorecardPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ScorecardPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionScoreCol(self, val):
        return self._add_param('predictionScoreCol', val)

    def setCalculateScorePerFeature(self, val):
        return self._add_param('calculateScorePerFeature', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ScorecardTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.ScorecardTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ScorecardTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setAlphaEntry(self, val):
        return self._add_param('alphaEntry', val)

    def setAlphaStay(self, val):
        return self._add_param('alphaStay', val)

    def setConstOptimMethod(self, val):
        return self._add_param('constOptimMethod', val)

    def setDefaultWoe(self, val):
        return self._add_param('defaultWoe', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setForceSelectedCols(self, val):
        return self._add_param('forceSelectedCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLinearModelType(self, val):
        return self._add_param('linearModelType', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setOdds(self, val):
        return self._add_param('odds', val)

    def setPdo(self, val):
        return self._add_param('pdo', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setScaleInfo(self, val):
        return self._add_param('scaleInfo', val)

    def setScaledValue(self, val):
        return self._add_param('scaledValue', val)

    def setVizName(self, val):
        return self._add_param('vizName', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithSelector(self, val):
        return self._add_param('withSelector', val)



class SegmentBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.SegmentBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SegmentBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setUserDefinedDict(self, val):
        return self._add_param('userDefinedDict', val)



class SelectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.SelectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SelectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class ShiftBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.ShiftBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ShiftBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setShiftNum(self, val):
        return self._add_param('shiftNum', val)



class ShuffleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.ShuffleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ShuffleBatchOp, self).__init__(*args, **kwargs)
        pass



class SideOutputBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.utils.SideOutputBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SideOutputBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIndex(self, val):
        return self._add_param('index', val)



class SimpleSelectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.SelectBatchOp$SimpleSelectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SimpleSelectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class SingleSourceShortestPathBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.SingleSourceShortestPathBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SingleSourceShortestPathBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)

    def setSourcePoint(self, val):
        return self._add_param('sourcePoint', val)

    def setAsUndirectedGraph(self, val):
        return self._add_param('asUndirectedGraph', val)

    def setEdgeWeightCol(self, val):
        return self._add_param('edgeWeightCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)



class SoftmaxModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.SoftmaxModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SoftmaxModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class SoftmaxPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.SoftmaxPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(SoftmaxPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

