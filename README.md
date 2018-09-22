# Taxi-Trip-Time-Prediction

### Notes

This project is in development.

### Goal

Predict the remaining taxi time given the taxi route taken so far and other features.

Submit the total time taken.

### List of Data Sources

https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii/data

### List of Data Descriptions

- Descriptions taken from https://www.kaggle.com/c/pkdd-15-taxi-trip-time-prediction-ii/data
1. TRIP_ID: (String) It contains an unique identifier for each trip;
2. CALL_TYPE: (char) It identifies the way used to demand this service. It may contain one of three possible values:
‘A’ if this trip was dispatched from the central;
‘B’ if this trip was demanded directly to a taxi driver on a specific stand;
‘C’ otherwise (i.e. a trip demanded on a random street).
3. ORIGIN_CALL: (integer) It contains an unique identifier for each phone number which was used to demand, at least, one service. It identifies the trip’s customer if CALL_TYPE=’A’. Otherwise, it assumes a NULL value;
4. ORIGIN_STAND: (integer): It contains an unique identifier for the taxi stand. It identifies the starting point of the trip if CALL_TYPE=’B’. Otherwise, it assumes a NULL value;
5. TAXI_ID: (integer): It contains an unique identifier for the taxi driver that performed each trip;
6. TIMESTAMP: (integer) Unix Timestamp (in seconds). It identifies the trip’s start;
7. DAYTYPE: (char) It identifies the daytype of the trip’s start. It assumes one of three possible values:
‘B’ if this trip started on a holiday or any other special day (i.e. extending holidays, floating holidays, etc.);
‘C’ if the trip started on a day before a type-B day;
‘A’ otherwise (i.e. a normal day, workday or weekend).
8. MISSING_DATA: (Boolean) It is FALSE when the GPS data stream is complete and TRUE whenever one (or more) locations are missing
9. POLYLINE: (String): It contains a list of GPS coordinates (i.e. WGS84 format) mapped as a string. The beginning and the end of the string are identified with brackets (i.e. [ and ], respectively). Each pair of coordinates is also identified by the same brackets as [LONGITUDE, LATITUDE]. This list contains one pair of coordinates for each 15 seconds of trip. The last list item corresponds to the trip’s destination while the first one represents its start;

### Ideas

- At every path step, create a row and target, time to arrival

### Today's Goal

- Plan the steps of the project

### Steps

- ETL (Training Dataset)
  - X Get the time taken in total
  - We manually edited the 41st line of the metadata file to fix a typo
  - Get the closest locations "polyline_names"
  - Use "polylines_names" to create a markov chain
  - With the markov chain, find the E(X) steps to end given any starting location (Used as a feature later) (It has about 60 unique values)
  - Save the ~60 unique locations and their E(X) steps to end in a CSV markov_expected_steps.csv
  - Save the transformed_train.csv CSV with polyline_names
- ETL (Test Dataset)
  - Get the closest locations "polyline_names"
  - Save the transformed_test.csv CSV with polyline_names
- Explore
  - Create a visualization for the Markov Chain for presentation later (A Simple transition matrix heatmap is probably good enough)
  - consider dropping rows with missing data.  Found we should drop it.
- Prepare Data
  - Clean
    - Drop rows with missing data if it is a small amount
    - Consider cleaning call_type or day_type if bad values
    - Consider cleaning origin_call or origin_stand if something other than NULL and the regular values
  - New Rows/Columns
    - Get average time taken for call_typeA/B/C (3 columns) (Take one time per trip_id and average correctly)
    - Get average time taken for those with that origin_call or origin_stand (Including NA) (One column, combine them into one column) (Take one time per trip_id and average correctly)
    - add lots of day features (See MLM blogpost for ideas)
    - Average path length given each of those day features, then drop the day features (Take one time per trip_id and average correctly)
    - Turn each row into many rows (# of rows is the polylines length of coordinates) and label each row number
    - Given the row number, trim polylines to be the length of coordinates of that number
    - Use the newly created table and use that value for the first step in the journey
    - Use that created table and "polyline_names" for the middle step in the journey so far
    - Use that created table and "polyline_names" for the last step in the journey so far
    - Drop polyline_names
    - drop taxi_id and trip_id
