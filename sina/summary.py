import pymongo
from sina.douban_settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME_POST, DB_NAME

years = [2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
types = ['搞笑', '文艺', '科幻', '惊悚', '爱国', '红色', '共产党']
type_other=['搞笑', '文艺', '科幻', '惊悚']
type_v=[ '爱国', '红色', '共产党']

def summary():
    client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    db = client[DB_NAME_POST]
    summary_ = {}
    for _year in years:
        for index, _type in enumerate(types):
            table = "movie{}{}".format(index, _year)
            info = dict()
            info['count'] = db[table].find().count()
            info['style'] = _type
            info['year'] = _year
            info['rate_aver'] = 0
            sum_star = 0
            sum_rate = 0
            sum_vote = 0
            votes = 0
            stars = dict()
            top10 = []
            limit = 0
            for item in db[table].find():
                if item.get('rate'):
                    info['rate_aver'] += eval(item.get('rate'))
                    sum_rate += 1
                if item.get('star'):
                    stars[item['star']] = stars.get(item['star'], 0) + 1
                if item['information'].get('star5'):
                    stars['star_aver_5'] = stars.get('star_aver_5', 0) + eval(item['information']['star5'][0:-1])
                    stars['star_aver_4'] = stars.get('star_aver_4', 0) + eval(item['information']['star4'][0:-1])
                    stars['star_aver_3'] = stars.get('star_aver_3', 0) + eval(item['information']['star3'][0:-1])
                    stars['star_aver_2'] = stars.get('star_aver_2', 0) + eval(item['information']['star2'][0:-1])
                    stars['star_aver_1'] = stars.get('star_aver_1', 0) + eval(item['information']['star1'][0:-1])
                    info['star_aver_5'] = stars['star_aver_5']
                    info['star_aver_4'] = stars['star_aver_4']
                    info['star_aver_3'] = stars['star_aver_3']
                    info['star_aver_2'] = stars['star_aver_2']
                    info['star_aver_1'] = stars['star_aver_1']
                    sum_star += 1
                if item['information'].get('votes'):
                    votes += int(item['information'].get('votes'))
                    sum_vote += 1
                if limit < 10:
                    top10.append(item)
                    limit += 1
            info['sum_star'] = sum_star
            info['sum_rate'] = sum_rate
            info['sum_vote'] = sum_vote
            info['votes'] = votes
            info['top10'] = top10
            summary_[table] = info

            with open('summary.txt', 'a') as file:
                print('----------------------------------------------------', file=file)
                print('类型', info['style'], file=file)
                print('年份', info['year'], file=file)
                print('影片数量', info['count'], file=file)
                if sum_vote == 0:
                    print('评价人数(平均)', int(votes), file=file)
                else:
                    print('评价人数(平均)', int(votes * 1.0 / sum_vote), file=file)
                if sum_rate == 0:
                    print('评分(平均)', info['rate_aver'], file=file)
                else:
                    print('评分(平均)', int(info['rate_aver'] * 1.0 / sum_rate), file=file)

                print('星级(平均)', file=file)
                if sum_star == 0:
                    sum_star = 1
                print(
                    '---5星:{}%'.format(int(stars['star_aver_5'] * 1.0 / sum_star) if stars.get('star_aver_5') else ''),
                    file=file)
                print(
                    '---4星:{}%'.format(int(stars['star_aver_4'] * 1.0 / sum_star) if stars.get('star_aver_4') else ''),
                    file=file)
                print(
                    '---3星:{}%'.format(int(stars['star_aver_3'] * 1.0 / sum_star) if stars.get('star_aver_3') else ''),
                    file=file)
                print(
                    '---2星:{}%'.format(int(stars['star_aver_2'] * 1.0 / sum_star) if stars.get('star_aver_2') else ''),
                    file=file)
                print(
                    '---1星:{}%'.format(int(stars['star_aver_1'] * 1.0 / sum_star) if stars.get('star_aver_1') else ''),
                    file=file)
                print('----------------------------------------------------', file=file)

            with open('summary_top10.txt', 'a') as file:
                print('----------------------------------------------------', file=file)
                print('类型', info['style'], file=file)
                print('年份', info['year'], file=file)
                print('top10', file=file)
                for i, top in enumerate(top10):
                    print('------top{}------'.format(i), file=file)
                    print('片名', top.get('title'), file=file)
                    print('评分', top.get('rate'), file=file)
                    print('评价人数', top['information'].get('votes'), file=file)
                    print('星级', file=file)
                    print('---5星:{}'.format(top['information'].get('star5')), file=file)
                    print('---4星:{}'.format(top['information'].get('star4')), file=file)
                    print('---3星:{}'.format(top['information'].get('star3')), file=file)
                    print('---2星:{}'.format(top['information'].get('star2')), file=file)
                    print('---1星:{}'.format(top['information'].get('star1')), file=file)

                print('----------------------------------------------------', file=file)

    need_count = ['count', 'sum_vote', 'votes', 'rate_aver', 'sum_star', 'sum_rate', 'sum_vote','star_aver_5',
                  'star_aver_4', 'star_aver_3', 'star_aver_2', 'star_aver_1']

    #按类型汇总
    for index, _type in enumerate(types):
        info = dict()
        for _year in years:
            table = "movie{}{}".format(index, _year)
            summ = summary_[table]
            for key in need_count:
                if summ.get(key):
                    info[key] = info.get(key, 0) + summ[key]


        with open('summary_all_year.txt', 'a') as file:
            print('----------------------------------------------------', file=file)
            print('类型', _type, file=file)
            print('影片数量', info['count'], file=file)
            if info['sum_vote'] == 0:
                print('评价人数(平均)', int(info['votes']), file=file)
            else:
                print('评价人数(平均)', int(info['votes'] * 1.0 / info['sum_vote']), file=file)
            if info['sum_rate'] == 0:
                print('评分(平均)', info['rate_aver'], file=file)
            else:
                print('评分(平均)', int(info['rate_aver'] * 1.0 / info['sum_rate']), file=file)

            print('星级(平均)', file=file)
            if info['sum_star'] == 0:
                info['sum_star'] = 1
            print(
                '---5星:{}%'.format(int(info['star_aver_5'] * 1.0 / info['sum_star']) if info.get('star_aver_5') else ''),
                file=file)
            print(
                '---4星:{}%'.format(int(info['star_aver_4'] * 1.0 / info['sum_star']) if info.get('star_aver_4') else ''),
                file=file)
            print(
                '---3星:{}%'.format(int(info['star_aver_3'] * 1.0 / info['sum_star']) if info.get('star_aver_3') else ''),
                file=file)
            print(
                '---2星:{}%'.format(int(info['star_aver_2'] * 1.0 / info['sum_star']) if info.get('star_aver_2') else ''),
                file=file)
            print(
                '---1星:{}%'.format(int(info['star_aver_1'] * 1.0 / info['sum_star']) if info.get('star_aver_1') else ''),
                file=file)
            print('----------------------------------------------------', file=file)

    # 按类型（爱国一类）汇总
    for index, _type in enumerate(type_other):
        info = dict()
        for _year in years:
            table = "movie{}{}".format(index, _year)
            summ = summary_[table]
            for key in need_count:
                if summ.get(key):
                    info[key] = info.get(key, 0) + summ[key]

        with open('summary_all_year_other.txt', 'a') as file:
            print('----------------------------------------------------', file=file)
            print('类型', _type, file=file)
            print('影片数量', info['count'], file=file)
            if info['sum_vote'] == 0:
                print('评价人数(平均)', int(info['votes']), file=file)
            else:
                print('评价人数(平均)', int(info['votes'] * 1.0 / info['sum_vote']), file=file)
            if info['sum_rate'] == 0:
                print('评分(平均)', info['rate_aver'], file=file)
            else:
                print('评分(平均)', int(info['rate_aver'] * 1.0 / info['sum_rate']), file=file)

            print('星级(平均)', file=file)
            if info['sum_star'] == 0:
                info['sum_star'] = 1
            print(
                '---5星:{}%'.format(int(info['star_aver_5'] * 1.0 / info['sum_star']) if info.get('star_aver_5') else ''),
                file=file)
            print(
                '---4星:{}%'.format(int(info['star_aver_4'] * 1.0 / info['sum_star']) if info.get('star_aver_4') else ''),
                file=file)
            print(
                '---3星:{}%'.format(int(info['star_aver_3'] * 1.0 / info['sum_star']) if info.get('star_aver_3') else ''),
                file=file)
            print(
                '---2星:{}%'.format(int(info['star_aver_2'] * 1.0 / info['sum_star']) if info.get('star_aver_2') else ''),
                file=file)
            print(
                '---1星:{}%'.format(int(info['star_aver_1'] * 1.0 / info['sum_star']) if info.get('star_aver_1') else ''),
                file=file)
            print('----------------------------------------------------', file=file)

    info = dict()
    for index, _type in enumerate(type_v):
        for _year in years:
            table = "movie{}{}".format(index+4, _year)
            summ = summary_[table]
            for key in need_count:
                if summ.get(key):
                    info[key] = info.get(key, 0) + summ[key]
                    if key == 'count':
                        print('count',summ[key])
                        print('count--', info[key])

    with open('summary_all_year_guo.txt', 'a') as file:
        print('----------------------------------------------------', file=file)
        print('影片数量', info['count'], file=file)
        if info['sum_vote'] == 0:
            print('评价人数(平均)', int(info['votes']), file=file)
        else:
            print('评价人数(平均)', int(info['votes'] * 1.0 / info['sum_vote']), file=file)
        if info['sum_rate'] == 0:
            print('评分(平均)', info['rate_aver'], file=file)
        else:
            print('评分(平均)', int(info['rate_aver'] * 1.0 / info['sum_rate']), file=file)

        print('星级(平均)', file=file)
        if info['sum_star'] == 0:
            info['sum_star'] = 1
        print(
            '---5星:{}%'.format(int(info['star_aver_5'] * 1.0 / info['sum_star']) if info.get('star_aver_5') else ''),
            file=file)
        print(
            '---4星:{}%'.format(int(info['star_aver_4'] * 1.0 / info['sum_star']) if info.get('star_aver_4') else ''),
            file=file)
        print(
            '---3星:{}%'.format(int(info['star_aver_3'] * 1.0 / info['sum_star']) if info.get('star_aver_3') else ''),
            file=file)
        print(
            '---2星:{}%'.format(int(info['star_aver_2'] * 1.0 / info['sum_star']) if info.get('star_aver_2') else ''),
            file=file)
        print(
            '---1星:{}%'.format(int(info['star_aver_1'] * 1.0 / info['sum_star']) if info.get('star_aver_1') else ''),
            file=file)
        print('----------------------------------------------------', file=file)


if __name__ == '__main__':
    summary()
