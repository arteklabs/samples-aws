=========================
EC2 Cluster Configuration
=========================

The full load cluster configuration is not very important (``dms.r5.xlarge`` for 582G of data for < 3 days), but the CDC cluster config is important, as it will run permanently.

Empower Data Spatial Specs
--------------------------

* table space total (G): 582
* average schema size (MB): 79
* most schemas size (MB): ~60
* max 10 schemas (MB):
    * 4171.25
    * 3498.94
    * 2579.94
    * 2345.56
    * 2263.56
    * 1949.0
    * 1897.25
    * 1740.31
    * 1677.19
    * 1649.63
* average row count: 1185
* 12 of 40 tables have 0 rows accross **all schemas**
* 28 tables with more than 0 rows:
    * AUDITTRAIL in 7700 schemas
    * CALCURVE in 4633 schemas
    * CALIB in 4664 schemas
    * CHROMATOGRAM in 4760 schemas
    * CHROMSYSCONFIG in 5992 schemas
    * DRAWDEF in 22 schemas
    * FIELDCUSTOM in 7930 schemas
    * FRACTION in 3 schemas
    * METHOD in 7237 schemas
    * MILLDATABASEVERSION in 7930 schemas
    * INJECTION in 5051 schemas
    * INJECTIONLOG in 3016 schemas
    * INJ2SET in 4761 schemas
    * INSTMATCH in 12 schemas
    * PEAK in 4694 schemas
    * PEAKMS in 4370 schemas
    * PEAKPDA in 41 schemas
    * PROJECTINTEGRITY in 1713 schemas
    * RESULT in 4695 schemas
    * RESULTSET in 4594 schemas
    * REPORTS in 4083 schemas
    * PREFERENCES in 7877 schemas
    * SAMPLESET in 5055 schemas
    * SIGNOFF in 4338 schemas
    * SUITPEAK in 4399 schemas
    * VIAL in 5053 schemas
    * VIEWFILTER in 6943 schemas
    * VIEWTEMPIDS in 1527 schemas
* 10 of 28 tables selected by the LOB as important for use cases (CDC)
    * CALCURVE (4633) (1893933)
    * CALIB (4664) (281451)
    * CHROMSYSCONFIG (5992) (32213)
    * INJECTION (5051) (2477877)
    * PEAK (4694) (43638523)
    * RESULT (4695) (3297574)
    * RESULTSET (4594) (128692)
    * SAMPLESET (5055) (222031)
    * SIGNOFF (4338) (5295658)
    * VIAL (5053) (2166718)

EC2 Cluster Config for CDC
--------------------------

* instances count: 
* ``SupportLobs``: ``false`` (irrelevant for business, play an important role in allocating memory in the tasks)
* architecture:
    * t3.large:
        * CALIB
        * CHROMSYSCONFIG
        * MILLENNIUM.PROJECTINFO
        * 9 tasks
    * t3.large:
        * RESULTSET
        * SAMPLESET
        * 8 tasks
    * r5.xlarge:
        * PEAK
        * RESULT
        * 8 tasks
    * r5.xlarge:
        * CALCURVE
        * INJECTION
        * SIGNOFF
        * VIAL
        * 16 tasks

* ``MaxFullLoadSubTasks`` (parallel tasks): 12 (T3 Instances are burstable, they don’t operate with Full vCPU capacity at all times (to reduce costs), read these `docs <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html>`_)
* S3 target connection details (read the `docs <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring>`_)
    * ``cdcMaxBatchInterval``
        * Defines the interval of which files are output to S3. Default is 60 seconds. We can delay this to allow more information to be written to S3 at a single time.
        * We can start changing this from 60 to 75 and then adjust if we see or not improvements.
    * ``cdcMinFileSize``
        * Defines the minimum size of the file to be output to S3. Default is 32 MB.
        * We can start changing this setting from 32 to 45MB.
    * **only one of these parameters triggers the write to S3**

EC2 Cluster Config for Full Load
--------------------------------

* instances count: 4
* ``SupportLobs``: ``false`` (irrelevant for business, play an important role in allocating memory in the tasks)
* architecture:
    * two ``r5.large`` (more cost effective than c5, and t3 were not good due to memory issues)
    * 4-5 tasks of ingestion (``MaxFullLoadSubTasks`` > 1 creates a bottleneck with a single task)
        * pattern suggestions:
            * ``where schema name is like 'W_%' and table name is like 'CALIB', include`` or
            * ``where schema name is like 'W_0%' and table name is like 'CALIB', include``
            * ``where schema name is like 'W_1%' and table name is like 'CALIB', include``
            * ...
* ``MaxFullLoadSubTasks`` (parallel tasks): 12 (T3 Instances are burstable, they don’t operate with Full vCPU capacity at all times (to reduce costs), read these `docs <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html>`_)
* S3 target connection details (read the `docs <https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html#CHAP_Target.S3.Configuring>`_)
    * ``cdcMaxBatchInterval``
        * Defines the interval of which files are output to S3. Default is 60 seconds. We can delay this to allow more information to be written to S3 at a single time.
        * We can start changing this from 60 to 75 and then adjust if we see or not improvements.
    * ``cdcMinFileSize``
        * Defines the minimum size of the file to be output to S3. Default is 32 MB.
        * We can start changing this setting from 32 to 45MB.
    * **only one of these parameters triggers the write to S3**
* approximated cost: 1200 USD / month (Use the `calculator <https://calculator.aws/#/estimate?id=66ff33471174dd085941448d131d8c8c5063fcad >`_ to calculate cost)
