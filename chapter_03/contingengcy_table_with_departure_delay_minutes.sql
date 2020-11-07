use bts;
-- true negative
select count(dest) from flights where arr_delay < ARR_DELAY_THRESH and dep_delay < DEP_DELAY_THRESH;
-- false negative （H0 error, position of this type-1 error in the contingency table is different from convention in statistics ）
select count(dest) from flights where arr_delay >= ARR_DELAY_THRESH and dep_delay < DEP_DELAY_THRESH;
-- false positive
select count(dest) from flights where arr_delay < ARR_DELAY_THRESH and dep_delay >= DEP_DELAY_THRESH;
-- true positive
select count(dest) from flights where arr_delay >= ARR_DELAY_THRESH and dep_delay >= DEP_DELAY_THRESH;