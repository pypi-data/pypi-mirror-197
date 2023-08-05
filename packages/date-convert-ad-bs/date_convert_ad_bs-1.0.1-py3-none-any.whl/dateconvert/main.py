from datetime import datetime
import json
import os
# Get the absolute path of the 'common' directory
common_dir = os.path.join(os.getcwd(), '..', '..', 'common')

with open(os.path.join(common_dir, 'constants.json'), 'r') as f:
    constants = json.load(f)


class DateConvert:
    def __init__(self):
        self.max_day_diff = constants['MAX_DAY_DIFF']
        self.min_bs_year = constants['MIN_BS_YEAR']
        self.mills_in_day = constants['MILLS_IN_DAY']
        self.min_ad_year = constants['MIN_AD_YEAR']
        self.min_ad_month = constants['MIN_AD_MONTH']
        self.min_ad_day = constants['MIN_AD_DAY']
        self.numberOfDaysEachYearBS = constants['DAYS_EACH_YEAR_BS']
        self.numberOfDaysEachMonthBS = constants['DAYS_EACH_MONTH_BS']

    def format_bs_date(self, year: int, month: int, day: int) -> str:
        month_str = f"0{month}" if month < 10 else str(month)
        day_str = f"0{day}" if day < 10 else str(day)
        return f"{year}-{month_str}-{day_str}"

    def ad_to_bs(self, year=int, month=int, day=int) -> str:
        """
            Convert a date from the Gregorian calendar(AD) to the Bikram Sambat (BS) calendar.

            Args:
                year (int): The Gregorian year (1943 to 2044).
                month (int): The Gregorian month (0 to 11).
                day (int): The Gregorian day (1 to 31).

            Returns:
                str: The corresponding date in the Gregorian calendar in the format 'YYYY-MM-DD'.

            Raises:
                ValueError: If the year, month, or day are out of range.
        """
        start_date = datetime(
            self.min_ad_year, self.min_ad_month+1, self.min_ad_day)

        if not year:
            year = datetime.utcnow().year
        if not month:
            month = datetime.utcnow().month
        if not day:
            day = datetime.utcnow().day

        if year < 1943 or year > 2044:
            return ValueError("Invalid Date out of range.")

        if month < 0 or month > 11:
            return ValueError("Month must be between 0 and 11.")

        if day < 1 or day > 31:
            return ValueError("Day must be between 1 and 31.")

        day_diff = int(
            (datetime(year, month+1, day) -
             start_date).total_seconds()*1000 / self.mills_in_day
        )

        if day_diff < 0 or day_diff > self.max_day_diff:
            return ValueError("Invalid Date out of range.")

        year_bs = self.min_bs_year
        total_count = 0
        count_upto_previous_year = 0

        # find Year only first
        for key, value in self.numberOfDaysEachYearBS.items():
            count_upto_previous_year = total_count
            total_count += value
            if total_count > day_diff:
                year_bs = key
                break
        nth_day_of_year = day_diff - count_upto_previous_year + 1

        # find month
        total_count_month_wise = 0
        count_upto_previous_month = 0
        month_bs = 0

        for days_in_month in self.numberOfDaysEachMonthBS[year_bs]:
            count_upto_previous_month = total_count_month_wise
            total_count_month_wise += days_in_month
            if count_upto_previous_month > 0:
                month_bs += 1
            if nth_day_of_year <= total_count_month_wise:
                break

        day_bs = nth_day_of_year - count_upto_previous_month
        return self.format_bs_date(year_bs, month_bs+1, day_bs)

    def bs_to_ad(self, year=int, month=int, day=int) -> str:
        """
        Convert a date from the Bikram Sambat (BS) calendar to the Gregorian calendar(AD).

        Args:
            year (int): The Bikram Sambat year (2000 to 2100).
            month (int): The Bikram Sambat month (0 to 11).
            day (int): The Bikram Sambat day (1 to 33).

        Returns:
            str: The corresponding date in the Gregorian calendar in the format 'YYYY-MM-DD'.

        Raises:
            ValueError: If the year, month, or day are out of range.
        """
        if year < 2000 or year > 2100:
            return ValueError("Invalid Date out of range.")

        if month < 0 or month > 11:
            return ValueError("Month must be between 0 and 11.")

        if day < 1 or day > 33:
            return ValueError("Day must be between 1 and 33.")

        dayCount = 0
        for key, value in self.numberOfDaysEachYearBS.items():
            if year == 2000:
                break
            dayCount += value
            if int(key) == year - 1:
                break

        for i in range(month):
            dayCount += self.numberOfDaysEachMonthBS[str(year)][i]

        dayCount += day - 1

        final_time = (
            int(datetime(self.min_ad_year,
                         self.min_ad_month+1,
                         self.min_ad_day)
                .timestamp()) * 1000
            + dayCount * self.mills_in_day
        )
        return datetime.fromtimestamp(final_time / 1000).strftime("%Y-%m-%d")
