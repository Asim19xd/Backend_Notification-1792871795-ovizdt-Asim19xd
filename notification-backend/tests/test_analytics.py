from services.worker.analytics import AnalyticsPipeline


def test_analytics_pipeline():
    pipeline = AnalyticsPipeline()
    pipeline.record_event("transaction_alert")
    pipeline.record_dispatch("sms", "transaction_alert", "delivered")
    pipeline.record_dispatch("email", "transaction_alert", "failed")

    summary = pipeline.summary()

    assert summary["counters"]["events_received"] == 1
    assert summary["counters"]["delivered"] == 1
    assert summary["counters"]["failed"] == 1
    assert summary["by_channel"]["sms"]["delivered"] == 1
