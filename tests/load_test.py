
import asyncio
import time
import statistics
import httpx

URL = "http://127.0.0.1:8000/recommend"
TOTAL_REQUESTS = 50
CONCURRENCY = 50


async def main():
    latencies = []
    successes = 0
    failures = 0

    limits = httpx.Limits(
        max_connections=CONCURRENCY,
        max_keepalive_connections=CONCURRENCY,
    )
    timeout = httpx.Timeout(30.0)

    async with httpx.AsyncClient(
        limits=limits, timeout=timeout
    ) as client:

        async def send_request():
            nonlocal successes, failures

            payload = {
                "student_id": "NEW-STUDENT",
                "top_k": 5,
            }

            start = time.perf_counter()

            try:
                response = await client.post(URL, json=payload)
                elapsed = time.perf_counter() - start
                latencies.append(elapsed * 1000)

                if response.status_code == 200:
                    successes += 1
                else:
                    failures += 1
                    print("HTTP error:", response.status_code)

            except Exception as error:
                failures += 1
                print("Request failed:", error)

        start_all = time.perf_counter()

        await asyncio.gather(
            *(send_request() for _ in range(TOTAL_REQUESTS))
        )

        total_time = time.perf_counter() - start_all

    print("\n===== LOAD TEST RESULTS =====")
    print("Total requests:", TOTAL_REQUESTS)
    print("Concurrent requests:", CONCURRENCY)
    print("Successful requests:", successes)
    print("Failed requests:", failures)
    print(f"Total test time: {total_time:.3f} seconds")

    if latencies:
        sorted_latencies = sorted(latencies)
        p95_index = max(0, int(0.95 * len(sorted_latencies)) - 1)

        print(
            f"Average latency: {statistics.mean(latencies):.2f} ms"
        )
        print(
            f"Median latency: {statistics.median(latencies):.2f} ms"
        )
        print(
            f"P95 latency: {sorted_latencies[p95_index]:.2f} ms"
        )
        print(
            f"Throughput: {successes / total_time:.2f} successful requests/second"
        )


if __name__ == "__main__":
    asyncio.run(main())
