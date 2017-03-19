#!/usr/bin/env python
#coding=utf8


def C_live_new_nginx_metric_upstream_response_time(gte, lte):
    request_body = {"query":{"filtered":{"query":{"query_string":{"query":"*","analyze_wildcard":"true"}},"filter":{"bool":{"must":[{"query":{"query_string":{"analyze_wildcard":"true","query":"*"}}},{"range":{"@timestamp":{"gte":None,"lte":None,"format":"epoch_millis"}}}],"must_not":[]}}}},"size":0,"aggs":{"2":{"max":{"field":"upstream_response_time"}},"3":{"avg":{"field":"upstream_response_time"}},"4":{"min":{"field":"upstream_response_time"}},"5":{"percentile_ranks":{"field":"upstream_response_time","values":[0.2,0.8,1.2,2.2]}}}}
    request_body['query']['filtered']['filter']['bool']['must'][1]['range']['@timestamp']['gte'] = gte
    request_body['query']['filtered']['filter']['bool']['must'][1]['range']['@timestamp']['lte'] = lte
    return request_body


def C_live_share(gte, lte):
    request_body = {"query":{"filtered":{"query":{"query_string":{"query":"*","analyze_wildcard":"true"}},"filter":{"bool":{"must":[{"query":{"query_string":{"analyze_wildcard":"true","query":"*"}}},{"range":{"@timestamp":{"gte":None,"lte":None,"format":"epoch_millis"}}}],"must_not":[]}}}},"size":0,"aggs":{"2":{"terms":{"field":"request_domain.raw","include":{"pattern":".*gotlive.*","flags":"CASE_INSENSITIVE"},"size":10,"order":{"_count":"desc"}},"aggs":{"3":{"terms":{"field":"request.raw","include":{"pattern":".*/share/live/.*"},"size":30,"order":{"_count":"desc"}}}}}}}
    request_body['query']['filtered']['filter']['bool']['must'][1]['range']['@timestamp']['gte'] = gte
    request_body['query']['filtered']['filter']['bool']['must'][1]['range']['@timestamp']['lte'] = lte
    return request_body