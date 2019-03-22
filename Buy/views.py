from Buy.models import *
from alipay import AliPay
import random,datetime,time,os
from Seller.views import myencode
from django.http import JsonResponse
from Seller.models import Goods,Seller
from ShopProject.settings import MEDIA_ROOT
from django.core.paginator import Paginator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render,HttpResponseRedirect

def randomNum():
    num=random.randint(100000,999999)
    return num

def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        username = cookie.get("name")
        session = request.session.get("user") #获取session
        user = Buy.objects.filter(username = username).first()
        if user and session == user.username: #校验session
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buy/login/")
    return inner



def about_myself(request):
    return render(request,'buy/about_myself.html')

def shipin(request):

    urladdress = request.POST.get('url')
    request.session['url2'] = urladdress
    url = []
    urllist = Url.objects.all()
    for i in urllist:
        url.append({"name":i.address,"url":i.url})

    return render(request,'buy/shipin.html',locals())

def index(request):
    hot_one = Goods.objects.filter(id =19)[0]
    hot_one_img = str(hot_one.image_set.first().img_adress)
    hot_one_description = hot_one.goods_name
    hot_one_id=hot_one.id
    hot_tow = Goods.objects.filter(id= 21)[0]
    hot_tow_img = str(hot_tow.image_set.first().img_adress)
    hot_tow_description = hot_tow.goods_name
    hot_tow_id = hot_tow.id

    data = []
    data2 = []
    data3 =[]
    goods = Goods.objects.all()
    num=1
    for i in goods:
        image = i.image_set.first()
        img = str(image.img_adress)
        if num < 5:
            data2.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        if 22>num>19:
            data.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        if 24>num>21:
            data3.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        num += 1
    return render(request,'buy/index.html',locals())


def contact_us(request):
    if request.method == 'POST' and request.POST:
        name = request.POST.get('your-name')
        email = request.POST.get('your-email')
        phone = request.POST.get('your-phone')
        subject = request.POST.get('your-subject')
        message = request.POST.get('your-message')
        c=ContactUs()
        c.name=name
        c.email=email
        c.phone=phone
        c.subject=subject
        c.message=message
        c.save()
        return HttpResponseRedirect('/buy/about_myself/')
    return render(request,'buy/contact_us.html')

@cookieValid
def all_shop(request,page):
    data = []
    page = int(page)
    id = request.session.get("id")
    # s = Seller.objects.get(id=id)
    db_student = Goods.objects.all()
    everone = Paginator(db_student,9)  # 每一页的数据条
    count_data = everone.count  # 统计所有数据
    list = everone.page(page)  # 第一页数据
    # page_range=everone.page_range #页码范围
    pageEnd = count_data / 1
    bj = count_data//9
    if bj<5:
        page_range = range(1,bj+2)
    else:
        if pageEnd != int(pageEnd):
            pageEnd = pageEnd + 1
        if page <=3:
            page_range = range(1, 6)
        elif page > pageEnd:
            page_range = range(1, 6)
        elif page >= pageEnd - 2:
            page_range = range(int(pageEnd)-4, int(pageEnd) + 1)
        elif page>3:
            page_range = range(page - 2, page + 3)
    for i in list:
        image = i.image_set.first()
        img = str(image.img_adress)
        data.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id,"nowprice":i.goods_now_price})
    return render(request,'buy/all_shop.html',locals())

def jd(request):
    return render(request,'buy/jd.html')


def login(request):
    data=''
    if request.method=='POST' and request.POST:
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=Buy.objects.filter(email=email).first()
        if user and user.password==myencode(password):
            response=HttpResponseRedirect('/buy/index/')
            response.set_cookie('name',user.username)
            response.set_cookie('id',user.id)
            request.session['user']=user.username
            return response
        else:
            data='用户名或密码错误'
    return render(request, 'buy/login.html',{"data":data})

@cookieValid
def logout(request):
    response = HttpResponseRedirect("/buy/login/")
    response.delete_cookie("name")
    response.delete_cookie("id")
    del request.session["user"]
    return response


def sendemail(request):
    data={"data":"返回值"}
    if request.method=="GET" and request.GET:
        email=request.GET.get("email")
        subject = "注册邮件"
        num=randomNum()
        text_content = "hello python"
        html_content ="""
            <p>尊敬的用户，你的验证码为%s</p>
        """%num
        message = EmailMultiAlternatives(subject,text_content,"18224516533@163.com",[email])
        message.attach_alternative(html_content,"text/html")
        message.send()
        check=CheckEmail()
        check.num=num
        check.time=datetime.datetime.now()
        check.email=email
        check.save()
    return JsonResponse(data)


