class PayoutReportFormatter:
    BORDERS = f"{'=' * 60}"
    HEADER = f"{'':<16}  {'name':<20}{'hours':>6}{'rate':>6}  {'payout':>8}"
    ROW = f"{'-' * 16:<16}  {{name:<20}}{{hours:>6}}{{rate:>6}}  {{payout:>8}}"
    TOTAL = f"{'Total:':<16}  {{name:<20}}{{hours:>6}}{{rate:>6}}  {{payout:>8}}"

    def format_payout_report(self, data: dict) -> str:
        lines = ['', self.BORDERS, 'Payout Report', self.BORDERS, self.HEADER]

        for department, employees in data.items():
            lines.append(f"{department}")
            total_hours = 0
            total_payout = 0

            for emp in employees:
                hours = int(emp.get("hours_worked", 0))
                rate = int(emp.get(
                    "hourly_rate", emp.get(
                        "rate", emp.get(
                            "salary", 0)
                    )
                ))
                payout = hours * rate
                total_hours += hours
                total_payout += payout

                lines.append(self.ROW.format(
                    name=emp["name"],
                    hours=hours,
                    rate=rate,
                    payout=f"${payout}"
                ))

            lines.append(self.TOTAL.format(
                name='', hours=total_hours, rate='', payout=f"${total_payout}"
            ))
            lines.append('')
        lines.append(self.BORDERS)
        return '\n'.join(lines)
