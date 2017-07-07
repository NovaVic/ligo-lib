CDI Linker Library
==================

|License|

The **CDI Linker** python library is aimed to identify and link records that belong to the same entity(individual)
within a single or multiple file. The process is called de-duplication if it is only applied to a single data file.

This library is inspired by `Python Record Linkage Toolkit <https://github.com/J535D165/recordlinkage>`__.
Some of the algorithms and functions are taken from Python Record Linkage Toolkit and are adapted to our linking model.


Dependencies
------------

The **CDI Linker** library needs to be executed in a Unix environment because it utilizes some shell scripting. It depends on:

- Python (>=3.5)
- NumPy (>=1.11.2)
- Pandas (>=0.19.2)
- jellyfish (>=0.5.6)
- xhtml2pdf (>=0.0.6)
- jinja2 (>=2.8.1)


Installation
------------

To install the library simply use:

.. code:: sh

    pip install -e cdi-linking
    pip install -e linking_ext


Tests
-----

The **CDI Linker** library tests depend on:

- pytest>=3.0.7
- pytest-cov>=2.5.1
- pytest-allure-adaptor>=1.7.7
- coverage>=4.3.1

To test the library simply use:

.. code:: sh

    pytest

By default, all tests are configured to run. However, some tests will take considerable amount of time.
To skip running the time consuming tests in the library, use:

.. code:: sh

    pytest -m "not slow"


Docker Environment
~~~~~~~~~~~~~~~~~~

If you are on a Windows host, ensure your local repo is saving files in unix format (LF instead of CRLF).
The functional tests will fail if the test input CSV files are saved in Windows format.
To set your local repository to that state, do:

.. code:: sh

    git config core.autocrlf input

To run the tests within a docker environment (such as when you are on a Windows host) run the following:

.. code:: sh

    docker build . -f Dockerfile-dev -t datalinking_test
    docker run --rm -it datalinking_test

To enter and explore the Docker container directly do the following:

.. code:: sh

    docker run --rm -it datalinking_test /bin/bash


How to Use
----------

To use the library and run a linking/de-duplication project, you need to create your project json file.
Having a json project, you can apply the library by :

.. code:: python

    python -m cdilinker.linker.link_json -p <project-file>


De-Duplication Project
----------------------

The input of the linking code is a linking/de-duplication project which, is defined as a sequence of
linking/de-duplication steps. De-duplication/Linking projects are defined by json files.
Below are samples of de-duplication and linking projects :

.. code:: JSON

    {
       "matched_url":"",
       "datasets":[
          {
             "description":"Education data file to be de-deplicated.",
             "format":"CSV",
             "url":"/projects/cdi/linkage/datasets/educ_for_dedup.csv",
             "title":"Education raw data for deduplication",
             "entity_field":"REC_ID",
             "index_field":"INGESTION_ID",
             "name":"Educ_For_Dedup"
          }
       ],
       "description":"Deduplication project of Education data",
       "linked_url":"",
       "output_root":"/projects/cdi/linkage/linking/",
       "steps":[
          {
             "group":false,
             "seq":1,
             "blocking_schema":{
                "transformations":[
                   "EXACT",
                   "SOUNDEX"
                ],
                "left":[
                   "BIRTH_DATE",
                   "FAMILY_NAME"
                ]
             },
             "linking_schema":{
                "comparisons":[
                   {
                      "name":"SOUNDEX"
                   },
                   {
                      "name":"EXACT"
                   },
                   {
                      "name":"NYSIIS"
                   }
                ],
                "left":[
                   "FIRST_GIVEN_NAME",
                   "CANADIAN_POSTAL_CODE",
                   "PREF_FIRST_GIVEN_NAME"
                ]
             }
          },
          {
             "group":true,
             "seq":2,
             "blocking_schema":{
                "transformations":[
                   "EXACT",
                   "NYSIIS"
                ],
                "left":[
                   "BIRTH_DATE",
                   "PREF_FIRST_GIVEN_NAME"
                ]
             },
             "linking_schema":{
                "comparisons":[
                   {
                      "name":"SOUNDEX"
                   },
                   {
                      "name":"NYSIIS"
                   },
                   {
                      "name":"SOUNDEX"
                   },
                   {
                      "name":"SOUNDEX"
                   }
                ],
                "left":[
                   "FIRST_GIVEN_NAME",
                   "PREF_FAMILY_NAME",
                   "SECOND_GIVEN_NAME",
                   "FAMILY_NAME"
                ]
             }
          }
       ],
       "type":"DEDUP",
       "linking_method":"DTR",
       "name":"Educ_For_Dedup"
    }