def register(request):
    data=''
    if request.method=='POST' and request.POST:
        name=request.POST.get("name")
        useremail=request.POST.get("email")
        password=request.POST.get("password")
        userpassword=request.POST.get("passwordaging")
        code=request.POST.get("number")
        phone = request.POST.get("phone")
        email = CheckEmail.objects.filter(email=useremail).first()
        if email and code==email.num:
            now=time.mktime(datetime.datetime.now().timetuple())
            old=time.mktime(email.time.timetuple())
            if now-old>=84600:
                data='验证码过期'
                email.delete()
            else:
                if userpassword==password:
                    b=Buy()
                    b.phone=phone
                    b.username=name
                    b.email=useremail
                    b.password=myencode(password)
                    b.save()
                    email.delete()
                    return HttpResponseRedirect('/buy/login/')
                else:
                    data="密码不一致！"
                    email.delete()
        else:
            data='验证码或邮箱错误'
            email.delete()
    return render(request,'buy/register.html',{"data":data})

@cookieValid
def all_seller(request):
    all=[]
    shop=Seller.objects.all()
    for i in shop:
        all.append({'img':str(i.photo),'name':i.nickname,'id':i.id})
    return render(request,'buy/all_seller.html',locals())

@cookieValid
def seller_shop(request,id):
    id=int(id)
    a=Seller.objects.get(id=id)
    data = []
    goods = a.goods_set.all()
    for i in goods:
        image = i.image_set.first()
        img = str(image.img_adress)
        data.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
    return render(request, 'buy/seller_shop.html', {'data': data,"a":a})

@cookieValid
def shop_detail(request,num):
    all={}
    data=0
    allimg=[]
    other = []
    others =Goods.objects.all()
    bj=0
    for i in others:
        image = i.image_set.first()
        img = str(image.img_adress)
        if 7<bj<10:
            other.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        if 21>bj>18:
            other.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        if 23>bj>21:
            other.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
        bj += 1
    good=Goods.objects.get(id=num)
    seller=good.seller.id
    goods=Goods.objects.filter(seller_id=seller)
    mg=good.image_set.all()
    bj = 0
    for i in mg:
        if bj<=2:
            allimg.append(str(i.img_adress))
            bj+=1
    for i in goods:
        images=i.image_set.first()
        paths=(str(images.img_adress))
        if int(i.id)!=int(num) and data<=4:
            all[i]=paths
            data+=1
    img=good.image_set.first()
    path = str(img.img_adress)
    return render(request,'buy/shop_detail.html',locals())

@cookieValid
def cart(request):
    id=request.COOKIES.get("id")
    add=Address.objects.filter(buyer=int(id))
    data=[]
    pay=0
    number=0
    goods = BuyCar.objects.filter(user = int(id))
    for i in goods:
        money=float(i.price)*int(i.num)
        pay+=money
        number=int(i.num)
        data.append({'money':money,'other':i})
    return render(request,'buy/cart.html',locals())

@cookieValid
def jump_cart(request,goodid):
    id=request.COOKIES.get("id")
    s = Goods.objects.filter(id=int(goodid)).first()
    img = s.image_set.first()
    if request.method=="POST" and request.POST:
        count=request.POST.get("count")
        butcar=BuyCar.objects.filter(user=int(id),goodId=goodid).first()
        if butcar:
            butcar.num+=int(count)
            butcar.save()
        else:
            car=BuyCar()
            car.goodId=goodid
            car.name=s.goods_name
            car.price=s.goods_price
            car.user=Buy.objects.get(id=int(id))
            car.num=int(count)
            car.picture=img.img_adress
            car.save()
    else:
        HttpResponseRedirect('/buy/login/')
    return HttpResponseRedirect('/buy/cart/')

@cookieValid
def clear(request):
    id = request.COOKIES.get("id")
    goods = BuyCar.objects.filter(user=int(id))
    goods.delete()
    return HttpResponseRedirect('/buy/cart/')

@cookieValid
def delete(request,num):
    id = request.COOKIES.get("id")
    goods=BuyCar.objects.filter(user=int(id),goodId=num)
    goods.delete()
    return HttpResponseRedirect('/buy/cart/')

@cookieValid
def add_address(request):
    id=request.COOKIES.get('id')
    if request.method=='POST' and request.POST:
        recver=request.POST.get('recver')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        add=Address()
        add.recver=recver
        add.phone=phone
        add.address=address
        add.buyer=Buy.objects.get(id=int(id))
        add.save()
        return HttpResponseRedirect('/buy/address/')
    return render(request,'buy/add_address.html')

@cookieValid
def address(request):
    id = request.COOKIES.get('id')
    add=Address.objects.filter(buyer=int(id))
    return render(request, 'buy/address.html', locals())

