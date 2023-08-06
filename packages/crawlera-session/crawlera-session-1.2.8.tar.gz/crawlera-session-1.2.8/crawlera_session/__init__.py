"""
See repo README
"""
import uuid
import logging
import random
from collections import OrderedDict
from functools import partial

from scrapy import Request, signals
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware


__version__ = "1.2.8"

logger = logging.getLogger(__name__)


class SessionNotInitializedError(Exception):
    pass


class WrongSessionError(Exception):
    pass


class RequestSession(object):
    def __init__(
        self,
        crawlera_session=True,
        x_crawlera_cookies="disable",
        x_crawlera_profile=None,
        x_crawlera_wait=None,
        new_session_retries=3,
        priority_adjust=0,
    ):
        self.crawlera_session = crawlera_session
        self.x_crawlera_cookies = x_crawlera_cookies
        self.x_crawlera_profile = x_crawlera_profile
        self.x_crawlera_wait = x_crawlera_wait
        self.new_session_retries = new_session_retries
        self.priority_adjust = priority_adjust

    def follow_session(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            try:
                cookiejar = response.meta["cookiejar"]
            except KeyError:
                raise SessionNotInitializedError("You must initialize previous request.")

            for obj in wrapped(spider, response, *args, **kwargs):
                if (
                    isinstance(obj, Request)
                    and not obj.meta.get("no_crawlera_session", False)
                    and "cookiejar" not in obj.meta
                ):
                    self.assign_crawlera_session(spider, obj, cookiejar)
                    obj.priority = response.request.priority + self.priority_adjust
                yield obj

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def assign_crawlera_session(self, spider, request, cookiejar=None):
        if cookiejar is None:
            if spider.can_add_new_sessions():
                self.init_request(request)
                spider.locked_sessions.add(request.meta["cookiejar"])
                return True
            if spider.available_sessions:
                cookiejar = random.choice(spider.available_sessions)
        if cookiejar is None:
            return False
        else:
            if self.crawlera_session and "X-Crawlera-Session" not in request.headers:
                session = spider.crawlera_sessions[cookiejar]
                logger.debug(f"Assigned session {session} to {request} from cookiejar {cookiejar}")
                request.headers["X-Crawlera-Session"] = session
            self._adapt_request(request)
            if "cookiejar" not in request.meta:
                request.meta["cookiejar"] = cookiejar
            else:
                # this shouldn't be happening, but lets add a check line in case logic fails somewhere
                raise WrongSessionError(f"{request} Tried to assign a session to a request that already had one.")
            spider.locked_sessions.add(cookiejar)
            return True

    def _adapt_request(self, request):
        if self.x_crawlera_cookies is not None:
            request.headers["X-Crawlera-Cookies"] = self.x_crawlera_cookies
        if self.x_crawlera_profile is not None:
            request.headers["X-Crawlera-Profile"] = self.x_crawlera_profile
        if self.x_crawlera_wait is not None:
            request.headers["X-Crawlera-Wait"] = self.x_crawlera_wait

    def init_request(self, request):
        if "cookiejar" not in request.meta:
            request.meta["cookiejar"] = str(uuid.uuid1())
        if self.crawlera_session:
            request.headers["X-Crawlera-Session"] = "create"
        self._adapt_request(request)
        logger.debug(f"Session initiation for {request}")
        return request

    def init_start_requests(self, wrapped):
        def _wrapper(spider):
            if not hasattr(spider, "crawlera_sessions"):
                raise AttributeError("You have to subclass your spider from CrawleraSessionMixinSpider class")
            for request in wrapped(spider):
                self.init_request(request)
                yield request

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def init_requests(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            for obj in wrapped(spider, response, *args, **kwargs):
                if isinstance(obj, Request) and not obj.meta.get("no_crawlera_session", False):
                    self.init_request(obj)
                yield obj

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def defer_assign_session(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            for obj in wrapped(spider, response, *args, **kwargs):
                if isinstance(obj, Request):
                    # session will be assigned at downloader enqueue
                    obj.meta["defer_assign_crawlera_session"] = self.assign_crawlera_session
                yield obj

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def unlock_session(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            spider.locked_sessions.discard(response.meta["cookiejar"])
            return wrapped(spider, response, *args, **kwargs)

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def discard_session(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            spider.drop_session(response)
            return wrapped(spider, response, *args, **kwargs)

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper

    def new_session_on_retry(self, wrapped):
        def _wrapper(spider, response, *args, **kwargs):
            for obj in wrapped(spider, response, *args, **kwargs):
                if isinstance(obj, Request):
                    # for skipping retry middleware
                    obj.meta["dont_retry"] = True
                    obj.meta["crawlera_session_obj"] = self
                    obj.meta["retries"] = self.new_session_retries
                    errback_name = obj.callback.__name__ + "_errback"
                    assert hasattr(spider, errback_name), f"Spider doesn't implement {errback_name} method"
                    errback = getattr(spider, errback_name)
                    assert (
                        not obj.errback or obj.errback is errback
                    ), f"Can't assign spider.{errback_name}() to request: already has an errback."
                    obj.errback = partial(spider._session_retry_errback, errback=errback)
                yield obj

        _wrapper.__name__ = wrapped.__name__
        _wrapper.wrapped = wrapped
        return _wrapper


class CrawleraSessionRedirectMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        obj = super(CrawleraSessionRedirectMiddleware, self).process_response(request, response, spider)
        if isinstance(obj, Request):
            if "X-Crawlera-Session" in response.headers:
                obj.headers["X-Crawlera-Session"] = response.headers["X-Crawlera-Session"]
        return obj


class CrawleraSessionCookiesMiddleware(CookiesMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        obj = super().from_crawler(crawler)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_closed, signal=signals.spider_closed)
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.retained_requests = []

    def spider_opened(self, spider):
        scheduler = spider.crawler.engine.slot.scheduler
        orig_scheduler_next_request = scheduler.next_request

        def _can_enqueue_request(request):
            if request.meta.get("cookiejar"):
                return True
            if spider.can_add_new_sessions():
                return True
            if spider.crawler.engine.spider_is_idle(spider):
                spider.locked_sessions = set()
            if spider.available_sessions:
                return True

            return False

        def _next_request():
            for request in list(self.retained_requests):
                if _can_enqueue_request(request):
                    self.retained_requests.remove(request)
                    return request

            new_request = orig_scheduler_next_request()
            if new_request is not None:
                if _can_enqueue_request(new_request):
                    return new_request
                self.retained_requests.append(new_request)

        scheduler.next_request = _next_request

    def spider_closed(self, spider):
        if self.retained_requests:
            logger.error(
                f"Request {self.retained_requests[0]} and {len(self.retained_requests) - 1} others"
                "retained requests were not unqueued."
            )

    def process_request(self, request, spider):
        assign_crawlera_session = request.meta.get("defer_assign_crawlera_session")
        if assign_crawlera_session is not None:
            if assign_crawlera_session(spider, request):
                request.meta.pop("defer_assign_crawlera_session")
            else:
                spider.crawler.stats.inc_value("crawlera_sessions/no_unlocked_sessions")
                raise IgnoreRequest(f"No unlocked session for {request}")
        return super().process_request(request, spider)

    def process_response(self, request, response, spider):
        if "X-Crawlera-Session" in response.headers:
            cookiejar = request.meta["cookiejar"]
            spider.crawlera_sessions.setdefault(cookiejar, response.headers["X-Crawlera-Session"])
        return super().process_response(request, response, spider)


class CrawleraSessionMixinSpider:

    crawlera_sessions = OrderedDict()
    locked_sessions = set()

    MAX_PARALLEL_SESSIONS = None

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        DW_MIDDLEWARES = settings.get("DOWNLOADER_MIDDLEWARES")

        pos = settings.get("DOWNLOADER_MIDDLEWARES_BASE").pop(
            "scrapy.downloadermiddlewares.redirect.RedirectMiddleware"
        )
        DW_MIDDLEWARES["crawlera_session.CrawleraSessionRedirectMiddleware"] = pos
        pos = settings.get("DOWNLOADER_MIDDLEWARES_BASE").pop("scrapy.downloadermiddlewares.cookies.CookiesMiddleware")
        DW_MIDDLEWARES["crawlera_session.CrawleraSessionCookiesMiddleware"] = pos

    def can_add_new_sessions(self):
        return self.MAX_PARALLEL_SESSIONS is None or len(self.crawlera_sessions) < self.MAX_PARALLEL_SESSIONS

    @property
    def available_sessions(self):
        return [k for k in self.crawlera_sessions.keys() if k not in self.locked_sessions]

    def drop_session(self, response_or_request):
        session_id = response_or_request.meta.get("cookiejar")
        if session_id is not None:
            self.locked_sessions.discard(session_id)
            self.crawlera_sessions.pop(session_id)

    def _session_retry_errback(self, failure, errback):
        self.drop_session(failure.request)
        retries = failure.request.meta["retries"]
        if retries == 0:
            self.logger.info(f"Gave up session retries for {failure.request}")
            return
        request = errback(failure)
        if request is not None:
            failure.request.meta["crawlera_session_obj"].init_request(request)
            request.dont_filter = True
            request.errback = partial(self._session_retry_errback, errback=errback)
            request.meta["retries"] = retries - 1
            yield request
