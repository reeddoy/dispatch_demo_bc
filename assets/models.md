# Models

- Chat

  - sender_id `str`
  - receiver_id `str`
  - files `list[dict]`
  - message `str`
  - url `str`

- User

  - user_type `str`
  - email `str`
  - password `str`
  - first_name `str` `nr`
  - last_name `str`
  - company_name `str`
  - image `str`
  - address `str`
  - referral `str`
  - affiliate_id `str`
  - phone_number `str`
  - user_name `str`
  - website `str`
  - service_areas `list[str]`
  - dispatche_fees `list[str]`
  - accept_new_authorities `bool`
  - ein `str`
  - mc `str`
  - dot `str`
  - offered_services `list[str]`
  - equipment_types `list[str]`
  - description `str`
  - verified `bool`
  - saved_loads `list[str]`
  - saved_trucks `list[str]`
  - favourites `list[str]`
  - membership `str`
  - on_trial `bool`
  - trial_complete `bool`
  - active `bool`
  - customer_id `str`
  - account_id `str`
  - contacts `list`
  - otp `int`
  - subscription_on `bool`

- Truck

  - user_id `str`
  - pickup `str`
  - delivery `str`
  - full_or_partial `str`
  - weight `float`
  - origin `str`
  - destination `str`
  - available_point `int`
  - phone_number `str`
  - equipment_type `str`
  - length `float`
  - comments `str`
  - trip_miles `str` `nr`

  - origin_latitude `float`
  - origin_longitude `float`
  - destination_latitude `float`
  - destination_longitude `float`

- Report

  - user_id `str`
  - company_name `float`
  - reported_company_name `str`
  - reported_company_id `str`
  - report `str`
  - files `list[str]`

- Review

  - user_id `str`
  - rating `float`
  - rater_id `str`
  - review `str`

- ReviewReply

  - user_id `str`
  - review_id `str`
  - rater_id `str`
  - reply `str`

- Comment

  - user_id `str`
  - post_id `str`
  - content `str`
  - files `list[str]`

- Post

  - user_id `str`
  - content `str`
  - likes `list[str]`
  - comments_ids `list[str]`
  - files `list[str]`

- LoadReferral

  - user_id `str`
  - pickup `str`
  - delivery `str`
  - full_or_partial `str`
  - weight `float`
  - origin `str`
  - destination `str`
  - number_of_stops `int`
  - phone_number `str`
  - equipment_type `str`
  - length `float`
  - comments `str`
  - rate_estimate `float`
  - points `int`
  - xchange_rate `float`
  - trip_miles `str` `nr`
  - origin_latitude `float`
  - origin_longitude `float`
  - destination_latitude `float`
  - destination_longitude `float`

- Load

  - user_id `str`
  - user_type `str`
  - load_type `str`
  - equipment_type `str`
  - load_id `int`
  - status `str`
  - truck `str`
  - bill_to `str`
  - rate `float`
  - trailer `str`
  - load_manager `str`
  - name `str`

  - shippers `list[dict]`
  - receivers `list[dict]`
  - other_charges `list[dict]`
  - note `str` `nr`

  - origin `str`
  - destination `str`

  - files `list[str]`
  - origin_latitude `float`
  - origin_longitude `float`
  - destination_latitude `float`
  - destination_longitude `float`

  - hours `float`

- Lounge

  - title `str`
  - user_id `str`
  - call_id `str`
  - description `str` `nr`
  - active_time `int`
  - closed `bool`
  - participants `list[str]`

- Subscription

  - subcription_id `str`
  - customer `str`
  - user_id `str`
  - package `str`
  - currency `str`

- UserBillTo

  - user_id `str`
  - company_name `str`
  - address `str`
  - phone_number `str`
  - email `str`
  - notes `str`

- UserLoadTo

  - user_id `str`
  - company_name `str`
  - address `str`
  - phone_number `str`
  - email `str`
  - notes `str`

- UserDriver

  - user_id `str`
  - driver_name `str`
  - address `str`
  - phone_number `str`
  - email `str`
  - notes `str`

- UserShipper

  - user_id `str`
  - company_name `str`
  - phone_number `str`
  - contact_person `str`
  - notes `str`

- UserReceiver

  - user_id `str`
  - company_name `str`
  - phone_number `str`
  - contact_person `str`
  - notes `str`

- UserTruck

  - user_id `str`
  - truck_number `str`
  - year `str`
  - make `str`
  - model `str`
  - tag_number `str`
  - notes `str`

- UserTrailer

  - user_id `str`
  - trailer_number `str`
  - year `str`
  - make `str`
  - model `str`
  - tag_number `str`
  - notes `str`

- UserSession

  - user_id `str`
  - logged_in `bool`

- Notification

  - user_id `str` `nr`
  - uid `str`
  - type `str`
  - username `str`
  - fetched `bool`
  - uid2 `str`
