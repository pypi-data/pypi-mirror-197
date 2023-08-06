# -*- coding: utf-8 -*-

from ..base import BatchOperator, BaseSinkBatchOp
from ..mixins import WithTrainInfo, EvaluationMetricsCollector, ExtractModelInfoBatchOp, WithModelInfoBatchOp



class AftSurvivalRegModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class AftSurvivalRegPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setQuantileProbabilities(self, val):
        return self._add_param('quantileProbabilities', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)



class AftSurvivalRegTrainBatchOp(BatchOperator, WithModelInfoBatchOp, WithTrainInfo):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.AftSurvivalRegTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AftSurvivalRegTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setCensorCol(self, val):
        return self._add_param('censorCol', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)



class AggLookupBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.AggLookupBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AggLookupBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

    def setDelimiter(self, val):
        return self._add_param('delimiter', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AgnesBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.AgnesBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AgnesBatchOp, self).__init__(*args, **kwargs)
        pass

    def setIdCol(self, val):
        return self._add_param('idCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceThreshold(self, val):
        return self._add_param('distanceThreshold', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setLinkage(self, val):
        return self._add_param('linkage', val)



class AgnesModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.clustering.agnes.AgnesModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AgnesModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class AkSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.AkSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setOverwriteSink(self, val):
        return self._add_param('overwriteSink', val)

    def setPartitionCols(self, val):
        return self._add_param('partitionCols', val)



class AkSourceBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.source.AkSourceBatchOp'
    OP_TYPE = 'SOURCE'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AkSourceBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setPartitions(self, val):
        return self._add_param('partitions', val)



class AlsImplicitTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsImplicitTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsImplicitTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setAlpha(self, val):
        return self._add_param('alpha', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setNonnegative(self, val):
        return self._add_param('nonnegative', val)

    def setNumBlocks(self, val):
        return self._add_param('numBlocks', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRank(self, val):
        return self._add_param('rank', val)



class AlsItemsPerUserRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsItemsPerUserRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsItemsPerUserRecommBatchOp, self).__init__(*args, **kwargs)
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

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AlsModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class AlsRateRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsRateRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsRateRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AlsSimilarItemsRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsSimilarItemsRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsSimilarItemsRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AlsSimilarUsersRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsSimilarUsersRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsSimilarUsersRecommBatchOp, self).__init__(*args, **kwargs)
        pass

    def setRecommCol(self, val):
        return self._add_param('recommCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setInitRecommCol(self, val):
        return self._add_param('initRecommCol', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AlsTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setItemCol(self, val):
        return self._add_param('itemCol', val)

    def setRateCol(self, val):
        return self._add_param('rateCol', val)

    def setUserCol(self, val):
        return self._add_param('userCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setNonnegative(self, val):
        return self._add_param('nonnegative', val)

    def setNumBlocks(self, val):
        return self._add_param('numBlocks', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setRank(self, val):
        return self._add_param('rank', val)



class AlsUsersPerItemRecommBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.recommendation.AlsUsersPerItemRecommBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AlsUsersPerItemRecommBatchOp, self).__init__(*args, **kwargs)
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

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AppendIdBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.dataproc.AppendIdBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AppendIdBatchOp, self).__init__(*args, **kwargs)
        pass

    def setAppendType(self, val):
        return self._add_param('appendType', val)

    def setIdCol(self, val):
        return self._add_param('idCol', val)



class AppendModelStreamFileSinkBatchOp(BaseSinkBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sink.AppendModelStreamFileSinkBatchOp'
    OP_TYPE = 'SINK'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AppendModelStreamFileSinkBatchOp, self).__init__(*args, **kwargs)
        pass

    def setFilePath(self, val):
        return self._add_param('filePath', val)

    def setModelTime(self, val):
        return self._add_param('modelTime', val)

    def setNumFiles(self, val):
        return self._add_param('numFiles', val)

    def setNumKeepModel(self, val):
        return self._add_param('numKeepModel', val)



class ApplyAssociationRuleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.ApplyAssociationRuleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ApplyAssociationRuleBatchOp, self).__init__(*args, **kwargs)
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



class ApplySequenceRuleBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.associationrule.ApplySequenceRuleBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ApplySequenceRuleBatchOp, self).__init__(*args, **kwargs)
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



class ArimaBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.ArimaBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(ArimaBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOrder(self, val):
        return self._add_param('order', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setEstMethod(self, val):
        return self._add_param('estMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeasonalOrder(self, val):
        return self._add_param('seasonalOrder', val)

    def setSeasonalPeriod(self, val):
        return self._add_param('seasonalPeriod', val)



class AsBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.sql.AsBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AsBatchOp, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)



class AutoArimaBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.AutoArimaBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AutoArimaBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setD(self, val):
        return self._add_param('d', val)

    def setEstMethod(self, val):
        return self._add_param('estMethod', val)

    def setIcType(self, val):
        return self._add_param('icType', val)

    def setMaxOrder(self, val):
        return self._add_param('maxOrder', val)

    def setMaxSeasonalOrder(self, val):
        return self._add_param('maxSeasonalOrder', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeasonalPeriod(self, val):
        return self._add_param('seasonalPeriod', val)



class AutoCrossAlgoTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.AutoCrossAlgoTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AutoCrossAlgoTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setBinningMethod(self, val):
        return self._add_param('binningMethod', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setFixCoefs(self, val):
        return self._add_param('fixCoefs', val)

    def setFraction(self, val):
        return self._add_param('fraction', val)

    def setKCross(self, val):
        return self._add_param('kCross', val)

    def setMaxSearchStep(self, val):
        return self._add_param('maxSearchStep', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)



class AutoCrossPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.AutoCrossPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AutoCrossPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setOutputFormat(self, val):
        return self._add_param('outputFormat', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class AutoCrossTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.AutoCrossTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AutoCrossTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setBinningMethod(self, val):
        return self._add_param('binningMethod', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setFixCoefs(self, val):
        return self._add_param('fixCoefs', val)

    def setFraction(self, val):
        return self._add_param('fraction', val)

    def setKCross(self, val):
        return self._add_param('kCross', val)

    def setMaxSearchStep(self, val):
        return self._add_param('maxSearchStep', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)



class AutoGarchBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.timeseries.AutoGarchBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(AutoGarchBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setValueCol(self, val):
        return self._add_param('valueCol', val)

    def setIcType(self, val):
        return self._add_param('icType', val)

    def setIfGARCH11(self, val):
        return self._add_param('ifGARCH11', val)

    def setMaxOrder(self, val):
        return self._add_param('maxOrder', val)

    def setMinusMean(self, val):
        return self._add_param('minusMean', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictNum(self, val):
        return self._add_param('predictNum', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BaseStepWiseSelectorBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.common.finance.stepwiseSelector.BaseStepWiseSelectorBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BaseStepWiseSelectorBatchOp, self).__init__(*args, **kwargs)
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

    def setLinearModelType(self, val):
        return self._add_param('linearModelType', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setStepWiseType(self, val):
        return self._add_param('stepWiseType', val)

    def setVizName(self, val):
        return self._add_param('vizName', val)

    def setWithViz(self, val):
        return self._add_param('withViz', val)



class BertTextClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.BertTextClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextClassifierPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BertTextClassifierTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.BertTextClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBertModelName(self, val):
        return self._add_param('bertModelName', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setCustomConfigJson(self, val):
        return self._add_param('customConfigJson', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxSeqLength(self, val):
        return self._add_param('maxSeqLength', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFineTunedLayers(self, val):
        return self._add_param('numFineTunedLayers', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)



class BertTextEmbeddingBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.nlp.BertTextEmbeddingBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextEmbeddingBatchOp, self).__init__(*args, **kwargs)
        pass

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setBertModelName(self, val):
        return self._add_param('bertModelName', val)

    def setDoLowerCase(self, val):
        return self._add_param('doLowerCase', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLayer(self, val):
        return self._add_param('layer', val)

    def setMaxSeqLength(self, val):
        return self._add_param('maxSeqLength', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BertTextPairClassifierPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.BertTextPairClassifierPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextPairClassifierPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BertTextPairClassifierTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.classification.BertTextPairClassifierTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextPairClassifierTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)

    def setTextPairCol(self, val):
        return self._add_param('textPairCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBertModelName(self, val):
        return self._add_param('bertModelName', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setCustomConfigJson(self, val):
        return self._add_param('customConfigJson', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxSeqLength(self, val):
        return self._add_param('maxSeqLength', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFineTunedLayers(self, val):
        return self._add_param('numFineTunedLayers', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)



class BertTextPairRegressorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.BertTextPairRegressorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextPairRegressorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BertTextPairRegressorTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.BertTextPairRegressorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextPairRegressorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)

    def setTextPairCol(self, val):
        return self._add_param('textPairCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBertModelName(self, val):
        return self._add_param('bertModelName', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setCustomConfigJson(self, val):
        return self._add_param('customConfigJson', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxSeqLength(self, val):
        return self._add_param('maxSeqLength', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFineTunedLayers(self, val):
        return self._add_param('numFineTunedLayers', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)



class BertTextRegressorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.BertTextRegressorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextRegressorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setInferBatchSize(self, val):
        return self._add_param('inferBatchSize', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)



class BertTextRegressorTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.regression.BertTextRegressorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BertTextRegressorTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTextCol(self, val):
        return self._add_param('textCol', val)

    def setBatchSize(self, val):
        return self._add_param('batchSize', val)

    def setBertModelName(self, val):
        return self._add_param('bertModelName', val)

    def setCheckpointFilePath(self, val):
        return self._add_param('checkpointFilePath', val)

    def setCustomConfigJson(self, val):
        return self._add_param('customConfigJson', val)

    def setIntraOpParallelism(self, val):
        return self._add_param('intraOpParallelism', val)

    def setLearningRate(self, val):
        return self._add_param('learningRate', val)

    def setMaxSeqLength(self, val):
        return self._add_param('maxSeqLength', val)

    def setNumEpochs(self, val):
        return self._add_param('numEpochs', val)

    def setNumFineTunedLayers(self, val):
        return self._add_param('numFineTunedLayers', val)

    def setNumPSs(self, val):
        return self._add_param('numPSs', val)

    def setNumWorkers(self, val):
        return self._add_param('numWorkers', val)

    def setPythonEnv(self, val):
        return self._add_param('pythonEnv', val)

    def setRemoveCheckpointBeforeTraining(self, val):
        return self._add_param('removeCheckpointBeforeTraining', val)



class BinarizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BinarizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinarizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setThreshold(self, val):
        return self._add_param('threshold', val)



class BinarySelectorPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.BinarySelectorPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinarySelectorPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelFilePath(self, val):
        return self._add_param('modelFilePath', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)



class BinarySelectorTrainBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.BinarySelectorTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinarySelectorTrainBatchOp, self).__init__(*args, **kwargs)
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



class BinningModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.common.feature.binning.BinningModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinningModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class BinningPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BinningPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinningPredictBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDefaultWoe(self, val):
        return self._add_param('defaultWoe', val)

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



class BinningTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BinningTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinningTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setBinningMethod(self, val):
        return self._add_param('binningMethod', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setDiscreteThresholdsMap(self, val):
        return self._add_param('discreteThresholdsMap', val)

    def setFromUserDefined(self, val):
        return self._add_param('fromUserDefined', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setNumBucketsMap(self, val):
        return self._add_param('numBucketsMap', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setUserDefinedBin(self, val):
        return self._add_param('userDefinedBin', val)

    def setVizName(self, val):
        return self._add_param('vizName', val)



class BinningTrainForScorecardBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.finance.BinningTrainForScorecardBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BinningTrainForScorecardBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setBinningMethod(self, val):
        return self._add_param('binningMethod', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setDiscreteThresholdsMap(self, val):
        return self._add_param('discreteThresholdsMap', val)

    def setFromUserDefined(self, val):
        return self._add_param('fromUserDefined', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setNumBucketsMap(self, val):
        return self._add_param('numBucketsMap', val)

    def setPositiveLabelValueString(self, val):
        return self._add_param('positiveLabelValueString', val)

    def setUserDefinedBin(self, val):
        return self._add_param('userDefinedBin', val)

    def setVizName(self, val):
        return self._add_param('vizName', val)



class BisectingKMeansModelInfoBatchOp(BatchOperator, ExtractModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansModelInfoBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansModelInfoBatchOp, self).__init__(*args, **kwargs)
        pass



class BisectingKMeansPredictBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansPredictBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansPredictBatchOp, self).__init__(*args, **kwargs)
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



class BisectingKMeansTrainBatchOp(BatchOperator, WithModelInfoBatchOp):
    CLS_NAME = 'com.alibaba.alink.operator.batch.clustering.BisectingKMeansTrainBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BisectingKMeansTrainBatchOp, self).__init__(*args, **kwargs)
        pass

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setDistanceType(self, val):
        return self._add_param('distanceType', val)

    def setK(self, val):
        return self._add_param('k', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setMinDivisibleClusterSize(self, val):
        return self._add_param('minDivisibleClusterSize', val)

    def setRandomSeed(self, val):
        return self._add_param('randomSeed', val)



class BoxPlotOutlier4GroupedDataBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.BoxPlotOutlier4GroupedDataBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BoxPlotOutlier4GroupedDataBatchOp, self).__init__(*args, **kwargs)
        pass

    def setInputMTableCol(self, val):
        return self._add_param('inputMTableCol', val)

    def setOutputMTableCol(self, val):
        return self._add_param('outputMTableCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

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



class BoxPlotOutlierBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.outlier.BoxPlotOutlierBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BoxPlotOutlierBatchOp, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setDirection(self, val):
        return self._add_param('direction', val)

    def setFeatureCol(self, val):
        return self._add_param('featureCol', val)

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



class BucketizerBatchOp(BatchOperator):
    CLS_NAME = 'com.alibaba.alink.operator.batch.feature.BucketizerBatchOp'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(BucketizerBatchOp, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setCutsArray(self, val):
        return self._add_param('cutsArray', val)

    def setCutsArrayStr(self, val):
        return self._add_param('cutsArrayStr', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

