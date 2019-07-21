# Psychological Traits Aggregation Package

This package allows users to apply the proper aggregation method to raw totals of speech data. Find the raw totals [HERE](https://jelambert.com/leader-psych/)

###Important notes:
* Users should ensure that the data has the proper type (int).

* This package assumes users are using the standard variable names from Profiler Plus (see list at bottom)

* Users should ensure no missing data is passed to the function.



## Installation and import:
* Clone into a directory

* Navigate to Psych_Agg/

* python setup.py install

* from Psych_Agg import Agg_Raw as ar

## Primary function:

  calc_raws(df)
    This will return a dataframe of the aggregated totals with correct values for LTA and OPcode variables.


## Example usage:

user_dataframe = raw_totals.groupby(["date_unit", "group_unit"])[list_of_raw_variables].sum().reset_index()

aggregated_data = ar.calc_raws(user_dataframe)


### List of standard variable names:
list_of_raw_variables = ['vcount', 'HDIS', 'LDIS', 'HTASK', 'LTASK', 'IC',
       'EC', 'HBIAS', 'LBIAS', 'HSC', 'LSC', 'HCC', 'LCC', 'HPWR', 'LPWR',
       'self-pun', 'self-threat', 'self oppose', 'self appeal', 'self promise',
       'self reward', 'other punish', 'other threaten', 'other oppose',
       'other appeal', 'other promise', 'other reward']
