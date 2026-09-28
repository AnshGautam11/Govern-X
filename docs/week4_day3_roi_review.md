
## ROI formula review (report_service.py, _sample_roi_for_remediation and _build_roi)
- roi_ratio = risk_reduced / cost; returns None when cost is 0 (no divide-by-zero).
- _build_roi returns status "no_gap_data" with no items when there are no remediations, so no ROI is invented.
- Each item carries data_quality "assumed_sample_data" plus the assumed reduction percentage and severity.
- roi_ratio is a benefit/cost ratio, not net ROI (cost is not subtracted). Recommend labelling it "benefit/cost ratio" in the PDF so executives do not read it as a percentage return.
- Not yet reviewed: how risk_reduced is derived and whether it can be negative under Monte Carlo sampling; behaviour for a severity missing from the cost table.