A De-duplication project consists of the input data file and a set of de-duplication steps.
The input datafile definition includes the path(URL) to data file,
name and title and the index field that uniquely identifies each record in the file.

Each de-duplication step includes the specification of blocking and linking variables and the transformation/comparison
algorithms. The blocking variables are used to reduce the comparison space and find potential record pairs.
The linking schema specifies the variables the must be compared by the corresponding comparison algorithms to find
records that belong to the same entities.

The group flag in each step indicates if the matched records will be grouped as a single entity and removed from
the input file or not. If the flag is false then not entity identifier will be generated for the matched records and
they will used in next de-duplication step. Otherwise, the matched records will be grouped and assigned the same entity
id and the records will be removed from the input file.

The outputs of a de-duplication project are :

*   De-duplicated output file with the new ENTITY_ID column. All the records that belong to the same entity will be
assigned same entity id. The file is sorted by entity id.

*   De-duplication summary report as a pdf file.

*   De-duplication detailed output that indicates the records are linked and the first step at which they are linked.


Linking Project Project
-----------------------

.. code:: JSON

    {
      "matched_url": "",
      "datasets": [
        {
          "description": "Education de-duplicated dataset",
          "format": "CSV",
          "url": "/projects/cdi/linkage/datasets/educ_dedup.csv",
          "title": "De-deplicated dataset",
          "entity_field": "ENTITY_ID",
          "index_field": "REC_ID",
          "name": "Education_Dedup"
        },
        {
          "description": "JTST Deduped dataset",
          "format": "CSV",
          "url": "/projects/cdi/linkage/datasets/jtst_dedup.csv",
          "title": "JTST Deduped dataset",
          "entity_field": "ENTITY_ID",
          "index_field": "REC_ID",
          "name": "JTST_DEDUPED"
        }
      ],
      "description": "Education JTST data linking",
      "linked_url": "",
      "output_root": "/Projects/cdi/linkage/linking/",
      "results_file": "education_jtst_summary.pdf",
      "steps": [
        {
          "seq": 1,
          "blocking_schema": {
            "right": [
              "BIRTH_DT",
              "FIRST_NAME_TXT"
            ],
            "transformations": [
              "EXACT",
              "SOUNDEX"
            ],
            "left": [
              "BIRTH_DATE",
              "FIRST_GIVEN_NAME"
            ]
          },
          "linking_schema": {
            "comparisons": [
              {
                "args": {
                  "max_edits": 2
                },
                "name": "LEVENSHTEIN"
              },
              {
                "name": "EXACT"
              }
            ],
            "right": [
              "LAST_NAME_TXT",
              "POSTAL_TXT"
            ],
            "left": [
              "FAMILY_NAME",
              "CANADIAN_POSTAL_CODE"
            ]
          }
        },
        {
          "seq": 2,
          "blocking_schema": {
            "right": [
              "POSTAL_TXT",
              "LAST_NAME_TXT"
            ],
            "transformations": [
              "EXACT",
              "SOUNDEX"
            ],
            "left": [
              "CANADIAN_POSTAL_CODE",
              "FAMILY_NAME"
            ]
          },
          "linking_schema": {
            "comparisons": [
              {
                "name": "SOUNDEX"
              },
              {
                "name": "NYSIIS"
              }
            ],
            "right": [
              "COMMUNITY_TXT",
              "FIRST_NAME_TXT"
            ],
            "left": [
              "COMMUNITY_OR_LOCATION",
              "FIRST_GIVEN_NAME"
            ]
          }
        }
      ],
      "relationship_type": "1T1",
      "type": "LINK",
      "linking_method": "DTR",
      "name": "education_jtst"
    }

A linking project is defined by:

*   Datasets. These are the files to be linked.

*   Type of entity relationship. This defines how entities relate to each other:

    1. 1T1 : one-to-one
    2. 1TM: One-to-many
    3. MT1: many-to-one


*   Linking steps

Each linking step is defined by:

*   Selection of blocking variables. This defines the size of the search space
*   Selection of linking variables. This defines the comparison space
*   Selection of comparison operations to be performed on blocking and linking variables.


Blocking and Linking Variables
------------------------------

In general, a variable could function as a blocking or linking variable or both; this functionality may change from one
step to another. In order words, a variable could be a blocking variable or a linking variable or both
(e.g., blocking: Soundex of first name; linking: jaro-winkler of first name) within a step and this might change in
a different linking step.


The linking process generates the following output files:

*   Linking summary pdf report.

*   Linked output file. This file contains information about linked entities.
it also describes the linking step where said entities were linked.

*   Matched_but_not_linked file. This file contains information about matched entities that were not linked due to
conflicts on the type-of-relationship.

.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
    :alt: License: MIT
.. |nbsp| unicode:: 0xA0