import pandas as pd
from googletrans import Translator

def pre_missingvalue(df):
    """
    Applicable for user data
    """
    __before_df = df
    __remove_missingvalues = __before_df.dropna()
    df = __remove_missingvalues[~__remove_missingvalues['gender'].fillna('').str.contains('unknown')]
    print(
        'BEFORE : ', len(__before_df),
        ' NOW : ', len(df),
        ' OMITTED : ', len(__before_df) - len(df)
    )
    return df

def pre_category_translation():
    products = pd.read_csv('_products.csv')
    # 오류(SettingWithCopyError 발생)
    pd.set_option('mode.chained_assignment', 'raise') # SettingWithCopyError
    # 경고(SettingWithCopyWarning 발생, 기본 값입니다)
    pd.set_option('mode.chained_assignment', 'warn') # SettingWithCopyWarning
    # 무시
    pd.set_option('mode.chained_assignment',  None) # <==== 경고를 끈다

    products_category = products.category.unique()
    products_category_df = pd.DataFrame(products_category, columns=['category'])

    translator = Translator()
    products_category_df['category_trans'] = 'category'

    for i in range(len(products.index)-1):
        products_category_df.loc[i, 'category_trans'] = products_category_df['category_trans'][i].replace('category', translator.translate(products_category_df.category[i], dest='ko').text)
