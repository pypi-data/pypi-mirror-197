import datetime
from urllib.parse import urljoin
from typing import List, Tuple
import requests
import time

now = datetime.datetime.now()


class Unitester:
    """
    A testing framework that provides a variety of assertion methods to check conditions and raise an
    AssertionError if they are not met.

    Attributes: tests (list): A list of tuples that define the tests to run, where each tuple contains a test
    function or method and optional arguments or fixtures to use in the test. passed (list): A list of the names of
    tests that passed. failed (dict): A dictionary that stores information about failed tests.

    Methods:
        test(fn, *args, **kwargs): Defines a new test to run.
        run(): Runs all defined tests and handles any failures or errors that occur.
        summary(): Prints a summary of the test results.
        assert_equal(expected, actual, msg=None): Asserts that the expected and actual values are equal.
        assert_true(actual, msg=None): Asserts that the actual value is True.
        assert_false(actual, msg=None): Asserts that the actual value is False.
        assert_raises(expected_exception, callable, *args, **kwargs): Asserts that a specific exception is raised by a callable.
        assert_in(item, iterable, msg=None): Asserts that the item is in the iterable.
        assert_not_in(item, iterable, msg=None): Asserts that the item is not in the iterable.
        assert_is(expected, actual, msg=None): Asserts that the expected and actual values are the same object.
        assert_is_not(expected, actual, msg=None): Asserts that the expected and actual values are not the same object.
        assert_is_none(actual, msg=None): Asserts that the actual value is None.
        assert_is_not_none(actual, msg=None): Asserts that the actual value is not None.
        assert_greater(first, second, msg=None): Asserts that the first value is greater than the second value.
        assert_greater_equal(first, second, msg=None): Asserts that the first value is greater than or equal to the second value.
        assert_less(first, second, msg=None): Asserts that the first value is less than the second value.
        assert_less_equal(first, second, msg=None): Asserts that the first value is less than or equal to the second value.
        assert_is_instance(obj, cls, msg=None): Asserts that the object is an instance of the class.
        assert_not_is_instance(obj, cls, msg=None): Asserts that the object is not an instance of the class.
        assert_is_subtype(obj, cls, msg=None): Asserts that the object is a subtype of the class.
        assert_not_is_subtype(obj, cls, msg=None): Asserts that the object is not a subtype of the class.
        assert_regex_match(pattern, string, msg=None): Asserts that the string matches the regular expression pattern.
        assert_regex_search(pattern, string, msg=None): Asserts that the string contains the regular expression pattern.
        assert_type(obj, typ, msg=None): Asserts that the object is of the specified type.
        assert_not_type(obj, typ, msg=None): Asserts that the object is not of the specified type.
    """

    def __init__(self):
        self.tests = []
        self.passed = []
        self.failed = {}

    def test(self, fn, *args, **kwargs):
        if 'fixtures' in kwargs:
            for fixture in kwargs['fixtures']:
                self.tests.append((fn, fixture))
        elif 'params' in kwargs:
            for param in kwargs['params']:
                self.tests.append((fn, (param,)))
        else:
            self.tests.append((fn, None))

    def run(self):
        for test, fixture in self.tests:
            try:
                if fixture:
                    inputs, expected_output = fixture
                    output = test(*inputs)
                    self.assert_equal(output, expected_output, f"Expected {expected_output}, but got {output}")
                else:
                    test()
                self.passed.append(test.__name__)
                # print(f"{test.__name__} passed")
            except AssertionError as e:
                self.handle_failure(test.__name__, e)
            except Exception as e:
                self.handle_error(test.__name__, e)

    def handle_failure(self, test_name, assertion_error):
        if test_name in self.failed:
            self.failed[test_name]['failures'].append((assertion_error, test_name))
        else:
            self.failed[test_name] = {'failures': [(assertion_error, test_name)], 'errors': []}

    def handle_error(self, test_name, exception):
        if test_name in self.failed:
            self.failed[test_name]['errors'].append(str(exception))
        else:
            self.failed[test_name] = {'failures': [], 'errors': [str(exception)]}
        print(f"{test_name} failed: {exception}")

    def summary(self):
        print(f"IUNI Test Results - {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nSummary:")
        print(f"        Total tests: {len(self.tests)}")
        print(f"        Tests passed: {len(self.passed)}")
        print(f"        Tests failed: {len(self.failed)}")

        if len(self.failed) > 0:
            print(f"\nFailed tests:")
            for failure in self.failed.values():
                for error, test_name in failure['failures']:
                    reason = str(error)
                    if hasattr(error, 'args') and error.args:
                        reason = error.args[0]
                    print(f"        ✗ {test_name}: Failed")

        if len(self.passed) > 0:
            print(f"\nPassed tests:")
            for test_name in self.passed:
                print(f"        ✓ {test_name}: Passed")

    def export_results(self, filename):
        with open(f"{filename}.log", "w") as f:
            f.write(f"IUNI Test Results - {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\nSummary:\n")
            f.write(f"Total tests: {len(self.tests)}\n")
            f.write(f"Tests passed: {len(self.passed)}\n")
            f.write(f"Tests failed: {len(self.failed)}\n")
            f.write("\nFailed tests:\n")
            for test_name, failures_and_errors in self.failed.items():
                for failure in failures_and_errors['failures']:
                    reason = str(failure)
                    if hasattr(failure, 'args') and failure.args:
                        reason = failure.args[0]
                    f.write(f"  ✗ {test_name}: Failed\n")

            f.write("\nPassed tests:\n")
            for test_name in self.passed:
                f.write(f"  ✓ {test_name}: Passed\n")

    def assert_equal(self, expected, actual, msg=None):
        if expected != actual:
            raise AssertionError(msg or f"Expected {expected}, but got {actual}")

    def assert_true(self, actual, msg=None):
        if not actual:
            raise AssertionError(msg or "Expected True, but got False")

    def assert_false(self, actual, msg=None):
        if actual:
            raise AssertionError(msg or "Expected False, but got True")

    def assert_raises(self, expected_exception, callable, *args, **kwargs):
        try:
            callable(*args, **kwargs)
            raise AssertionError(f"Expected {expected_exception}, but no exception was raised")
        except expected_exception:
            pass
        except Exception as e:
            raise AssertionError(f"Expected {expected_exception}, but got {type(e)}")

    def assert_in(self, item, iterable, msg=None):
        if item not in iterable:
            raise AssertionError(msg or f"{item} not found in {iterable}")

    def assert_not_in(self, item, iterable, msg=None):
        if item in iterable:
            raise AssertionError(msg or f"{item} found in {iterable}")

    def assert_is(self, expected, actual, msg=None):
        if expected is not actual:
            raise AssertionError(msg or f"Expected {expected} ({type(expected)}), but got {actual} ({type(actual)})")

    def assert_is_not(self, expected, actual, msg=None):
        if expected is actual:
            raise AssertionError(
                msg or f"Expected {expected} ({type(expected)}) not to be the same object as {actual} ({type(actual)})")

    def assert_is_none(self, actual, msg=None):
        if actual is not None:
            raise AssertionError(msg or f"Expected None, but got {actual} ({type(actual)})")

    def assert_is_not_none(self, actual, msg=None):
        if actual is None:
            raise AssertionError(msg or "Expected a value, but got None")

    def assert_greater(self, first, second, msg=None):
        if not first > second:
            raise AssertionError(msg or f"{first} not greater than {second}")

    def assert_greater_equal(self, first, second, msg=None):
        if not first >= second:
            raise AssertionError(msg or f"{first} not greater than or equal to {second}")

    def assert_less(self, first, second, msg=None):
        if not first < second:
            raise AssertionError(msg or f"{first} not less than {second}")

    def assert_less_equal(self, first, second, msg=None):
        if not first <= second:
            raise AssertionError(msg or f"{first} not less than or equal to {second}")

    def assert_is_instance(self, obj, cls, msg=None):
        if not isinstance(obj, cls):
            raise AssertionError(msg or f"{obj} is not an instance of {cls}")

    def assert_not_is_instance(self, obj, cls, msg=None):
        if isinstance(obj, cls):
            raise AssertionError(msg or f"{obj} is an instance of {cls}")

    def assert_is_subtype(self, obj, cls, msg=None):
        if not issubclass(type(obj), cls):
            raise AssertionError(msg or f"{type(obj)} is not a subtype of {cls}")

    def assert_not_is_subtype(self, obj, cls, msg=None):
        if issubclass(type(obj), cls):
            raise AssertionError(msg or f"{type(obj)} is a subtype of {cls}")

    def assert_regex_match(self, pattern, string, msg=None):
        import re
        if not re.match(pattern, string):
            raise AssertionError(msg or f"{string} does not match pattern {pattern}")

    def assert_regex_search(self, pattern, string, msg=None):
        import re
        if not re.search(pattern, string):
            raise AssertionError(msg or f"{string} does not contain pattern {pattern}")

    def assert_type(self, obj, typ, msg=None):
        if type(obj) is not typ:
            raise AssertionError(msg or f"{obj} is not of type {typ}")

    def assert_not_type(self, obj, typ, msg=None):
        if type(obj) is typ:
            raise AssertionError(msg or f"{obj} is of type {typ}")


