#coding:utf8

from algorithm import *
from filesys import *

# thanks for BeautifulSoup for xml/html parsing
from BeautifulSoup import *

htmlentities='''1.特色的
©	&copy;	&#169;	版权标志
|	&__n_e_v_e_r_e_x_i_s_t_1_; 	&#124;	竖线，常用作菜单或导航中的分隔符
·	&middot;	&#183;	圆点，有时被用来作为菜单分隔符
↑	&uarr;	&#8593;	上箭头，常用作网页“返回页面顶部”标识
€	&euro;	&#8364;	欧元标识
²	&sup2;	&#178;	上标2，数学中的平方，在数字处理中常用到，例如：1000²
½	&frac12;	&#189;	二分之一
♥	&hearts;	&#9829;	心型，用来表达你的心
2.常用的
 	&nbsp;	&#160;	空格
&	&amp;	&#38;	and符号，与
"	&quot;	&#34;	引号
©	&copy;	&#169;	版权标志
®	&reg;	&#174;	注册标志
™	&trade;	&#153;	商标标志
“	&ldquo;	&#147;	左双引号
”	&rdquo;	&#148;	右双引号
‘	&lsquo;	&#145;	做单引号
’	&rsquo;	&#146;	右单引号
«	&laquo;	&#171;	左三角双引号
»	&raquo;	&#187;	右三角双引号
‹	&lsaquo;	&#8249;	左三角单引号
›	&rsaquo;	&#8250;	右三角单引号
§	&sect;	&#167;	章节标志
¶	&para;	&#182;	段落标志
•	&bull;	&#149;	列表圆点（大）
·	&middot;	&#183;	列表圆点（中）
…	&hellip;	&#8230;	省略号
|	&__n_e_v_e_r_e_x_i_s_t_1_;		&#124;	竖线
¦	&brvbar;	&#166;	断的竖线
–	&ndash;	&#150;	短破折号
—	&mdash;	&#151;	长破折号
3.货币类
¤	&curren;	&#164;	一般货币符号
$	&__n_e_v_e_r_e_x_i_s_t_2_; 		&#36;	美元符号
¢	&cent;	&#162;	分
£	&pound;	&#163;	英镑
¥	&yen;	&#165;	日元
€	&euro;	&#8364;	欧元
4 数学类
<	&lt;		&#60;	小于号
>	&gt;		&#62;	大于号
≤	&le;		&#8804;	小于等于号
≥	&ge;		&#8805;	大于等于号
×	&times;	&#215;	乘号
÷	&divide;	&#247;	除号
−	&minus;	&#8722;	减号
±	&plusmn;	&#177;	加/减号
≠	&ne;		&#8800;	不等于号
¹	&sup1;	&#185;	上标1
²	&sup2;	&#178;	上标2
³	&sup3;	&#179;	上标3
½	&frac12;	&#189;	二分之一
¼	&frac14;	&#188;	四分之一
¾	&frac34;	&#190;	四分之三
‰	&permil;	&#8240;	千分率
°	&deg;	&#176;	度
√	&radic;	&#8730;	平方根
∞	&infin;	&#8734;	无限大
5.方向类
←	&larr;	&#8592;	左箭头
↑	&uarr;	&#8593;	上箭头
→	&rarr;	&#8594;	右箭头
↓	&darr;	&#8595;	下箭头
↔	&harr;	&#8596;	左右箭头
↵	&crarr;	&#8629;	回车箭头
⌈	&lceil;	&#8968;	左上限
⌉	&rceil;	&#8969;	右上限
⌊	&lfloor;	&#8970;	左下限
⌋	&rfloor;	&#8971;	右下限
6.其它
♠	&spades;	&#9824;	黑桃
♣	&clubs;	&#9827;	梅花
♥	&hearts;	&#9829;	红桃，心
♦	&diams;	&#9830;	方块牌
◊	&loz;	&#9674;	菱形
†	&dagger;	&#8224;	匕首
‡	&Dagger;	&#8225;	双剑号
¡	&iexcl;	&#161;	反向感叹号
¿	&iquest;	&#191;	反向问号'''.decode('utf8').split('\n')

htmlentities=filter(lambda line: not str.isdigit(line[0].encode('utf8')), htmlentities)
htmlentities=[tuple(line.split()) for line in htmlentities]
htmlentities=[t if t[0]!='&nbsp;' else tuple([" "]+list(t)) for t in htmlentities]

def clean_htmlentities(s):
	for (ch, en, num, text) in htmlentities:
		s=s.replace(en, '').replace(num, '')
	return s
	
def replace_htmlentities(s):
	'''html 实体替换'''
	for (ch, en, num, text) in htmlentities:
		s=s.replace(en, ch).replace(num, ch)
	return s

def parse_html(html):
	return BeautifulSoup(html)
	
def extract_body_text(html, rate=1):
	lst=html.split("\n")
	lst=[l.strip() for l in lst]
	lnum=[len(l) for l in lst]
	
	w=0
	for i in range(len(lnum)):
		now=lnum[i]
		if now==0:
			w+=1
			lnum[i]=-w*rate
		if now!=0 and w!=0:
			for j in range(1, int(w/2)+1):
				lnum[i-j]=-j*rate
				lnum[i-(w+1-j)]=-j*rate
			w=0
			
	max_sum, begin, end=max_sub_seq_sum(lnum)
	# print lnum
	return filter(lambda i:len(i)>0, lst[begin:end+1])
	
if __name__=="__main__":
	for i in htmlentities:
		a, b, c, d=i
		print i

