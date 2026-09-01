from unittest.mock import MagicMock, patch

from collectors.aws_collector import check_cloudtrail_enabled


def test_cloudtrail_enabled_when_logging():
    mock_client = MagicMock()

    mock_client.describe_trails.return_value = {
        "trailList": [
            {
                "Name": "governx-test-trail",
                "TrailARN": (
                    "arn:aws:cloudtrail:us-east-1:"
                    "123456789012:trail/governx-test-trail"
                ),
            }
        ]
    }

    mock_client.get_trail_status.return_value = {
        "IsLogging": True
    }

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_client,
    ):
        results = check_cloudtrail_enabled()

    assert len(results) == 1
    assert results[0].check_id == "cloudtrail_enabled"
    assert results[0].status.value == "PASS" 