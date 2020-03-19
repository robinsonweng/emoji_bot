from pixivpy3 import AppPixivAPI


appapi = AppPixivAPI()

# need login now
print(appapi.illust_detail(80111848))