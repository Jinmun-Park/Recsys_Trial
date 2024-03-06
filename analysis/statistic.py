from scipy import stats

def normality_test(data):
    stat, p = stats.shapiro(data)
    print("-- statistics = " + str('{:.2f}'.format(stat)))
    print("-- p-value = " + str('{:.2f}'.format(p)))
    if p > 0.05:
        print('-- Result : Sample data is normally distributed')
    else:
        print('-- Result : Sample data is not normally distributed')

def homogeneity_variance_test(*args):
    # H0: Groups have equal variances
    # H1: Groups have different variances
    stat, p = stats.levene(*args)
    print("-- statistics = " + str(list(map('{:.2f}'.format, stat))))
    print("-- p-value = " + str(list(map('{:.2f}'.format, p))))
    if p > 0.05:
        print('-- Result : Equal variance assumption is true')
    else:
        print('-- Result : Equal variance assumption is false')

def kruskal_test(*args):
    stat, p = stats.kruskal(*args)
    print("-- statistics = " + str(list(map('{:.2f}'.format, stat))))
    print("-- p-value = " + str(list(map('{:.2f}'.format, p))))
    if p > 0.05:
        print('-- Result : Equal variance assumption is true')
    else:
        print('-- Result : Equal variance assumption is false')

def two_sample_test(*args):
    """
    https://www.jmp.com/en_is/statistics-knowledge-portal/t-test/two-sample-t-test.html
    - When the variances for the two groups are not equal, we cannot use the pooled estimate of standard deviation.
    - Instead, we take the standard error for each group separately.
    - 모수 검정
    - 일반적으로 두 모집단의 표준편차가 동일하다고 가정하고 이들이 정규분포를 이룬다는 전제하에서 두 모집단의 평균의 차이를 검정한다.
    """
    # H0: The underlying population means are the same.
    # H1: The underlying population means are not equal.

    stat, p = stats.ttest_ind(*args, equal_var=False)
    print("-- statistics = " + str(list(map('{:.2f}'.format, stat))))
    print("-- p-value = " + str(list(map('{:.2f}'.format, p))))

    if p > 0.05:
        print('-- Result : Two sample groups have equal mean')
    else:
        print('-- Result : Two sample groups do not have equal mean')

def mann_whitney_test(*args):
    """
    Ordinal Scale(서열척도)에 사용되지만, 두 표본 집단의 관측치가 무작위로 추출되고 또 그 측정값을 순위할 수 있어야만 사용가능
    - 두 표본집단이 동일한 확률분포를 갖는 모집단으로부터 추출되었는지의 여부를 검정 -
    - 사회과학 분야에서 모집단이 정규분포를 이루고 있다는 전제조건을 충족시키기 어려운 경우여서 많이 이용됨 -
    """
    stat, p = stats.mannwhitneyu(*args)
    print("-- statistics = " + str(list(map('{:.2f}'.format, stat))))
    print("-- p-value = " + str(list(map('{:.2f}'.format, p))))

    if p > 0.05:
        print('-- Result : Two sample groups have equal mean')
    else:
        print('-- Result : Two sample groups do not have equal mean')


# run and preprocessing
_purchase_log = pd.read_csv(os.path.abspath(os.curdir) + '\\Recsys_Trial\\data\\' + '_purchase_log' + '.csv', na_values=np.nan)
_users = pd.read_csv(os.path.abspath(os.curdir) + '\\Recsys_Trial\\data\\' + '_users' + '.csv', na_values=np.nan)
_plog_users = pd.merge(_purchase_log, _users, on='user_id', how='left')


## (user_id vs product_id) 두 표본평균의 차이가 유의미한가
__print_missing_values([_plog_users])  # No missing values after the merge
plog_users = _plog_users.groupby(['user_id', 'gender'], as_index=False)['measure'].sum()
female_plog_users = plog_users.loc[plog_users['gender'] == 'f'][['measure']].reset_index(drop=True)  # 385 count
male_plog_users = plog_users.loc[plog_users['gender'] == 'm'][['measure']].reset_index(drop=True)  # 233 count


# 모집단의 분산이 알려져 있지 않은 경우
# 두 표본집단이 독립적이라고 가정

# Homogeneity Test
# P-value : 0.02
# Reject null - Groups have different variances (No Homogeneity)
homogeneity_variance_test(
    male_plog_users,
    female_plog_users
)

# Shapiro-Wilk
normality_test(male_plog_users)  # p-value 0.00 | Sample data is not normally distributed
normality_test(female_plog_users)  # p-value 0.00 | Sample data is not normally distributed

# Two Sample T test
# P-value : 0.08
# Reject null - Two sample groups have equal mean
two_sample_test(
    male_plog_users,
    female_plog_users
)

# Two sample non-parametric test
# P-value : 0.00
# Reject null - Two sample groups do not have equal mean
mann_whitney_test(
    male_plog_users,
    female_plog_users
)
