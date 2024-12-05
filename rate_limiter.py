import time
from typing import Optional


class RateLimiter:
    def __init__(self, rate: int, per: int):
        """
        Initialize a rate limiter.

        :param rate: Maximum number of requests allowed
        :param per: Time window in minutes
        """
        self.rate = rate
        self.per = per  # minute
        self.requests = []
        self.last_request_time = None

    def _cleanup_old_requests(self) -> None:
        """
        Remove requests older than the time window.
        """
        current_time = time.time()
        time_window = self.per * 60  # convert minutes to seconds
        self.requests = [
            req for req in self.requests
            if current_time - req < time_window
        ]

    def allow_request(self) -> bool:
        """
        Check if a request is allowed based on the rate limit.

        :return: True if request is allowed, False otherwise
        """
        current_time = time.time()

        # Clean up old requests
        self._cleanup_old_requests()

        # Check if we've exceeded the rate limit
        if len(self.requests) >= self.rate:
            return False

        # Add current request time
        self.requests.append(current_time)
        self.last_request_time = current_time

        return True

    def wait_time(self) -> Optional[float]:
        """
        Calculate the wait time before the next request is allowed.

        :return: Time to wait in seconds, or None if request can be made immediately
        """
        current_time = time.time()
        self._cleanup_old_requests()

        # If we haven't reached the rate limit, no wait time needed
        if len(self.requests) < self.rate:
            return None

        # Calculate wait time based on the oldest request in the window
        time_window = self.per * 60  # convert minutes to seconds
        oldest_request = min(self.requests)
        wait_duration = (oldest_request + time_window) - current_time

        return max(0, wait_duration)

    def reset(self) -> None:
        """
        Reset the rate limiter, clearing all tracked requests.
        """
        self.requests.clear()
        self.last_request_time = None