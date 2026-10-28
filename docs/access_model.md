# Access model

How the access module decides who has access to vaccination.

- An area counts as served if an **active** provider is within the
  service radius of the area's center point.
- Distance is the great-circle (haversine) distance in kilometers.
- This measures **geographic access, not medical need**.
- Candidate mobile sites are only scored on areas that are currently
  underserved, so a site gets no credit for areas that are already served.
- Population is counted per area: an area is either covered or not.