class APILoadTester(Unitester):
    """
    Part of the IUNI framework, a class that provides functionality for load testing a web API.

    Attributes:
        url (str): The base URL of the web API to be tested.
        headers (dict): HTTP headers to be included in each request.
        concurrency_level (int): The number of concurrent requests to be made during the load test.
        duration (float): The duration of the load test in seconds.
        requests (list): A list of requests to be made during the load test.
        results (dict): A dictionary containing the results of the load test.

    Methods:
        set_url(url): Sets the base URL of the web API to be tested.
        set_headers(headers): Sets the HTTP headers to be included in each request.
        set_concurrency_level(level): Sets the number of concurrent requests to be made during the load test.
        set_duration(duration): Sets the duration of the load test in seconds.
        add_request(method, path, data=None, headers=None): Adds a request to the list of requests to be made during the load test.
        run_load_test(): Runs the load test and collects performance metrics.
        print_results(): Prints the results of the load test.
    """

    def __init__(self):
        super().__init__()
        self.url = ""
        self.headers = {}
        self.concurrency_level = 1
        self.duration = 0
        self.requests = []
        self.results = {}

    def set_url(self, url):
        self.url = url

    def set_headers(self, headers):
        self.headers = headers

    def set_concurrency_level(self, level):
        self.concurrency_level = level

    def set_duration(self, duration):
        self.duration = duration

    def add_request(self, method, path, data=None, headers=None):
        request = {
            "method": method,
            "path": path,
            "data": data,
            "headers": headers or self.headers
        }
        self.requests.append(request)

    def run_load_test(self):
        start_time = time.time()
        end_time = start_time + self.duration
        results = {
            "total_requests": 0,
            "total_time": 0,
            "response_times": [],
            "throughput": 0,
            "errors": 0
        }

        while time.time() < end_time:
            responses = []
            start = time.time()
            for i in range(self.concurrency_level):
                request = self.requests[i % len(self.requests)]
                try:
                    response = requests.request(
                        request["method"],
                        self.url + request["path"],
                        data=request["data"],
                        headers=request["headers"]
                    )
                    responses.append(response)
                except Exception as e:
                    self.handle_error(request["path"], e)
                    results["errors"] += 1

            end = time.time()
            response_times = [(r.elapsed.total_seconds() * 1000) for r in responses]
            results["total_requests"] += len(response_times)
            results["total_time"] += (end - start)
            results["response_times"].extend(response_times)

        self.results = results

    def print_results(self):
        print(f"IUNI - API Performance Test Results - {now}")
        print(f"\nLoad Test Results:")
        print(f"        Total Requests: {self.results['total_requests']}")
        print(f"        Total Time (s): {self.results['total_time']:.2f}")
        print(
            f"        Average Response Time (ms): {sum(self.results['response_times']) / self.results['total_requests']: .2f}")
        print(f"        Throughput (requests/s): {self.results['total_requests'] / self.duration:.2f}")
        print(f"        Errors: {self.results['errors']}")
        if self.results["response_times"]:
            percentile_50 = self.percentile(self.results["response_times"], 50)
            percentile_90 = self.percentile(self.results["response_times"], 90)
            percentile_95 = self.percentile(self.results["response_times"], 95)
            percentile_99 = self.percentile(self.results["response_times"], 99)
            print(f"\nResponse Time Percentiles:")
            print(f"        50%: {percentile_50:.2f} ms")
            print(f"        90%: {percentile_90:.2f} ms")
            print(f"        95%: {percentile_95:.2f} ms")
            print(f"        99%: {percentile_99:.2f} ms")

    def export_api_load(self, filename):
        # Get the current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Open the file for writing
        with open(f"{filename}.log", "w") as f:
            # Write the header
            f.write(f"IUNI - API Performance Test Results - {now}\n\n")
            # Write the load test results
            f.write(f"Load Test Results:\n")
            f.write(f"        Total Requests: {self.results['total_requests']}\n")
            f.write(f"        Total Time (s): {self.results['total_time']:.2f}\n")
            f.write(
                f"        Average Response Time (ms): {sum(self.results['response_times']) / self.results['total_requests']: .2f}\n")
            f.write(f"        Throughput (requests/s): {self.results['total_requests'] / self.duration:.2f}\n")
            f.write(f"        Errors: {self.results['errors']}\n\n")
            if self.results["response_times"]:
                percentile_50 = self.percentile(self.results["response_times"], 50)
                percentile_90 = self.percentile(self.results["response_times"], 90)
                percentile_95 = self.percentile(self.results["response_times"], 95)
                percentile_99 = self.percentile(self.results["response_times"], 99)
                f.write(f"Response Time Percentiles:\n")
                f.write(f"        50%: {percentile_50:.2f} ms\n")
                f.write(f"        90%: {percentile_90:.2f} ms\n")
                f.write(f"        95%: {percentile_95:.2f} ms\n")
                f.write(f"        99%: {percentile_99:.2f} ms\n")

    def percentile(self, response_times, p):
        """
        Calculates the pth percentile of the given response times.

        Args:
            response_times (list): A list of response times in milliseconds.
            p (float): The desired percentile, expressed as a float between 0 and 100.

        Returns:
            The pth percentile of the response times.
        """
        if not response_times:
            return None
        response_times = sorted(response_times)
        k = (len(response_times) - 1) * (p / 100.0)
        f = int(k)
        c = k - f
        if f + 1 < len(response_times):
            return response_times[f] + c * (response_times[f + 1] - response_times[f])
        else:
            return response_times[f]


