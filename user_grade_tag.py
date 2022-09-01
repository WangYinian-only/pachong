# -*- codeing = utf-8 -*-
# @Time : 2022/3/12 17:05
# @Author : 王伊念
# File : user_grade_tag.py
# @Software : PyCharm

def main():
    target_table = 'profile_tag_user_grade'
    # 数据库
    use_database = '''use sparkTest3_2'''

    # 用户等级
    insert_user_grade_tag_01 = '''create table''' + target_table + '''
    as
    select user_id,
    'A111U003_001' as tag_id,
    user_grade as tag_name,
    '用户等级' as tag_type
    from user_info_new_tb
    where user_grade like '%钻石会员%'
    '''

    insert_user_grade_tag_02 = '''insert into table''' + target_table + '''
    select u.user_id,
    'A111U003_002' as tag_id,
    u.user_grade as tag_name,
    '用户等级' as tag_type
    from user_info_new_tb u
    where u.user_grade like '%金牌会员%'
    '''
