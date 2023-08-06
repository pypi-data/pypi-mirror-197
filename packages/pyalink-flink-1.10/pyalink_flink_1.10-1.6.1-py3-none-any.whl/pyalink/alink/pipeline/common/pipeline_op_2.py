# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator
from ..tuning.base import BaseGridSearch, BaseRandomSearch
from ..mixins import HasLazyPrintModelInfo, HasLazyPrintTrainInfo
from ..local_predictor import LocalPredictable
from ...common.types.bases.model_stream_scan_params import ModelStreamScanParams



class CrossFeature(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.CrossFeature'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CrossFeature, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

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



class CrossFeatureModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.CrossFeatureModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CrossFeatureModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

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



class CsvToColumns(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToColumns'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToColumns, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

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



class CsvToJson(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToJson'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToJson, self).__init__(*args, **kwargs)
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



class CsvToKv(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToKv'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToKv, self).__init__(*args, **kwargs)
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



class CsvToVector(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.format.CsvToVector'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(CsvToVector, self).__init__(*args, **kwargs)
        pass

    def setCsvCol(self, val):
        return self._add_param('csvCol', val)

    def setSchemaStr(self, val):
        return self._add_param('schemaStr', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setCsvFieldDelimiter(self, val):
        return self._add_param('csvFieldDelimiter', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setQuoteChar(self, val):
        return self._add_param('quoteChar', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorSize(self, val):
        return self._add_param('vectorSize', val)



class DCT(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DCT'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DCT, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setInverse(self, val):
        return self._add_param('inverse', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class Dbscan(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.Dbscan'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Dbscan, self).__init__(*args, **kwargs)
        pass

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setMinPoints(self, val):
        return self._add_param('minPoints', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DbscanModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.DbscanModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DbscanModel, self).__init__(*args, **kwargs)
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



class DecisionTreeClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.DecisionTreeClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeClassificationModel, self).__init__(*args, **kwargs)
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



class DecisionTreeClassifier(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.DecisionTreeClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeClassifier, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DecisionTreeEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeEncoder, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DecisionTreeEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeEncoderModel, self).__init__(*args, **kwargs)
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



class DecisionTreeRegEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DecisionTreeRegEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegEncoder, self).__init__(*args, **kwargs)
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

    def setTreeType(self, val):
        return self._add_param('treeType', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class DecisionTreeRegEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.DecisionTreeRegEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegEncoderModel, self).__init__(*args, **kwargs)
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



class DecisionTreeRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.DecisionTreeRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegressionModel, self).__init__(*args, **kwargs)
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



class DecisionTreeRegressor(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.DecisionTreeRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DecisionTreeRegressor, self).__init__(*args, **kwargs)
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



class DocCountVectorizer(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocCountVectorizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizer, self).__init__(*args, **kwargs)
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

    def setVocabSize(self, val):
        return self._add_param('vocabSize', val)



class DocCountVectorizerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocCountVectorizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocCountVectorizerModel, self).__init__(*args, **kwargs)
        pass

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



class DocHashCountVectorizer(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocHashCountVectorizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setFeatureType(self, val):
        return self._add_param('featureType', val)

    def setMinDF(self, val):
        return self._add_param('minDF', val)

    def setMinTF(self, val):
        return self._add_param('minTF', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumFeatures(self, val):
        return self._add_param('numFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class DocHashCountVectorizerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.DocHashCountVectorizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(DocHashCountVectorizerModel, self).__init__(*args, **kwargs)
        pass

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



class EqualWidthDiscretizer(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.EqualWidthDiscretizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class EqualWidthDiscretizerModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.EqualWidthDiscretizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(EqualWidthDiscretizerModel, self).__init__(*args, **kwargs)
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

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class ExclusiveFeatureBundle(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.ExclusiveFeatureBundle'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExclusiveFeatureBundle, self).__init__(*args, **kwargs)
        pass

    def setSparseVectorCol(self, val):
        return self._add_param('sparseVectorCol', val)

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



class ExclusiveFeatureBundleModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.ExclusiveFeatureBundleModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExclusiveFeatureBundleModel, self).__init__(*args, **kwargs)
        pass

    def setSparseVectorCol(self, val):
        return self._add_param('sparseVectorCol', val)

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



class ExtractMfccFeature(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.audio.ExtractMfccFeature'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ExtractMfccFeature, self).__init__(*args, **kwargs)
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



class FeatureHasher(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.FeatureHasher'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FeatureHasher, self).__init__(*args, **kwargs)
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



class FmClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.FmClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassificationModel, self).__init__(*args, **kwargs)
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



class FmClassifier(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.FmClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

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

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmItemsPerUserRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.FmItemsPerUserRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmItemsPerUserRecommender, self).__init__(*args, **kwargs)
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



class FmRateRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.FmRateRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRateRecommender, self).__init__(*args, **kwargs)
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



class FmRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.FmRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressionModel, self).__init__(*args, **kwargs)
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



class FmRegressor(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.FmRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmRegressor, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

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

    def setNumFactor(self, val):
        return self._add_param('numFactor', val)

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

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)

    def setWithLinearItem(self, val):
        return self._add_param('withLinearItem', val)



class FmUsersPerItemRecommender(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.recommendation.FmUsersPerItemRecommender'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(FmUsersPerItemRecommender, self).__init__(*args, **kwargs)
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



class GaussianMixture(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GaussianMixture'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GaussianMixture, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

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

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class GaussianMixtureModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GaussianMixtureModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GaussianMixtureModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

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



class GbdtClassificationModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.GbdtClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtClassificationModel, self).__init__(*args, **kwargs)
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



class GbdtClassifier(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.GbdtClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.GbdtEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtEncoder, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.GbdtEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtEncoderModel, self).__init__(*args, **kwargs)
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



class GbdtRegEncoder(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.GbdtRegEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegEncoder, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GbdtRegEncoderModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.GbdtRegEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegEncoderModel, self).__init__(*args, **kwargs)
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



class GbdtRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GbdtRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegressionModel, self).__init__(*args, **kwargs)
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



class GbdtRegressor(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GbdtRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GbdtRegressor, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCriteria(self, val):
        return self._add_param('criteria', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setFeatureImportanceType(self, val):
        return self._add_param('featureImportanceType', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setGamma(self, val):
        return self._add_param('gamma', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setMinSumHessianPerLeaf(self, val):
        return self._add_param('minSumHessianPerLeaf', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNewtonStep(self, val):
        return self._add_param('newtonStep', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GeneralizedLinearRegression(Estimator, HasLazyPrintModelInfo, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GeneralizedLinearRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeneralizedLinearRegression, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFamily(self, val):
        return self._add_param('family', val)

    def setFitIntercept(self, val):
        return self._add_param('fitIntercept', val)

    def setLink(self, val):
        return self._add_param('link', val)

    def setLinkPower(self, val):
        return self._add_param('linkPower', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

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

    def setOffsetCol(self, val):
        return self._add_param('offsetCol', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setRegParam(self, val):
        return self._add_param('regParam', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVariancePower(self, val):
        return self._add_param('variancePower', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)



class GeneralizedLinearRegressionModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.GeneralizedLinearRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeneralizedLinearRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setLinkPredResultCol(self, val):
        return self._add_param('linkPredResultCol', val)

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



class GeoKMeans(Estimator, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GeoKMeans'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeans, self).__init__(*args, **kwargs)
        pass

    def setLatitudeCol(self, val):
        return self._add_param('latitudeCol', val)

    def setLongitudeCol(self, val):
        return self._add_param('longitudeCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

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



class GeoKMeansModel(Model, LocalPredictable, ModelStreamScanParams):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.GeoKMeansModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GeoKMeansModel, self).__init__(*args, **kwargs)
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



class GridSearchCV(BaseGridSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchCV'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchCV, self).__init__(*args, **kwargs)
        pass

    def setNumFolds(self, val):
        return self._add_param('NumFolds', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setParallelTuningMode(self, val):
        return self._add_param('parallelTuningMode', val)



class GridSearchCVModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.GridSearchCVModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(GridSearchCVModel, self).__init__(*args, **kwargs)
        pass

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

