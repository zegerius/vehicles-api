# Vehicles API

We need a simple API with a single endpoint returning list of vehicles for the applied filters. List of vehicles is provided as a Python dictionary in `data.py`, API should import and use it as the data source. Consider this API is going to be used by a UI with three filtering drop-down lists. On this hypothetical UI, end user will be able to apply filters and see the resulting list of vehicles. After applying one filter, end user expects to see only relevant options for other filters.

- API should support filtering on three properties of vehicles: `brand`, `type` and `color`.
- Applying multiple filters at the same time should be possible.
- API should return **possible filtering options** for these three properties as well as **filtered list of vehicles**.
- When a filter is applied, possible filtering options for **other filters** should be narrowed down. **Example:** API should not return a **yellow** color option when `type=train` filter applied, because there are no yellow trains in the data, but `type` filter should still have `car` and `airplane` options available.

Any libraries or frameworks may be used, as far as it can install itself and run on a computer which has the Python interepreter. Readability and maintainability of the code will be valued more than extra fancy features. If you have any questions about the assignment, please don't hesitate to contact and ask us.
