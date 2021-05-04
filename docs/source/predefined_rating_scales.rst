Predefined Rating Scales
========================

The transitionMatrix package supports a variety of credit rating scales. They are grouped together in :mod:`transitionMatrix.creditratings.creditsystems`.

The key ones are described here in more detail.


Rating Scales currently covered
--------------------------------

The focus of the current selection is on *long-term issuer* ratings scales (others will be added):

- AM Best Europe-Rating Services Ltd.
- ARC Ratings S.A.
- Cerved Rating Agency S.p.A.
- Creditreform Rating AG
- DBRS Ratings Limited
- Fitch Ratings
- Moody’s Investors Service
- Scope Ratings AG
- Standard & Poor’s Ratings Services

Data per Scale
-------------------------------------------

Each rating scale is a StateSpace (see :ref:`State Spaces`) and thus inherits the attributes and methods of that object, namely:

- The entity defining the scale (the originating entity)
- The full name of the scale (as most originators of rating scales offer multiple scales with different meaning an/or use)
- The definition of the scale (as a list of tuples in the form [('0', 'X1'), ... , ('N-1', 'XN)] where X are the symbols used to denote the credit state
- The CQS (credit quality step) mapping of the scale as defined by regulatory authorities (see next section)


CQS Mappings
------------

The Credit Quality Step (CQS) denotes a standardised indicator of Credit Risk that is recognized in the European Union

* The CQS Credit Rating Scale is based on numbers, ranging from 1 to 6.
* 1 is the highest quality, 6 is the lowest quality

The European Supervisory Authorities maintain mappings between credit rating agencies and CQS


.. note:: Consult the original documents from definitive mappings available at the `EBA Website <https://eba.europa.eu/regulation-and-policy/external-credit-assessment-institutions-ecai/draft-implementing-technical-standards-on-the-mapping-of-ecais-credit-assessments>`_

The Rating Agency State Spaces and mappings are obtained from the latest (20 May 2019) Regulatory Reference:

::

    JC 2018 11, FINAL REPORT: REVISED DRAFT ITS ON THE MAPPING OF ECAIS’ CREDIT ASSESSMENTS UNDER CRR

Example of Label Conversion
""""""""""""""""""""""""""""
Convert labels between credit rating scales

.. image:: ../../examples/scale_conversions.png

