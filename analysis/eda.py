import pandas as pd
from datetime import datetime
from static.category import age_range, dayname
from analysis.descriptive import readcsv
from analysis.preprocess import pre_missingvalue
import seaborn as sns
sns.set_palette("Blues_d")
sns.set(font_scale=1)

# run and preprocessing
_click_log = readcsv('_click_log')
_products = readcsv('_products')
_purchase_log = readcsv('_purchase_log')
_users = readcsv('_users')


"""
## USER DEMOGRAPHY # 1.1
"""
user = pre_missingvalue(_users)
user['age_range'] = pd.Categorical(user['age_range'], age_range)

ax111_1 = sns.histplot(
    data=user,
    x='gender'
)
ax111_2 = sns.histplot(
    data=user,
    x='age_range',
    hue='gender'
)
ax111_2.tick_params(axis='x', rotation=45)

"""
PURCHASE SUM # 1.2
"""
_purchase_log['dt'] = pd.to_datetime(_purchase_log['dt'], format='%Y%m%d')
ax121_1 = sns.displot(
    data=_purchase_log,
    x="measure",
    kind="kde",
    fill=True)

ax121_2_df = _purchase_log.groupby(['dt'], as_index=False)['measure'].sum()
ax121_2 = sns.lineplot(
    data=ax121_2_df,
    x="dt",
    y="measure"
)
ax121_2.tick_params(axis='x', rotation=45)

_purchase_log['dt'] = pd.to_datetime(_purchase_log['dt'], format='%Y%m%d')
_purchase_log['dayname'] = _purchase_log['dt'].dt.day_name()
_purchase_log['dayname'] = pd.Categorical(_purchase_log['dayname'], dayname)
ax121_3_df = _purchase_log.groupby(['dayname'], as_index=False)['measure'].sum()
ax121_3 = sns.barplot(
    data=ax121_3_df,
    x='dayname',
    y='measure'
)
ax121_3.tick_params(axis='x', rotation=45)
ax121_3.bar_label(ax121_3.containers[0], fontsize=14)