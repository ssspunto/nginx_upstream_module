#
# Common HTTP function for make tests easy
#

import json
import urllib
import urllib2
import traceback


#VERBOSE = True
VERBOSE = False
BASE_URL = 'http://0.0.0.0:8081'


def post_form(url, values, headers=None):
    out = '{}'
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        response = urllib2.urlopen(req)
        out = response.read()
        rc = response.getcode()
        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")
        if rc != 500:
            return (rc, json.loads(out))
        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();
        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")
        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)


def post(url, data, headers):
    out = '{}'
    try:
        req = urllib2.Request(url)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        req.add_header('Content-Type', 'application/json')

        res = urllib2.urlopen(req, json.dumps(data).encode('utf8'))
        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")

        if rc != 500:
            return (rc, json.loads(out))

        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();

        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")

        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def request_raw(url, data, headers):
    out = '{}'
    try:
        req = urllib2.Request(url)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        req.add_header('Content-Type', 'application/json')

        res = urllib2.urlopen(req, data)
        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")

        if rc != 500:
            return (rc, json.loads(out))

        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();

        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")

        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def request(url, data, headers = None):
    return request_raw(url, json.dumps(data), headers)

def put(url, data, headers):
    out = '{}'
    try:
        req = urllib2.Request(url)
        req.get_method = lambda: 'PUT'
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        if data:
            req.add_header('Content-Type', 'application/json')
            res = urllib2.urlopen(req, json.dumps(data))
        else:
            res = urllib2.urlopen(req)

        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")

        if rc != 500:
            return (rc, json.loads(out))

        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();

        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")

        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def get(url, data, headers):
    out = '{}'
    try:
        full_url = url
        if data:
            full_url = url + '?' + urllib.urlencode(data)
        req = urllib2.Request(full_url)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])

        res = urllib2.urlopen(req)
        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")

        if rc != 500:
            return (rc, json.loads(out))

        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();

        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")

        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def get_result(o):
    return o['result'][0]

def assert_if_not_error(s, code = None):
    assert('error' in s), 'expected error'
    assert('message' in s['error']), 'expected error message'
    assert('code' in s['error']), 'expected error message'
    if code:
        assert(s['error']['code'] == code), 'expected code'

def get_success(url, data, headers):
    (code, msg) = get(url, data, headers)
    assert(code == 200), 'expected 200'
    result = get_result(msg)
    return result

def get_success_pure(url, data, headers):
    (code, msg) = get(url, data, headers)
    assert(code == 200), 'expected 200'
    return msg

def post_success(url, data, headers=None, print_f=None):
    (code, msg) = post(url, data, headers)
    if print_f:
        print_f(code, msg)
    assert(code == 200), 'expected 200'
    result = get_result(msg)
    return result

def post_form_success(url, data, headers=None, print_f=None):
    (code, msg) = post_form(url, data, headers)
    if print_f:
        print_f(code, msg)
    assert(code == 200), 'expected 200'
    return msg

def post_form_ec500(url, data, headers=None, print_f=None):
    (code, msg) = post_form(url, data, headers)
    if print_f:
        print_f(code, msg)
    assert(code == 500), 'expected 500'
    return msg

def post_success_pure(url, data, headers=None):
    (code, msg) = post(url, data, headers)
    assert(code == 200), 'expected 200'
    return msg

def put_success(url, data, headers):
    (code, msg) = put(url, data, headers)
    assert(code == 200), 'expected 200'
    result = get_result(msg)
    return result

def put_fail(url, data, headers):
    return put(url, data, headers)

def get_fail(url, data, headers):
    (code, msg) = get(url, data, headers)
    return (code, msg)

def delete(url, data, headers):
    out = '{}'
    try:
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        if data:
            req.add_header('Content-Type', 'application/json')
            res = urllib2.urlopen(req, json.dumps(data))
        else:
            res = urllib2.urlopen(req)

        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        if VERBOSE:
            print("code: ", rc, " recv: '", out, "'")

        if rc != 500:
            return (rc, json.loads(out))

        return (rc, False)
    except urllib2.HTTPError as e:
        if e.code == 400:
            out = e.read();

        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")

        return (e.code, json.loads(out))
    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def delete_success(url, data, headers):
    (code, msg) = delete(url, data, headers)
    assert(code == 200), 'expected 200'
    result = get_result(msg)
    return result

def assert_headers(result, headers_in):
    for header in headers_in:
        header_from_server = result[0]['headers'][header]
        assert(header_from_server == headers_in[header]), 'expected headers_in'

def assert_headers_pure(result, headers_in):
    for header in headers_in:
        header_from_server = result['headers'][header]
        assert(header_from_server == headers_in[header]), 'expected headers_in'

def assert_query_args(result, args):
    for arg in args:
        server_arg = result[0]['args'][arg]
        assert(str(args[arg]) == server_arg), 'mismatch'

def default_print_f(code, msg):
    print('-------')
    print(code)
    print(msg)

def post_2(url, data, headers):
    out = '{}'
    try:
        req = urllib2.Request(url)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])
        req.add_header('Content-Type', 'application/json')

        res = urllib2.urlopen(req, json.dumps(data).encode('utf8'))
        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        return (rc, json.loads(out))
    except urllib2.HTTPError as e:
        out = e.read();
        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")
        return (e.code, json.loads(out))

    except Exception as e:
        print(traceback.format_exc())
        return (False, e)

def get_2(url, data, headers):
    out = '{}'
    try:
        full_url = url
        if data:
            full_url = url + '?' + urllib.urlencode(data)
        req = urllib2.Request(full_url)
        if headers:
            for header in headers:
                req.add_header(header, headers[header])

        res = urllib2.urlopen(req)
        out = res.read()
        out = out + res.read()
        rc = res.getcode()

        return (rc, json.loads(out))
    except urllib2.HTTPError as e:
        if VERBOSE:
            print("code: ", e.code, " recv: '", out, "'")
        return (e.code, json.loads(out))

    except Exception as e:
        print(traceback.format_exc())
        return (False, e)