@cookieValid
def addressDel(request,id):
    add = Address.objects.filter(id=int(id))
    add.delete()
    return HttpResponseRedirect('/buy/address/')

@cookieValid
def addressChange(request,id):
    addChange=Address.objects.filter(id=int(id)).first()
    if request.method == 'POST' and request.POST:
        recver = request.POST.get('recver')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        addChange.recver = recver
        addChange.phone = phone
        addChange.address = address
        addChange.save()
        return HttpResponseRedirect('/buy/address/')
    return render(request, 'buy/add_address.html',locals())

@cookieValid
def payMoney(request):
    buyId=request.COOKIES.get('id')
    address=request.POST.get('address')
    Addr=Address.objects.get(id=int(address))
    money = request.POST.get("zj")
    order=Order()
    now=datetime.datetime.now()
    number=str(random.randint(10000,99999))+now.strftime("%Y%m%d%I%M%S")
    order.number=number
    order.time=now
    order.statue=1
    order.money=money
    order.user=Buy.objects.get(id=int(buyId))
    order.orderAddress=Addr
    order.save()
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQAB
    -----END PUBLIC KEY-----'''
    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
        MIIEpQIBAAKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQABAoIBAQCwT2ezsS1pG6xsMwQ//9vcwt8mlvEOVZG4iDVYxcHsaOP10E7lWmUibR5XT5FDkjjq/NeSHwfzKV5EtpxAlmh73qAAaH53sJcZPJMUCI67qJXXDM5xNy8YItaV/Q28QbIoDnuiH57WepxbzcuQdyX66pdLrxTcpTf+yTynQcJOzLc+AKQQnF2DdXO/3/mDmkabMK4L1B0u9zQlIj4gvf3o5GJJaiQZvSEgjxerWRwE5f+wrNb37RNTEgNZ4i64qYYg3+0SVG+d+gxhzJvHJUZ68Bj3JBT5pIxV94lsExyDK89dfbMWJ6O1Fk5D3hrSJK5DFAsHmAtw8/2GCrmIGtA5AoGBAPDG4Hmhw04Jt3ITlS2KXBdW8fTsuMMkWoxIeWk3kHGJoHRYN5sMLMoKvgIoYS0sVGw/3K92eftRzFxXOw8NCFjKI7bYEUsZiLDNSR1pUOPmE3D0t3rF4ZxHbpAHpw/ewOMP5tksg1RZrN0oxEmdx0RsS2OEdm/Q8OA+mppjpJEdAoGBAM1ELuIdP4RAb6Yp+e8nlcnWG+i5y1A6a/IftM5kK8KMOs7m6KejTzE2MufzTaPvXl4VxqDIxwhY993cE3Y7sIsehnEPnMgVlIk03drHRqOhnEjUNcwjHwA1VaqY+IJQDuRKD7jD4yS6Z6jImFzI89J3TLp1rXaJhWHA7dhv+IFHAoGBAL885swU3H/eHdNAlIsQSubKyvDDGFj+ReEIK06TsGlNa6Ec9EV03Ro4gARMuCpd/EviSVEf4/DmXk+1hRYGPuvu2YD/inTAuh3bX0g5/uKUOjrMU/Lyuqga4EkLmvhy73cpiSxTO5hChZc/KvBhngTNku9fJYbYSImDj94yaGJNAoGAO5TSAwI4YJwPjGzcxmV4HhkPCtN7R3Ndx+8aHVqINTVdEJeH6rkFkKRJzHgcDjy56Jdri1ocI7knYXezEnuq+AbJQWIlwRI6hkUZLJrxTyfm5GDsqK99HSNeFWHHqJOybuNsgtYhRZTx59UqHKyb0XidhfYIfsLWO5SztUJzIJsCgYEA2QG2u/d+8dJQry76QU8SP8dELxUwHHAipVPALA7PMbgZBx2O5KWcXh9TdBjroT4NrO1O2HgyOTOLBaVMNgcziuK8WfHmZg9trFWLjGcsZYPYh056CNYZGcf5k1pk1BtRHJ0T0OefmCNErTqcHYrfovEUMg3hXo+nZXJfJv/wdI8=
    -----END RSA PRIVATE KEY-----'''
    alipay = AliPay(
        appid="2016092400585742",  # 支付宝app的id
        app_notify_url=None,  # 会掉视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=number,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="果饮ORGANIK:订单编号"+number,
        return_url="http://118.89.241.6/buy/car/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    data_r = ("https://openapi.alipaydev.com/gateway.do?" + order_string)
    return HttpResponseRedirect(data_r)