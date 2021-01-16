# encoding: utf-8

from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor


document = """
1. Background
1.1 Context
In 2019, Treasury Board (TB) published the Guide to Cost Estimating, which replaced the 2016 Guidelines on Costing.  The new guide provides practical guidance for departments on how to develop credible cost estimates, and presents a four‑step approach to costing.

The Employment and Social Development Canada (ESDC) Costing Policy requires the Department to have accurate, relevant and timely costing information that supports decision making at all levels of the organization. Accurate and complete cost estimates require high-quality and timely information to support decisions.

ESDC manages in excess of $146 billion in public funds to deliver the programs under its mandate, including $3.3 billion in operating funds to manage its day-to-day operationsFootnote1. Inaccurate or incomplete costing may cause cost overruns or budgetary lapses in both major projects and implementation of programs, resulting in internal financial pressures or lapses. The need to improve costing information has been identified by TB as a key strategic objective.

1.2 Audit objective
The objectives of this audit were to assess whether the Department’s:

costing process and methodology are in compliance with the TB Guidelines on CostingFootnote2 and are consistently applied across the Department
cost estimates are reliable
process to support the requirement for the Chief Financial Officer (CFO) attestation is adequate
1.3 Scope
ESDC’s costing landscape includes costing to establish resource requirements (Resource Determination Model), costing of Cabinet proposals, project costing and activity-based costing.

This audit focused on project costing only. The audit scope included all types of projectsFootnote3 completed during the period from April 2018 to June 2019:

major projects greater than $1,000,000
minor projects between $250,000 and $1,000,000
small projects under $250,000
Costing accuracy was not examined in the context of this audit.

1.4 Methodology
The audit was conducted using a number of methodologies including:

reviewed and analyzed ESDC’s costing framework to assess its alignment with the TB Guidelines on Costing. Elements of ESDC’s framework that were reviewed and analyzed include the Costing Policy, Costing Process and Guide to Project Costing and Reporting
performed walkthroughs
interviewed management and staff
reviewed a judgmental sample of project costing workbooks and documentation and performed gap analysis on ESDC’s costing practices to identify areas for improvement, based on best practices recommended by the TB Guidelines on Costing
The approach and methodology followed the TB Policy on Internal Audit and the International Standards for the Professional Practice of Internal Auditing. These standards require that the audit be planned and performed in such a way as to obtain reasonable assurance that the audit objectives are achieved.

2. Audit findings
Project costing at ESDC
ESDC has implemented a stage-gated process for project management. The stage-gate approach segments the project lifecycle into a series of activities (stages) and decision points (gates). Stages represent the project progress, gates are point-in-time where decisions are made by the appropriate governance body to continue investing in the project, based on the information available at the time. Gates occur at the end of project stages.

ESDC uses a standardized costing template to establish the cost estimated to deliver the project. The costing process requires the Project Manager (PM) and the Financial Management Advisor (FMA) to collaborate on the development of sound cost estimates and effective expenditure management for each of the five stage gates which include the justification, initiation, planning, execution and closure stages of a project.

Requirements on the accuracy of cost estimates vary as the projects progress from Gate 1 to 5. Cost accuracy could go from ±100% at Gate 1 to ±50% at Gate 2 to ±10% at Gate 3. Cost variance needs to be explained at each gate. At Gate 5, the variance between the actual cost and cost estimates are documented by completing variance analysis and lessons learned.
"""

# Object of automatic summarization.
auto_abstractor = AutoAbstractor()
# Set tokenizer.
auto_abstractor.tokenizable_doc = SimpleTokenizer()
# Set delimiter for making a list of sentence.
auto_abstractor.delimiter_list = [".", "\n"]
# Object of abstracting and filtering document.
abstractable_doc = TopNRankAbstractor()
# Summarize document.
result_dict = auto_abstractor.summarize(document, abstractable_doc)

print("result: ")
print(" ".join([s.strip() for s in result_dict["summarize_result"]]))
