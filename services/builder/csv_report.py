from services.builder.base import BaseReportBuilder
from services.builder.formats.payout_report import PayoutReportFormatter


class PayoutReport(BaseReportBuilder):

    def build(self, data: dict) -> str:
        formatter = PayoutReportFormatter()
        return formatter.format_payout_report(data)
