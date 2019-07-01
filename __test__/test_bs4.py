from bs4 import BeautifulSoup

html = '''<td class="title black">
	<div class="tit3" id='my-div'>
		<a href="/movie/bi/mi/basic.nhn?code=163788" title="알라딘">알라딘</a>
	</div>
</td>
'''


# 1. tag 조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    # print(bs)
    # print(type(bs))

    tag = bs.td
    # print(tag)
    # print(type(tag))

    tag = bs.a
    # print(tag)
    # print(type(tag))

    tag = bs.td.div
    # print(tag)
    # print(type(tag))

    tag = bs.td.h4
    print(tag)
    print(type(tag))


# 2. attribute 값 가져오기
def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag['class']) # list

    tag = bs.div
    # print(tag['id']) 에러! 없는값
    print(tag.attrs)


# 3. attribute 로 태그 조회하기
def ex3():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.find('td',attrs={'class':'title'})
    #print(tag)

    tag = bs.find(attrs={'class':'tit3'})
    print(tag)
    print(type(tag))


def main():
    # ex1()
    # ex2()
    ex3()


if  __name__ == '__main__':
    main()