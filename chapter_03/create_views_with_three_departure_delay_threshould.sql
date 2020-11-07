use bts;
CREATE VIEW delayed_over_10_min AS SELECT * FROM flights WHERE dep_delay > 10;
CREATE VIEW delayed_over_15_min AS SELECT * FROM flights WHERE dep_delay > 15;
CREATE VIEW delayed_over_20_min AS SELECT * FROM flights WHERE dep_delay > 20;
