# OLXHelper

In need of additional function "Holiday" on polish marketplace olx.pl I created this helper where I would like add more missing functionalities. 

Functions list with short description:
- Holiday: go through all offers adding text to description eg. "I'm on holiday untill xx.xx.xxx", and increase price by specified value to handle extra costs of shipping during holiday or to aware customers of making orders if we i crease price for eg. 1000.

## New Feature: Parallel Processing

To improve the speed of processing multiple offers, the code now utilizes parallel processing using `concurrent.futures.ThreadPoolExecutor`. This allows multiple offers to be processed simultaneously, significantly reducing the overall processing time.

### How It Works

1. The `main.py` script now includes a `process_offer` function that encapsulates the logic for processing a single offer.
2. The `for` loop in `main.py` has been replaced with a `concurrent.futures.ThreadPoolExecutor` to handle multiple offers simultaneously.
3. The methods in `methods.py` that interact with web elements have been adapted to support parallel execution by adding necessary locks or synchronization mechanisms.
4. Each thread creates a new WebDriver instance to avoid conflicts and ensure thread safety.
5. The script uses a headless browser like `pyppeteer` or `Playwright` for better concurrency and parallel execution.

### Benefits

- **Speed**: Parallel processing allows multiple offers to be processed at the same time, reducing the total time required.
- **Efficiency**: By utilizing multiple threads, the script can handle a large number of offers more efficiently.
- **Thread Safety**: Creating a new WebDriver instance for each thread ensures that there are no conflicts between threads.
- **Better Concurrency**: Using a headless browser like `pyppeteer` or `Playwright` improves concurrency and parallel execution.

### Usage

To use the new parallel processing feature, simply run the `main.py` script as usual. The script will automatically handle the offers in parallel.
