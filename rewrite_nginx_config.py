# from nginxparser import load
from nginxparser import dump
# from nginxparser import dumps
# print load(open("/Users/yinshuo/baidu/python-scripts/pycharm/ali_config/nginx.conf"))
# dump([['worker_processes', '8'], [['events'], [['use', 'epoll'], ['worker_connections', '10240']]]], open("/Users/yinshuo/baidu/python-scripts/pycharm/ali_config/new-nginx.conf", 'w'))
# print dumps([['worker_processes', '8'], [['events'], [['use', 'epoll'], ['worker_connections', '10240']]]])
# print load(open("/Users/yinshuo/baidu/python-scripts/pycharm/ali_config/nginx.conf"))


class rewrite_nginx_config(object):
    def __init__(self, upsteram_ip_dict):
        self.upsteram_ip_dict = upsteram_ip_dict
        self.global_block = []
        self.events_block = []
        self.http_block = []
        self.location_block = []
        self.add_global_parms()
        self.add_events_parms()
        self.add_http_parms()

    def add_global_parms(self, ifbrace=False):
        if ifbrace:
            inner_block = []
        self.global_block.append(['worker_processes', '8'])

    def add_events_parms(self, ifbrace=True):
        if ifbrace:
            inner_block = []
        self.events_block.append(['events'])
        inner_block.append(['use', 'epoll'])
        inner_block.append(['worker_connections', '10240'])
        self.events_block.append(inner_block)
        self.global_block.append(self.events_block)

    def add_upstream_parms(self, ifbrace=True, upsteram_ip_list=None, upsteram_name=None):
        upstream_block = []
        if ifbrace:
            inner_block = []
        upstream_block.append(['upstream', upsteram_name])
        if not upsteram_ip_list:
            print 'no upsteram_ip_list send'
        if not upsteram_name:
            print 'nog upsteram_name send'
        if 'https' in upsteram_name:
            upstream_port = '8443'
        else:
            upstream_port = '8080'
        for each_ip in upsteram_ip_list:
            inner_block.append(['server', each_ip + ':' + upstream_port + ' weight=1'])
        # inner_block.append(['check', 'interval=10000 rise=2 fall=3 timeout=6000'])
        upstream_block.append(inner_block)
        return upstream_block

    def add_location_parms(self, ifbrace=True, location_name=None, location_backend_name=None):
        location_block = []
        if ifbrace:
            inner_block = []
        if not location_name:
            print 'no location_name send'
        if not location_backend_name:
            print 'no location_backend_name send'
        location_block.append(['location', location_name])
        if 'https' in location_backend_name:
            inner_block.append(['proxy_pass', 'https://' + location_backend_name])
        else:
            inner_block.append(['proxy_pass', 'http://' + location_backend_name])
        inner_block.append(['proxy_http_version', '1.1'])
        inner_block.append(['proxy_set_header', 'Connection ""'])
        inner_block.append(['proxy_connect_timeout', '600'])
        inner_block.append(['proxy_read_timeout', '600'])
        inner_block.append(['proxy_send_timeout', '600'])
        inner_block.append(['proxy_set_header', 'Host $host'])
        inner_block.append(['proxy_set_header', 'X-Real-IP $remote_addr'])
        inner_block.append(['proxy_set_header', 'REMOTE-HOST $remote_addr'])
        inner_block.append(['proxy_set_header', 'X-Forwarded-For $proxy_add_x_forwarded_for'])
        location_block.append(inner_block)
        return location_block

    def add_server_parms(self, ifbrace=True, server_if_https=None):
        server_block = []
        if ifbrace:
            inner_block = []
        server_block.append(['server'])
        if server_if_https:
            inner_block.append(['listen', '443 ssl'])
            inner_block.append(['server_name', '*.gotye.com.cn'])
            inner_block.append(['ssl', 'on'])
            inner_block.append(['ssl_certificate', '/usr/local/1__.gotye.com.cn_bundle.crt'])
            inner_block.append(['ssl_certificate_key', '/usr/local/2__.gotye.com.cn.key'])
            # add location block
            inner_block.append(self.add_location_parms(location_name='/', location_backend_name='https_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi', location_backend_name='https_others_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/AccessToken', location_backend_name='https_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetVideoUrls', location_backend_name='https_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetServerUrl', location_backend_name='https_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetLiveContext', location_backend_name='https_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/SetLiveStatus', location_backend_name='https_backend'))
            server_block.append(inner_block)
            return server_block
        else:
            inner_block.append(['listen', '80'])
            inner_block.append(['server_name', 'localhost'])
            inner_block.append(self.add_location_parms(location_name='/', location_backend_name='http_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi', location_backend_name='http_others_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/AccessToken', location_backend_name='http_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetVideoUrls', location_backend_name='http_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetServerUrl', location_backend_name='http_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/GetLiveContext', location_backend_name='http_backend'))
            # inner_block.append(self.add_location_parms(location_name='/liveApi/SetLiveStatus', location_backend_name='http_backend'))
            server_block.append(inner_block)
            return server_block

    def add_http_parms(self, ifbrace=True):
        if ifbrace:
            inner_block = []
        self.http_block.append(['http'])
        inner_block.append(['include', 'mime.types'])
        inner_block.append(['default_type', 'application/octet-stream'])
        inner_block.append(['log_format', 'main \'$remote_addr [$time_local] "$request" $upstream_addr $upstream_status "$http_x_forwarded_for" $status $body_bytes_sent $upstream_response_time $request_time $request_length $request_body\''])
        inner_block.append(['access_log', '/usr/local/nginx/logs/access.log  main'])
        inner_block.append(['sendfile', 'on'])
        inner_block.append(['keepalive_timeout', '10'])
        inner_block.append(['limit_req_zone', '$binary_remote_addr  zone=api:10m   rate=30r/s'])
        inner_block.append(['client_max_body_size', '500M'])
        inner_block.append(['proxy_ignore_client_abort', 'on'])
        inner_block.append(['client_header_buffer_size', '2048k'])
        inner_block.append(['large_client_header_buffers', '4 2048k'])
        # add upstream block, once a time
        inner_block.append(self.add_upstream_parms(self, upsteram_ip_list = self.upsteram_ip_dict['upsteram_ip_list'], upsteram_name = 'https_backend'))
        inner_block.append(self.add_upstream_parms(self, upsteram_ip_list = self.upsteram_ip_dict['upsteram_ip_list'], upsteram_name = 'http_backend'))
        # inner_block.append(self.add_upstream_parms(self, upsteram_ip_list = self.upsteram_ip_dict['other_upstrean_ip_list'], upsteram_name = 'https_others_backend'))
        # inner_block.append(self.add_upstream_parms(self, upsteram_ip_list = self.upsteram_ip_dict['other_upstrean_ip_list'], upsteram_name = 'http_others_backend'))
        # add server block, once a time
        inner_block.append(self.add_server_parms(self,server_if_https = True))
        inner_block.append(self.add_server_parms(self,server_if_https = False))
        self.http_block.append(inner_block)
        self.global_block.append(self.http_block)