class SecurityTester:

    def __init__(self, target_url, headers=None, cookies=None):
        self.target_url = target_url
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.results = []

    def run_tests(self):
        self.test_sql_injection()
        self.test_cross_site_scripting()
        self.test_command_injection()
        self.test_file_inclusion()
        self.test_insecure_direct_object_reference()
        self.test_command_injection_post()
        self.test_cross_site_request_forgery()
        self.print_summary()

    def add_result(self, test_name, status, description=None):
        self.results.append({'test_name': test_name, 'status': status, 'description': description})

    def test_sql_injection(self, payloads=["' or 1=1", "'; DROP TABLE users; --"]):
        for payload in payloads:
            url = f"{self.target_url}?q={payload}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if payload in response.text:
                self.add_result('SQL injection', 'failed',
                                f"SQL injection vulnerability detected with payload: {payload}")
            else:
                self.add_result('SQL injection', 'passed')

    def test_cross_site_scripting(self, payloads=["<script>alert('XSS')</script>"]):
        for payload in payloads:
            url = f"{self.target_url}?search={payload}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if payload in response.text:
                self.add_result('Cross-site scripting', 'failed',
                                f"Cross-site scripting vulnerability detected with payload: {payload}")
            else:
                self.add_result('Cross-site scripting', 'passed')

    def test_command_injection(self, payloads=["; cat /etc/passwd"]):
        for payload in payloads:
            url = f"{self.target_url}?cmd={payload}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if payload in response.text:
                self.add_result('Command injection', 'failed',
                                f"Command injection vulnerability detected with payload: {payload}")
            else:
                self.add_result('Command injection', 'passed')

    def test_file_inclusion(self, payloads=["../../../../etc/passwd"]):
        for payload in payloads:
            url = f"{self.target_url}?file={payload}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if payload in response.text:
                self.add_result('File inclusion', 'failed',
                                f"File inclusion vulnerability detected with payload: {payload}")
            else:
                self.add_result('File inclusion', 'passed')

    def test_insecure_direct_object_reference(self, payloads=["admin", "123", "user"]):
        for payload in payloads:
            url = f"{self.target_url}/{payload}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if response.status_code == 200:
                self.add_result('Insecure direct object reference', 'failed',
                                f"Insecure direct object reference vulnerability detected with payload: {payload}")
            else:
                self.add_result('Insecure direct object reference', 'passed')

    def test_command_injection_post(self, payloads=["; cat /etc/passwd"]):
        for payload in payloads:
            data = {"cmd": payload}
            response = requests.post(self.target_url, data=data, headers=self.headers, cookies=self.cookies)
            if payload in response.text:
                self.add_result('Command injection via POST', 'failed',
                                f"Command injection vulnerability detected with payload: {payload}")

    def add_result(self, name: str, status: str, message: str):
        self.results.append((name, status, message))

    def test_command_injection(self, path: str, payload: str):
        url = urljoin(self.target_url, path)
        data = {'input': payload}
        response = requests.post(url, data=data)

        if payload in response.text:
            self.add_result('Command injection via POST', 'failed',
                            f"Command injection vulnerability detected with payload: {payload}")
        else:
            self.add_result('Command injection via POST', 'passed', "No command injection vulnerability detected")

    def test_xss_vulnerability(self, path: str):
        url = urljoin(self.target_url, path)
        response = requests.get(url, headers=self.headers, cookies=self.cookies)

        if '<script>' in response.text:
            self.add_result('XSS vulnerability', 'failed', "XSS vulnerability detected")
        else:
            self.add_result('XSS vulnerability', 'passed', "No XSS vulnerability detected")

    def test_sql_injection(self, path: str, payload: str):
        url = urljoin(self.target_url, path)
        data = {'input': payload}
        response = requests.post(url, data=data)

        if 'SQL syntax' in response.text:
            self.add_result('SQL injection via POST', 'failed',
                            f"SQL injection vulnerability detected with payload: {payload}")
        else:
            self.add_result('SQL injection via POST', 'passed', "No SQL injection vulnerability detected")

    def run_tests(self, tests: List[Tuple[str, str, str]]):
        for test in tests:
            name, path, payload = test
            print(f"Running {name} test...")
            if name == 'Command injection':
                self.test_command_injection(path, payload)
            elif name == 'XSS vulnerability':
                self.test_xss_vulnerability(path)
            elif name == 'SQL injection':
                self.test_sql_injection(path, payload)

    def print_summary(self):
        print("Security Testing Summary")
        print("------------------------")
        for result in self.results:
            print(f"{result[0]}: {result[1]} - {result[2]}")

# TODO: class UITester(IUNI)
