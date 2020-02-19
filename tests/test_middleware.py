from django.test import TestCase, override_settings


class TestHttp2ServerPushRedirectMiddleware(TestCase):
    # Must set DEBUG to True for the logger to trigger:
    # https://docs.djangoproject.com/en/2.2/topics/http/middleware/#marking-middleware-as-unused
    @override_settings(DEBUG=True, SECURE_PROXY_SSL_HEADER=None)
    def test_disabled_when_secure_proxy_ssl_header_is_not_configured(self):
        with self.assertLogs("django.request", level="DEBUG") as cm:
            self.client.get("/")
        self.assertIn(
            "DEBUG:django.request:MiddlewareNotUsed"
            "('push_redirect.middleware.Http2ServerPushRedirectMiddleware'):"
            " SECURE_PROXY_SSL_HEADER is not configured",
            cm.output,
        )

    def test_opt_out(self):
        """
        Does not add the preload header to responses that have opted out
        """
        response = self.client.get("/opt-out/")
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertNotIn("Link", response)

    def test_non_secure_request(self):
        """
        Does not add the preload header redirects requested over HTTP
        """
        response = self.client.get("/")
        self.assertRedirects(response, "/hello", fetch_redirect_response=False)
        self.assertNotIn("Link", response)

    def test_secure_request(self):
        """
        Adds the preload header to redirects requested over HTTPS
        """
        response = self.client.get("/", secure=True)
        self.assertRedirects(response, "/hello", fetch_redirect_response=False)
        self.assertIn("Link", response)
        self.assertEqual("</hello>; as=document; rel=preload", response["Link"])

    def test_post_requests(self):
        """
        Does not add the preload header to redirects following
        a POST (or any other non-GET) request
        """
        response = self.client.post("/", secure=True)
        self.assertRedirects(response, "/hello", fetch_redirect_response=False)
        self.assertNotIn("Link", response)

    def test_non_redirect_responses(self):
        """
        Does not add the preload header to a 200 (OK) response
        """
        response = self.client.get("/hello/world/", secure=True)
        self.assertEqual(200, response.status_code)
        self.assertNotIn("Link", response)

    def test_custom_redirect_responses(self):
        """
        Does not add the preload header to a custom
        (non HttpResponseRedirectBase) response
        """
        response = self.client.get("/custom-redirect/", secure=True)
        # Cannot use assertRedirects as it also requires the url attribute
        # added by HttpResponseRedirectBase
        # self.assertRedirects(response, "/custom-redirect/redirected/", fetch_redirect_response=False)
        self.assertIn("Location", response)
        self.assertEqual("/custom-redirect/redirected/", response["Location"])
        self.assertNotIn("Link", response)

    def test_existing_link_header_in_responses(self):
        """
        Does not overwrite existing Link headers
        """
        response = self.client.get("/custom-link/", secure=True)
        self.assertRedirects(
            response, "https://www.google.com/", fetch_redirect_response=False
        )
        self.assertIn("Link", response)
        self.assertEqual("<https://www.google.com/>; rel=preconnect", response["Link"])

    def test_external_redirect_response(self):
        """
        Does not add the preload header to a external redirect
        """
        response = self.client.get("/google/", secure=True)
        self.assertRedirects(
            response, "https://www.google.com/", fetch_redirect_response=False
        )
        self.assertNotIn("Link", response)

    def test_common_middleware(self):
        """
        Adds the preload header to redirects created by Django's
        CommonMiddleware (APPEND_SLASH)
        """
        response = self.client.get("/hello/moon", secure=True)
        self.assertRedirects(
            response, "/hello/moon/", 301, fetch_redirect_response=False
        )
        self.assertIn("Link", response)
        self.assertEqual("</hello/moon/>; as=document; rel=preload", response["Link"])
