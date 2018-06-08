import sys
from baseX import base_decode

def url_to_id(pic_url):
    base16 = '0123456789abcdef'
    base62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    token = pic_url.split('/')[4][:8]
    if token[:2] != '00':
        id = base_decode(token,alphabet=base16)
    else:
        id = base_decode(token)
    return id

if __name__ == "__main__":
    id = url_to_id(sys.argv[1])
    print('uploader\'s homepage : http://weibo.com/%s' %id)
