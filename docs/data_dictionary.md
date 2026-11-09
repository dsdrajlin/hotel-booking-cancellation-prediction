# Data Dictionary

This document is a technical reference for the 32 columns in `data/raw/hotel_bookings.csv`. It describes what each column represents, its data type, and relevant value conventions. Exploratory findings and modeling decisions are documented in the EDA notebook.

## Columns

| Column | Type | Description |
| --- | --- | --- |
| `hotel` | Categorical | Hotel associated with the booking: `City Hotel` or `Resort Hotel`. |
| `is_canceled` | Binary target | Whether the booking was canceled: `1` = canceled, `0` = not canceled. This is the prediction target. |
| `lead_time` | Integer | Number of days between the booking date and the arrival date. |
| `arrival_date_year` | Integer | Calendar year of the planned arrival. |
| `arrival_date_month` | Categorical | Month of the planned arrival, stored as a month name. |
| `arrival_date_week_number` | Integer | Week number of the planned arrival date. |
| `arrival_date_day_of_month` | Integer | Day of the month of the planned arrival date. |
| `stays_in_weekend_nights` | Integer | Number of weekend nights (Saturday or Sunday) included in the booking. |
| `stays_in_week_nights` | Integer | Number of week nights (Monday through Friday) included in the booking. |
| `adults` | Integer | Number of adults included in the booking. |
| `children` | Numeric | Number of children included in the booking. |
| `babies` | Integer | Number of babies included in the booking. |
| `meal` | Categorical | Meal plan associated with the booking. Examples include `BB` (bed and breakfast), `HB` (half board), `FB` (full board), and `SC` (self-catering). |
| `country` | Categorical | Country of origin of the guest, represented by a country code. |
| `market_segment` | Categorical | Market segment associated with the booking, such as `Direct`, `Groups`, or `Online TA`. |
| `distribution_channel` | Categorical | Channel through which the booking was distributed, such as `Direct` or `TA/TO` (travel agents/tour operators). |
| `is_repeated_guest` | Binary | Whether the guest had made a booking at the hotel before: `1` = repeated guest, `0` = not repeated. |
| `previous_cancellations` | Integer | Number of previous bookings by the guest that were canceled before this booking. |
| `previous_bookings_not_canceled` | Integer | Number of previous bookings by the guest that were not canceled before this booking. |
| `reserved_room_type` | Categorical | Code for the room type reserved. The room-type codes are anonymized. |
| `assigned_room_type` | Categorical | Code for the room type assigned to the booking. The room-type codes are anonymized. |
| `booking_changes` | Integer | Number of changes made to the booking. |
| `deposit_type` | Categorical | Deposit policy associated with the booking: `No Deposit`, `Non Refund`, or `Refundable`. |
| `agent` | Categorical identifier | Identifier of the travel agent associated with the booking, when applicable. The value is an ID, not a measured quantity. |
| `company` | Categorical identifier | Identifier of the company associated with the booking, when applicable. The value is an ID, not a measured quantity. |
| `days_in_waiting_list` | Integer | Number of days the booking was on the waiting list before it was confirmed. |
| `customer_type` | Categorical | Booking type: `Contract`, `Group`, `Transient`, or `Transient-Party`. |
| `adr` | Numeric | Average daily rate associated with the booking. |
| `required_car_parking_spaces` | Integer | Number of car parking spaces requested by the booking. |
| `total_of_special_requests` | Integer | Number of special requests associated with the booking. |
| `reservation_status` | Categorical | Final status of the reservation, such as `Check-Out`, `Canceled`, or `No-Show`. |
| `reservation_status_date` | Date | Date on which the reservation status was set. |

## Sources

- [Hotel Booking Demand dataset on Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) — dataset download page.
- [António, Almeida, and Nunes, “Hotel booking demand datasets,” Data in Brief (2019)](https://doi.org/10.1016/j.dib.2018.11.126) — original data article describing the datasets and variables.
