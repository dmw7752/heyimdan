class Post(object):
    def __init__(self, my_date):
        self.date = my_date

post1 = Post('2014-03-20')
post2 = Post('2015-02-21')
post3 = Post('2015-03-22')
post4 = Post('2011-03-24')

posts = {'post1': post1, 'post2': post2, 'post3': post3, 'post4': post4}

for post in sorted(posts.values(), key=lambda x:x.date, reverse=True):
    print post.date

'''
OUTPUT

(heyimdan)(03/26 10:51:19) [dawhite@ hey_im_dan]$ python test.py
2015-03-22
2015-02-21
2014-03-20
2011-03-24
'''