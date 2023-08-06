from typing import TYPE_CHECKING

from traccuracy._utils import get_relevant_kwargs, validate_matched_data

if TYPE_CHECKING:
    from typing import Dict, List, Optional, Type

    from traccuracy import TrackingData
    from traccuracy.matchers._matched import Matched
    from traccuracy.metrics._base import Metric


def run_metrics(
    gt_data: "TrackingData",
    pred_data: "TrackingData",
    matcher: "Type[Matched]",
    metrics: "List[Type[Metric]]",
    matcher_kwargs: "Optional[Dict]" = None,
    metrics_kwargs: "Optional[Dict]" = None,  # weights
) -> "Dict":
    """Compute given metrics on data using the given matcher.

    An error will be thrown if the given matcher is not compatible with
    all metrics in the given list. The returned result dictionary will
    contain all metrics computed by the given Metric classes, as well as
    general summary numbers e.g. false positive/false negative detection
    and edge counts.

    Args:
        gt_data (TrackingData): ground truth graph and optionally segmentation
        pred_data (TrackingData): predicted graph and optionally segmentation
        matcher (Matched): matching class to use to create correspondence
        metrics (List[Metric]): list of metrics to compute as class names
        matcher_kwargs (optional, dict): Dictionary of keyword argument for the
            matcher class
        metric_kwargs (optional, dict): Dictionary of any keyword args for the
            Metric classes

    Returns:
        Dict: dictionary of metrics indexed by metric name. Dictionary will be
        nested for metrics that return multiple values.
    """
    if matcher_kwargs is None:
        matcher_kwargs = {}
    matched = matcher(gt_data, pred_data, **matcher_kwargs)
    validate_matched_data(matched, metrics)
    metric_kwarg_dict = {
        m_class: get_relevant_kwargs(m_class, metrics_kwargs) for m_class in metrics
    }
    results = {}
    for _metric in metrics:
        relevant_kwargs = metric_kwarg_dict[_metric]
        result = _metric(matched, **relevant_kwargs)
        results[_metric.__name__] = result.results
    return results
