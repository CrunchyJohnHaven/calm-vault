// Jurisdictional pay-rate floor for trial / first-project rates.
// Numbers are USD-per-hour minimums for independent-contractor work.
// US workers get federal minimum wage floor; other countries get a market
// floor that avoids race-to-the-bottom while remaining competitive.
// Admin can override any floor per-match.

export const COUNTRY_FLOOR = {
  // US: $7.25/hr federal floor; we set higher for our own ethics.
  "United States": 12.00,
  "Canada": 12.00,
  "United Kingdom": 11.00,
  "Ireland": 11.00,
  "Germany": 11.00,
  "France": 10.50,
  "Netherlands": 11.00,
  "Spain": 9.50,
  "Portugal": 8.50,
  "Italy": 9.50,
  "Poland": 6.50,
  "Greece": 7.00,
  "Romania": 5.00,
  "Ukraine": 4.50,
  "Serbia": 5.00,
  "Turkey": 4.50,
  "Israel": 9.00,
  "Egypt": 3.50,
  "Morocco": 3.50,
  "Nigeria": 3.50,
  "Ghana": 3.50,
  "Kenya": 3.50,
  "South Africa": 4.50,
  "India": 4.00,
  "Pakistan": 3.50,
  "Bangladesh": 3.50,
  "Sri Lanka": 3.50,
  "Nepal": 3.50,
  "Indonesia": 3.50,
  "Vietnam": 4.00,
  "Thailand": 4.50,
  "Malaysia": 5.00,
  "Philippines": 4.00,
  "Japan": 9.00,
  "South Korea": 9.00,
  "Australia": 14.00,
  "New Zealand": 12.00,
  "Mexico": 5.00,
  "Brazil": 5.00,
  "Argentina": 4.00,
  "Chile": 6.00,
  "Colombia": 4.00,
  "Peru": 4.00,
  "Other": 4.00
};

export function floorForCountry(country) {
  if (!country) return 4.00;
  if (COUNTRY_FLOOR[country] != null) return COUNTRY_FLOOR[country];
  return 4.00; // unknown country → conservative floor
}