def rewrite_final_nginx(upsteram_ip_list, nginx_file_pwd):
    # example upsteram_ip_dict = {'upsteram_ip_list': ['10.10.10.1', '10.10.10.2'], 'other_upstrean_ip_list': ['10.10.10.3', '10.10.10.4']}
    # upsteram_ip_dict = {'upsteram_ip_list': upsteram_ip_list, 'other_upstrean_ip_list': other_upstrean_ip_list}
    upsteram_ip_dict = {'upsteram_ip_list': upsteram_ip_list}

    rewrite_object = rewrite_nginx_config(upsteram_ip_dict)
    # example dump(rewrite_object.global_block, open("/Users/yinshuo/baidu/python-scripts/pycharm/ali_config/new-nginx.conf", 'w'))
    try:
        dump(rewrite_object.global_block, open(nginx_file_pwd, 'w'))
        return True
    except:
        False
    # print rewrite_object.global_block
    # print dumps(rewrite_object.global_block, indentation = 4)

if __name__ == "__main__":
    upsteram_ip_list = ['10.10.10.1', '10.10.10.2']
    # other_upstrean_ip_list = ['10.10.10.3', '10.10.10.4']
    nginx_file_pwd = "/usr/local/nginx/new-nginx.conf"
    rewrite_final_nginx(upsteram_ip_list, nginx_file_pwd)

