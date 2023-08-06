# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator
from ..tuning.base import BaseGridSearch, BaseRandomSearch
from ..mixins import HasLazyPrintModelInfo, HasLazyPrintTrainInfo
from ..local_predictor import LocalPredictable
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class GridSearchTVSplit(BaseGridSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchTVSplit'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchTVSplit, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setParallelTuningMode(self, val):
        return self._add_param('parallelTuningMode', val)

    def setTrainRatio(self, val):
        return self._add_param('trainRatio', val)



class GridSearchTVSplitModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchTVSplitModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchTVSplitModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class HashCrossFeature(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.HashCrossFeature'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(HashCrossFeature, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class IForestModelOutlier(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.outlier.IForestModelOutlier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IForestModelOutlier, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingSize(self, val):
        return self._add_param('subsamplingSize', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class IForestModelOutlierModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.outlier.IForestModelOutlierModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IForestModelOutlierModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class IForestOutlier4GroupedData(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.operator.common.outlier.IForestOutlier4GroupedData'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IForestOutlier4GroupedData, self).__init__(*args, **kwargs)
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

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOutlierThreshold(self, val):
        return self._add_param('outlierThreshold', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setSubsamplingSize(self, val):
        return self._add_param('subsamplingSize', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class Id3(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.Id3'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Id3, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

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

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class Id3Encoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.Id3Encoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Id3Encoder, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

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

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class Id3EncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.Id3EncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Id3EncoderModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class Id3Model(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.Id3Model'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Id3Model, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class Imputer(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.Imputer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Imputer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setFillValue(self, val):
        return self._add_param('fillValue', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setStrategy(self, val):
        return self._add_param('strategy', val)



class ImputerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.ImputerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ImputerModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class IndexToString(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.IndexToString'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IndexToString, self).__init__(*args, **kwargs)
        pass

    def setModelName(self, val):
        return self._add_param('modelName', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class IsotonicRegression(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.IsotonicRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

    def setFeatureIndex(self, val):
        return self._add_param('featureIndex', val)

    def setIsotonic(self, val):
        return self._add_param('isotonic', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class IsotonicRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.IsotonicRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(IsotonicRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)



class ItemCfItemsPerUserRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ItemCfItemsPerUserRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ItemCfItemsPerUserRecommender, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ItemCfRateRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ItemCfRateRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ItemCfRateRecommender, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ItemCfSimilarItemsRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ItemCfSimilarItemsRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ItemCfSimilarItemsRecommender, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ItemCfUsersPerItemRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.ItemCfUsersPerItemRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ItemCfUsersPerItemRecommender, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setExcludeKnown(self, val):
        return self._add_param('excludeKnown', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class JsonToColumns(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToColumns, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class JsonToCsv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class JsonToKv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToKv, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class JsonToVector(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.JsonToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonToVector, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class JsonValue(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.JsonValue'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(JsonValue, self).__init__(*args, **kwargs)
        pass

    def setJsonPath(self, val):
        return self._add_param('jsonPath', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputColTypes(self, val):
        return self._add_param('outputColTypes', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSkipFailed(self, val):
        return self._add_param('skipFailed', val)



class KMeans(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KMeans'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeans, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setInitMode(self, val):
        return self._add_param('initMode', val)

    def setInitSteps(self, val):
        return self._add_param('initSteps', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KMeansModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KMeansModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KMeansModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPredictionDistanceCol(self, val):
        return self._add_param('predictionDistanceCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KModes(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KModes'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KModes, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KModesModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.KModesModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KModesModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KerasSequentialClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.KerasSequentialClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KerasSequentialClassifier(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.KerasSequentialClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBestMetric(self, val):
        return self._add_param('bestMetric', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOptimizer(self, val):
        return self._add_param('optimizer', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSaveBestOnly(self, val):
        return self._add_param('saveBestOnly', val)

    def setSaveCheckpointsEpochs(self, val):
        return self._add_param('saveCheckpointsEpochs', val)

    def setSaveCheckpointsSecs(self, val):
        return self._add_param('saveCheckpointsSecs', val)

    def setValidationSplit(self, val):
        return self._add_param('validationSplit', val)



class KerasSequentialRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.KerasSequentialRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KerasSequentialRegressor(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.KerasSequentialRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KerasSequentialRegressor, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTensorCol(self, val):
        return self._add_param('tensorCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBestMetric(self, val):
        return self._add_param('bestMetric', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setOptimizer(self, val):
        return self._add_param('optimizer', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSaveBestOnly(self, val):
        return self._add_param('saveBestOnly', val)

    def setSaveCheckpointsEpochs(self, val):
        return self._add_param('saveCheckpointsEpochs', val)

    def setSaveCheckpointsSecs(self, val):
        return self._add_param('saveCheckpointsSecs', val)

    def setValidationSplit(self, val):
        return self._add_param('validationSplit', val)



class KnnClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.KnnClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KnnClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class KnnClassifier(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.KnnClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KnnClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class KvToColumns(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToColumns, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToCsv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToCsv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToCsv, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToJson(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToJson, self).__init__(*args, **kwargs)
        pass

    def setJsonCol(self, val):
        return self._add_param('jsonCol', val)

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class KvToVector(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.KvToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(KvToVector, self).__init__(*args, **kwargs)
        pass

    def setKvCol(self, val):
        return self._add_param('kvCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setKvColDelimiter(self, val):
        return self._add_param('kvColDelimiter', val)

    def setKvValDelimiter(self, val):
        return self._add_param('kvValDelimiter', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class LassoRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LassoRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LassoRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LassoRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LassoRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class Lda(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.Lda'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Lda, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setTopicNum(self, val):
        return self._add_param('topicNum', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setBeta(self, val):
        return self._add_param('beta', val)

    def setLearningDecay(self, val):
        return self._add_param('learningDecay', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOnlineLearningOffset(self, val):
        return self._add_param('onlineLearningOffset', val)

    def setOptimizeDocConcentration(self, val):
        return self._add_param('optimizeDocConcentration', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRate(self, val):
        return self._add_param('subsamplingRate', val)

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)



class LdaModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.LdaModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LinearRegStepwise(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegStepwise'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegStepwise, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setMethod(self, val):
        return self._add_param('method', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LinearRegStepwiseModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegStepwiseModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegStepwiseModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class LinearRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LinearRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class LinearSvm(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvm'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvm, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LinearSvmModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvmModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class LinearSvr(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearSvr'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvr, self).__init__(*args, **kwargs)
        pass

    def setC(self, val):
        return self._add_param('C', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setTau(self, val):
        return self._add_param('tau', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class LinearSvrModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearSvrModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvrModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

