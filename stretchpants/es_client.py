import httplib2
import json
import urlparse

from json_encoder import JsonEncoder


class ElasticSearchClient(object):
    
    def __init__(self, host="localhost", port=9201):
        self.host = host
        self.port = port
        self._url_stub = "http://%s:%s" % (host, port)
        
        # create connection to elasticsearch
        self._connection = httplib2.Http(self.host, self.port)
    
    def _make_url(self, idx_doc):
        index_path = idx_doc.index + "/" + idx_doc.document_type + "/" + \
                     str(idx_doc.document_id)
        return urlparse.urljoin(self._url_stub, index_path)
    
    def _make_request(self, method, url, body=None):
        # coerce body to json via special json encoder
        body = json.dumps(body, cls=JsonEncoder)
        
        # make request and interpret response
        response, content = self._connection.request(url, method, body=body)
        if response.status != 200:
            raise Exception("Request failed. Status: %s" % response['status'])
        return content
    
    def _put(self, url, body):
        """Perform HTTP PUT.
        """
        return self._make_request("PUT", url, body)
        
    def _delete(self, url):
        """Perform HTTP DELETE.
        """
        return self._make_request("DELETE", url)
    
    def index(self, idx_doc):
        """Index a document.
        """
        url = self._make_url(idx_doc)
        return self._put(url, idx_doc.document)

    def search(self, index="_search", type=None, search_spec=None):
        """Perform a search using a pre-composed spec.
        
        :param search_spec: A ``dict``. Must comply with ElasticSearch DSL.
        :returns: A list of hydrated objects.
        """
        pass

    def delete(self, idx_doc):
        """Index a document.
        """
        url = self._make_url(idx_doc)
        return self._delete(url)
