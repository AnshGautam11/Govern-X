from unittest.mock import MagicMock, patch

from collectors.aws_collector import check_vpc_flow_logs_enabled


def test_vpc_flow_logs_enabled_when_enabled():
    mock_client = MagicMock()

    mock_client.describe_vpcs.return_value = {
        "Vpcs": [
            {
                "VpcId": "vpc-0123456789abcdef0",
            }
        ]
    }

    mock_client.describe_flow_logs.return_value = {
        "FlowLogs": [
            {
                "FlowLogId": "fl-0123456789abcdef0",
                "ResourceId": "vpc-0123456789abcdef0",
                "FlowLogStatus": "ACTIVE",
            }
        ]
    }

    with patch(
        "collectors.aws_collector.get_client",
        return_value=mock_client,
    ):
        results = check_vpc_flow_logs_enabled()

    assert len(results) == 1
    assert results[0].check_id == "vpc_flow_logs_enabled"
    assert results[0].status.value == "PASS"