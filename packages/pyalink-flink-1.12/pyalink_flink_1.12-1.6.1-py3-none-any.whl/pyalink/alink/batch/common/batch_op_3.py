# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class DbscanModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.clustering.dbscan.DbscanModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DbscanModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class DbscanOutlier4GroupedDataBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.DbscanOutlier4GroupedDataBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DbscanOutlier4GroupedDataBatchOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class DbscanOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.DbscanOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DbscanOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setMaxSampleNumPerGroup(self, val):
        return self._add_param('maxSampleNumPerGroup', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class DbscanPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.DbscanPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DbscanPredictBatchOp, self).__init__(*args, **kwargs)
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



class DecisionTreeEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.DecisionTreeEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeEncoderTrainBatchOp, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreeModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class DecisionTreePredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreePredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreePredictBatchOp, self).__init__(*args, **kwargs)
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



class DecisionTreeRegEncoderTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.DecisionTreeRegEncoderTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegEncoderTrainBatchOp, self).__init__(*args, **kwargs)
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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class DecisionTreeRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DecisionTreeRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.DecisionTreeRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegTrainBatchOp, self).__init__(*args, **kwargs)
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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.DecisionTreeTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeTrainBatchOp, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DeepARPreProcessBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.DeepARTrainBatchOp$DeepARPreProcessBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DeepARPreProcessBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setStride(self, val):
        return self._add_param('stride', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWindow(self, val):
        return self._add_param('window', val)



class DeepARPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.DeepARPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DeepARPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DeepARTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.DeepARTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DeepARTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setTimeCol(self, val):
        return self._add_param('timeCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setStride(self, val):
        return self._add_param('stride', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWindow(self, val):
        return self._add_param('window', val)



class DeepWalkBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.DeepWalkBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DeepWalkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSourceCol(self, val):
        return self._add_param('sourceCol', val)

    def setTargetCol(self, val):
        return self._add_param('targetCol', val)

    def setWalkLength(self, val):
        return self._add_param('walkLength', val)

    def setWalkNum(self, val):
        return self._add_param('walkNum', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setIsToUndigraph(self, val):
        return self._add_param('isToUndigraph', val)

    def setMinCount(self, val):
        return self._add_param('minCount', val)

    def setNegative(self, val):
        return self._add_param('negative', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRandomWindow(self, val):
        return self._add_param('randomWindow', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWindow(self, val):
        return self._add_param('window', val)



class DistinctBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.DistinctBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DistinctBatchOp, self).__init__(*args, **kwargs)
        pass



class DocCountVectorizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocCountVectorizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DocCountVectorizerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocCountVectorizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMaxDF(self, val):
        return self._add_param('maxDF', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)



class DocHashCountVectorizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocHashCountVectorizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DocHashCountVectorizerTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocHashCountVectorizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)



class DocWordCountBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.DocWordCountBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocWordCountBatchOp, self).__init__(*args, **kwargs)
        pass

    def setContentCol(self, val):
        return self._add_param('contentCol', val)

    def setDocIdCol(self, val):
        return self._add_param('docIdCol', val)

    def setWordDelimiter(self, val):
        return self._add_param('wordDelimiter', val)



class EasyTransferConfigTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.common.dl.EasyTransferConfigTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EasyTransferConfigTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setConfigJson(self, val):
        return self._add_param('configJson', val)

    def setTaskType(self, val):
        return self._add_param('taskType', val)

    def setUserFiles(self, val):
        return self._add_param('userFiles', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setUserParams(self, val):
        return self._add_param('userParams', val)



class EcodOutlier4GroupedDataBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.EcodOutlier4GroupedDataBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EcodOutlier4GroupedDataBatchOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class EcodOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.EcodOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EcodOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setGroupCols(self, val):
        return self._add_param('groupCols', val)

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

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class EdgeClusterCoefficientBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.graph.EdgeClusterCoefficientBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EdgeClusterCoefficientBatchOp, self).__init__(*args, **kwargs)
        pass

    def setEdgeSourceCol(self, val):
        return self._add_param('edgeSourceCol', val)

    def setEdgeTargetCol(self, val):
        return self._add_param('edgeTargetCol', val)

    def setAsUndirectedGraph(self, val):
        return self._add_param('asUndirectedGraph', val)



class EqualWidthDiscretizerModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class EqualWidthDiscretizerPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerPredictBatchOp, self).__init__(*args, **kwargs)
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



class EqualWidthDiscretizerTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.EqualWidthDiscretizerTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)



class EsdOutlier4GroupedDataBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.EsdOutlier4GroupedDataBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EsdOutlier4GroupedDataBatchOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMaxOutlierNumPerGroup(self, val):
        return self._add_param('maxOutlierNumPerGroup', val)

    def setMaxOutlierRatio(self, val):
        return self._add_param('maxOutlierRatio', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)



class EsdOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.EsdOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EsdOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

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



class EvalBinaryClassBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalBinaryClassBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalBinaryClassBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)



class EvalClusterBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalClusterBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalClusterBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class EvalMultiClassBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalMultiClassBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalMultiClassBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)



class EvalMultiLabelBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalMultiLabelBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalMultiLabelBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelRankingInfo(self, val):
        return self._add_param('labelRankingInfo', val)

    def setPredictionRankingInfo(self, val):
        return self._add_param('predictionRankingInfo', val)



class EvalOutlierBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setOutlierValueStrings(self, val):
        return self._add_param('outlierValueStrings', val)



class EvalRankingBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalRankingBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalRankingBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLabelRankingInfo(self, val):
        return self._add_param('labelRankingInfo', val)

    def setPredictionRankingInfo(self, val):
        return self._add_param('predictionRankingInfo', val)



class EvalRegressionBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalRegressionBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalRegressionBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)



class EvalTimeSeriesBatchOp(BatchOperator, EvaluationMetricsCollector):
    CLS_NAME = 'com.alibaba.alink.operator.batch.evaluation.EvalTimeSeriesBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EvalTimeSeriesBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)



class ExclusiveFeatureBundleModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.ExclusiveFeatureBundleModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExclusiveFeatureBundleModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class ExclusiveFeatureBundlePredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.ExclusiveFeatureBundlePredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExclusiveFeatureBundlePredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSparseVectorCol(self, val):
        return self._add_param('sparseVectorCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ExtractMfccFeatureBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.audio.ExtractMfccFeatureBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExtractMfccFeatureBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSampleRate(self, val):
        return self._add_param('sampleRate', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHopTime(self, val):
        return self._add_param('hopTime', val)

    def setNumMfcc(self, val):
        return self._add_param('numMfcc', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWindowTime(self, val):
        return self._add_param('windowTime', val)



class FeatureHasherBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.FeatureHasherBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FeatureHasherBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FilterBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.FilterBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FilterBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class FirstNBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.FirstNBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FirstNBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSize(self, val):
        return self._add_param('size', val)



class FlattenKObjectBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.FlattenKObjectBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FlattenKObjectBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setOutputColTypes(self, val):
        return self._add_param('outputColTypes', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FlattenMTableBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.FlattenMTableBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FlattenMTableBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setHandleInvalidMethod(self, val):
        return self._add_param('handleInvalidMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class FmClassifierModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class FmClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierPredictBatchOp, self).__init__(*args, **kwargs)
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



class FmClassifierTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.FmClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitStdev(self, val):
        return self._add_param('initStdev', val)

    def setLambda0(self, val):
        return self._add_param('lambda0', val)

    def setLambda1(self, val):
        return self._add_param('lambda1', val)

    def setLambda2(self, val):
        return self._add_param('lambda2', val)

    def setLearnRate(self, val):
        return self._add_param('learnRate', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)

