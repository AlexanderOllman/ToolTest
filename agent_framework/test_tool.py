import httpx, sys

def smoke_test(host: str):
    spec = httpx.get(f"http://{host}/docs").json()
    path, ops = next(iter(spec["paths"].items()))
    method = next(iter(ops))
    url = f"http://{host}{path}"
    resp = getattr(httpx, method)(url, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError("Health check failed")

if __name__ == "__main__":
    smoke_test(sys.argv[1]) 